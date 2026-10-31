from ex0.Card import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical


class EliteCard(Card, Combatable, Magical):
    def __init__(self, name: str, cost: int, rarity: str,
                 attack_value: int, health: int, mana: int) -> None:
        super().__init__(name, cost, rarity)
        self.attack_value = attack_value
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana * 3

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': 'Elite creature summoned with combat and magic abilities'
        }

    def attack(self, target) -> dict:
        return {
            'attacker': self.name,
            'target': target,
            'damage': self.attack_value,
            'combat_type': 'melee'
        }

    def defend(self, incoming_damage: int) -> dict:
        damage_blocked = incoming_damage // 2
        damage_taken = incoming_damage - damage_blocked
        self.health = max(0, self.health - damage_taken)
        return {
            'defender': self.name,
            'damage_taken': damage_taken,
            'damage_blocked': damage_blocked,
            'still_alive': self.health > 0
        }

    def get_combat_stats(self) -> dict:
        return {
            'name': self.name,
            'attack': self.attack_value,
            'health': self.health,
            'defense_ratio': 0.5
        }

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        mana_cost = len(targets) * 2
        if self.mana < mana_cost:
            return {
                'caster': self.name,
                'spell': spell_name,
                'success': False,
                'reason': 'Insufficient mana'
            }
        self.mana -= mana_cost
        return {
            'caster': self.name,
            'spell': spell_name,
            'targets': targets,
            'mana_used': mana_cost,
        }

    def channel_mana(self, amount: int) -> dict:
        self.mana += amount
        return {
            'channeled': amount,
            'total_mana': self.mana,
        }

    def get_magic_stats(self) -> dict:
        mana_pct = (
            (self.mana / self.max_mana * 100) if self.max_mana > 0 else 0
        )
        return {
            'name': self.name,
            'current_mana': self.mana,
            'max_mana': self.max_mana,
            'mana_percentage': round(mana_pct, 1)
        }
