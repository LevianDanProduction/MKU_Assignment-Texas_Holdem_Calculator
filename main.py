from collections import Counter
from itertools import groupby, combinations

class HandEvaluator:
    suits = ["hearts", "diamonds", "clubs", "spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    @staticmethod
    def evaluate_hand(player_hand, community_cards):
        all_cards = player_hand + community_cards
        all_values = [card.value for card in all_cards]
        all_suits = [card.suit for card in all_cards]

        value_counts = Counter(all_values)
        suit_counts = Counter(all_suits)

        flush = HandEvaluator.check_flush(suit_counts, all_cards)
        straight = HandEvaluator.check_straight(value_counts)
        hand_rank = HandEvaluator.determine_hand_rank(value_counts, flush, straight)

        return hand_rank

    @staticmethod
    def check_flush(suit_counts, all_cards):
        flush_suit = next((suit for suit, count in suit_counts.items() if count >= 5), None)
        if flush_suit:
            flush_cards = [card for card in all_cards if card.suit == flush_suit]
            flush_cards.sort(key=lambda card: Card.values.index(card.value), reverse=True)
            return flush_cards
        return None

    @staticmethod
    def check_straight(value_counts):
        value_indices = sorted([Card.values.index(value) for value in value_counts.keys()])

        # Add Ace to the beginning of the list for Ace-low straights
        if 12 in value_indices:
            value_indices.insert(0, -1)

        for _, group in groupby(enumerate(value_indices), lambda x: x[0] - x[1]):
            consecutive_values = list(map(lambda x: x[1], group))
            if len(consecutive_values) >= 5:
                top_straight_value = consecutive_values[-1]
                return Card.values[top_straight_value]
        return None

    @staticmethod
    def determine_hand_rank(value_counts, flush, straight):
        if flush and straight:
            if flush[0].value == straight:
                return "Straight flush"
        if any(count >= 4 for count in value_counts.values()):
            return "Four of a kind"
        if HandEvaluator.has_full_house(value_counts):
            return "Full house"
        if flush:
            return "Flush"
        if straight:
            return "Straight"
        if any(count >= 3 for count in value_counts.values()):
            return "Three of a kind"
        if HandEvaluator.has_two_pair(value_counts):
            return "Two pair"
        return "One pair" if any(count >= 2 for count in value_counts.values()) else "High card"

    @staticmethod
    def has_full_house(value_counts):
        three_of_a_kind = any(count >= 3 for count in value_counts.values())
        one_pair = any(count >= 2 for count in value_counts.values())
        return three_of_a_kind and one_pair

    @staticmethod
    def has_two_pair(value_counts):
        return sum(1 for count in value_counts.values() if count >= 2) >= 2
    
    
    @staticmethod
    def rank_hand(player_hand, community_cards):
        all_cards = player_hand + community_cards
        all_values = [card.value for card in all_cards]
        all_suits = [card.suit for card in all_cards]

        value_counts = Counter(all_values)
        suit_counts = Counter(all_suits)

        flush = HandEvaluator.check_flush(suit_counts, all_cards)
        straight = HandEvaluator.check_straight(value_counts)
        hand_rank = HandEvaluator.determine_hand_rank(value_counts, flush, straight)

        tiebreaker_values = HandEvaluator.get_tiebreaker_values(value_counts, hand_rank, flush)

        return hand_rank, tiebreaker_values
    
    @staticmethod
    def get_tiebreaker_values(value_counts, hand_rank, flush):
        if hand_rank in ["Straight flush", "Flush"]:
            return [HandEvaluator.values.index(card.value) for card in flush[:5]]
        if hand_rank == "Four of a kind":
            four_of_a_kind_value = [v for v, count in value_counts.items() if count == 4][0]
            kicker_value = max(v for v, count in value_counts.items() if count != 4)
            return [HandEvaluator.values.index(four_of_a_kind_value), HandEvaluator.values.index(kicker_value)]
        if hand_rank == "Full house":
            three_of_a_kind_value = [v for v, count in value_counts.items() if count == 3][0]
            pair_value = [v for v, count in value_counts.items() if count == 2][0]
            return [HandEvaluator.values.index(three_of_a_kind_value), HandEvaluator.values.index(pair_value)]
        if hand_rank == "Straight":
            return [HandEvaluator.values.index(straight)]
        if hand_rank == "Three of a kind":
            three_of_a_kind_value = [v for v, count in value_counts.items() if count == 3][0]
            kickers = sorted([v for v, count in value_counts.items() if count != 3], reverse=True)[:2]
            return [HandEvaluator.values.index(three_of_a_kind_value)] + [HandEvaluator.values.index(k) for k in kickers]
        if hand_rank == "Two pair":
            pair_values = sorted([v for v, count in value_counts.items() if count == 2], reverse=True)
            kicker_value = max(v for v, count in value_counts.items() if count == 1)
            return [HandEvaluator.values.index(p) for p in pair_values] + [HandEvaluator.values.index(kicker_value)]
        if hand_rank == "One pair":
            pair_value = [v for v, count in value_counts.items() if count == 2][0]
            kickers = sorted([v for v, count in value_counts.items() if count != 2], reverse=True)[:3]
            return [HandEvaluator.values.index(pair_value)] + [HandEvaluator.values.index(k) for k in kickers]
        if hand_rank == "High card":
            high_cards = sorted(value_counts.keys(), key=lambda x: HandEvaluator.values.index(x), reverse=True)[:5]
            return [HandEvaluator.values.index(h) for h in high_cards]

# Update the TexasHoldem class play_game method
def play_game(self):
    self.deal_hands()

    print("Players' hands :")
    for player in self.players:
        print(f"{player.name}: {player.show_hand()}")

    self.deal_community_cards()

    print("Community cards:")
    print(self.show_community_cards())

    print("Hand evaluations:")
    for player in self.players:
        hand_rank = HandEvaluator.evaluate_hand(player.hand, self.community_cards)
        print(f"{player.name}: {hand_rank}")

if __name__ == "__main__":
    player1 = Player("Alice")
    player2 = Player("Bob")
    player3 = Player("Carol")

    game = TexasHoldem([player1, player2, player3])
    game.play_game()