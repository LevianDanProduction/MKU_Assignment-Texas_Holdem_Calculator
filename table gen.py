import itertools
import numpy as np 
import pandas as pd 
import assesor
import time


# Define the deck of cards
deck = ['2♥ ', '2♦', '2♣', '2♠', '3♥ ', '3♦', '3♣', '3♠',
        '4♥ ', '4♦', '4♣', '4♠', '5♥ ', '5♦', '5♣', '5♠',
        '6♥ ', '6♦', '6♣', '6♠', '7♥ ', '7♦', '7♣', '7♠',
        '8♥ ', '8♦', '8♣', '8♠', '9♥ ', '9♦', '9♣', '9♠',
        '10♥ ', '10♦', '10♣', '10♠', 'j♥', 'j♦', 'j♣', 'j♠',
        'q♥', 'q♦', 'q♣', 'q♠', 'k♥', 'k♦', 'k♣', 'k♠',
        'a♥', 'a♦', 'a♣', 'a♠']

# Define a function to sort the cards by power
def card_power(card):
    rank = card[:-1]
    power_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
    return power_map[rank]

# Sort the deck by power
#sorted_deck = sorted(deck, key=card_power)

# Record the start time
all_start_time = time.perf_counter()

comb_start_time = time.perf_counter()

# Generate all combinations of 5 cards from the sorted deck
card_combinations = list(itertools.combinations(deck, 5))

comb_end_time = time.perf_counter()
comb_elapsed = comb_end_time - comb_start_time
print(f"Time elapsed: {comb_elapsed} seconds")

# Print the total number of combinations
print("Total combinations:", len(card_combinations))

# Print the first 10 combinations
print("First 10 combinations:", card_combinations[:10])


def collectRank(x):
    result = assesor.rank(x)
    return result[0]
def collectTie(x):
    result = assesor.rank(x)
    return result[1]

join_start_time = time.perf_counter()

df = pd.DataFrame([' '.join(i) for i in card_combinations],columns=["hand"])
print(df)


join_end_time = time.perf_counter()
join_elapsed = join_end_time - join_start_time
print(f"Time elapsed: {join_elapsed} seconds")

cards = df

rank_start_time = time.perf_counter()

cards["rank"] = cards["hand"].apply(collectRank)
print("Ranks done")
cards["tie"] = cards["hand"].apply(collectTie)
print("Ties done in")
print(cards[:20])

cards.to_csv("cards.csv")


rank_end_time = time.perf_counter()
rank_elapsed = rank_end_time - rank_start_time
print(f"Time elapsed: {rank_elapsed} seconds")


end_time = time.perf_counter()

# Calculate the time taken to execute the function
time_elapsed = end_time - all_start_time


print(f"Total Time elapsed: {time_elapsed} seconds")

'''
ranksHand = []
combo = 0
for i in card_combinations:
    combo += 1
    print(combo)
    ranksHand.append((i,assesor.rank(' '.join(i))))
    if combo == 50:
        break

print(ranksHand[:10])
'''
