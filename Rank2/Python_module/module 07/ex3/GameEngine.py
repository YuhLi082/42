from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    def __init__(self):
        self.factory = None
        self.strategy = None
        self.turns_simulated = 0
        self.total_damage = 0
        self.cards_created = set()

    def configure_engine(self, factory: CardFactory,
                         strategy: GameStrategy) -> None:
        self.factory = factory
        self.strategy = strategy

    def simulate_turn(self) -> dict:
        if not self.factory or not self.strategy:
            return {
                'error': 'Engine not configured',
                'message': 'Please call configure_engine first'
            }

        hand = [
            self.factory.create_creature('dragon'),
            self.factory.create_creature('goblin'),
            self.factory.create_spell('fireball')
        ]

        for card in hand:
            self.cards_created.add(card.name)

        battlefield = []
        actions = self.strategy.execute_turn(hand, battlefield)

        self.turns_simulated += 1
        if 'damage_dealt' in actions:
            self.total_damage += actions['damage_dealt']

        return {
            'strategy': self.strategy.get_strategy_name(),
            'actions': actions
        }

    def get_engine_status(self) -> dict:
        return {
            'turns_simulated': self.turns_simulated,
            'strategy_used': (
                self.strategy.get_strategy_name() if self.strategy else 'None'
                ),
            'total_damage': self.total_damage,
            'cards_created': len(self.cards_created)
        }
