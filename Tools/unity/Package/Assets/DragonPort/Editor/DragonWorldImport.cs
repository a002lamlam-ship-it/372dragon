using System;
using System.IO;
using UnityEditor;
using UnityEngine;
namespace DragonPort.Editor
{
    public static class DragonWorldImport
    {
        private static Material MaterialAsset(string path,Shader shader,Color color)
        {
            var material=AssetDatabase.LoadAssetAtPath<Material>(path);
            if(material)return material;
            material=new Material(shader);
            if(material.HasProperty("_BaseColor"))material.SetColor("_BaseColor",color);
            if(material.HasProperty("_Color"))material.SetColor("_Color",color);
            AssetDatabase.CreateAsset(material,path);
            return material;
        }
        [MenuItem("Tools/Dragon Port/Enable Development Combat on Selected Map")]
        public static void EnableCombat()
        {
            var selected=Selection.activeGameObject;
            var loader=selected?selected.GetComponent<DragonWorldLoader>():null;
            if(!loader)throw new InvalidOperationException("Select the imported map root first");
            var snapshot=selected.GetComponent<DragonWorldSession>();
            if(snapshot){Undo.RecordObject(snapshot,"Disable source snapshot session");snapshot.enabled=false;EditorUtility.SetDirty(snapshot);}
            var combat=selected.GetComponent<DragonCombatClient>();
            if(!combat)combat=Undo.AddComponent<DragonCombatClient>(selected);
            combat.Loader=loader;combat.enabled=true;EditorUtility.SetDirty(combat);
        }
        [MenuItem("Tools/Dragon Port/Import Exported Map")]
        public static void Import()
        {
            var json=EditorUtility.OpenFilePanel("Select exported map JSON","","json");
            if(string.IsNullOrEmpty(json))return;
            ImportPath(json);
        }
        public static void ImportPath(string json)
        {
            var world=JsonUtility.FromJson<DragonWorldData>(File.ReadAllText(json));
            if(world==null || world.schema!=1 || world.width<=0)throw new InvalidDataException("Not a Dragon map export");
            var source=Path.GetDirectoryName(json);
            var destination="Assets/DragonPort/Imported/"+world.sceneId;
            Directory.CreateDirectory(destination);
            foreach(var suffix in new[]{".json",".heights.bytes",".cells.bytes"})
            {
                var input=Path.Combine(source,world.sceneId+suffix);
                var output=destination+"/"+world.sceneId+suffix;
                if(Path.GetFullPath(input)!=Path.GetFullPath(output)) File.Copy(input,output,true);
            }
            AssetDatabase.Refresh();
            var obj=new GameObject("Dragon Map "+world.sceneId+" "+world.name);
            Undo.RegisterCreatedObjectUndo(obj,"Import Dragon map");
            var loader=obj.AddComponent<DragonWorldLoader>();
            loader.WorldJson=AssetDatabase.LoadAssetAtPath<TextAsset>(destination+"/"+world.sceneId+".json");
            loader.HeightSamples=AssetDatabase.LoadAssetAtPath<TextAsset>(destination+"/"+world.sceneId+".heights.bytes");
            loader.CellFlags=AssetDatabase.LoadAssetAtPath<TextAsset>(destination+"/"+world.sceneId+".cells.bytes");
            var shader=Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Standard") ?? Shader.Find("HDRP/Lit");
            if(shader)
            {
                loader.GroundMaterial=MaterialAsset(destination+"/Ground.mat",shader,new Color(0.3f,0.4f,0.25f));
                loader.NpcMaterial=MaterialAsset(destination+"/Npc.mat",shader,Color.yellow);
                loader.MonsterMaterial=MaterialAsset(destination+"/Monster.mat",shader,Color.red);
            }
            obj.AddComponent<DragonWorldSession>().Loader=loader;
            EditorUtility.SetDirty(loader);
            Selection.activeGameObject=obj;
            Debug.Log("Assign a Ground Material (and optional Prefab Library), then use Build World or press Play.",obj);
        }
    }
}
