using System;
using System.IO;
using UnityEditor;
using UnityEngine;
namespace DragonPort.Editor
{
    public sealed class DragonWorldBrowser : EditorWindow
    {
        [Serializable] private sealed class Map
        {
            public int sceneId,width,depth,entityCount,npcCount,monsterCount,warningCount,skippedEntityCount;
            public string name;
        }
        [Serializable] private sealed class Catalog { public int schema; public Map[] scenes; }
        private TextAsset catalogAsset;
        private Catalog catalog;
        private string query="";
        private Vector2 scroll;
        [MenuItem("Tools/Dragon Port/Browse Maps")]
        public static void Open(){GetWindow<DragonWorldBrowser>("Dragon Maps");}
        private void OnEnable()
        {
            catalogAsset=AssetDatabase.LoadAssetAtPath<TextAsset>("Assets/DragonPort/Data/catalog.json");
            Reload();
        }
        private void Reload()
        {
            catalog=catalogAsset ? JsonUtility.FromJson<Catalog>(catalogAsset.text) : null;
        }
        private void OnGUI()
        {
            EditorGUI.BeginChangeCheck();
            catalogAsset=(TextAsset)EditorGUILayout.ObjectField("Catalog",catalogAsset,typeof(TextAsset),false);
            if(EditorGUI.EndChangeCheck())Reload();
            query=EditorGUILayout.TextField("Find ID or name",query);
            if(catalog==null || catalog.schema!=1 || catalog.scenes==null)
            {EditorGUILayout.HelpBox("Choose the exported catalog.json from the map package.",MessageType.Info);return;}
            EditorGUILayout.LabelField(catalog.scenes.Length+" exported maps; source placements only, no live AI.");
            scroll=EditorGUILayout.BeginScrollView(scroll);
            foreach(var map in catalog.scenes)
            {
                if(query.Length>0 && map.name.IndexOf(query,StringComparison.OrdinalIgnoreCase)<0 && !map.sceneId.ToString().Contains(query))continue;
                EditorGUILayout.BeginVertical("box");
                EditorGUILayout.LabelField(map.sceneId+" — "+map.name,EditorStyles.boldLabel);
                EditorGUILayout.LabelField(map.width+"×"+map.depth+" | NPC "+map.npcCount+" | Other spawns "+map.monsterCount);
                if(map.warningCount>0 || map.skippedEntityCount>0)
                    EditorGUILayout.LabelField("Source warnings: "+map.warningCount+"; skipped entities: "+map.skippedEntityCount);
                if(GUILayout.Button("Import this map"))
                {
                    var directory=Path.GetDirectoryName(AssetDatabase.GetAssetPath(catalogAsset));
                    var path=Path.Combine(directory,map.sceneId.ToString(),map.sceneId+".json");
                    if(File.Exists(path))DragonWorldImport.ImportPath(path);
                    else Debug.LogError("Map bundle missing: "+path);
                }
                EditorGUILayout.EndVertical();
            }
            EditorGUILayout.EndScrollView();
        }
    }
}
