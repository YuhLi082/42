from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):
    def execute_turn(self, hand: list, battlefield: list) -> dict:
        def get_cost(card):
            return card.cost
        sorted_hand = sorted(hand, key=get_cost)

        cards_played = []
        mana_used = 0
        damage_dealt = 0
        available_mana = 10

        for card in sorted_hand:
            if mana_used + card.cost <= available_mana:
                cards_played.append(card.name)
                mana_used += card.cost

                try:
                    damage_dealt += card.attack
                except AttributeError:
                    try:
                        if card.effect_type == 'damage':
                            damage_dealt += 3
                    except AttributeError:
                        pass

        return {
            'cards_played': cards_played,
            'mana_used': mana_used,
            'targets_attacked': ['Enemy Player'],
            'damage_dealt': damage_dealt
        }

    def get_strategy_name(self) -> str:
        return 'AggressiveStrategy'

    def prioritize_targets(self, available_targets: list) -> list:
        prioritized = []
        if 'Enemy Player' in available_targets:
            prioritized.append('Enemy Player')
        for target in available_targets:
            if target != 'Enemy Player' and target not in prioritized:
                prioritized.append(target)

        return prioritized
