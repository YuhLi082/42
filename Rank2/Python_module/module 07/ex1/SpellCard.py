from ex0.Card import Card


class SpellCard(Card):
    def __init__(self, name: str, cost: int,
                 rarity: str, effect_type: str) -> None:
        super().__init__(name, cost, rarity)
        self.effect_type = effect_type

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': f'Deal {self.cost} damage to target'
        }

    def resolve_effect(self, targets: list) -> dict:
        return {
            'spell_name': self.name,
            'targets': targets,
            'effect_type': self.effect_type,
            'resolved': True
        }
