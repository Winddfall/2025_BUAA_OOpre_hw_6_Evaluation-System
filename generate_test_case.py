import random
import os
import math

from id_pools import (
    adventurer_id_pool, bottle_id_pool, sword_id_pool,
    magicbook_id_pool, armour_id_pool, spell_id_pool
)

# --- 新增配置项 ---
# 有多大概率会尝试生成让“死亡冒险者”执行操作的指令
PROB_USE_DEAD_ACTOR = 0.2

def generate_test_case(test_case_id, num_operations, debug: bool = False):
    """
    根据新的需求生成一个测试用例，并将其写入文件。
    此版本会特意生成让死亡冒险者执行操作的样例。
    :param test_case_id: 测试用例的ID，用于命名文件。
    :param num_operations: 要生成的指令数量。
    """
    
    bottle_types = ["HpBottle", "AtkBottle", "DefBottle", "ManaBottle"]
    equipment_types = ["Sword", "Magicbook", "Armour"]
    spell_types = ["HealSpell", "AttackSpell"]

    # --- 物品类型定义 ---
    ITEM_TYPE_BOTTLE = "Bottle"
    ITEM_TYPE_SWORD = "Sword"
    ITEM_TYPE_MAGICBOOK = "Magicbook"
    ITEM_TYPE_ARMOUR = "Armour"
    ITEM_TYPE_SPELL = "Spell"

    # --- 背包容量限制 --
    BOTTLE_CAPACITY = 10

    # --- 状态追踪变量 ---
    existing_adv = [] # 存放已经存在的冒险者ID
    # 'money'属性已包含在内
    adv_attributes = {}  # {adv_id: {'hp': int, 'atk': int, 'def': int, 'mana': int, 'money': int}} 冒险者状态
    adv_owned_items = {}  # {adv_id: {item_id: item_type_str}} 拥有的物品（不包括法术）。只要某冒险者不再拥有物品，就应该从该字典中删除该物品ID
    adv_backpacks = {}  # {adv_id: {'bottles': list, 'sword': str, 'magicbook': str, 'armour': str}} 背包内的物品，按类型分类
    adv_learned_spells = {}  # {adv_id: {spell_id: {'type': str, 'mana_cost': int, 'power': int}}} 学习的法术
    item_details = {}  
    '''
    {
        item_id: {'type': str, 'effect': int}, 药水瓶
        item_id: {'type': str, 'ce': int}, 装备
        item_id: {'type': str, 'mana_cost': int, 'power': int} 法术
    }
    '''
    
    # 雇佣关系追踪
    employer_employees = {}  # {employer_id: [employee_id, ...]} 雇主到雇员的映射
    employee_employer = {}  # {employee_id: employer_id} 雇员到雇主的映射
    
    # 用来记录已使用的所有ID，确保全局唯一性
    used_ids = []

    def get_item_category(item_id):
        """根据物品ID判断物品类别"""
        if item_id in sword_id_pool:
            return ITEM_TYPE_SWORD
        elif item_id in magicbook_id_pool:
            return ITEM_TYPE_MAGICBOOK
        elif item_id in armour_id_pool:
            return ITEM_TYPE_ARMOUR
        elif item_id in bottle_id_pool:
            return ITEM_TYPE_BOTTLE
        elif item_id in spell_id_pool:
            return ITEM_TYPE_SPELL
        else:
            return None

    def discard_oldest_bottle(adv_id: str) -> str:
        """顶替最早的药水瓶"""
        bottles = adv_backpacks[adv_id].get('bottles', [])
        if not bottles:
            return
        # 获取最早的药水瓶（列表第一个）并移除
        bottles.pop(0) 

    def remove_weapon_if_exists(adv_id):
        """如果有武器装备，移除现有的武器（为新武器让位），返回被替换的ID"""
        backpack = adv_backpacks[adv_id]
        if backpack.get('sword') is not None: # 如果是剑
            backpack['sword'] = None  # 设置为None而不是删除键
        elif backpack.get('magicbook') is not None: # 如果是魔法书
            backpack['magicbook'] = None  # 设置为None而不是删除键

    def remove_armour_if_exists(adv_id):
        """如果有装甲装备，移除现有的装甲（为新装甲让位）"""
        backpack = adv_backpacks[adv_id]
        if backpack.get('armour') is not None:
            backpack['armour'] = None  # 设置为None而不是删除键

    def calculate_kill_gold(killed_adv_id):
        """
        计算击杀获得的金币数
        金币计算公式：被击杀者金币 + 药水瓶effect总和 + 装备CE总和 (注意：是拥有的物品，不是携带的)
        """
        # 被击杀者拥有的金币
        killed_money = adv_attributes[killed_adv_id]['money']
        # 计算药水瓶effect总和
        bottle_effect_sum = 0
        equipment_ce_sum = 0
        owned_items = adv_owned_items.get(killed_adv_id, {})
        for item_id, item_type_str in owned_items.items(): # 遍历所有物
            if item_id not in item_details:
                continue  # 如果物品不在 item_details 中，跳过
            item_info = item_details[item_id]
            # 药水瓶 effect 总和
            if item_type_str in bottle_types:
                bottle_effect_sum += item_info.get('effect', 0)
            # 装备 CE 总和
            elif item_type_str in equipment_types:
                equipment_ce_sum += item_info.get('ce', 0)
        total_gold = killed_money + bottle_effect_sum + equipment_ce_sum
        return total_gold

    def calculate_defense_power(adv_id):
        """计算冒险者的最终防御力（基础防御 + 携带装甲CE）"""
        # 基础防御力
        base_def = adv_attributes[adv_id]['def']
        # 携带装甲的CE加成
        backpack = adv_backpacks.get(adv_id, {})
        armor_id = backpack.get('armour')

        armor_defense_ce = 0
        if armor_id is not None:
            armor_defense_ce = item_details[armor_id]['ce']

        return base_def + armor_defense_ce

    def calculate_attack_power(adv_id):
        """计算冒险者的最终攻击力（基础攻击 + 携带Sword CE）"""
        # 基础攻击力
        base_atk = adv_attributes[adv_id]['atk']

        # 携带Sword的CE加成
        backpack = adv_backpacks.get(adv_id, {})
        sword_id = backpack.get('sword')

        weapon_attack_ce = 0
        if sword_id is not None:
            weapon_attack_ce = item_details[sword_id]['ce']

        return base_atk + weapon_attack_ce

    def get_magicbook_ce_value(adv_id):
        """获取冒险者携带的魔法书的CE值（用于魔法攻击判定和消耗）"""
        backpack = adv_backpacks.get(adv_id, {})
        magicbook_id = backpack.get('magicbook')

        if magicbook_id is not None:
            return item_details[magicbook_id].get('ce', 0)
        return 0

    def perform_battle(attacker_id, target_ids):
        """执行战斗逻辑 (target_ids 必须是活着的冒险者)"""
        # 记录原始血量用于援助判断
        old_hps = {tid: adv_attributes[tid]['hp'] for tid in target_ids}
        # 计算攻击者的最终攻击力、魔力、魔法书CE
        attacker_final_atk = calculate_attack_power(attacker_id)
        attacker_mana = adv_attributes[attacker_id]['mana']
        magicbook_ce = get_magicbook_ce_value(attacker_id)
        # 确定受攻击方的整体防御能力 (Max Def)
        target_defs = [calculate_defense_power(tid) for tid in target_ids]     
        overall_def = max(target_defs)
        # 判断攻击类型和成功条件
        backpack = adv_backpacks.get(attacker_id, {})
        carried_magicbook = backpack.get('magicbook') # 有没有带魔法书
        is_magic_attack = carried_magicbook is not None # 魔法攻击：有魔法书
        battle_successful = False
        damage = 0
        if is_magic_attack:
            if attacker_mana >= math.ceil(math.sqrt(magicbook_ce)):
                battle_successful = True
                # 魔法攻击伤害：所有被攻击者的体力值减去攻击者的攻击力
                damage = attacker_final_atk
                # 消耗魔力 (ceil(CE) - here CE is integer so just CE)
                adv_attributes[attacker_id]['mana'] -= math.ceil(math.sqrt(magicbook_ce))
        else: # Physical attack: carried_sword is not None or no weapon
            # 物理攻击：Attacker Final ATK > Overall Defense
            if attacker_final_atk > overall_def:
                battle_successful = True
                # 物理攻击伤害：攻击者的攻击力 - 整体防御能力
                damage = attacker_final_atk - overall_def
        # 战斗成功
        if battle_successful:
            for target_id in target_ids:
                adv_attributes[target_id]['hp'] -= damage #掉血
                # 检查是否击杀（<=0 都视为死亡）
                if adv_attributes[target_id]['hp'] <= 0:
                    # 将血量规范为 0，且执行被击杀时应做的清理/转移
                    adv_attributes[target_id]['hp'] = 0
                    # 击杀成功，计算并转移金币
                    kill_gold = calculate_kill_gold(target_id)
                    adv_attributes[attacker_id]['money'] += kill_gold
                    # 清理死亡冒险者的雇佣关系
                    cleanup_employment_on_death(target_id)
                # 检查是否需要援助（仅对仍然存活的目标）
                if adv_attributes[target_id]['hp'] > 0:
                    old_hp = old_hps[target_id]
                    new_hp = adv_attributes[target_id]['hp']
                    # 判断是否需要援助: 0 < new_hp <= old_hp / 2
                    if 0 < new_hp <= old_hp // 2:
                        try_assist_healing(target_id)
            return True # 战斗结果不在这里打印，由外部主程序处理

        return False

    def get_unused_id(pool):
        """从ID池中获取一个未使用的ID，将其加入used_ids集合中并返回"""
        available_ids = [_id for _id in pool if _id not in used_ids]
        if not available_ids: return None
        new_id = random.choice(available_ids)
        used_ids.append(new_id)
        return new_id

    # 雇佣关系辅助函数
    # 注意：没有雇主的冒险者不应该出现在employee_employer中
    def find_all_superiors(adv_id) -> list[str]:
        """找到所有上级（递归查找，带循环检测）"""
        superiors = []
        current = adv_id
        
        while current in employee_employer:
            boss = employee_employer[current]
            superiors.append(boss)
            current = boss
        return superiors

    # 注意：没有下级的冒险者不应该出现在employer_employees中
    def find_all_subordinates(adv_id) -> list[str]:
        """找到所有下级（递归查找，带循环检测）"""
        subordinates = []
        if adv_id not in employer_employees:
            return subordinates
        
        for employee in employer_employees[adv_id]:
            subordinates.append(employee)
            subordinates.extend(find_all_subordinates(employee))
        return subordinates
    
    def cleanup_employment_on_death(dead_adv_id):
        """当冒险者死亡时清理雇佣关系"""
        # 如果是雇主
        if dead_adv_id in employer_employees:
            # 所有雇员失去雇主
            for employee_id in employer_employees[dead_adv_id]:
                del employee_employer[employee_id]
            # 删除该雇主的雇员列表
            del employer_employees[dead_adv_id]
        # 如果是雇员
        if dead_adv_id in employee_employer:
            employer_id = employee_employer[dead_adv_id]
            # 从雇主的雇员列表中移除
            employer_employees[employer_id].remove(dead_adv_id)
            # 如果雇主没有雇员了，删除雇主的雇员列表
            if not employer_employees[employer_id]:
                del employer_employees[employer_id]
            # 该雇员失去雇主
            del employee_employer[dead_adv_id]
    
    def try_assist_healing(target_id):
        """尝试让所有下级对目标进行援助治疗"""
        subordinates = find_all_subordinates(target_id)
        heal_success_count = 0
        for sub_id in subordinates:
            # 检查是否有治疗法术
            heal_spells = {spell_id: spell_info for spell_id, spell_info in adv_learned_spells.get(sub_id, {}).items() 
                          if spell_info['type'] == 'HealSpell'}
            if not heal_spells:
                continue  # 没有治疗法术，跳过
            # 筛选出可以使用的治疗法术（魔力足够）
            usable_spells = {}
            for spell_id, spell_info in heal_spells.items():
                if adv_attributes[sub_id]['mana'] >= spell_info['mana_cost']:
                    usable_spells[spell_id] = spell_info
            if not usable_spells:
                continue  # 没有可用的治疗法术，跳过
            # 选择最佳法术（power最高，若相同则魔力消耗最低）
            best_spell_id = max(usable_spells.items(), key=lambda x: (x[1]['power'], -x[1]['mana_cost']))[0]
            # 执行治疗
            adv_attributes[sub_id]['mana'] -= usable_spells[best_spell_id]['mana_cost']
            adv_attributes[target_id]['hp'] += usable_spells[best_spell_id]['power']
            heal_success_count += 1

    if not os.path.exists("input_data"):
        os.makedirs("input_data")

    with open(f"input_data/input_{test_case_id}.txt", "w") as f_input:
        # 第一行写入操作总数
        f_input.write(str(num_operations) + "\n")
        # 生成n条随机指令
        _ = 0
        violations = []  # debug: 记录任何将死亡冒险者作为被攻击目标的事件
        while _ < num_operations:
            line = ""
            living_adv = [adv for adv in existing_adv if adv_attributes[adv]['hp'] > 0] # 更新存活冒险者们
            dead_adv = [adv for adv in existing_adv if adv_attributes[adv]['hp'] <= 0] # 更新死亡冒险者们
            
            # --- 动态确定可执行的操作 ---
            possible_ops = []
            # 存在还没使用的冒险者id
            if any(adv not in used_ids for adv in adventurer_id_pool): possible_ops.append("aa")

            if existing_adv: # 只要有冒险者存在，就可以考虑这些操作，即使操作者是死的
                # 检查是否存在未使用的药水瓶ID
                if any(bot not in used_ids for bot in bottle_id_pool): possible_ops.append("ab")
                # 检查三个装备池中是否有可用ID
                equipment_pools = [sword_id_pool, magicbook_id_pool, armour_id_pool]
                if any(any(equ not in used_ids for equ in pool) for pool in equipment_pools):
                    possible_ops.append("ae")
                # 检查是否存在未使用的法术ID
                if any(spe not in used_ids for spe in spell_id_pool): possible_ops.append("ls")
                # 检查是否存在冒险者持有物品不为空
                if any(adv_owned_items.get(adv) for adv in existing_adv): 
                    possible_ops.append("ri") 
                    possible_ops.append("ti")
                # 检查是否有冒险者可以执行 use 操作
                for adv in existing_adv:
                    # 检查是否有药水或学会了法术
                    owned_bottles = [item_id for item_id in adv_owned_items.get(adv, {}).keys() if adv_owned_items.get(adv, {})[item_id] in bottle_types]
                    has_learned_spell = bool(adv_learned_spells.get(adv))
                    if owned_bottles or has_learned_spell:
                        possible_ops.append("use")
                        break
                # 检查是否有冒险者可以执行购买操作（有可用物品ID）
                for adv in existing_adv:
                    # 检查是否有可购买的物品
                    has_available_bottles = any(bot not in used_ids for bot in bottle_id_pool)
                    has_available_equipment = any(any(equ not in used_ids for equ in pool) for pool in equipment_pools)
                    if has_available_bottles or has_available_equipment:
                        # possible_ops.append("bi")
                        break
                # 检查是否有冒险者可以执行战斗操作（有其他存活冒险者）
                if len(living_adv) >= 2:
                    possible_ops.append("fight")
                # 添加雇佣关系操作（ar和rr）
                if len(living_adv) >= 2:
                    possible_ops.append("ar")
                    # 如果有雇佣关系存在，可以尝试解除
                    if employer_employees:
                        possible_ops.append("rr")
            
            if not possible_ops:
                print(f"Warning: No more possible operations for test case {test_case_id}. Stopping early.")
                break

            # --- 根据权重选择一种指令 ---
            weights_map = {"aa": 0.08, "ab": 0.08, "ae": 0.08, "ls": 0.08, "ti": 0.08, "use": 0.08, "ri": 0.06, "bi": 0.12, "fight": 0.15, "ar": 0.10, "rr": 0.07}
            op_weights = [weights_map.get(op, 0) for op in possible_ops]
            op_type = random.choices(possible_ops, weights=op_weights, k=1)[0]

            # --- 生成具体指令并更新状态 ---
            actor_id, actor_is_alive = None, False

            if op_type == "aa":
                # ... aa logic (same as before)
                new_adv_id = get_unused_id(adventurer_id_pool)
                if new_adv_id:
                    line = f"aa {new_adv_id}\n"
                    existing_adv.append(new_adv_id)
                    adv_attributes[new_adv_id] = {'hp': 500, 'atk': 1, 'def': 0, 'mana': 10, 'money': 50} # 冒险者属性
                    adv_owned_items[new_adv_id] = {}
                    adv_learned_spells[new_adv_id] = {}
                    adv_backpacks[new_adv_id] = {
                        'bottles': [],
                        'sword': None,
                        'magicbook': None,
                        'armour': None
                    }
            
            elif op_type in ["ab", "ae", "ls"]:
                # ... ab/ae/ls actor selection and logic (same as before)
                # 概率触发对死亡冒险者进行操作
                if dead_adv and random.random() < PROB_USE_DEAD_ACTOR: 
                    actor_id = random.choice(dead_adv)
                elif existing_adv: 
                    actor_id = random.choice(list(existing_adv))
                else: continue
                
                actor_is_alive = adv_attributes[actor_id]['hp'] > 0
                new_item_id = None
                
                if op_type == "ab":
                    new_item_id = get_unused_id(bottle_id_pool)
                    if new_item_id:
                        bot_type = random.choice(bottle_types)
                        effect = random.randint(1, 100)
                        line = f"ab {actor_id} {new_item_id} {bot_type} {effect}\n"
                        adv_owned_items[actor_id][new_item_id] = bot_type
                        item_details[new_item_id] = {'type': bot_type, 'effect': effect}
                elif op_type == "ae":
                    equipment_pools = [sword_id_pool, magicbook_id_pool, armour_id_pool]
                    available_pools = [pool for pool in equipment_pools if any(equ not in used_ids for equ in pool)]

                    if available_pools:
                        selected_pool = random.choice(available_pools)
                        new_item_id = get_unused_id(selected_pool)
                        ce = random.randint(1, 100)
                        if new_item_id:
                            item_type_str = ""
                            if selected_pool == sword_id_pool:
                                item_type_str = "Sword"
                            elif selected_pool == magicbook_id_pool:
                                item_type_str = "Magicbook"
                            elif selected_pool == armour_id_pool:
                                item_type_str = "Armour"

                            line = f"ae {actor_id} {new_item_id} {item_type_str} {ce}\n"

                            adv_owned_items[actor_id][new_item_id] = item_type_str
                            item_details[new_item_id] = {'type': item_type_str, 'ce': ce}
                elif op_type == "ls":
                    new_item_id = get_unused_id(spell_id_pool)
                    if new_item_id:
                        spell_weights = [0.5, 0.5] # 治疗 攻击
                        spe_type = random.choices(spell_types, weights=spell_weights, k=1)[0]
                        # 确保 mana_cost 不为负
                        mana_cost = random.randint(0, adv_attributes[actor_id].get('mana', 10) + 5) 
                        power = random.randint(0, 500)
                        line = f"ls {actor_id} {new_item_id} {spe_type} {mana_cost} {power}\n"
                        spell_info = {'type': spe_type, 'mana_cost': mana_cost, 'power': power}
                        
                        adv_learned_spells[actor_id][new_item_id] = spell_info
                        item_details[new_item_id] = spell_info
            
            # 移除物品
            elif op_type == "ri":
                # 找到所有有物品的冒险者
                owners = [adv for adv in living_adv if adv_owned_items.get(adv)]
                if not owners: continue
                
                # 概率触发死亡冒险者
                if dead_adv and random.random() < PROB_USE_DEAD_ACTOR: 
                    candidate_adv = [adv for adv in dead_adv if adv in owners] # 仅从有物品的死亡冒险者中选择
                    if candidate_adv:
                        actor_id = random.choice(candidate_adv)
                    else: continue    
                elif existing_adv: 
                    candidate_adv = [adv for adv in living_adv if adv in owners] # 仅从有物品的存活冒险者中选择
                    if candidate_adv:
                        actor_id = random.choice(candidate_adv)
                    else: continue    
                
                # actor_id = random.choice(owners)
                actor_is_alive = adv_attributes[actor_id]['hp'] > 0
                    
                available_items = list(adv_owned_items[actor_id].keys())
                item_id_to_remove = random.choice(available_items)
                line = f"ri {actor_id} {item_id_to_remove}\n"
                
                # 更新状态
                item_category = get_item_category(item_id_to_remove)
                # 从拥有的物品中删除
                del adv_owned_items[actor_id][item_id_to_remove]
                # 从背包中删除
                backpack = adv_backpacks.get(actor_id)
                # 如果有背包
                if backpack:
                    if item_category == ITEM_TYPE_BOTTLE:
                        if item_id_to_remove in backpack.get('bottles', []):
                            backpack['bottles'].remove(item_id_to_remove)
                    elif item_category == ITEM_TYPE_SWORD:
                        if backpack.get('sword') == item_id_to_remove:
                            backpack['sword'] = None
                    elif item_category == ITEM_TYPE_MAGICBOOK:
                        if backpack.get('magicbook') == item_id_to_remove:
                            backpack['magicbook'] = None
                    elif item_category == ITEM_TYPE_ARMOUR:
                        if backpack.get('armour') == item_id_to_remove:
                            backpack['armour'] = None
            
            # 携带物品 (TI)
            elif op_type == "ti":
                # 找到所有有物品的冒险者
                owners = [adv for adv in existing_adv if adv_owned_items.get(adv)]
                if not owners: continue
                
                # 随机选择一个冒险者来执行 ti 操作
                candidates_dead = [adv for adv in owners if adv in dead_adv]
                candidates_alive = [adv for adv in owners if adv in living_adv]
                if candidates_dead and random.random() < PROB_USE_DEAD_ACTOR: 
                    actor_id = random.choice(candidates_dead)
                elif candidates_alive: 
                    actor_id = random.choice(candidates_alive)
                else:
                    continue

                actor_is_alive = adv_attributes[actor_id]['hp'] > 0
                
                item_id_to_take = random.choice(list(adv_owned_items[actor_id].keys())) 
                line = f"ti {actor_id} {item_id_to_take}\n"
                
                item_category = get_item_category(item_id_to_take)
                
                if item_category == ITEM_TYPE_SWORD:
                    # 移除现有武器，分配新武器
                    remove_weapon_if_exists(actor_id)
                    adv_backpacks[actor_id]['sword'] = item_id_to_take
                elif item_category == ITEM_TYPE_MAGICBOOK:
                    # 移除现有武器，分配新武器
                    remove_weapon_if_exists(actor_id)
                    adv_backpacks[actor_id]['magicbook'] = item_id_to_take
                elif item_category == ITEM_TYPE_ARMOUR:
                    # 移除现有装甲，分配新装甲
                    remove_armour_if_exists(actor_id)
                    adv_backpacks[actor_id]['armour'] = item_id_to_take
                elif item_category == ITEM_TYPE_BOTTLE:
                    bottles_list = adv_backpacks[actor_id]['bottles']
                    if len(bottles_list) >= BOTTLE_CAPACITY:
                        # 药水瓶满了，顶替最早的
                        discard_oldest_bottle(actor_id)
                    # 添加新的药水瓶 (新的药水瓶在列表末尾)
                    adv_backpacks[actor_id]['bottles'].append(item_id_to_take)
            
            # 购买物品 (BI)
            elif op_type == "bi":
                # ... bi actor selection (same as before)
                if dead_adv and random.random() < PROB_USE_DEAD_ACTOR: 
                    actor_id = random.choice(dead_adv)
                elif existing_adv: 
                    actor_id = random.choice(living_adv)
                else: continue

                actor_is_alive = adv_attributes[actor_id]['hp'] > 0

                # 选择要购买的物品类型
                available_purchase_types = []
                if any(bot not in used_ids for bot in bottle_id_pool):
                    available_purchase_types.extend(["HpBottle", "AtkBottle", "DefBottle", "ManaBottle"])
                if any(equ not in used_ids for equ in sword_id_pool):
                    available_purchase_types.append("Sword")
                if any(equ not in used_ids for equ in magicbook_id_pool):
                    available_purchase_types.append("Magicbook")
                if any(equ not in used_ids for equ in armour_id_pool):
                    available_purchase_types.append("Armour")

                if not available_purchase_types: continue
                item_type = random.choice(available_purchase_types)
                # 计算消耗的金币数 (x = min(money, 100))
                current_money = adv_attributes[actor_id].get('money', 0)
                cost = min(current_money, 100)
                new_item_id = None

                # 根据消耗的金币数决定物品效果/属性
                if item_type in ["HpBottle", "AtkBottle", "DefBottle", "ManaBottle"]:
                    new_item_id = get_unused_id(bottle_id_pool)
                    if new_item_id:
                        effect = cost  
                        line = f"bi {actor_id} {new_item_id} {item_type}\n"
                        adv_attributes[actor_id]['money'] -= cost
                        adv_owned_items[actor_id][new_item_id] = item_type
                        item_details[new_item_id] = {'type': item_type, 'effect': effect}
                else:  # 装备类型
                    if item_type == "Sword":
                        item_pool = sword_id_pool
                    elif item_type == "Magicbook":
                        item_pool = magicbook_id_pool
                    elif item_type == "Armour":
                        item_pool = armour_id_pool
                    new_item_id = get_unused_id(item_pool)
                    if new_item_id:
                        line = f"bi {actor_id} {new_item_id} {item_type}\n"
                        ce = cost
                        adv_attributes[actor_id]['money'] -= cost
                        adv_owned_items[actor_id][new_item_id] = item_type 
                        item_details[new_item_id] = {'type': item_type, 'ce': ce}
            
            # 添加雇佣关系
            elif op_type == "ar":
                if len(living_adv) < 2: continue
                # 随机选择雇主
                employer_id = random.choice(living_adv)
                # 找到所有不能作为该雇主雇员的人（避免循环）
                invalid_employees = []
                # 1. 雇主自己不能雇佣自己
                invalid_employees.append(employer_id)
                # 2. 雇主的上级不能成为其雇员
                superiors = find_all_superiors(employer_id)
                invalid_employees.extend(superiors)
                # 3. 已经有雇主的冒险者不能再次被雇佣
                invalid_employees.extend(list(employee_employer.keys()))
                # 找到所有有效的雇员候选
                valid_employees = [adv for adv in living_adv if adv not in invalid_employees]
                
                if not valid_employees: continue

                employee_id = random.choice(valid_employees)
                line = f"ar {employer_id} {employee_id}\n"

                # 更新雇佣关系
                if employer_id not in employer_employees:
                    employer_employees[employer_id] = []
                employer_employees[employer_id].append(employee_id)
                employee_employer[employee_id] = employer_id
            
            # 移除雇佣关系
            elif op_type == "rr":
                if not employer_employees: continue
                # 随机选择一条雇佣关系来解除
                all_relations = [(employee, employer) for employee, employer in employee_employer.items()]
                if not all_relations: continue               
                employee_id, employer_id = random.choice(all_relations)
                line = f"rr {employer_id} {employee_id}\n"
                # 更新雇佣关系
                employer_employees[employer_id].remove(employee_id)
                del employee_employer[employee_id]

            # 战斗指令
            elif op_type == "fight":
                # ... fight logic (updated to use new perform_battle)
                if not existing_adv: continue
                if dead_adv and random.random() < PROB_USE_DEAD_ACTOR:
                    attacker_id = random.choice(dead_adv)
                elif living_adv:
                    attacker_id = random.choice(living_adv)
                else:
                    continue
                # 目标必须存在且全部存活，且不能包含攻击者自己
                alive_targets = [adv for adv in living_adv if adv != attacker_id]
                if not alive_targets:
                    continue
                # 决定单目标或多目标
                if random.random() < 0.7 or len(alive_targets) < 3:
                    target_id = random.choice(alive_targets)
                    target_ids = [target_id]
                    line = f"fight {attacker_id} 1 {target_id}\n"
                else:
                    num_targets = min(random.randint(2, 30), len(alive_targets))
                    target_ids = random.sample(alive_targets, num_targets)
                    target_ids_str = " ".join(target_ids)
                    line = f"fight {attacker_id} {len(target_ids)} {target_ids_str}\n"
                # 执行战斗逻辑 (无论攻击者是否存活，都尝试生成并执行)
                perform_battle(attacker_id, target_ids)
                # 注：战斗状态更新已在 perform_battle 中完成，这里不需要额外的 if actor_is_alive 检查，因为 perform_battle 假设指令已执行。
                
            # 使用物品/法术 (USE)
            elif op_type == "use":
                # 判断冒险者是否拥有药水瓶
                def has_bottle(adv:str):
                    for key in adv_owned_items.get(adv, {}).keys():
                        if get_item_category(key) == ITEM_TYPE_BOTTLE:
                            return True
                    return False
                # 判断冒险者是否学会法术
                def has_spell(adv:str):
                    return bool(adv_learned_spells.get(adv))
                # 找到持有药水瓶或学会法术的冒险者
                bottle_owners = [adv for adv in existing_adv if has_bottle(adv)]
                spell_owners = [adv for adv in existing_adv if has_spell(adv)]
                # 如果没有持有药水瓶或学会法术的冒险者，则跳过
                if not bottle_owners and not spell_owners: continue

                # 确定冒险者id
                # 概率触发死亡冒险者
                dead_owners = [adv for adv in bottle_owners + spell_owners if adv in dead_adv]
                living_owners = [adv for adv in bottle_owners + spell_owners if adv in living_adv]
                
                if random.random() < PROB_USE_DEAD_ACTOR:
                    if dead_owners:
                        actor_id = random.choice(dead_owners)
                    elif living_owners:
                        actor_id = random.choice(living_owners)
                else:
                    if living_owners:
                        actor_id = random.choice(living_owners)
                    elif dead_owners:
                        actor_id = random.choice(dead_owners)

                actor_is_alive = adv_attributes[actor_id]['hp'] > 0
                
                # 确定目标id
                # 目标可以是死人也可以是活人
                target_id = random.choice(existing_adv)
                old_hp = adv_attributes[target_id]['hp']
                target_is_alive = old_hp > 0

                # 选择一个物品或法术
                owned_bottles = [item_id for item_id in adv_owned_items.get(actor_id, {}).keys() if get_item_category(item_id) == ITEM_TYPE_BOTTLE]
                learned_spells = list(adv_learned_spells.get(actor_id, {}).keys())
                if owned_bottles and learned_spells:
                    if random.random() < 0.7:
                        usable_items = owned_bottles
                    else:
                        usable_items = learned_spells
                elif owned_bottles:
                    usable_items = owned_bottles
                elif learned_spells:
                    usable_items = learned_spells
                # 确定使用物品id
                usable_id = random.choice(usable_items) 
                line = f"use {actor_id} {usable_id} {target_id}\n"
                
                # 状态更新 
                is_spell = get_item_category(usable_id) == ITEM_TYPE_SPELL
                is_bottle = get_item_category(usable_id) == ITEM_TYPE_BOTTLE
                if is_spell:
                    if adv_attributes[actor_id]['mana'] >= item_details[usable_id]['mana_cost']:
                        adv_attributes[actor_id]['mana'] -= item_details[usable_id]['mana_cost']
                        if item_details[usable_id]['type'] == 'HealSpell':
                            adv_attributes[target_id]['hp'] += item_details[usable_id]['power']
                        elif item_details[usable_id]['type'] == 'AttackSpell':
                            adv_attributes[target_id]['hp'] -= item_details[usable_id]['power']
                elif is_bottle:
                    bottle_is_taken = usable_id in adv_backpacks.get(actor_id, {}).get('bottles', [])  
                    if bottle_is_taken: # 必须是携带的药水瓶
                        if item_details[usable_id]['type'] == 'HpBottle': adv_attributes[target_id]['hp'] += item_details[usable_id]['effect']
                        elif item_details[usable_id]['type'] == 'AtkBottle': adv_attributes[target_id]['atk'] += item_details[usable_id]['effect']
                        elif item_details[usable_id]['type'] == 'DefBottle': adv_attributes[target_id]['def'] += item_details[usable_id]['effect']
                        elif item_details[usable_id]['type'] == 'ManaBottle': adv_attributes[target_id]['mana'] += item_details[usable_id]['effect']
                        # 药水消耗
                        del adv_owned_items[actor_id][usable_id]
                        if usable_id in adv_backpacks[actor_id]['bottles']:
                            adv_backpacks[actor_id]['bottles'].remove(usable_id)
                new_hp = adv_attributes[target_id]['hp']            
                
                if new_hp <= 0:
                    # 爆金币
                    kill_gold = calculate_kill_gold(target_id)
                    adv_attributes[actor_id]['money'] += kill_gold
                    # 清理死亡冒险者的雇佣关系
                    cleanup_employment_on_death(target_id)

                # 检查是否需要援助                    
                if 0 < new_hp <= old_hp // 2:
                    try_assist_healing(target_id)

            if line:
                f_input.write(line)
                _ += 1

    print(f"Test case {test_case_id} generated with {num_operations} operations.")

if __name__ == "__main__":
    generate_test_case(1, 2000)
    # 猜想：错误把活人变成了死人，然后ri该人的物品，则物品实际上没有被删除，下一次还能use
    # 猜想：错误把活人变成了死人，然后use该人的物品，则物品实际上没有被删除，下一次还能use
    # 结论：错误地把本该活着的人变成了死人，对该死人操作，不移除物品