from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    def __init__(self, name: str, cost: int, rarity: str,
                 attack_value: int, health: int,
                 base_rating: int = 1200) -> None:
        super().__init__(name, cost, rarity)
        self.attack_value = attack_value
        self.health = health
        self.wins = 0
        self.losses = 0
        self.base_rating = base_rating

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': 'Tournament card summoned'
        }

    def get_card_info(self) -> dict:
        info = super().get_card_info()
        info.update({
            'type': 'Tournament',
            'attack': self.attack_value,
            'health': self.health,
            'rating': self.calculate_rating(),
            'record': f"{self.wins}-{self.losses}"
        })
        return info

    def attack(self, target) -> dict:
        return {
            'attacker': self.name,
            'target': target,
            'damage': self.attack_value,
            'combat_type': 'tournament',
            'resolved': True
        }

    def defend(self, incoming_damage: int) -> dict:
        damage_blocked = incoming_damage // 2
        damage_taken = incoming_damage - damage_blocked
        self.health = max(0, self.health - damage_taken)
        return {
            'defender': self.name,
            'damage_taken': damage_taken,
            'damage_blocked': damage_blocked,
            'health_remaining': self.health,
            'still_alive': self.health > 0
        }

    def get_combat_stats(self) -> dict:
        return {
            'name': self.name,
            'attack': self.attack_value,
            'health': self.health,
            'defense_ratio': 0.5
        }

    def calculate_rating(self) -> int:
        rating = self.base_rating + (self.wins * 16) - (self.losses * 16)
        return max(800, rating)

    def update_wins(self, wins: int) -> None:
        self.wins += wins

    def update_losses(self, losses: int) -> None:
        self.losses += losses

    def get_rank_info(self) -> dict:
        total_matches = self.wins + self.losses
        win_rate = (
            (self.wins / total_matches * 100) if total_matches > 0 else 0
            )
        return {
            'name': self.name,
            'rating': self.calculate_rating(),
            'wins': self.wins,
            'losses': self.losses,
            'win_rate': f"{win_rate:.1f}%",
            'total_matches': total_matches
        }
