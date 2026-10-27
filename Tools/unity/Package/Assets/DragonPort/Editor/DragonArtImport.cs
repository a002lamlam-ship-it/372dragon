using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering;
namespace DragonPort.Editor
{
    public static class DragonArtImport
    {
        [Serializable] private sealed class Asset { public string assetId,file; }
        [Serializable] private sealed class Actor { public int modelId; public string assetId; public float importScale=1; }
        [Serializable] private sealed class Scenery { public string resource,assetId; }
        [Serializable] private sealed class Catalog { public int schema; public Asset[] assets; public Actor[] actorBindings; public Scenery[] sceneryBindings; }
        private const string Destination="Assets/DragonPort/GeneratedArt";
        private static Vector3 V(float[] values){return new Vector3(values[0],values[1],values[2]);}
        private static Quaternion Q(float[] values){return new Quaternion(values[0],values[1],values[2],values[3]).normalized;}
        private static string BoneName(int id){return "Bone_"+id.ToString("D3");}
        [MenuItem("Tools/Dragon Port/Import Original Meshes and Animations")]
        public static void Import()
        {
            var file=EditorUtility.OpenFilePanel("Select art-catalog.json inside imported Assets/DragonPort/Art","Assets/DragonPort/Art","json");
            if(string.IsNullOrEmpty(file))return;
            var source=Path.GetDirectoryName(file);
            var absoluteAssets=Path.GetFullPath(Application.dataPath)+Path.DirectorySeparatorChar;
            if(!Path.GetFullPath(source).StartsWith(absoluteAssets,StringComparison.Ordinal))throw new InvalidOperationException("Copy the art pack under this project's Assets folder first");
            var catalog=JsonUtility.FromJson<Catalog>(File.ReadAllText(file));
            if(catalog==null || catalog.schema!=1)throw new InvalidDataException("Invalid art catalog");
            Directory.CreateDirectory(Destination);AssetDatabase.Refresh();
            var prefabs=new Dictionary<string,GameObject>();
            try
            {
                for(var i=0;i<catalog.assets.Length;++i)
                {
                    var asset=catalog.assets[i];
                    if(EditorUtility.DisplayCancelableProgressBar("Import original art",asset.assetId,(float)i/catalog.assets.Length))break;
                    var prefabPath=Destination+"/"+asset.assetId+".prefab";
                    var prefab=AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath);
                    // Preserve existing generated/user-edited assets on repeated imports.
                    try
                    {
                        if(!prefab && !File.Exists(Path.Combine(source,asset.file)))continue; // Partial art packs are supported.
                        if(!prefab)prefab=Build(Path.Combine(source,asset.file),source,asset.assetId,prefabPath);
                        prefabs[asset.assetId]=prefab;
                    }
                    catch(Exception error){Debug.LogError("Art import failed for "+asset.assetId+": "+error.Message);}
                }
            }
            finally{EditorUtility.ClearProgressBar();AssetDatabase.SaveAssets();}
            var libraryPath=Destination+"/OriginalPrefabs.asset";
            var library=AssetDatabase.LoadAssetAtPath<DragonPrefabLibrary>(libraryPath);
            if(!library){library=ScriptableObject.CreateInstance<DragonPrefabLibrary>();AssetDatabase.CreateAsset(library,libraryPath);}
            var actors=new List<DragonPrefabLibrary.ActorBinding>(library.actors);
            var knownActors=new HashSet<int>();foreach(var old in library.actors)knownActors.Add(old.modelId);
            foreach(var binding in catalog.actorBindings)
            {
                GameObject prefab;
                if(!knownActors.Contains(binding.modelId) && prefabs.TryGetValue(binding.assetId,out prefab))actors.Add(new DragonPrefabLibrary.ActorBinding{modelId=binding.modelId,prefab=prefab,scale=binding.importScale});
            }
            var scenery=new List<DragonPrefabLibrary.SceneryBinding>(library.scenery);
            var knownScenery=new HashSet<string>();foreach(var old in library.scenery)knownScenery.Add(old.resource);
            foreach(var binding in catalog.sceneryBindings)
            {
                GameObject prefab;
                if(!knownScenery.Contains(binding.resource) && prefabs.TryGetValue(binding.assetId,out prefab))scenery.Add(new DragonPrefabLibrary.SceneryBinding{resource=binding.resource,prefab=prefab});
            }
            library.actors=actors.ToArray();library.scenery=scenery.ToArray();EditorUtility.SetDirty(library);AssetDatabase.SaveAssets();
            Selection.activeObject=library;
            Debug.Log("Imported "+prefabs.Count+" original meshes. Assign OriginalPrefabs to DragonWorldLoader.Prefabs. See art-catalog.json for missing/unsupported assets and unverified object composition.");
        }
        private static GameObject Build(string file,string source,string id,string prefabPath)
        {
            var data=JsonUtility.FromJson<DragonArtData>(File.ReadAllText(file));
            if(data==null || data.schema!=1)throw new InvalidDataException("Invalid art data");
            var folder=Destination+"/"+id;
            if(Directory.Exists(folder))throw new InvalidOperationException("Existing partial asset folder preserved: "+folder);
            Directory.CreateDirectory(folder);AssetDatabase.Refresh();
            var root=new GameObject(id);
            try
            {
                var bones=new Dictionary<int,Transform>();var boneData=new Dictionary<int,DragonBone>();var boneOrder=new List<int>();
                Transform rigRoot=null;
                if(data.rig!=null && data.rig.bones!=null)
                {
                    rigRoot=new GameObject("Rig").transform;rigRoot.SetParent(root.transform,false);
                    foreach(var bone in data.rig.bones)
                    {
                        var t=new GameObject(BoneName(bone.id)).transform;bones.Add(bone.id,t);boneData.Add(bone.id,bone);boneOrder.Add(bone.id);
                    }
                    boneOrder.Sort();
                    foreach(var bone in data.rig.bones)
                    {
                        var t=bones[bone.id];t.SetParent(bone.parent<0?rigRoot:bones[bone.parent],false);
                        t.localPosition=V(bone.position);t.localRotation=Q(bone.rotation);t.localScale=V(bone.scale);
                    }
                }
                for(var partIndex=0;partIndex<data.parts.Length;++partIndex)
                {
                    var part=data.parts[partIndex];var count=part.positions.Length/3;
                    var vertices=new Vector3[count];for(var j=0;j<count;++j)vertices[j]=new Vector3(part.positions[j*3],part.positions[j*3+1],part.positions[j*3+2]);
                    var mesh=new Mesh{name=id+"_"+partIndex,indexFormat=count>65535?IndexFormat.UInt32:IndexFormat.UInt16};mesh.vertices=vertices;mesh.triangles=part.triangles;
                    if(part.normals!=null && part.normals.Length==count*3)
                    {
                        var normals=new Vector3[count];for(var j=0;j<count;++j)normals[j]=new Vector3(part.normals[j*3],part.normals[j*3+1],part.normals[j*3+2]);mesh.normals=normals;
                    }
                    else mesh.RecalculateNormals();
                    if(part.uv!=null && part.uvComponents>=2 && part.uv.Length==count*part.uvComponents)
                    {
                        var uv=new Vector2[count];for(var j=0;j<count;++j)uv[j]=new Vector2(part.uv[j*part.uvComponents],part.uv[j*part.uvComponents+1]);mesh.uv=uv;mesh.RecalculateTangents();
                    }
                    var child=new GameObject("Mesh_"+partIndex);child.transform.SetParent(root.transform,false);
                    Renderer renderer;
                    if(part.hasSkin)
                    {
                        if(!rigRoot)throw new InvalidDataException("Skin without rig");
                        var dense=new Dictionary<int,int>();var transforms=new Transform[boneOrder.Count];var bindposes=new Matrix4x4[boneOrder.Count];
                        for(var j=0;j<boneOrder.Count;++j){dense[boneOrder[j]]=j;transforms[j]=bones[boneOrder[j]];bindposes[j]=transforms[j].worldToLocalMatrix*child.transform.localToWorldMatrix;}
                        var weights=new BoneWeight[count];
                        for(var j=0;j<count;++j)
                        {
                            var k=j*4;
                            weights[j]=new BoneWeight{boneIndex0=part.weights[k]>0?dense[part.boneIds[k]]:0,boneIndex1=part.weights[k+1]>0?dense[part.boneIds[k+1]]:0,boneIndex2=part.weights[k+2]>0?dense[part.boneIds[k+2]]:0,boneIndex3=part.weights[k+3]>0?dense[part.boneIds[k+3]]:0,weight0=part.weights[k],weight1=part.weights[k+1],weight2=part.weights[k+2],weight3=part.weights[k+3]};
                        }
                        mesh.boneWeights=weights;mesh.bindposes=bindposes;
                        var skin=child.AddComponent<SkinnedMeshRenderer>();skin.bones=transforms;skin.rootBone=rigRoot;skin.sharedMesh=mesh;skin.updateWhenOffscreen=true;renderer=skin;
                    }
                    else
                    {
                        child.AddComponent<MeshFilter>().sharedMesh=mesh;renderer=child.AddComponent<MeshRenderer>();
                        child.AddComponent<MeshCollider>().sharedMesh=mesh;
                    }
                    mesh.RecalculateBounds();AssetDatabase.CreateAsset(mesh,folder+"/Mesh_"+partIndex+".asset");
                    var info=data.materials[partIndex];var shader=Shader.Find("Universal Render Pipeline/Lit")??Shader.Find("Standard")??Shader.Find("HDRP/Lit");
                    if(!shader)throw new InvalidOperationException("No supported lit shader found");
                    var material=new Material(shader){name=info.name};
                    if(!string.IsNullOrEmpty(info.textureFile))
                    {
                        var absolute=Path.GetFullPath(Path.Combine(source,info.textureFile)).Replace('\\','/');
                        var assetPath="Assets"+absolute.Substring(Path.GetFullPath(Application.dataPath).Replace('\\','/').Length);
                        var texture=AssetDatabase.LoadAssetAtPath<Texture2D>(assetPath);
                        if(!texture)throw new InvalidDataException("Missing texture; copy all art packs before import: "+info.textureFile);
                        if(material.HasProperty("_BaseMap"))material.SetTexture("_BaseMap",texture);
                        if(material.HasProperty("_MainTex"))material.SetTexture("_MainTex",texture);
                    }
                    if(info.alphaCutoff>0)
                    {
                        material.EnableKeyword("_ALPHATEST_ON");material.SetFloat("_Cutoff",info.alphaCutoff);material.renderQueue=2450;
                        if(material.HasProperty("_AlphaClip"))material.SetFloat("_AlphaClip",1);
                        if(material.HasProperty("_Mode"))material.SetFloat("_Mode",1);
                    }
                    if(info.transparent)
                    {
                        if(material.HasProperty("_Surface"))material.SetFloat("_Surface",1);
                        if(material.HasProperty("_Mode"))material.SetFloat("_Mode",3);
                        material.SetInt("_SrcBlend",(int)BlendMode.SrcAlpha);material.SetInt("_DstBlend",(int)BlendMode.OneMinusSrcAlpha);material.SetInt("_ZWrite",0);material.EnableKeyword("_ALPHABLEND_ON");material.renderQueue=3000;
                    }
                    if(info.doubleSided && material.HasProperty("_Cull"))material.SetInt("_Cull",(int)CullMode.Off);
                    AssetDatabase.CreateAsset(material,folder+"/Material_"+partIndex+".mat");renderer.sharedMaterial=material;
                }
                if(data.rig!=null && data.rig.animations!=null && data.rig.animations.Length>0)
                {
                    var animation=root.AddComponent<Animation>();var names=new List<string>();
                    for(var index=0;index<data.rig.animations.Length;++index)
                    {
                        var original=data.rig.animations[index];var clip=new AnimationClip{name=original.name,legacy=true,frameRate=30};
                        foreach(var track in original.tracks)
                        {
                            var bone=boneData[track.boneId];var path=AnimationUtility.CalculateTransformPath(bones[track.boneId],root.transform);
                            var position=new[]{new AnimationCurve(),new AnimationCurve(),new AnimationCurve()};
                            var rotation=new[]{new AnimationCurve(),new AnimationCurve(),new AnimationCurve(),new AnimationCurve()};
                            var scale=new[]{new AnimationCurve(),new AnimationCurve(),new AnimationCurve()};
                            foreach(var key in track.keys)
                            {
                                var p=V(bone.position)+V(key.position);var q=Q(bone.rotation)*Q(key.rotation);var s=Vector3.Scale(V(bone.scale),V(key.scale));
                                for(var axis=0;axis<3;++axis){position[axis].AddKey(key.time,p[axis]);scale[axis].AddKey(key.time,s[axis]);}
                                for(var axis=0;axis<4;++axis)rotation[axis].AddKey(key.time,q[axis]);
                            }
                            for(var axis=0;axis<3;++axis){SetCurve(clip,path,"localPosition."+"xyz"[axis],position[axis]);SetCurve(clip,path,"localScale."+"xyz"[axis],scale[axis]);}
                            for(var axis=0;axis<4;++axis)SetCurve(clip,path,"localRotation."+"xyzw"[axis],rotation[axis]);
                        }
                        clip.EnsureQuaternionContinuity();AssetDatabase.CreateAsset(clip,folder+"/Clip_"+index+".anim");animation.AddClip(clip,original.name);names.Add(original.name);
                    }
                    var playback=root.AddComponent<DragonOriginalAnimation>();playback.Idle=Choose(names,"站立","idle","stand","休闲");playback.Run=Choose(names,"跑步","行走","run","walk");playback.Attack=Choose(names,"攻击","attack");playback.Hit=Choose(names,"受击","hit");playback.Death=Choose(names,"倒地","死亡","death","die");
                }
                return PrefabUtility.SaveAsPrefabAsset(root,prefabPath);
            }
            catch
            {
                // Only this newly created transaction folder is removed; pre-existing folders were rejected above.
                AssetDatabase.DeleteAsset(folder);throw;
            }
            finally{UnityEngine.Object.DestroyImmediate(root);}
        }
        private static void SetCurve(AnimationClip clip,string path,string property,AnimationCurve curve)
        {
            for(var i=0;i<curve.length;++i){AnimationUtility.SetKeyLeftTangentMode(curve,i,AnimationUtility.TangentMode.Linear);AnimationUtility.SetKeyRightTangentMode(curve,i,AnimationUtility.TangentMode.Linear);}
            clip.SetCurve(path,typeof(Transform),property,curve);
        }
        private static string Choose(List<string> names,params string[] choices)
        {
            foreach(var choice in choices)foreach(var name in names)if(name.Equals(choice,StringComparison.OrdinalIgnoreCase))return name;
            foreach(var choice in choices)foreach(var name in names)if(name.IndexOf(choice,StringComparison.OrdinalIgnoreCase)>=0)return name;
            return names.Count>0?names[0]:null;
        }
    }
}
