-- Generated from combat_core.lua: verbatim basic methods, not the complete skill/impact system.
local define=require "define"
local enum_damage_type={IDX_DAMAGE_PHY=0}
local M={}

function M:calculate_hit_rate(hit, miss)
	if hit == 0 and miss == 0 then
		return 0.5  -- 如果没有数据，默认50%命中率
	end
    return hit / (hit + miss)
end

-- 计算暴击率
-- @param mind_attack 攻击者的精神属性
-- @param mind_defend 防御者的精神属性
-- @return 暴击率（0-1之间的小数）

function M:calculate_critical_rate(mind_attack, mind_defend)
	if not mind_defend or mind_defend == 0 then
		mind_defend = 1  -- 防止除零错误
	end
    return mind_attack / (mind_defend * 20)
    -- 备选公式: return mind_attack / (mind_defend + mind_attack)
end

-- 判断是否命中
-- @param accuracy 命中率（0-1之间的小数）
-- @param rand 随机数（0-100）
-- @return 是否命中

function M:is_hit(accuracy, rand)
    local result = rand <= accuracy * 100
    -- skynet.error("[DBG_COMBAT] is_hit: accuracy=", accuracy, " rand=", rand, " threshold=", accuracy and (accuracy * 100) or "nil", " result=", result)
    return result
end

-- 判断是否暴击
-- @param critical_rate 暴击率（0-1之间的小数）
-- @param rand 随机数（0-100）
-- @return 是否暴击

function M:is_critical_hit(critical_rate, rand)
	if critical_rate >= 1 then
		return true  -- 暴击率100%时必定暴击
	end
    return rand <= critical_rate * 100
end

-- 获取战斗结果
-- 计算攻击者对防御者造成的所有类型伤害，并返回伤害结果
-- @param attacker 攻击者对象
-- @param defencer 防御者对象
-- @param imp 伤害影响对象
-- @return 伤害影响对象

function M:physical_damage(attacker, defencer, addition_attack, addition_defence, traits)
    local damage
    local attack = attacker:get_attack_physics() + addition_attack
    local defence = defencer:get_defence_physics() + addition_defence
    local ignorerate = 0  -- 免伤率
    local trait = traits[enum_damage_type.IDX_DAMAGE_PHY]
    
    -- 获取防御者的物理免伤率（仅玩家）
    if defencer:get_obj_type() == "human" then
        ignorerate = defencer:item_value(define.ITEM_ATTRIBUTE.IATTRIBUTE_IMMUNITY_P)
    end
    
    -- 检查技能是否忽略防御
    local skill_info = attacker:get_skill_info()
	if skill_info and skill_info.id then
		local ignore_defence = skill_info:get_is_ignore_defence()
		if ignore_defence then
			defence = 0  -- 忽略防御，防御力设为0
		end
	end
	
    -- 获取攻击和防御的百分比加成（仅玩家）
    local kfs_wg_attack_rate = 0
    local kfs_wg_defence_rate = 0
    if attacker:get_obj_type() == "human" then
        kfs_wg_attack_rate = attacker:item_value(define.ITEM_ATTRIBUTE.IATTRIBUTE_POINT_ADD_ATTACK_PHYSIC_DAMAGE_RATE)
    end
    if defencer:get_obj_type() == "human" then
        kfs_wg_defence_rate = defencer:item_value(define.ITEM_ATTRIBUTE.IATTRIBUTE_POINT_ADD_PHYSIC_DEFENCE_RATE)
    end
    kfs_wg_attack_rate = kfs_wg_attack_rate - kfs_wg_defence_rate
    kfs_wg_attack_rate = math.max(-10000, kfs_wg_attack_rate)
    
    -- 计算基础伤害：攻击力平方除以攻击力与防御力之和
    if attack + defence == 0 then
        damage = 0
    else
        damage = attack * attack / (attack + defence) * trait / 1000000
    end
    
    -- 应用免伤率
    ignorerate = ignorerate < 0 and 0 or ignorerate
    ignorerate = ignorerate > 100 and 100 or ignorerate
    damage = damage - damage * ignorerate / 100
    
    -- 应用百分比加成
    damage = damage * (10000 + kfs_wg_attack_rate) / 10000
    damage = damage < 0 and 0 or damage
    return damage
end

-- 计算魔法伤害
-- @param attacker 攻击者对象
-- @param defencer 防御者对象
-- @param addition_attack 额外攻击力
-- @param addition_defence 额外防御力
-- @param traits 攻击特性配置
-- @return 魔法伤害值
return M
