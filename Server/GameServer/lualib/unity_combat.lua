-- Authoritative development PvE adapter. Reuses source basic physical formulas/stats/nav;
-- does not claim the full TLBB skill/equipment/impact/mission systems are connected.
local json=require 'cjson'
local legacy=require 'unity_legacy_combat'
local M={}
local function read_json(path)
    local file=io.open(path,'rb');if not file then return nil end
    local raw=file:read('*a');file:close();local ok,data=pcall(json.decode,raw);if ok then return data end
end
local function finite(v)return type(v)=='number' and v==v and v~=math.huge and v~=-math.huge end
local function distance(a,b)local dx,dz=a.x-b.x,a.z-b.z;return math.sqrt(dx*dx+dz*dz)end
local function actor(stats,kind)
    return {stats=stats,get_attack_physics=function(self)return self.stats.attack end,
        get_defence_physics=function(self)return self.stats.defence end,
        get_obj_type=function()return kind end,get_skill_info=function()return nil end,item_value=function()return 0 end}
end
function M.new(world_provider,opts)
    opts=opts or {};local skynet=require 'skynet'
    local now=opts.now or function()return skynet.now()*10 end
    local roll=opts.random or math.random
    local root=world_provider.data_root()
    local data=root and read_json(root..'/combat-data.json')
    local sessions,worlds,order={},{},{}
    local engine={}
    local function event(world,kind,fields)
        world.sequence=world.sequence+1;fields.kind=kind;fields.sequence=world.sequence;fields.time=now()
        world.events[#world.events+1]=fields
        if #world.events>128 then table.remove(world.events,1)end
    end
    local function height(world,x,z)
        local w,d=world.source.width,world.source.depth
        x=math.max(0,math.min(w,x));z=math.max(0,math.min(d,z))
        local ix,iz=math.min(math.floor(x),w-1),math.min(math.floor(z),d-1)
        local u,v=x-ix,z-iz
        local function sample(a,b)return string.unpack('<f',world.heights,((b*(w+1)+a)*4)+1)end
        local a,b,c,e=sample(ix,iz),sample(ix+1,iz),sample(ix,iz+1),sample(ix+1,iz+1)
        if (world.flags:byte(iz*w+ix+1)&1)~=0 then
            if v<=u then return a+(b-a)*u+(e-b)*v else return a+(e-c)*u+(c-a)*v end
        end
        if u+v<=1 then return a+(b-a)*u+(c-a)*v end
        return e+(c-e)*(1-u)+(b-e)*(1-v)
    end
    local function valid(world,x,z)
        return finite(x) and finite(z) and x>=0 and z>=0 and x<world.source.width and z<world.source.depth
    end
    local function route(world,a,b)
        if not valid(world,a.x,a.z) or not valid(world,b.x,b.z)then return nil end
        if not world.nav:walkable({x=a.x,y=a.z}) or not world.nav:walkable({x=b.x,y=b.z})then return nil end
        if distance(a,b)<.01 then return {} end
        local nodes=world.nav:findpath({x=a.x,y=a.z},{x=b.x,y=b.z})
        if not nodes or #nodes==0 then return nil end
        return nodes
    end
    local function load_world(id)
        if worlds[id]then return worlds[id]end
        local source=world_provider.get_world(id)
        if not source then return nil,'WORLD_NOT_FOUND' end
        if not source.combatNavigationAvailable or not source.navFile then return nil,'COMBAT_NAV_UNAVAILABLE' end
        if #order>=4 then
            local evict
            for i,key in ipairs(order)do if next(worlds[key].players)==nil then evict=i;break end end
            if not evict then return nil,'COMBAT_WORLD_CAPACITY' end
            worlds[table.remove(order,evict)]=nil
        end
        local nav=(opts.nav_factory or function()return require('unitynav').new()end)()
        if not nav:load(root..'/'..source.navFile)then return nil,'COMBAT_NAV_UNAVAILABLE' end
        local function binary(suffix)
            local file=io.open(root..'/'..string.format('%d',id)..suffix,'rb');if not file then return nil end
            local result=file:read('*a');file:close();return result
        end
        local heights,flags=binary('.heights.bytes'),binary('.cells.bytes')
        if not heights or #heights~=(source.width+1)*(source.depth+1)*4 or not flags or #flags~=source.width*source.depth then return nil,'COMBAT_TERRAIN_UNAVAILABLE' end
        local world={source=source,nav=nav,heights=heights,flags=flags,mobs={},players={},events={},sequence=0,lastTick=now()}
        for _,spawn in ipairs(source.entities)do
            local stats=data.templates[string.format('%d',spawn.templateId)]
            if stats then
                local mob=actor(stats,'monster');mob.id=spawn.id;mob.spawn=spawn;mob.hp=stats.hp;mob.maxHp=stats.hp
                mob.x,mob.y,mob.z=spawn.x,spawn.y,spawn.z;mob.action='idle';mob.cooldown=0;mob.yaw=spawn.yaw or 0
                mob.hostile=spawn.kind=='monster' and not stats.isNpc and (spawn.aiType==1 or spawn.aiType==2) and stats.hp>0
                world.mobs[mob.id]=mob
            end
        end
        worlds[id]=world;order[#order+1]=id;return world
    end
    local function attack(world,sender,target)
        local t=now();sender.yaw=math.deg(math.atan(target.x-sender.x,target.z-sender.z));sender.cooldown=t+math.max(100,sender.stats.cooldownMilliseconds)
        sender.action='attack';sender.actionUntil=t+math.max(100,sender.stats.actionMilliseconds or 500)
        local accuracy=legacy:calculate_hit_rate(sender.stats.hit,target.stats.miss)
        local hit=legacy:is_hit(accuracy,roll(100));local damage=0;local critical=false
        if hit then
            local trait=sender.stats.traitId and data.physicalTraits[string.format('%d',sender.stats.traitId)] or 1000000
            if not trait then return nil,'COMBAT_TRAIT_UNAVAILABLE' end
            damage=legacy:physical_damage(sender,target,0,0,{[0]=trait})
            -- Original configs:get_fluctuation = 1.2; same random expression as combat_core.
            damage=damage*(1+(2*1.2*(50-roll(100))/100)/100)
            critical=legacy:is_critical_hit(legacy:calculate_critical_rate(sender.stats.critical,target.stats.criticalDefence),roll(100))
            if critical then damage=damage*2.2 end -- source std_impact_003 baseline +120%; equipment hooks excluded.
            damage=math.min(target.hp,math.max(0,math.floor(damage)))
            target.hp=target.hp-damage
            if target.hp<=0 then
                target.action='dead';target.path=nil;target.deadAt=t
                if target.spawn then
                    local delay=target.spawn.respawnMilliseconds
                    target.respawnAt=delay and delay>=0 and t+delay or nil
                end
                event(world,'death',{targetId=target.id,sourceId=sender.id})
            elseif damage>0 then target.action='hit';target.actionUntil=t+300 end
        end
        event(world,hit and 'damage' or 'miss',{sourceId=sender.id,targetId=target.id,damage=damage,critical=critical,hp=target.hp})
        return {damage=damage,hit=hit,critical=critical,targetId=target.id,targetHp=target.hp,dead=target.hp<=0,cooldownUntil=sender.cooldown}
    end
    local function advance(world,unit,dt)
        if not unit.path or unit.hp<=0 then return end
        local budget=math.max(0,unit.stats.speed or 0)*dt/1000
        local oldX,oldZ=unit.x,unit.z
        while budget>0 and unit.path[unit.pathIndex or 1]do
            unit.pathIndex=unit.pathIndex or 1
            local node=unit.path[unit.pathIndex];local goal={x=node.x,z=node.y};local length=distance(unit,goal)
            if length<=budget then unit.x,unit.z=goal.x,goal.z;budget=budget-length;unit.pathIndex=unit.pathIndex+1
            else local factor=budget/length;unit.x=unit.x+(goal.x-unit.x)*factor;unit.z=unit.z+(goal.z-unit.z)*factor;budget=0 end
        end
        unit.y=height(world,unit.x,unit.z)
        if math.abs(unit.x-oldX)+math.abs(unit.z-oldZ)>.0001 then unit.yaw=math.deg(math.atan(unit.x-oldX,unit.z-oldZ))end
        if not unit.path[unit.pathIndex or 1]then unit.path=nil;unit.pathIndex=nil end
        if not unit.actionUntil or now()>=unit.actionUntil then unit.action=unit.path and 'run' or 'idle' end
    end
    function engine:tick()
        local t=now()
        for _,world in pairs(worlds)do
            local dt=math.max(0,math.min(500,t-world.lastTick));world.lastTick=t
            for _,player in pairs(world.players)do advance(world,player,dt)end
            for _,mob in pairs(world.mobs)do
                if mob.hp<=0 then
                    if mob.respawnAt and t>=mob.respawnAt then
                        mob.hp=mob.maxHp;mob.x,mob.y,mob.z=mob.spawn.x,mob.spawn.y,mob.spawn.z;mob.action='idle';mob.respawnAt=nil;mob.target=nil
                        event(world,'respawn',{targetId=mob.id,hp=mob.hp})
                    end
                elseif mob.hostile and next(world.players)then
                    local target=mob.target and world.players[mob.target]
                    if not target or target.hp<=0 or distance(target,mob)>12 or distance(mob,mob.spawn)>16 then target=nil;mob.target=nil end
                    if not target and mob.spawn.aiType==1 then
                        local nearest=6
                        for id,player in pairs(world.players)do
                            local d=distance(mob,player)
                            if player.hp>0 and d<nearest then target=player;nearest=d;mob.target=id end
                        end
                    end
                    if target then
                        local d=distance(mob,target)
                        if d<=3 then
                            mob.path=nil
                            if t>=mob.cooldown then
                                local nodes=route(world,mob,target);local length=0;local previous=mob
                                if nodes then for _,node in ipairs(nodes)do local nextpos={x=node.x,z=node.y};length=length+distance(previous,nextpos);previous=nextpos end end
                                if nodes and length<=3.75 then attack(world,mob,target)end
                            end
                        elseif t>=(mob.repathAt or 0)then mob.path=route(world,mob,target);mob.pathIndex=1;mob.repathAt=t+1000 end
                    elseif distance(mob,mob.spawn)>.1 and t>=(mob.repathAt or 0)then mob.path=route(world,mob,mob.spawn);mob.pathIndex=1;mob.repathAt=t+1000 end
                    advance(world,mob,dt)
                end
                if mob.hp>0 and mob.actionUntil and t>=mob.actionUntil then mob.actionUntil=nil;mob.action=mob.path and 'run' or 'idle' end
            end
        end
    end
    local function view(unit)
        return {id=unit.id,x=unit.x,y=unit.y,z=unit.z,hp=unit.hp,maxHp=unit.maxHp,action=unit.action,yaw=unit.yaw or 0,alive=unit.hp>0,modelId=unit.spawn and unit.spawn.modelId or 0}
    end
    function engine:disconnect(connection)
        local player=sessions[connection]
        if player then player.world.players[player.id]=nil;sessions[connection]=nil end
    end
    function engine:call(connection,method,params)
        if not data then return nil,'COMBAT_DATA_UNAVAILABLE' end
        if type(params)~='table' then return nil,'INVALID_PARAMS' end
        self:tick()
        if method=='combat.join' then
            if sessions[connection]then return nil,'COMBAT_ALREADY_JOINED' end
            if not finite(params.sceneId) or params.sceneId%1~=0 then return nil,'WORLD_NOT_FOUND' end
            local sessionCount=0;for _ in pairs(sessions)do sessionCount=sessionCount+1 end
            if sessionCount>=32 then return nil,'COMBAT_SESSION_CAPACITY' end
            local world,error=load_world(params.sceneId);if not world then return nil,error end
            local anchor
            for _,spawn in ipairs(world.source.entities)do
                if valid(world,spawn.x,spawn.z) and world.nav:walkable({x=spawn.x,y=spawn.z})then anchor=spawn;break end
            end
            if not anchor then return nil,'COMBAT_NO_WALKABLE_SPAWN' end
            local player=actor(data.profile,'human');player.id='player:'..tostring(connection);player.world=world;player.hp=data.profile.hp;player.maxHp=player.hp
            local spawn=world.nav:findempty({x=math.min(world.source.width-.1,anchor.x+2.5),y=anchor.z}) or {x=anchor.x,y=anchor.z}
            player.x,player.z=spawn.x,spawn.y;player.y=height(world,player.x,player.z);player.home={x=player.x,z=player.z};player.action='idle';player.cooldown=0
            sessions[connection]=player;world.players[player.id]=player
            return {player=view(player),sceneId=world.source.sceneId,combatMode='legacy-basic-physical',persistent=false,fullLegacySkills=false}
        end
        local player=sessions[connection]
        if not player then return nil,'COMBAT_NOT_JOINED' end
        local world=player.world
        if method=='combat.leave' then self:disconnect(connection);return {left=true}end
        if method=='combat.snapshot' then
            local offset,limit=params.offset or 0,params.limit or 50
            if not finite(offset) or offset<0 or offset%1~=0 or not finite(limit) or limit<1 or limit>100 or limit%1~=0 then return nil,'INVALID_PAGINATION' end
            local nearby={}
            for _,mob in pairs(world.mobs)do if distance(mob,player)<=40 then nearby[#nearby+1]=mob end end
            table.sort(nearby,function(a,b)return a.id<b.id end)
            local items={};for i=offset+1,math.min(#nearby,offset+limit)do items[#items+1]=view(nearby[i])end
            local events={};local after=params.afterSequence or 0
            if not finite(after) or after<0 then return nil,'INVALID_PARAMS' end
            for _,item in ipairs(world.events)do if item.sequence>after then events[#events+1]=item;if #events>=64 then break end end end
            return {player=view(player),entities=#items>0 and items or json.null,total=#nearby,nextOffset=math.min(offset+limit,#nearby),events=#events>0 and events or json.null,sequence=#events>0 and events[#events].sequence or world.sequence,latestSequence=world.sequence,eventsTruncated=#world.events>0 and after<world.events[1].sequence-1 or false,combatMode='legacy-basic-physical',fullLegacySkills=false}
        end
        if method=='combat.respawn' then
            if player.hp>0 then return nil,'PLAYER_ALIVE' end
            if now()<(player.deadAt or now())+5000 then return nil,'RESPAWN_COOLDOWN' end
            player.hp=player.maxHp;player.x,player.z=player.home.x,player.home.z;player.y=height(world,player.x,player.z);player.action='idle';return {player=view(player)}
        end
        if player.hp<=0 then return nil,'PLAYER_DEAD' end
        if method=='combat.move' then
            if not valid(world,params.x,params.z)then return nil,'INVALID_POSITION' end
            if distance(player,params)>32 then return nil,'MOVE_TOO_FAR' end
            local path=route(world,player,params);if not path then return nil,'PATH_BLOCKED' end
            player.path=path;player.pathIndex=1;return {accepted=true,player=view(player)}
        end
        if method=='combat.attack' then
            if type(params.targetId)~='string' then return nil,'INVALID_TARGET' end
            local target=world.mobs[params.targetId]
            if not target or not target.hostile then return nil,'TARGET_NOT_HOSTILE' end
            if target.hp<=0 then return nil,'TARGET_DEAD' end
            if now()<player.cooldown then return nil,'ATTACK_COOLDOWN' end
            if distance(player,target)>data.profile.range then return nil,'OUT_OF_RANGE' end
            if not world.nav:lineofsight({x=player.x,y=player.z},{x=target.x,y=target.z})then return nil,'PATH_BLOCKED' end
            local nodes=route(world,player,target);if not nodes then return nil,'PATH_BLOCKED' end
            local length=0;local previous=player
            for _,node in ipairs(nodes)do local nextpos={x=node.x,z=node.y};length=length+distance(previous,nextpos);previous=nextpos end
            if length>data.profile.range*1.25 then return nil,'PATH_BLOCKED' end
            local result,error=attack(world,player,target)
            if result then target.target=player.id;player.path=nil end
            return result,error
        end
        return nil,'METHOD_NOT_IMPLEMENTED'
    end
    return engine
end
return M
