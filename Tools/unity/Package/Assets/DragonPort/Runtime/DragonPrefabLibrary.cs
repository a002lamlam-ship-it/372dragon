using System;
using UnityEngine;
namespace DragonPort
{
    [CreateAssetMenu(menuName="Dragon Port/Prefab Library")]
    public sealed class DragonPrefabLibrary : ScriptableObject
    {
        [Serializable] public sealed class ActorBinding
        {
            public int modelId;
            public float scale=1;
            public GameObject prefab;
        }
        [Serializable] public sealed class SceneryBinding
        {
            public string resource;
            public GameObject prefab;
        }
        public ActorBinding[] actors = new ActorBinding[0];
        public SceneryBinding[] scenery = new SceneryBinding[0];
        public GameObject Actor(int modelId)
        {
            foreach (var binding in actors) if (binding.modelId == modelId) return binding.prefab;
            return null;
        }
        public float ActorScale(int modelId)
        {
            foreach(var binding in actors)if(binding.modelId==modelId)return binding.scale;
            return 1;
        }
        public GameObject Scenery(string resource)
        {
            foreach (var binding in scenery) if (binding.resource == resource) return binding.prefab;
            return null;
        }
    }
}
