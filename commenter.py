import rank_compare
hand_to_row = 0

# Function to find the strongest hand among multiple hands using a hand_to_row dictionary
def strongestHand3(hands, hand_to_row):
    rankerhands = []

    for j, i in enumerate(hands):
        # Compress and sort the current hand
        current = compressHand(sort_hand(i))

        # Find the corresponding row using the hand_to_row dictionary for the current hand
        selected_row = hand_to_row[current]
        row_info = selected_row

        # Extract hand-related information from the row dictionary
        handy = row_info["hand"]
        rank = row_info["rank"]
        tie = row_info["points"]
        info = ast.literal_eval(row_info["tie"])
        group = [handy, rank, info, j, tie]
        rankerhands.append(group)

    # Find the strongest hand(s) based on the maximum points value
    max_value = float('-inf')
    max_lists = []

    for i in rankerhands:
        if i[4] > max_value:
            max_value = i[4]
            max_lists = [i]
        elif i[4] == max_value:
            max_lists.append(i)

    # Return the result as a list containing hand, rank, and points
    result = [[i[0], i[1], i[4]] for i in max_lists]
    return result

def compressHand():
    pass

def ast():
    pass

def sort_hand():
    pass

def finalEvaluation(self):
    # Create an empty list for the community hand
    communityHand = []
    self.allStrength = []

    # Convert cards in the community hand to the appropriate format
    for i in self.groups[3].cards:
        communityHand.append(rank_compare.toFormat((i.value, i.suit)))

    # Create an empty list for the player's hand and convert the cards to the appropriate format
    playerHand = []
    for i in self.groups[0].cards:
        playerHand.append(rank_compare.toFormat((i.value, i.suit)))

    # Create a list of enemy hands, converting the cards to the appropriate format
    enemyHands = []
    for j in self.groups[1]:
        temp = []
        for i in j.cards:
            temp.append(rank_compare.toFormat((i.value, i.suit)))
        enemyHands.append(temp + communityHand[:self.rev])

    # Calculate the strength of each enemy hand
    for j, i in enumerate(enemyHands):
        options = rank_compare.gameComp(i)
        if self.points:
            strongest = rank_compare.strongestHand3(options, hand_to_row)
            for i in strongest:
                self.allStrength.append([i[0].split(" "), i[1], i[2], j])

    # Add the player's hand to the list of hands to evaluate
    appender = self.handsToUse[0]
    appender.append("player")
    self.allStrength.append(appender)

    # Find the hand(s) with the highest score
    max_value = max(sub_list[2] for sub_list in self.allStrength)
    max_lists = [sub_list for sub_list in self.allStrength if sub_list[2] == max_value]

    # Determine the winner and print the results
    if len(max_lists) == 1:
        if not max_lists[0][3] == "player":
            self.groups[1][max_lists[0][3]]
            print("you have been beaten")
            for i in self.allStrength:
                print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
            return self.groups[1][max_lists[0][3]]
        else:
            print("Yay: you won")
            for i in self.allStrength:
                print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
            return self.groups[0]
    else:
        for i in max_lists:
            if i[3] == "player":
                print("It's a draw")
                for i in self.allStrength:
                    print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
                return
            else:
                print("you have been beaten")
                print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
    return

import itertools
import pandas as mt
fullDeck = 0

def futurehand(handr, commr, rev=0):
    # Determine the number of cards left to be drawn
    gutt = rev
    if gutt == 3:
        left = 2
    if gutt == 4:
        left = 1
    if gutt == 0:
        print("gutter")
        left = 0
    hand = handr
    comm = commr
    comm = comm[:5 - left]
    opti = hand + comm
    decka = [i for i in fullDeck if not i in comm and not i in hand]

    # Generate all possible card combinations for the remaining cards to be drawn
    card_combinations = list(itertools.combinations(decka, left))

    # Combine the current hand and community cards with the possible combinations
    card_combinations = [list(comb) + opti for comb in card_combinations]

    # Calculate the total number of possible combinations
    combine = mt.combinations(len(decka), left)

    # Calculate the strength of each card combination
    allStrength = []
    for j, i in enumerate(card_combinations):
        options = rank_compare.gameComp(i)
        strongest = rank_compare.strongestHand3(options, hand_to_row)
        i = strongest[0]
        allStrength.append([i[0].split(" "), i[1], i[2], j])

    # Print the strengths of all card combinations
    for i in allStrength:
        print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")

    # Return the list of strengths and the total number of possible combinations
    return (allStrength, combine)


def sim(sim=1, players=2, speed="instant", inject=False, phase=1, hand=['8♠', 'k♠'], comm=['a♠', '8♣', 'a♣', 'a♥', '2♥']):
    # Set the game phase to 0
    game.phase = 0
    
    # Initialize empty hands for each player
    for i in range(players):
        temphand.append(EHand())

    # Set up the game groups (main hand, enemy hands, deck, and community cards)
    game.groups = (mainhand, temphand, deck, commune)

    # Initialize win, loss, and draw counters
    Counter.wins = 0
    Counter.losses = 0
    Counter.draws = 0

    # Start a timer to measure the simulation time
    rank_start_time = time.perf_counter()

    # If the 'inject' option is enabled, set up the game with the provided hand, community cards, and phase
    if inject:
        Counter.player = hand
        Counter.community = comm
        Counter.phase = phase
        for i in range(sim):
            simulateGame3(i)
    
    # Run the simulation with the specified speed
    if speed == "instant":
        for i in range(sim):
            simulateGame2(i)
    else:
        for i in range(sim):
            simulateGame(i)

    # Calculate and print the time elapsed during the simulation
    rank_end_time = time.perf_counter()
    rank_elapsed = rank_end_time - rank_start_time
    print(f"Time elapsed: {rank_elapsed} seconds")

    # Print the number of wins and losses
    print(f"Wins: {Counter.wins} Losses: {Counter.losses}")
