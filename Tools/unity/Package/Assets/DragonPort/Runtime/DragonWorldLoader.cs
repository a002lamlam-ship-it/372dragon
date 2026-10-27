using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
namespace DragonPort
{
    [DefaultExecutionOrder(-100)]
    public sealed class DragonWorldLoader : MonoBehaviour
    {
        public TextAsset WorldJson, HeightSamples, CellFlags;
        public DragonPrefabLibrary Prefabs;
        public Material GroundMaterial, NpcMaterial, MonsterMaterial;
        public bool ShowLabels = true;
        [Range(8,128)] public int TileSize = 64;
        private readonly List<Mesh> meshes = new List<Mesh>();
        public DragonWorldData World { get; private set; }
        private void Start() { if(World==null || !transform.Find("__DragonWorld"))BuildWorld(); }
        private void Clear()
        {
            var old = transform.Find("__DragonWorld");
            if (old != null) Remove(old.gameObject);
            foreach (var mesh in meshes) if (mesh != null) Remove(mesh);
            meshes.Clear();
        }
        private static void Remove(UnityEngine.Object value)
        {
            if (Application.isPlaying) Destroy(value); else DestroyImmediate(value);
        }
        [ContextMenu("Build World")]
        public void BuildWorld()
        {
            if (!WorldJson || !HeightSamples || !CellFlags) throw new InvalidOperationException("Assign all three exported data assets");
            World = JsonUtility.FromJson<DragonWorldData>(WorldJson.text);
            if (World == null || World.schema != 1 || World.width < 1 || World.depth < 1 || World.width > 4096 || World.depth > 4096)
                throw new InvalidDataException("Unsupported world schema/dimensions");
            var heights = HeightSamples.bytes;
            var flags = CellFlags.bytes;
            if (heights.Length != checked((World.width+1)*(World.depth+1)*4) || flags.Length != World.width*World.depth)
                throw new InvalidDataException("Terrain byte count mismatch");
            var samples = new float[heights.Length/4];
            using (var reader = new BinaryReader(new MemoryStream(heights)))
                for (var i=0; i<samples.Length; ++i)
                {
                    samples[i] = reader.ReadSingle();
                    if (float.IsNaN(samples[i]) || float.IsInfinity(samples[i])) throw new InvalidDataException("Invalid height");
                }
            Clear();
            var root = new GameObject("__DragonWorld"); root.transform.SetParent(transform,false);
            if (!Application.isPlaying) root.hideFlags = HideFlags.DontSave;
            var tileSize = Mathf.Clamp(TileSize,8,128);
            for (var z=0; z<World.depth; z+=tileSize)
                for (var x=0; x<World.width; x+=tileSize)
                    MakeTile(root.transform, samples, flags, x,z,Math.Min(tileSize,World.width-x),Math.Min(tileSize,World.depth-z));
            foreach (var entity in World.entities ?? new DragonEntityData[0])
            {
                var prefab = Prefabs ? Prefabs.Actor(entity.modelId) : null;
                GameObject actor;
                if (prefab)
                {
                    actor = Instantiate(prefab,root.transform);
                    actor.transform.localScale *= Prefabs.ActorScale(entity.modelId);
                }
                else
                {
                    actor = new GameObject(); actor.transform.SetParent(root.transform,false);
                    var marker = GameObject.CreatePrimitive(PrimitiveType.Capsule);
                    marker.transform.SetParent(actor.transform,false); marker.transform.localPosition = Vector3.up;
                    var material = entity.kind == "npc" ? NpcMaterial : MonsterMaterial;
                    if (material) marker.GetComponent<Renderer>().sharedMaterial = material;
                }
                actor.name = entity.kind+" "+entity.name+" ["+entity.id+"]";
                actor.transform.localPosition = new Vector3(entity.x,entity.y,entity.z);
                actor.transform.localRotation = Quaternion.Euler(0,entity.yaw,0);
                actor.AddComponent<DragonSpawn>().Data = entity;
                if(prefab)
                {
                    var hitbox=actor.AddComponent<CapsuleCollider>();hitbox.center=Vector3.up;hitbox.height=2;hitbox.radius=.5f;
                }
                if (ShowLabels)
                {
                    var label = new GameObject("Name"); label.transform.SetParent(actor.transform,false);
                    label.transform.localPosition = new Vector3(0,2.3f,0);
                    var text = label.AddComponent<TextMesh>(); text.text = entity.name;
                    text.anchor = TextAnchor.LowerCenter; text.characterSize = 0.15f; text.fontSize = 32;
                    text.color = entity.kind == "npc" ? Color.yellow : Color.red;
                }
            }
            var unresolved=0;
            foreach (var item in World.staticObjects ?? new DragonStaticData[0])
            {
                var prefab = Prefabs ? Prefabs.Scenery(item.resource) : null;
                if (!prefab) { ++unresolved; continue; }
                var scenery = Instantiate(prefab,root.transform);
                scenery.transform.localPosition = new Vector3(item.x,item.y,item.z);
                scenery.transform.localRotation = item.rotation;
                // Bind prefabs authored in server-grid units; preserve each placement's source scale.
                if (item.sourceScale != null && item.sourceScale.Length == 3)
                    scenery.transform.localScale = Vector3.Scale(scenery.transform.localScale,new Vector3(item.sourceScale[0],item.sourceScale[1],item.sourceScale[2]));
            }
            Debug.Log("Loaded "+World.name+": "+World.entities.Length+" spawn placements; "+unresolved+" scenery prefab bindings missing. Enable DragonCombatClient for development PvE.",this);
        }
        private void MakeTile(Transform root,float[] heights,byte[] flags,int startX,int startZ,int w,int d)
        {
            var vertices=new Vector3[(w+1)*(d+1)]; var uv=new Vector2[vertices.Length];
            for(var z=0;z<=d;++z) for(var x=0;x<=w;++x)
            {
                var i=z*(w+1)+x; var gx=startX+x; var gz=startZ+z;
                vertices[i]=new Vector3(gx,heights[gz*(World.width+1)+gx],gz);
                uv[i]=new Vector2((float)gx/World.width,(float)gz/World.depth);
            }
            var triangles=new List<int>(w*d*6);
            for(var z=0;z<d;++z) for(var x=0;x<w;++x)
            {
                var flag=flags[(startZ+z)*World.width+startX+x];
                if((flag&2)!=0)continue;
                var a=z*(w+1)+x; var b=a+1; var c=a+w+1; var e=c+1;
                if((flag&1)!=0) triangles.AddRange(new[]{a,c,e,a,e,b});
                else triangles.AddRange(new[]{a,c,b,b,c,e});
            }
            var mesh=new Mesh {name="Terrain "+startX+","+startZ};
            mesh.vertices=vertices;mesh.uv=uv;mesh.triangles=triangles.ToArray();mesh.RecalculateNormals();mesh.RecalculateBounds();meshes.Add(mesh);
            var tile=new GameObject(mesh.name);tile.transform.SetParent(root,false);
            tile.AddComponent<MeshFilter>().sharedMesh=mesh;
            tile.AddComponent<MeshRenderer>().sharedMaterial=GroundMaterial;
            tile.AddComponent<MeshCollider>().sharedMesh=mesh;
        }
        private void OnDestroy() { foreach(var mesh in meshes) if(mesh) Remove(mesh); }
    }
}
