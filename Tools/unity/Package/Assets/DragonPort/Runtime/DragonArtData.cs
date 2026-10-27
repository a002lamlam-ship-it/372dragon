using System;
namespace DragonPort
{
    [Serializable] public sealed class DragonArtData
    {
        public int schema;
        public DragonArtPart[] parts;
        public DragonRig rig;
        public DragonArtMaterial[] materials;
    }
    [Serializable] public sealed class DragonArtPart
    {
        public string material;
        public float[] positions,normals,uv,weights;
        public int[] triangles,boneIds;
        public int uvComponents;
        public bool hasSkin;
    }
    [Serializable] public sealed class DragonRig
    {
        public DragonBone[] bones;
        public DragonClip[] animations;
    }
    [Serializable] public sealed class DragonBone
    {
        public int id,parent;
        public string name;
        public float[] position,rotation,scale;
    }
    [Serializable] public sealed class DragonClip
    {
        public string name;
        public float duration;
        public DragonTrack[] tracks;
    }
    [Serializable] public sealed class DragonTrack
    {
        public int boneId;
        public DragonKey[] keys;
    }
    [Serializable] public sealed class DragonKey
    {
        public float time;
        public float[] position,rotation,scale;
    }
    [Serializable] public sealed class DragonArtMaterial
    {
        public string name,textureFile;
        public bool transparent,doubleSided,sourceMaterialFound,shaderApproximation;
        public float alphaCutoff;
    }
}
