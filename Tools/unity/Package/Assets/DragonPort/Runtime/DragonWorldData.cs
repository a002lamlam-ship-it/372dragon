using System;
using UnityEngine;
namespace DragonPort
{
    [Serializable] public sealed class DragonWorldData
    {
        public int schema, sceneId, clientResourceId, width, depth;
        public string name, coordinates;
        public bool simulationReady;
        public DragonEntityData[] entities;
        public DragonStaticData[] staticObjects;
    }
    [Serializable] public sealed class DragonEntityData
    {
        public string id, kind, name, title, sourceSection;
        public int templateId, modelId, level, hp, scriptId, aiType, respawnMilliseconds;
        public float x, y, z, yaw;
    }
    [Serializable] public sealed class DragonStaticData
    {
        public string resource;
        public float x, y, z;
        public Quaternion rotation;
        public float[] sourceScale;
    }
}
