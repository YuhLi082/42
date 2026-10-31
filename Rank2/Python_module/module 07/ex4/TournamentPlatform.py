from ex4.TournamentCard import TournamentCard


class TournamentPlatform:
    def __init__(self) -> None:
        self.registered_cards: dict[str, TournamentCard] = {}
        self.matches_played = 0

    def register_card(self, card: TournamentCard, card_id: str = None) -> str:
        if card_id is None:
            card_id = card.name.lower().replace(' ', '_') + '_'
            + str(len(self.registered_cards))
        self.registered_cards[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        if card1_id not in self.registered_cards:
            return {'error': 'Invalid card ID'}
        if card2_id not in self.registered_cards:
            return {'error': 'Invalid card ID'}

        card1 = self.registered_cards[card1_id]
        card2 = self.registered_cards[card2_id]

        card1_power = card1.attack_value + (card1.calculate_rating() / 100)
        card2_power = card2.attack_value + (card2.calculate_rating() / 100)

        if card1_power >= card2_power:
            winner_id = card1_id
            loser_id = card2_id
            winner = card1
            loser = card2
        else:
            winner_id = card2_id
            loser_id = card1_id
            winner = card2
            loser = card1

        winner.update_wins(1)
        loser.update_losses(1)
        self.matches_played += 1

        return {
            'winner': winner_id,
            'loser': loser_id,
            'winner_rating': winner.calculate_rating(),
            'loser_rating': loser.calculate_rating()
        }

    def get_leaderboard(self) -> list:
        sorted_cards = sorted(
            self.registered_cards.items(),
            key=lambda x: x[1].calculate_rating(),
            reverse=True
        )
        leaderboard = []
        for rank, (card_id, card) in enumerate(sorted_cards, 1):
            leaderboard.append({
                'rank': rank,
                'card_id': card_id,
                'name': card.name,
                'rating': card.calculate_rating(),
                'record': f"{card.wins}-{card.losses}"
            })
        return leaderboard

    def generate_tournament_report(self) -> dict:
        total_cards = len(self.registered_cards)
        if total_cards == 0:
            return {
                'total_cards': 0,
                'matches_played': 0,
                'avg_rating': 0,
                'platform_status': 'empty'
            }
        ratings = [c.calculate_rating()
                   for c in self.registered_cards.values()]
        avg_rating = sum(ratings) / len(ratings)
        return {
            'total_cards': total_cards,
            'matches_played': self.matches_played,
            'avg_rating': round(avg_rating),
            'platform_status': 'active'
        }
