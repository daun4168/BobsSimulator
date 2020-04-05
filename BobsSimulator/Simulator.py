import copy
import random
from typing import List, Dict, Optional
from collections import defaultdict, OrderedDict, deque

from PySide2.QtCore import Signal, QObject

from BobsSimulator.HSType import HSObject, Battle, Minion, Zone, Player, Race, Enchantment, RACE_ALL
from BobsSimulator.HSLogging import simulator_logger, console_logger
from BobsSimulator.Util import Util


class Simulator(QObject):
    def __init__(self):
        super().__init__()
        self.battle = Battle()

    def simulate(self, battle: Battle, simulate_num=1) -> list:
        result = []
        # simulator_logger.info(f'''# {"=" * 50}''')
        # simulator_logger.info("Simulate Start")
        # simulator_logger.info("-" * 50)
        # simulator_logger.info("Battle Info")
        # battle.print_log(simulator_logger)
        # simulator_logger.info("-" * 50)

        print('='*50)
        print("Simulate Start")
        print('-'*50)
        print(battle.info())
        print('-'*50)

        for i in range(simulate_num):
            # simulator_logger.info("-" * 50)
            # simulator_logger.info(f"# Simulation {i + 1}/{simulate_num}")
            self.battle = copy.deepcopy(battle)
            result.append(self.simulate_once())
            # simulator_logger.info("-" * 50)
        # simulator_logger.info("=" * 50)
        return result

    def simulate_once(self):
        self.simulate_init()

        self.set_attack_player()
        self.simulate_hero_power()

        while True:
            self.battle.seq += 1
            if self.battle.me.not_attack_last_seq and self.battle.enemy.not_attack_last_seq:  # Draw
                return 0
            if self.battle.me.empty() and self.battle.enemy.empty():  # Draw
                return 0
            elif self.battle.me.empty():  # Lose
                return -self.battle.enemy.sum_damage()
            elif self.battle.enemy.empty():  # Win
                return self.battle.me.sum_damage()

            if self.battle.seq > 1000:
                simulator_logger.error("INFINITE LOOP")
                return 0

            self.simulate_attack()
            self.battle.is_me_attack = not self.battle.is_me_attack  # change atk player

    def simulate_init(self):
        self.battle.seq = 0
        for player in self.battle.players():
            player.not_attack_last_seq = False
            player.next_atk_minion_pos = None
            player.death_triggers = defaultdict(list)

    def set_attack_player(self):
        if self.battle.me.minion_num() > self.battle.enemy.minion_num():
            self.battle.is_me_attack = True
        elif self.battle.me.minion_num() < self.battle.enemy.minion_num():
            self.battle.is_me_attack = False
        else:
            self.battle.is_me_attack = bool(random.getrandbits(1))

    def simulate_hero_power(self):
        # TODO: make function
        pass

    def simulate_attack(self):
        attacker = self.find_next_attacker(self.battle.atk_player())
        if attacker is None:
            self.battle.atk_player().not_attack_last_seq = True
            return

        num_of_atk = 1 + attacker.windfury
        for i in range(num_of_atk):
            if attacker.zone != Zone.PLAY:
                return
            self.simulate_attack_once(attacker)

    def find_next_attacker(self, player: Player):
        if player.empty():
            return None
        if player.next_atk_minion_pos is None:
            player.next_atk_minion_pos = 1
        for i in range(player.minion_num()):
            if player.board[player.next_atk_minion_pos].attack != 0:
                attacker = player.board[player.next_atk_minion_pos]
                player.next_atk_minion_pos += 1
                if player.next_atk_minion_pos > player.minion_num():
                    player.next_atk_minion_pos -= player.minion_num()
                return attacker
            player.next_atk_minion_pos += 1
            if player.next_atk_minion_pos > player.minion_num():
                player.next_atk_minion_pos -= player.minion_num()
        return None

    def simulate_attack_once(self, attacker: Minion):
        if self.battle.dfn_player().empty():
            return

        """Glyph Guardian"""
        if attacker.card_id == 'BGS_045':
            attacker.attack *= 2
        elif attacker.card_id == 'TB_BaconUps_115':
            attacker.attack *= 3

        """Zapp Slywick"""
        defender = None  # type: Optional[Minion]
        if attacker.atk_lowest_atk_minion or attacker.card_id in ("BGS_022", "TB_BaconUps_091"):
            defender = self.random_lowest_atk_minion(self.battle.dfn_player())
        else:
            defender = self.random_defense_minion(self.battle.dfn_player())
        print(f"ATTACK: {self.battle.atk_player().hero.name()} {attacker.info()} attack {defender.info()}")

        self.simulate_damage_by_minion(defender, attacker)
        self.simulate_damage_by_minion(attacker, defender)

        """Foe Reaper 4000"""
        """Cave Hydra"""
        if attacker.card_id in ("GVG_113", "LOOT_078"):
            if defender.pos > 1 and self.battle.dfn_player().board[defender.pos - 1] is not None:
                self.simulate_damage_by_minion(self.battle.dfn_player().board[defender.pos - 1], attacker)
            if defender.pos < 7 and self.battle.dfn_player().board[defender.pos + 1] is not None:
                self.simulate_damage_by_minion(self.battle.dfn_player().board[defender.pos + 1], attacker)

        self.simulate_deaths()
        print('-'*50)
        print(self.battle.info())
        print('-'*50)

    def simulate_deaths(self):
        while True:
            for player in self.battle.players():
                player.death_init()

            is_minion_dead = self.check_deaths()
            if not is_minion_dead:
                return
            self.simulate_death_triggers()
            self.simulate_reborn_triggers()

    def simulate_death_triggers(self):
        for player in self.battle.players():
            player.trigger_pos = 0
            while player.death_triggers or player.trigger_pos <= player.minion_num():
                if player.trigger_pos < len(player.board) and player.board[player.trigger_pos] is not None:
                    minion = player.board[player.trigger_pos]
                    self.simulate_triggers_when_other_minion_death(minion, player)

                while player.death_triggers[player.trigger_pos]:
                    trigger = player.death_triggers[player.trigger_pos].popleft()
                    self.simulate_deathrattle(trigger, player)

                if player.trigger_pos in player.death_triggers:
                    del player.death_triggers[player.trigger_pos]
                player.trigger_pos += 1

    def simulate_triggers_when_other_minion_death(self, minion: Minion, player: Player):
        card_id = minion.card_id

        """Soul Juggler"""
        if card_id == "BGS_002":
            for i in range(player.death_num_this_turn_by_race[Race.DEMON]):
                self.simulate_damage_to_random_minion_by_minion(player.opponent, minion, 3)
        elif card_id == "TB_BaconUps_075":
            for i in range(player.death_num_this_turn_by_race[Race.DEMON] * 2):
                self.simulate_damage_to_random_minion_by_minion(player.opponent, minion, 3)

        """Scavenging Hyena"""
        if card_id == "EX1_531":
            for i in range(player.death_num_this_turn_by_race[Race.BEAST]):
                minion.attack += 2
                minion.health += 1
        elif card_id == "TB_BaconUps_043":
            for i in range(player.death_num_this_turn_by_race[Race.BEAST]):
                minion.attack += 4
                minion.health += 2

        """Junkbot"""
        if card_id == "GVG_106":
            for i in range(player.death_num_this_turn_by_race[Race.MECHANICAL]):
                minion.attack += 2
                minion.health += 2
        elif card_id == "TB_BaconUps_046":
            for i in range(player.death_num_this_turn_by_race[Race.MECHANICAL]):
                minion.attack += 4
                minion.health += 4

    def simulate_deathrattle(self, trigger: Minion, player: Player):
        print(f"DEATHRATTLE: {player.hero.name()} {trigger.info()}")

        card_id = trigger.card_id
        golden = trigger.golden

        """Imprisoner"""
        if card_id == 'BGS_014':  # Imprisoner
            new_minion = Util.make_default_minion('BRM_006t', golden=golden)
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_113':  # Imprisoner lv2
            new_minion = Util.make_default_minion('TB_BaconUps_030t', golden=golden)
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Harvest Golem"""
        if card_id == 'EX1_556':  # Harvest Golem
            new_minion = Util.make_default_minion('skele21', golden=golden)  # Damaged Golem
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_006':  # Harvest Golem lv2
            new_minion = Util.make_default_minion('TB_BaconUps_006t', golden=golden)  # Damaged Golem lv2
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Kindly Grandmother"""
        if card_id == 'KAR_005':  # Kindly Grandmother
            new_minion = Util.make_default_minion('KAR_005a', golden=golden)  # Big Bad Wolf
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_004':  # Kindly Grandmother lv2
            new_minion = Util.make_default_minion('TB_BaconUps_004t', golden=golden)  # Big Bad Wolf lv2
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Infested Wolf"""
        if card_id == 'OG_216':  # Infested Wolf
            for i in range(2):
                new_minion = Util.make_default_minion('OG_216a', golden=golden)  # Spider
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_026':  # Infested Wolf lv2
            for i in range(2):
                new_minion = Util.make_default_minion('TB_BaconUps_026t', golden=golden)  # Spider lv2
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Voidlord"""
        if card_id == 'LOOT_368':
            for i in range(3):
                new_minion = Util.make_default_minion('CS2_065', golden=golden)
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_059':
            for i in range(3):
                new_minion = Util.make_default_minion('TB_BaconUps_059t', golden=golden)
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Savannah Highmane"""
        if card_id == 'EX1_534':
            for i in range(2):
                new_minion = Util.make_default_minion('EX1_534t', golden=golden)
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_049':
            for i in range(2):
                new_minion = Util.make_default_minion('TB_BaconUps_049t', golden=golden)
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Mecharoo"""
        if card_id == 'BOT_445':
            new_minion = Util.make_default_minion('BOT_445t', golden=golden)
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_002':
            new_minion = Util.make_default_minion('TB_BaconUps_002t', golden=golden)
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Mechano-Egg"""
        if card_id == 'BOT_537':
            new_minion = Util.make_default_minion('BOT_537t', golden=golden)
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_039':
            new_minion = Util.make_default_minion('TB_BaconUps_039t', golden=golden)
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Rat Pack"""
        if card_id == 'CFM_316':
            for i in range(trigger.attack):
                new_minion = Util.make_default_minion('CFM_316t', golden=golden)
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_027':
            for i in range(trigger.attack):
                new_minion = Util.make_default_minion('TB_BaconUps_027t', golden=golden)
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Sneed's Old Shredder"""
        if card_id == 'BGS_006':
            new_minion = Util.random_bp_minion_elite(golden=golden, except_card_ids='BGS_006')
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_080':
            for i in range(2):
                new_minion = Util.random_bp_minion_elite(golden=golden, except_card_ids='BGS_006')
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Ghastcoiler"""
        if card_id == 'BGS_008':
            for i in range(2):
                new_minion = Util.random_bp_minion_deathrattle(golden=golden, except_card_ids='BGS_008')
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_057':
            for i in range(4):
                new_minion = Util.random_bp_minion_deathrattle(golden=golden, except_card_ids='BGS_008')
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Piloted Shredder"""
        if card_id == 'BGS_023':
            new_minion = Util.random_bp_minion_cost(cost=2, golden=golden)
            self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_035':
            for i in range(2):
                new_minion = Util.random_bp_minion_cost(cost=2, golden=golden)
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

        """Kangor's Apprentice"""
        if card_id == 'BGS_012':
            summon_num = 0
            for dead_minion in player.graveyard:
                if dead_minion.race in (Race.MECHANICAL, Race.ALL):
                    new_minion = Util.make_default_minion(dead_minion.card_id, golden=dead_minion.golden, level2=dead_minion.level2)
                    self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
                    summon_num += 1
                if summon_num >= 2:
                    break
        elif card_id == 'TB_BaconUps_087':
            summon_num = 0
            for dead_minion in player.graveyard:
                if dead_minion.race in (Race.MECHANICAL, Race.ALL):
                    new_minion = Util.make_default_minion(dead_minion.card_id, golden=dead_minion.golden, level2=dead_minion.level2)
                    self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
                    summon_num += 1
                if summon_num >= 4:
                    break

        """Spawn of N'Zoth"""
        if card_id == 'OG_256':
            for minion in player.minions():
                minion.attack += 1
                minion.health += 1
        elif card_id == 'TB_BaconUps_025':
            for minion in player.minions():
                minion.attack += 2
                minion.health += 2

        """Goldrinn, the Great Wolf"""
        if card_id == 'BGS_018':
            for minion in player.minions():
                if minion.race in (Race.PET, Race.ALL):
                    minion.attack += 4
                    minion.health += 4
        elif card_id == 'TB_BaconUps_085':
            for minion in player.minions():
                if minion.race in (Race.PET, Race.ALL):
                    minion.attack += 8
                    minion.health += 8

        """King Bagurgle"""
        if card_id == 'BGS_030':
            for minion in player.minions():
                if minion.race in (Race.MURLOC, Race.ALL):
                    minion.attack += 2
                    minion.health += 2
        elif card_id == 'TB_BaconUps_100':
            for minion in player.minions():
                if minion.race in (Race.MURLOC, Race.ALL):
                    minion.attack += 4
                    minion.health += 4

        """Selfless Hero"""
        if card_id == 'OG_221':
            not_divine_shield_minions = []
            for minion in player.minions():
                if not minion.divine_shield:
                    not_divine_shield_minions.append(minion)
            if not_divine_shield_minions:
                random_not_divine_shield_minion = random.choice(not_divine_shield_minions)  # type: Minion
                random_not_divine_shield_minion.divine_shield = True
        elif card_id == 'TB_BaconUps_014':
            for i in range(2):
                not_divine_shield_minions = []
                for minion in player.minions():
                    if not minion.divine_shield:
                        not_divine_shield_minions.append(minion)
                if not_divine_shield_minions:
                    random_not_divine_shield_minion = random.choice(not_divine_shield_minions)  # type: Minion
                    random_not_divine_shield_minion.divine_shield = True

        """Nadina the Red"""
        if card_id == 'BGS_040':
            for minion in player.minions():
                if minion.race in (Race.DRAGON, Race.ALL):
                    minion.divine_shield = True

        """Kaboom Bot"""
        if card_id == 'BOT_606':
            self.simulate_damage_to_random_minion_by_minion(player.opponent, trigger, 4)
        elif card_id == 'TB_BaconUps_028':
            for i in range(2):
                self.simulate_damage_to_random_minion_by_minion(player.opponent, trigger, 4)

        """The Beast"""
        if card_id == 'EX1_577':
            new_minion = Util.make_default_minion('EX1_finkle', golden=golden)
            self.simulate_summon_minion(new_minion, player.opponent)
        elif card_id == 'TB_BaconUps_042':
            new_minion = Util.make_default_minion('EX1_finkle', golden=golden)
            self.simulate_summon_minion(new_minion, player.opponent)

        """Fiendish Servant"""
        if card_id == 'YOD_026':
            random_minion = self.random_alive_minion(player)
            if random_minion is not None:
                random_minion.attack += trigger.attack
            random_minion.attack += trigger.attack
        elif card_id == 'TB_BaconUps_112':
            for i in range(2):
                random_minion = self.random_alive_minion(player)
                if random_minion is not None:
                    random_minion.attack += trigger.attack

        """Unstable Ghoul"""
        if card_id == 'FP1_024':
            self.simulate_damage_to_every_minions_by_minion(player, trigger, 1)
            self.simulate_damage_to_every_minions_by_minion(player.opponent, trigger, 1)
        elif card_id == 'TB_BaconUps_118':
            for i in range(2):
                self.simulate_damage_to_every_minions_by_minion(player, trigger, 1)
            self.simulate_damage_to_every_minions_by_minion(player.opponent, trigger, 1)

        """Replicating Menace"""
        if card_id == 'BOT_312':
            for i in range(3):
                new_minion = Util.make_default_minion('BOT_312t', golden=golden)
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)
        elif card_id == 'TB_BaconUps_032':
            for i in range(3):
                new_minion = Util.make_default_minion('TB_BaconUps_032t', golden=golden)
                self.simulate_summon_minion(new_minion, player, pos=player.trigger_pos)

    def simulate_reborn_triggers(self):
        for player in self.battle.players():
            player.reborn_trigger_pos = 0
            while player.reborn_triggers:
                while player.reborn_triggers[player.reborn_trigger_pos]:
                    card_id = player.reborn_triggers[player.reborn_trigger_pos].popleft()
                    new_minion = Util.make_default_minion(card_id)
                    new_minion.damage = new_minion.health - 1
                    new_minion.reborn = False

                    print(f"REBORN: {player.hero.name()} {new_minion.info()}")
                    self.simulate_summon_minion(new_minion, player, pos=player.reborn_trigger_pos)

                del player.reborn_triggers[player.reborn_trigger_pos]
                player.reborn_trigger_pos += 1

    def check_deaths(self):
        from copy import deepcopy
        is_minion_dead = False
        for player in self.battle.players():
            for minion in player.minions():
                # Do Deaths
                if minion.to_be_destroyed or minion.damage >= minion.health:
                    is_minion_dead = True

                    if minion.race is not None:
                        player.death_num_this_turn_by_race[minion.race] += 1
                        if minion.race == Race.ALL:
                            for race in RACE_ALL:
                                player.death_num_this_turn_by_race[race] += 1

                    if minion.deathrattle:
                        death_trigger = deepcopy(minion)
                        death_trigger.zone = Zone.SETASIDE
                        player.death_triggers[minion.pos].append(death_trigger)
                    if minion.reborn:
                        player.reborn_triggers[minion.pos].append(minion.card_id)
                    self.simulate_remove_minion(minion, minion.player)
                    self.simulate_minion_death_after(minion, minion.player)
        return is_minion_dead

    def simulate_minion_death_after(self, minion: Minion, player: Player):
        if isinstance(minion.last_damaged_by, Minion):
            if minion.last_damaged_by.race in (Race.DRAGON, Race.ALL):
                for opponent_minion in player.opponent.minions():
                    """Waxrider Togwaggle"""
                    if opponent_minion.card_id == "BGS_035":
                        opponent_minion.attack += 2
                        opponent_minion.health += 2
                    elif opponent_minion.card_id == "TB_BaconUps_105":
                        opponent_minion.attack += 4
                        opponent_minion.health += 4

    def simulate_overkill(self, minion: Minion):
        print(f'OVERKILL: {minion.player.hero.name()} {minion.info()}')

        card_id = minion.card_id
        golden = minion.golden

        """Ironhide Direhorn"""
        if card_id == 'TRL_232':
            new_minion = Util.make_default_minion('TRL_232t', golden=golden)
            self.simulate_summon_minion(new_minion, minion.player, minion.pos + 1)
        elif card_id == 'TB_BaconUps_051':
            new_minion = Util.make_default_minion('TB_BaconUps_051t', golden=golden)
            self.simulate_summon_minion(new_minion, minion.player, minion.pos + 1)

        """Herald of Flame"""
        if card_id == 'BGS_032':
            if self.battle.dfn_player().left_minion():
                self.simulate_damage_by_minion(defender=self.battle.dfn_player().left_minion(), attacker=minion, amount=3)
        elif card_id == 'TB_BaconUps_103':
            if self.battle.dfn_player().left_minion():
                self.simulate_damage_by_minion(defender=self.battle.dfn_player().left_minion(), attacker=minion, amount=6)

    def simulate_summon_minion(self, new_minion: Minion, player: Player, pos: Optional[int] = None) -> Optional[Minion]:
        if player.minion_num() >= 7:
            print(f"SUMMON Fail: {player.hero.name()} {new_minion.info()}")
            return None

        if pos is None:
            pos = player.minion_num() + 1

        if pos < 1 or pos > 7:
            print(f"SUMMON Fail: {player.hero.name()} {new_minion.info()}")
            return None

        # pos change
        for minion in player.minions():
            if minion.pos >= pos:
                minion.pos += 1
                player.board[minion.pos] = minion

        # trigger pos change
        if player.trigger_pos >= pos:
            player.trigger_pos += 1
        new_death_triggers = defaultdict(deque)
        for death_trigger_pos, death_triggers in player.death_triggers.items():
            for death_trigger in death_triggers:
                if death_trigger.pos >= pos:
                    death_trigger.pos += 1
                new_death_triggers[death_trigger.pos].append(death_trigger)
        player.death_triggers = new_death_triggers

        # reborn pos change
        if player.reborn_trigger_pos >= pos:
            player.reborn_trigger_pos += 1
        new_reborn_triggers = defaultdict(deque)
        for reborn_trigger_pos, reborn_triggers in player.reborn_triggers.items():
            if reborn_trigger_pos >= pos:
                new_reborn_triggers[reborn_trigger_pos + 1].extend(reborn_triggers)
            else:
                new_reborn_triggers[reborn_trigger_pos].extend(reborn_triggers)
        player.reborn_triggers = new_reborn_triggers

        new_minion.zone = Zone.PLAY
        new_minion.pos = pos
        new_minion.player = player
        player.board[pos] = new_minion

        # player.next_atk_minion_pos change
        if player.next_atk_minion_pos is not None:
            if player.minion_num() == 1:
                player.next_atk_minion_pos = pos
            else:
                if player.next_atk_minion_pos == 1 and pos == player.minion_num():
                    player.next_atk_minion_pos = pos
                elif new_minion.pos < player.next_atk_minion_pos:
                    player.next_atk_minion_pos += 1

        self.simulate_summon_minion_after(new_minion, player)
        print(f"SUMMON: {player.hero.name()} {new_minion.info()}")
        return new_minion

    def simulate_summon_minion_after(self, new_minion: Minion, player: Player):
        for minion in player.minions():
            if minion is new_minion:
                continue
            card_id = minion.card_id

            if new_minion.race in (Race.MECHANICAL, Race.ALL):
                """Deflect-o-Bot"""
                if card_id == "BGS_071":
                    minion.attack += 1
                    minion.divine_shield = True
                elif card_id == "TB_BaconUps_123":
                    minion.attack += 2
                    minion.divine_shield = True

            if new_minion.race in (Race.BEAST, Race.ALL):
                """Mama Bear"""
                if card_id == "BGS_021":
                    new_minion.attack += 5
                    new_minion.health += 5
                elif card_id == "TB_BaconUps_090":
                    new_minion.attack += 10
                    new_minion.health += 10

                """Pack Leader"""
                if card_id == "BGS_017":
                    new_minion.attack += 3
                elif card_id == "TB_BaconUps_086":
                    new_minion.attack += 6

        self.simulate_enchant_add(new_minion, player)

    def simulate_enchant_add(self, new_minion: Minion, player: Player):
        card_id = new_minion.card_id

        for minion in player.minions():
            if minion is new_minion:
                continue

            if minion.race in (Race.MURLOC, Race.ALL):

                """Murloc Warleader"""
                """Mrgglaargl!"""
                if card_id == "EX1_507":
                    self.make_enchant_and_add("EX1_507e", new_minion, minion)
                    minion.attack += 2
                elif card_id == "TB_BaconUps_008":
                    self.make_enchant_and_add("TB_BaconUps_008e", new_minion, minion)
                    minion.attack += 4

            if minion.pos in (new_minion.pos - 1, new_minion.pos + 1):

                """Dire Wolf Alpha"""
                """Strength of the Pack"""
                if card_id == "EX1_162":
                    self.make_enchant_and_add("EX1_162o", new_minion, minion)
                    minion.attack += 1
                elif card_id == "TB_BaconUps_088":
                    self.make_enchant_and_add("TB_BaconUps_088e", new_minion, minion)
                    minion.attack += 2




    def make_enchant_and_add(self, card_id: str, creator: HSObject, attached_minion: Minion) -> Enchantment:
        new_enchant = Enchantment()
        new_enchant.card_id = card_id

        new_enchant.creator = creator
        creator.created_enchants.append(new_enchant)

        new_enchant.attached_minion = attached_minion
        attached_minion.enchants.append(new_enchant)

        return new_enchant


    def simulate_remove_minion(self, removed_minion: Minion, player: Player):
        if player.board[removed_minion.pos] is not removed_minion:
            print(f'REMOVE Fail: {removed_minion.player.hero.name()} {removed_minion.info()}')
            return False

        # pos change
        player.board[removed_minion.pos] = None
        for change_pos_minion in player.minions():
            if change_pos_minion.pos > removed_minion.pos:
                player.board[change_pos_minion.pos] = None
                change_pos_minion.pos -= 1
                player.board[change_pos_minion.pos] = change_pos_minion

        # trigger pos change
        if player.trigger_pos > removed_minion.pos:
            player.trigger_pos -= 1
        new_death_triggers = defaultdict(deque)
        for death_trigger_pos, death_triggers in player.death_triggers.items():
            for death_trigger in death_triggers:
                if death_trigger.pos > removed_minion.pos:
                    death_trigger.pos -= 1
                new_death_triggers[death_trigger.pos].append(death_trigger)
        player.death_triggers = new_death_triggers

        # reborn pos change
        if player.reborn_trigger_pos > removed_minion.pos:
            player.reborn_trigger_pos -= 1
        new_reborn_triggers = defaultdict(deque)
        for reborn_trigger_pos, reborn_triggers in player.reborn_triggers.items():
            if reborn_trigger_pos > removed_minion.pos:
                new_reborn_triggers[reborn_trigger_pos - 1].extend(reborn_triggers)
            else:
                new_reborn_triggers[reborn_trigger_pos].extend(reborn_triggers)
        player.reborn_triggers = new_reborn_triggers

        # player.next_atk_minion_pos change
        if player.next_atk_minion_pos is not None:
            if removed_minion.pos == player.next_atk_minion_pos and player.board[removed_minion.pos] is None:  # removed minion is rightmost minion
                if player.empty():
                    player.next_atk_minion_pos = None
                else:
                    player.next_atk_minion_pos = 1

            elif removed_minion.pos < player.next_atk_minion_pos:
                player.next_atk_minion_pos -= 1

        removed_minion.pos = 0
        removed_minion.zone = Zone.GRAVEYARD

        self.simulate_remove_minion_after(removed_minion, player)

        print(f'REMOVE: {removed_minion.player.hero.name()} {removed_minion.info()}')
        removed_minion.attack = Util.default_attack_by_id(removed_minion.card_id)
        removed_minion.health = Util.default_health_by_id(removed_minion.card_id)
        removed_minion.damage = 0
        removed_minion.enchants.clear()
        removed_minion.created_enchants.clear()
        player.graveyard.append(removed_minion)

    def simulate_remove_minion_after(self, removed_minion: Minion, player: Player):
        self.simulate_enchant_remove(removed_minion, player)

    def simulate_enchant_remove(self, removed_minion: Minion, player: Player):
        # if removed_minion.card_id == "EX1_507":
        for created_enchant in removed_minion.created_enchants:
            if created_enchant.attached_minion and created_enchant.attached_minion.zone == Zone.PLAY:
                card_id = created_enchant.card_id
                minion = created_enchant.attached_minion

                """Murloc Warleader"""
                """Mrgglaargl!"""
                if card_id == "EX1_507e":
                    minion.attack -= 2
                elif card_id == "TB_BaconUps_008e":
                    minion.attack -= 4

                """Dire Wolf Alpha"""
                """Strength of the Pack"""
                if card_id == "EX1_162o":
                    minion.attack -= 1
                elif card_id == "TB_BaconUps_088e":
                    minion.attack -= 2



                created_enchant.attached_minion.enchants.remove(created_enchant)

    def simulate_damage(self, defender: Minion, amount: int, poisonous: bool = False):
        if amount <= 0:
            return False
        if defender.divine_shield:
            defender.divine_shield = False
            print(f"DAMAGE: {defender.player.hero.name()} {defender.info()}'s divine shield is broken")
            self.simualte_minion_broken_divine_shield_after(defender, defender.player)
            return False
        else:
            pre_defender_info = defender.info()
            defender.damage += amount
            if poisonous:
                defender.to_be_destroyed = True
            print(f"DAMAGE: {defender.player.hero.name()} {pre_defender_info} is damaged {amount} {'(poisonous)' if poisonous else ''} -> {defender.info()}")
            self.simulate_get_damage_after(defender)
            return True

    def simulate_damage_by_minion(self, defender: Minion, attacker: Minion, amount=None):
        if amount is None:
            amount = attacker.attack
        self.simulate_damage(defender, amount, attacker.poisonous)
        defender.last_damaged_by = attacker
        if attacker.zone == Zone.PLAY and attacker.overkill and attacker.player is self.battle.atk_player():  # attacker's turn
            if defender.hp() < 0:
                self.simulate_overkill(attacker)

    def simulate_damage_to_every_minions_by_minion(self, defender_player: Player, attacker: Minion, amount: int):
        for minion in defender_player.minions():
            self.simulate_damage_by_minion(minion, attacker, amount)

    def simulate_damage_to_random_minion_by_minion(self, defender_player: Player, attacker: Minion, amount=None):
        random_opponent_minion = self.random_alive_minion(defender_player)
        if random_opponent_minion is not None:
            self.simulate_damage_by_minion(random_opponent_minion, attacker, amount)

    def simualte_minion_broken_divine_shield_after(self, broken_minion: Minion, player: Player):
        for minion in player.minions():
            card_id = minion.card_id

            """Bolvar, Fireblood"""
            if card_id == 'ICC_858':
                minion.attack += 2
            elif card_id == 'TB_BaconUps_047':
                minion.attack += 4

            """Drakonid Enforcer"""
            if card_id == 'BGS_067':
                minion.attack += 2
                minion.health += 2
            elif card_id == 'TB_BaconUps_117':
                minion.attack += 4
                minion.health += 4

            """Holy Mackerel"""
            if card_id == 'BGS_068':
                if minion is not broken_minion:
                    minion.divine_shield = True

    def simulate_get_damage_after(self, defender: Minion):
        card_id = defender.card_id
        golden = defender.golden

        """Security Rover"""
        if card_id == 'BOT_218':
            new_minion = Util.make_default_minion('BOT_218t', golden=golden)
            self.simulate_summon_minion(new_minion, defender.player, pos=defender.pos + 1)
        elif card_id == 'TB_BaconUps_041':
            new_minion = Util.make_default_minion('TB_BaconUps_041t', golden=golden)
            new_minion.golden = True
            self.simulate_summon_minion(new_minion, defender.player, pos=defender.pos + 1)

        """Imp Gang Boss"""
        if card_id == 'BRM_006':
            new_minion = Util.make_default_minion('BRM_006t', golden=golden)
            self.simulate_summon_minion(new_minion, defender.player, pos=defender.pos + 1)
        elif card_id == 'TB_BaconUps_030':
            new_minion = Util.make_default_minion('TB_BaconUps_030t', golden=golden)
            self.simulate_summon_minion(new_minion, defender.player, pos=defender.pos + 1)

        """Imp Mama"""
        if card_id == "BGS_044":
            new_minion = Util.random_bp_minion_race(Race.DEMON, golden=golden, except_card_ids="BGS_044")
            self.simulate_summon_minion(new_minion, defender.player, pos=defender.pos + 1)
        elif card_id == "TB_BaconUps_116":
            for i in range(2):
                new_minion = Util.random_bp_minion_race(Race.DEMON, golden=golden, except_card_ids="BGS_044")
                self.simulate_summon_minion(new_minion, defender.player, pos=defender.pos + 1)

    def random_lowest_atk_minion(self, player: Player) -> Optional[Minion]:
        if player.empty():
            return None
        lowest_atk = None
        lowest_atk_minions = []  # type: List[Minion]

        for minion in player.minions():
            if not lowest_atk_minions:
                lowest_atk = minion.attack
                lowest_atk_minions.append(minion)
                continue
            if minion.attack == lowest_atk:
                lowest_atk_minions.append(minion)
            elif minion.attack < lowest_atk:
                lowest_atk_minions.clear()
                lowest_atk = minion.attack
                lowest_atk_minions.append(minion)

        return random.choice(lowest_atk_minions)

    def random_defense_minion(self, player: Player) -> Optional[Minion]:
        if player.empty():
            return None
        taunt_minions = []  # type: List[Minion]

        for minion in player.minions():
            if minion.taunt:
                taunt_minions.append(minion)

        if taunt_minions:
            return random.choice(taunt_minions)
        else:
            return random.choice(player.minions())

    def random_alive_minion(self, player: Player) -> Optional['Minion']:
        alive_minions = []
        for minion in player.minions():
            if minion.hp() > 0:
                alive_minions.append(minion)

        if alive_minions:
            return random.choice(alive_minions)
        else:
            return None











