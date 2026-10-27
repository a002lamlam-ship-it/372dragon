using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
namespace DragonPort
{
    // Fetches real source placements from the native gateway; not a multiplayer simulation client.
    public sealed class DragonWorldSession : MonoBehaviour
    {
        public string Host="127.0.0.1";
        public int Port=15800;
        public DragonWorldLoader Loader;
        private TcpClient client;
        private bool destroyed;
        [Serializable] private sealed class Parameters { public int sceneId,offset,limit=50; }
        [Serializable] private sealed class Request { public int v=1; public string id,method; public Parameters @params; }
        [Serializable] private sealed class Result { public int sceneId,width,depth,entityCount,total,nextOffset; public bool simulationReady; public DragonEntityData[] items; }
        [Serializable] private sealed class Error { public string code; }
        [Serializable] private sealed class Reply { public int v; public string id; public bool ok; public Result result; public Error error; }
        private async Task<Reply> Call(StreamReader input,StreamWriter output,string method,Parameters parameters)
        {
            var request=new Request {id=Guid.NewGuid().ToString("N"),method=method,@params=parameters};
            await output.WriteLineAsync(JsonUtility.ToJson(request));
            var read=input.ReadLineAsync();
            if(await Task.WhenAny(read,Task.Delay(5000))!=read)throw new TimeoutException("World response timeout");
            var line=await read;
            if(line==null)throw new IOException("Gateway disconnected");
            var reply=JsonUtility.FromJson<Reply>(line);
            if(reply==null || reply.v!=1 || reply.id!=request.id || !reply.ok)
                throw new IOException(reply!=null && reply.error!=null ? reply.error.code : "Invalid world response");
            return reply;
        }
        private async void Start()
        {
            try
            {
                if(!Loader)Loader=GetComponent<DragonWorldLoader>();
                if(!Loader)throw new InvalidOperationException("Assign DragonWorldLoader");
                if(Loader.World==null)Loader.BuildWorld();
                client=new TcpClient();
                var connect=client.ConnectAsync(Host,Port);
                if(await Task.WhenAny(connect,Task.Delay(5000))!=connect)throw new TimeoutException("Gateway connection timeout");
                await connect;
                if(destroyed)return;
                using(var stream=client.GetStream())
                using(var input=new StreamReader(stream,new UTF8Encoding(false)))
                using(var output=new StreamWriter(stream,new UTF8Encoding(false)){AutoFlush=true,NewLine="\n"})
                {
                    var p=new Parameters {sceneId=Loader.World.sceneId};
                    var entered=await Call(input,output,"world.enter",p);
                    if(entered.result.sceneId!=Loader.World.sceneId || entered.result.width!=Loader.World.width || entered.result.depth!=Loader.World.depth)
                        throw new InvalidDataException("Local terrain and server world do not match");
                    var actors=Loader.GetComponentsInChildren<DragonSpawn>();
                    var known=new System.Collections.Generic.Dictionary<string,DragonSpawn>();
                    foreach(var actor in actors)known[actor.Data.id]=actor;
                    var count=0;
                    while(p.offset<entered.result.entityCount)
                    {
                        var page=await Call(input,output,"world.entities",p);
                        if(page.result.nextOffset<=p.offset || page.result.nextOffset>page.result.total)throw new InvalidDataException("Invalid pagination");
                        foreach(var entity in page.result.items)
                        {
                            DragonSpawn actor;
                            if(!known.TryGetValue(entity.id,out actor))throw new InvalidDataException("Local spawn bundle differs from server");
                            actor.Data=entity;
                            actor.transform.localPosition=new Vector3(entity.x,entity.y,entity.z);
                            actor.transform.localRotation=Quaternion.Euler(0,entity.yaw,0);
                            ++count;
                        }
                        p.offset=page.result.nextOffset;
                    }
                    if(!destroyed)Debug.Log("Native world synchronized: "+count+" placements. Live AI/combat are not connected.",this);
                }
            }
            catch(Exception error){if(!destroyed)Debug.LogError("Dragon world: "+error.Message,this);}
            finally{client?.Close();}
        }
        private void OnDestroy(){destroyed=true;client?.Close();}
    }
}
