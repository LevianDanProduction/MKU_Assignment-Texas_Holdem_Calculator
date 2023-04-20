import math


def combinations(n, k):
    all_possibilities = float(math.factorial(n) / (math.factorial(k) * math.factorial(n - k)))
    return all_possibilities


def calculate_probability(frequency):
    all_possibilities = combinations(52, 5)
    return (frequency / all_possibilities) * 100


def poker_probabilities(type):
    
    royal_flush_frequency = combinations(4, 1)
    royal_flush_probability = calculate_probability(royal_flush_frequency)

    straight_flush_frequency = combinations(4, 1) * combinations(9, 1)
    straight_flush_probability = calculate_probability(straight_flush_frequency)

    # Available 13 cards, also 12 possibilities for the fifth one and 4 colors
    four_of_a_kind_frequency = combinations(13, 1) * combinations(13-1, 1) * combinations(4, 1)
    four_of_a_kind_probability = calculate_probability(four_of_a_kind_frequency)

    # We have first three: 13 cards, 4 possibilities, last two: 12 cards, 6 possibilities
    full_house_frequency = combinations(13, 1) * combinations(4, 3) * combinations(13-1, 1) * combinations(4, 2)
    full_house_probability = calculate_probability(full_house_frequency)

    flush_frequency = (combinations(13, 5) * combinations(4, 1) - royal_flush_frequency - straight_flush_frequency)
    flush = calculate_probability(flush_frequency)

    # 10 possible sequences are there,and also 4 choices from all the colours
    straight_frequency = combinations(10, 1) * 4**5 - straight_flush_frequency
    straight_probability = calculate_probability(straight_frequency)

    # Available 13 cards, 4 possibilities,we need to choose 2 from 12 cards,
    three_of_a_kind_frequency = combinations(13, 1) * combinations(4, 3) * combinations(13-1, 2) * 4**2
    three_of_a_kind_probability = calculate_probability(three_of_a_kind_frequency)

    # 2 pairs and the fifth card not from a pair
    two_pair_frequency = combinations(13, 2) * combinations(4, 2)**2 * combinations(13-2, 1) * combinations(4, 1)
    two_pair_probability = calculate_probability(two_pair_frequency)

    # 1 pair and three random cards without the one in the pair
    one_pair_frequency = combinations(13, 1) * combinations(4, 2) * combinations(13-1, 3) * combinations(4, 1)**3
    one_pair_probability = calculate_probability(one_pair_frequency)

    no_pair_frequency = (combinations(13, 5) - 10) * (combinations(4, 1)**5-4)  # no pair
    no_pair_probability = calculate_probability(no_pair_frequency)

def poker_probabilitie(hand_type,retu="prob"):
    from math import comb as combinations

    def calculate_probability(frequency):
        total_poker_hands = combinations(52, 5)
        return frequency / total_poker_hands

    hand_probabilities = {
        "royal-flush": calculate_probability(combinations(4, 1)),
        "straight-flush": calculate_probability(combinations(4, 1) * combinations(9, 1)),
        "four-of-a-kind": calculate_probability(combinations(13, 1) * combinations(12, 1) * combinations(4, 1)),
        "full-house": calculate_probability(combinations(13, 1) * combinations(4, 3) * combinations(12, 1) * combinations(4, 2)),
        "flush": calculate_probability((combinations(13, 5) * combinations(4, 1)) - combinations(4, 1) - (combinations(4, 1) * combinations(9, 1))),
        "straight": calculate_probability(combinations(10, 1) * 4**5 - combinations(4, 1) * combinations(9, 1)),
        "three-of-a-kind": calculate_probability(combinations(13, 1) * combinations(4, 3) * combinations(12, 2) * 4**2),
        "two-pair": calculate_probability(combinations(13, 2) * combinations(4, 2)**2 * combinations(11, 1) * combinations(4, 1)),
        "one-pair": calculate_probability(combinations(13, 1) * combinations(4, 2) * combinations(12, 3) * combinations(4, 1)**3),
        "high-card": calculate_probability((combinations(13, 5) - 10) * (combinations(4, 1)**5 - 4))
    }
    if retu == "prob":
        probability = hand_probabilities.get(hand_type, None)
        if probability is not None:
            return f"{probability * 100:.10f}%"
        else:
            return "Invalid hand type"
    else:
        return hand_probabilities.get(hand_type, "Invalid hand type")