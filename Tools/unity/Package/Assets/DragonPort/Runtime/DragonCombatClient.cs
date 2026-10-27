using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
namespace DragonPort
{
    [Serializable] public sealed class DragonCombatActor
    {
        public string id,action;
        public float x,y,z,yaw;
        public double hp,maxHp;
        public int modelId;
        public bool alive;
    }
    [Serializable] public sealed class DragonCombatEvent
    {
        public string kind,sourceId,targetId;
        public double sequence,damage,hp;
        public bool critical;
    }
    public sealed class DragonCombatClient : MonoBehaviour
    {
        public DragonWorldLoader Loader;
        public string Host="127.0.0.1";
        public int Port=15800;
        public GameObject PlayerPrefab;
        public Camera InputCamera;
        public DragonCombatActor PlayerState {get;private set;}
        public event Action<DragonCombatEvent> CombatEvent;
        private TcpClient client;
        private bool stopped;
        private readonly Dictionary<string,DragonSpawn> actors=new Dictionary<string,DragonSpawn>();
        private GameObject playerVisual;
        private string pendingAttack;
        private Vector3? pendingMove;
        private bool pendingRespawn;
        private double sequence;
        [Serializable] private sealed class Parameters
        {
            public int sceneId,offset,limit=100;
            public string targetId;
            public float x,z;
            public double afterSequence;
        }
        [Serializable] private sealed class Request {public int v=1;public string id,method;public Parameters @params;}
        [Serializable] private sealed class Result
        {
            public DragonCombatActor player;
            public DragonCombatActor[] entities;
            public DragonCombatEvent[] events;
            public double sequence;
            public int total,nextOffset;
            public double damage,targetHp;
            public bool hit,critical,dead;
        }
        [Serializable] private sealed class Error {public string code;}
        [Serializable] private sealed class Reply {public int v;public string id;public bool ok;public Result result;public Error error;}
        public void Attack(string sourceSpawnId){pendingAttack=sourceSpawnId;}
        public void MoveTo(Vector3 localGridPosition){pendingMove=localGridPosition;}
        public void Respawn(){pendingRespawn=true;}
        private async Task<Reply> Call(StreamReader input,StreamWriter output,string method,Parameters parameters)
        {
            var request=new Request{id=Guid.NewGuid().ToString("N"),method=method,@params=parameters};
            await output.WriteLineAsync(JsonUtility.ToJson(request));
            var read=input.ReadLineAsync();
            if(await Task.WhenAny(read,Task.Delay(5000))!=read)throw new TimeoutException("Combat response timed out");
            var line=await read;
            if(line==null)throw new IOException("Combat server disconnected");
            var reply=JsonUtility.FromJson<Reply>(line);
            if(reply==null || reply.v!=1 || reply.id!=request.id)throw new InvalidDataException("Invalid combat response");
            if(!reply.ok && !stopped)Debug.Log("Combat: "+(reply.error!=null?reply.error.code:"unknown error"),this);
            return reply;
        }
        private void Apply(DragonCombatActor state,Transform target)
        {
            var old=target.localPosition;var next=new Vector3(state.x,state.y,state.z);
            target.localRotation=Quaternion.Euler(0,state.yaw,0);
            target.localPosition=next;
            var playback=target.GetComponentInChildren<DragonOriginalAnimation>();
            if(playback)playback.PlayState(state.action);
        }
        private async void Start()
        {
            try
            {
                if(!Loader)Loader=GetComponent<DragonWorldLoader>();
                if(!Loader)throw new InvalidOperationException("Assign DragonWorldLoader");
                // WorldSession is a one-off source snapshot client; it must not race live combat updates.
                var sourceSession=Loader.GetComponent<DragonWorldSession>();
                if(sourceSession && sourceSession.enabled)throw new InvalidOperationException("Disable DragonWorldSession when enabling DragonCombatClient");
                if(Loader.World==null)Loader.BuildWorld();
                foreach(var spawn in Loader.GetComponentsInChildren<DragonSpawn>())actors[spawn.Data.id]=spawn;
                client=new TcpClient();var connect=client.ConnectAsync(Host,Port);
                if(await Task.WhenAny(connect,Task.Delay(5000))!=connect)throw new TimeoutException("Combat connection timed out");
                await connect;if(stopped)return;
                using(var stream=client.GetStream())
                using(var input=new StreamReader(stream,new UTF8Encoding(false)))
                using(var output=new StreamWriter(stream,new UTF8Encoding(false)){AutoFlush=true,NewLine="\n"})
                {
                    var joined=await Call(input,output,"combat.join",new Parameters{sceneId=Loader.World.sceneId});
                    if(!joined.ok)throw new IOException("Could not join development combat world");
                    PlayerState=joined.result.player;
                    playerVisual=PlayerPrefab?Instantiate(PlayerPrefab,Loader.transform):new GameObject("Development Player");
                    if(!PlayerPrefab)
                    {
                        playerVisual.transform.SetParent(Loader.transform,false);
                        var marker=GameObject.CreatePrimitive(PrimitiveType.Capsule);marker.transform.SetParent(playerVisual.transform,false);marker.transform.localPosition=Vector3.up;
                    }
                    playerVisual.name="Development Player "+PlayerState.id;Apply(PlayerState,playerVisual.transform);
                    Debug.Log("Connected: source basic physical damage, source nav/stats, server-owned HP/cooldown. Development player profile; not full TLBB skills or account persistence.",this);
                    while(!stopped)
                    {
                        if(pendingMove.HasValue)
                        {
                            var move=pendingMove.Value;pendingMove=null;
                            await Call(input,output,"combat.move",new Parameters{x=move.x,z=move.z});
                        }
                        if(pendingAttack!=null)
                        {
                            var target=pendingAttack;pendingAttack=null;
                            var reply=await Call(input,output,"combat.attack",new Parameters{targetId=target});
                            if(reply.ok)Debug.Log("Attack: "+(reply.result.hit?reply.result.damage.ToString():"miss")+"; target HP "+reply.result.targetHp,this);
                        }
                        if(pendingRespawn){pendingRespawn=false;await Call(input,output,"combat.respawn",new Parameters());}
                        var offset=0;
                        do
                        {
                            var snapshot=await Call(input,output,"combat.snapshot",new Parameters{offset=offset,afterSequence=sequence});
                            if(!snapshot.ok)throw new IOException("Combat snapshot rejected");
                            var result=snapshot.result;PlayerState=result.player;Apply(PlayerState,playerVisual.transform);
                            if(result.entities!=null)foreach(var state in result.entities)
                            {
                                DragonSpawn actor;if(actors.TryGetValue(state.id,out actor))Apply(state,actor.transform);
                            }
                            if(result.events!=null)foreach(var item in result.events)CombatEvent?.Invoke(item);
                            sequence=result.sequence;
                            if(result.nextOffset>=result.total)break;
                            if(result.nextOffset<=offset)throw new InvalidDataException("Combat page did not advance");
                            offset=result.nextOffset;
                        }while(!stopped);
                        await Task.Delay(100);
                    }
                }
            }
            catch(Exception error){if(!stopped)Debug.LogError("Dragon combat: "+error.Message,this);}
            finally{client?.Close();}
        }
        private void Update()
        {
#if ENABLE_LEGACY_INPUT_MANAGER
            if(!Loader || PlayerState==null)return;
            if(Input.GetKeyDown(KeyCode.R))Respawn();
            if(!Input.GetMouseButtonDown(0))return;
            var camera=InputCamera?InputCamera:Camera.main;if(!camera)return;
            RaycastHit hit;if(!Physics.Raycast(camera.ScreenPointToRay(Input.mousePosition),out hit,2000))return;
            var spawn=hit.collider.GetComponentInParent<DragonSpawn>();
            if(spawn)Attack(spawn.Data.id);
            else MoveTo(Loader.transform.InverseTransformPoint(hit.point));
#endif
        }
        private void OnDestroy(){stopped=true;client?.Close();if(playerVisual)Destroy(playerVisual);}
    }
}
