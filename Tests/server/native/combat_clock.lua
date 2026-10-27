local skynet=require 'skynet'
require 'skynet.manager'
skynet.start(function()
 local ok,error=xpcall(function()
  local world=require 'unity_world'
  local legacy=require 'unity_legacy_combat'
  assert(legacy:calculate_hit_rate(0,0)==.5)
  assert(legacy:calculate_hit_rate(100,100)==.5)
  assert(legacy:calculate_critical_rate(20,1)==1)
  local attacker={get_attack_physics=function()return 100 end,get_obj_type=function()return 'monster'end,get_skill_info=function()return nil end}
  local defender={get_defence_physics=function()return 100 end,get_obj_type=function()return 'monster'end}
  assert(legacy:physical_damage(attacker,defender,0,0,{[0]=1000000})==50)
  local time=1000
  local engine=require('unity_combat').new(world,{now=function()return time end,random=function()return 1 end})
  local joined,code=engine:call(70,'combat.join',{sceneId=6});assert(joined,code)
  local target='6:monster0'
  local snapshot=assert(engine:call(70,'combat.snapshot',{limit=100}))
  local initial
  for _,mob in ipairs(snapshot.entities)do if mob.id==target then initial=mob.hp end end
  assert(initial and initial>0)
  local dead=false
  for i=1,30 do
   local result,why=engine:call(70,'combat.attack',{targetId=target,damage=99999999})
   assert(result,why)
   assert(result.damage<100 and result.targetHp>=0)
   local _,cooldown=engine:call(70,'combat.attack',{targetId=target})
   assert(cooldown=='ATTACK_COOLDOWN' or cooldown=='TARGET_DEAD')
   if result.dead then dead=true;break end
   time=time+600
  end
  assert(dead,'source monster did not die from authoritative attacks')
  local _,why=engine:call(70,'combat.attack',{targetId=target});assert(why=='TARGET_DEAD')
  local respawn
  for _,spawn in ipairs(world.get_world(6).entities)do if spawn.id==target then respawn=spawn.respawnMilliseconds end end
  time=time+respawn-1;engine:tick()
  local state=assert(engine:call(70,'combat.snapshot',{limit=100}))
  for _,mob in ipairs(state.entities)do if mob.id==target then assert(mob.hp==0)end end
  time=time+1;engine:tick()
  state=assert(engine:call(70,'combat.snapshot',{limit=100}))
  local found=false
  for _,mob in ipairs(state.entities)do if mob.id==target then assert(mob.hp==initial);found=true end end
  assert(found,'respawned monster snapshot missing')
  local moved,move_error=engine:call(70,'combat.move',{x=joined.player.x+.25,z=joined.player.z})
  assert(moved,move_error)
  local before=assert(engine:call(70,'combat.snapshot',{limit=100})).player
  time=time+100;engine:tick()
  local after=assert(engine:call(70,'combat.snapshot',{limit=100})).player
  assert(math.abs(after.x-before.x)<=.51 and math.abs(after.z-before.z)<=.51,'client movement exceeded server speed')
  engine:disconnect(70)
  local _,missing=engine:call(70,'combat.snapshot',{});assert(missing=='COMBAT_NOT_JOINED')
 end,debug.traceback)
 if ok then io.stdout:write('COMBAT_CLOCK_OK\n')else io.stdout:write('COMBAT_CLOCK_FAILED '..error..'\n')end
 io.stdout:flush();skynet.abort()
end)
