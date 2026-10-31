import random
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard


class Deck:
    def __init__(self):
        self._cards = []

    def add_card(self, card: Card) -> None:
        self._cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        for card in self._cards:
            if card.name == card_name:
                self._cards.remove(card)
                return True
        return False

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def draw_card(self) -> Card | None:
        if not self._cards:
            return None
        card = self._cards[0]
        self._cards = self._cards[1:]
        return card

    def get_deck_stats(self) -> dict:
        total_cards = len(self._cards)
        if total_cards == 0:
            return {
                'total_cards': 0,
                'creatures': 0,
                'spells': 0,
                'artifacts': 0,
                'avg_cost': 0
            }
        creatures = sum(1 for c in self._cards if isinstance(c, CreatureCard))
        spells = sum(1 for c in self._cards if isinstance(c, SpellCard))
        artifacts = sum(1 for c in self._cards if isinstance(c, ArtifactCard))
        avg_cost = sum(c.cost for c in self._cards) / total_cards
        return {
            'total_cards': total_cards,
            'creatures': creatures,
            'spells': spells,
            'artifacts': artifacts,
            'avg_cost': round(avg_cost, 1)
        }
