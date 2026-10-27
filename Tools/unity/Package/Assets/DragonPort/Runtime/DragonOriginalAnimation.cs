using UnityEngine;
namespace DragonPort
{
    public sealed class DragonOriginalAnimation : MonoBehaviour
    {
        public string Idle,Run,Attack,Hit,Death;
        private Animation animationComponent;
        private string current;
        private void Awake(){animationComponent=GetComponent<Animation>();}
        private void Start(){PlayState("idle");}
        public void PlayState(string state)
        {
            if(!animationComponent)animationComponent=GetComponent<Animation>();
            if(!animationComponent)return;
            var clip=state=="dead"?Death:state=="attack"?Attack:state=="hit"?Hit:state=="run"?Run:Idle;
            if(string.IsNullOrEmpty(clip) || !animationComponent[clip])return;
            if(current==state && animationComponent.IsPlaying(clip))return;
            current=state;
            animationComponent[clip].wrapMode=(state=="idle" || state=="run")?WrapMode.Loop:WrapMode.ClampForever;
            animationComponent.CrossFade(clip,.08f);
        }
    }
}
