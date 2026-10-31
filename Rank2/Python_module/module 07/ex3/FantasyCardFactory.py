from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex3.CardFactory import CardFactory
from typing import Union
import random


class FantasyCardFactory(CardFactory):
    def __init__(self):
        self.creatures = {
            'dragon': ('Fire Dragon', 5, 'Legendary', 7, 5),
            'goblin': ('Goblin Warrior', 2, 'Common', 2, 1),
            'elf': ('Forest Elf', 3, 'Rare', 3, 3)
        }

        self.spells = {
            'fireball': ('Fireball', 4, 'Rare', 'damage'),
            'heal': ('Healing Spell', 3, 'Common', 'heal'),
            'frost': ('Frost Bolt', 2, 'Common', 'damage')
        }

        self.artifacts = {
            'mana_ring': ('Mana Ring', 2, 'Rare', 5, '+1 mana per turn'),
            'sword': ('Enchanted Sword', 3, 'Uncommon', 3, '+2 attack'),
            'shield': ('Aegis Shield', 4, 'Rare', 4, '+3 defense')
        }

        self._extended_creatures = {}
        self._extended_spells = {}
        self._extended_artifacts = {}

    def create_creature(self, name_or_power:
                        str | int | None = None) -> CreatureCard:
        if isinstance(name_or_power, str):
            name_key = name_or_power.lower()

            if name_key in self._extended_creatures:
                data = self._extended_creatures[name_key]
                return CreatureCard(data[0], data[1],
                                    data[2], data[3], data[4])

            if name_key in self.creatures:
                data = self.creatures[name_key]
                return CreatureCard(data[0], data[1],
                                    data[2], data[3], data[4])

        elif isinstance(name_or_power, int):
            templates = list(self.creatures.values())
            idx = min(name_or_power, len(templates) - 1)
            data = templates[idx]
            return CreatureCard(data[0], data[1], data[2], data[3], data[4])

        name_key = random.choice(list(self.creatures.keys()))
        data = self.creatures[name_key]
        return CreatureCard(data[0], data[1], data[2], data[3], data[4])

    def create_spell(self, name_or_power:
                     Union[str, int, None] = None) -> SpellCard:
        if isinstance(name_or_power, str):
            name_key = name_or_power.lower()

            if name_key in self._extended_spells:
                data = self._extended_spells[name_key]
                return SpellCard(data[0], data[1], data[2], data[3])

            if name_key in self.spells:
                data = self.spells[name_key]
                return SpellCard(data[0], data[1], data[2], data[3])

        elif isinstance(name_or_power, int):
            templates = list(self.spells.values())
            idx = min(name_or_power, len(templates) - 1)
            data = templates[idx]
            return SpellCard(data[0], data[1], data[2], data[3])

        name_key = random.choice(list(self.spells.keys()))
        data = self.spells[name_key]
        return SpellCard(data[0], data[1], data[2], data[3])

    def create_artifact(self, name_or_power:
                        Union[str, int, None] = None) -> ArtifactCard:
        if isinstance(name_or_power, str):
            name_key = name_or_power.lower()

            if name_key in self._extended_artifacts:
                data = self._extended_artifacts[name_key]
                return ArtifactCard(data[0], data[1],
                                    data[2], data[3], data[4])

            if name_key in self.artifacts:
                data = self.artifacts[name_key]
                return ArtifactCard(data[0], data[1],
                                    data[2], data[3], data[4])

        elif isinstance(name_or_power, int):
            templates = list(self.artifacts.values())
            idx = min(name_or_power, len(templates) - 1)
            data = templates[idx]
            return ArtifactCard(data[0], data[1], data[2], data[3], data[4])

        name_key = random.choice(list(self.artifacts.keys()))
        data = self.artifacts[name_key]
        return ArtifactCard(data[0], data[1], data[2], data[3], data[4])

    def create_themed_deck(self, size: int) -> dict:
        deck = {
            'creatures': [],
            'spells': [],
            'artifacts': []
        }

        for i in range(size):
            if i % 3 == 0:
                deck['creatures'].append(self.create_creature())
            elif i % 3 == 1:
                deck['spells'].append(self.create_spell())
            else:
                deck['artifacts'].append(self.create_artifact())

        return deck

    def get_supported_types(self) -> dict:
        return {
            'creatures': list(self.creatures.keys()),
            'spells': list(self.spells.keys()),
            'artifacts': list(self.artifacts.keys())
        }
