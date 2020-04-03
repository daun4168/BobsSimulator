import copy
import random
from typing import List, Dict, Optional

from PySide2.QtCore import Signal, QObject

from BobsSimulator.HSType import Battle, Minion, Zone, Player, Race
from BobsSimulator.HSLogging import simulator_logger, console_logger
from BobsSimulator.Util import Util


class Simulator(QObject):
    def __init__(self):
        super().__init__()
        self.battle = Battle()

    def simulate(self, battle: Battle, simulate_num=1) -> list:
        result = []
        simulator_logger.info(f'''# {"=" * 50}''')
        simulator_logger.info("# Simulate Start")
        simulator_logger.info("-" * 50)
        simulator_logger.info("# Battle Info")
        battle.print_log(simulator_logger)
        simulator_logger.info("-" * 50)

        print('='*50)
        print("# Simulate Start")
        print(battle.info())

        for i in range(simulate_num):
            simulator_logger.info("-" * 50)
            simulator_logger.info(f"# Simulation {i + 1}/{simulate_num}")
            self.battle = copy.deepcopy(battle)
            result.append(self.simulate_once())
            simulator_logger.info("-" * 50)
        simulator_logger.info("=" * 50)
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
        attacker = self.next_attacker(self.battle.atk_player())
        if attacker is None:
            self.battle.atk_player().not_attack_last_seq = True
            return

        num_of_atk = 1 + attacker.windfury
        for i in range(num_of_atk):
            if attacker.zone != Zone.PLAY:
                return
            self.attack_once(attacker)

    def next_attacker(self, player: Player):
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

    def attack_once(self, attacker: Minion):
        if self.battle.dfn_player().empty():
            return

        defender = None  # type: Optional[Minion]
        if attacker.atk_lowest_atk_minion:
            defender = self.random_lowest_atk_minion(self.battle.dfn_player())
        else:
            defender = self.random_defense_minion(self.battle.dfn_player())
        print(f"ATTACK {self.battle.atk_player().hero.name()}'s {attacker.info()} -> {self.battle.dfn_player().hero.name()}'s {defender.info()}")

        self.simulate_damage_by_minion(defender, attacker)
        self.simulate_damage_by_minion(attacker, defender)

        # cleave
        if attacker.card_id in ("GVG_113", "LOOT_078"):  # Foe Reaper 4000, Cave Hydra
            if defender.pos > 1 and self.battle.dfn_player().board[defender.pos - 1] is not None:
                self.simulate_damage_by_minion(self.battle.dfn_player().board[defender.pos - 1], attacker)
            if defender.pos < 7 and self.battle.dfn_player().board[defender.pos + 1] is not None:
                self.simulate_damage_by_minion(self.battle.dfn_player().board[defender.pos + 1], attacker)

        self.simulate_deaths()
        print(self.battle.info())

    def simulate_damage_by_minion(self, defender: Minion, attacker: Minion, amount=None):
        if amount is None:
            amount = attacker.attack
        self.simulate_damage(defender, amount, attacker.poisonous)
        if attacker.overkill and attacker.player is self.battle.atk_player():  # attacker's turn
            if defender.hp() < 0:
                self.simulate_overkill(attacker)


    def simulate_deaths(self):
        while True:
            is_minion_dead = self.check_deaths()
            if not is_minion_dead:
                return
            self.simulate_death_triggers()

    def simulate_death_triggers(self):
        pass

    def check_deaths(self):
        is_minion_dead = False
        for player in self.battle.players():
            for minion in player.minions():
                # Do Deaths
                if minion.to_be_destroyed or minion.damage >= minion.health:
                    self.buff_when_minion_death(minion)
                    self.simulate_remove_minion(minion, minion.player)

        # 하이에나류 버프
        # 곡예사, 죽메

    def buff_when_minion_death(self, death_minion: Minion):
        if death_minion.race == Race.BEAST:

            pass

    def simulate_overkill(self, minion: Minion):
        print(f'OVERKILL: {minion.info()}')
        if minion.card_id == 'TRL_232':  # Ironhide Direhorn
            new_minion = Util.make_default_minion('TRL_232t')
            self.simulate_summon_minion(new_minion, minion.player, minion.pos + 1)
        elif minion.card_id == 'TB_BaconUps_051':  # Ironhide Direhorn lv2
            new_minion = Util.make_default_minion('TB_BaconUps_051t')
            self.simulate_summon_minion(new_minion, minion.player, minion.pos + 1)

        elif minion.card_id == 'BGS_032':  # Herald of Flame
            if self.battle.dfn_player().left_minion():
                self.simulate_damage_by_minion(defender=self.battle.dfn_player().left_minion(), attacker=minion, amount=3)
        elif minion.card_id == 'TB_BaconUps_103':  # Herald of Flame lv2
            if self.battle.dfn_player().left_minion():
                self.simulate_damage_by_minion(defender=self.battle.dfn_player().left_minion(), attacker=minion, amount=6)

    def simulate_summon_minion(self, new_minion: Minion, player: Player, pos: Optional[int] = None):
        if player.minion_num() >= 7:
            print(f"SUMMON Fail: {new_minion.info()}")
            return False

        if pos is None:
            pos = player.minion_num() + 1

        if pos < 1 or pos > 7:
            print(f"SUMMON Fail: {new_minion.info()}")
            return False

        # pos change
        for minion in player.minions():
            if minion.pos >= pos:
                minion.pos += 1
                player.board[minion.pos] = minion

        new_minion.zone = Zone.PLAY
        new_minion.pos = pos
        new_minion.player = player
        player.board[pos] = new_minion

        # player.next_atk_minion_pos change
        if player.minion_num() == 1:
            player.next_atk_minion_pos = pos
        else:
            if player.next_atk_minion_pos == 1 and pos == player.minion_num():
                player.next_atk_minion_pos = pos
            elif new_minion.pos < player.next_atk_minion_pos:
                player.next_atk_minion_pos += 1

        print(f"SUMMON: {new_minion.info()}")

    def simulate_remove_minion(self, removed_minion: 'Minion', player: Player):
        if player.board[removed_minion.pos] is not removed_minion:
            print(f'REMOVE Fail: {removed_minion.info()}')
            return False

        # pos change
        player.board[removed_minion.pos] = None
        for change_pos_minion in player.minions():
            if change_pos_minion.pos > removed_minion.pos:
                player.board[change_pos_minion.pos] = None
                change_pos_minion.pos -= 1
                player.board[change_pos_minion.pos] = change_pos_minion

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

        print(f'REMOVE: {removed_minion.info()}')
        removed_minion.attack = Util.default_attack_by_id(removed_minion.card_id)
        removed_minion.health = Util.default_health_by_id(removed_minion.card_id)
        removed_minion.damage = 0
        player.graveyard.append(removed_minion)

    def simulate_damage(self, defender: Minion, amount: int, poisonous: bool = False):
        if amount <= 0:
            return False
        if defender.divine_shield:
            defender.divine_shield = False
            print(f"DAMAGE: {defender.player.hero.name()}'s {defender.info()}'s divine shield is broken")
            self.frendly_minion_break_divine_shield(defender.player)
            return False
        else:
            pre_defender_info = defender.info()
            defender.damage += amount
            if poisonous:
                defender.to_be_destroyed = True
            print(f"DAMAGE: {defender.player.hero.name()}'s {pre_defender_info} is damaged {amount} {'(poisonous)' if poisonous else ''} -> {defender.info()}")
            self.minion_damaged(defender)
            self.simulate_get_damage_after(defender)
            return True

    def frendly_minion_break_divine_shield(self, player: Player):
        pass

    def simulate_get_damage_after(self, defender: Minion):
        pass

    def minion_damaged(self, minion: Minion):
        pass

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











