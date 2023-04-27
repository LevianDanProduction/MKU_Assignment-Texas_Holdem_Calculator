import itertools
import numpy as np 
import pandas as pd 
import assesor
import time
import rank_compare
import pickle
import random
import mathymath as mt

fullDeck = ['2♥', '2♦', '2♣', '2♠', '3♥', '3♦', '3♣', '3♠',
        '4♥', '4♦', '4♣', '4♠', '5♥', '5♦', '5♣', '5♠',
        '6♥', '6♦', '6♣', '6♠', '7♥', '7♦', '7♣', '7♠',
        '8♥', '8♦', '8♣', '8♠', '9♥', '9♦', '9♣', '9♠',
        '10♥', '10♦', '10♣', '10♠', 'j♥', 'j♦', 'j♣', 'j♠',
        'q♥', 'q♦', 'q♣', 'q♠', 'k♥', 'k♦', 'k♣', 'k♠',
        'a♥', 'a♦', 'a♣', 'a♠']

def lowestBest(community,rev):
    if not rev == 5:
        return 20000000
    options = rank_compare.gameComp(community)
    strongest = rank_compare.strongestHand3(options,hand_to_row)
    allStrength = []
    for j,i in enumerate(strongest):
        allStrength.append([i[0].split(" "),i[1],i[2],j])
    return (allStrength[0][2],allStrength[0][1])

def futurehand(handr,commr,rev=0,convert=True):
    gutt = rev
    if gutt == 3:
        left = 2
    if gutt == 4:
        left = 1
    if gutt == 0:
        print("gutter")
        left = 0


    if convert:
        hand = [card.cardvar for card in handr.cards]
        comm = [card.cardvar for j,card in enumerate(commr.cards) if j < 5-left]
        decka = [i for i in fullDeck if not i in opti]
        comm = comm[:5-left]
        opti = hand+comm
    else:
        hand = handr
        comm = commr
        comm = comm[:5-left]
        opti = hand+comm
        decka = [i for i in fullDeck if not i in comm and not i in hand]
        

    print("opt\n\n\n\n\n",opti)
    print("\n\n\n\n\n",hand)
    print("comm\n\n\n\n\n",comm)
    #print("Deck fr")
    #print(decka)
    #print(len(decka))

    card_combinations = list(itertools.combinations(decka,left))
    #print("\n\n\n\n\n tooo \n\n\n\n",card_combinations)

    card_combinations = [list(comb)+opti for comb in card_combinations]
    #print(card_combinations)


    combine = mt.combinations(len(decka),left)
    #print("combine",combine)


    allStrength = []
    for j,i in enumerate(card_combinations):
        options = rank_compare.gameComp(i)
        #print("opti tiop  :",options)
        strongest = rank_compare.strongestHand3(options,hand_to_row)
        #("Sgrog ", strongest)
        i = strongest[0]
        allStrength.append([i[0].split(" "),i[1],i[2],j])
    
    for i in allStrength:
        print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
    
    return (allStrength, combine)

def future_eval(hands,type=2,readeval=1081,lowestbest=(20000000,"high-card")):
    if type == 1:
        count = 0
        count2 = 0
        count3 = 0
        for i in hands:
            if i[2] >= 50000000:
                count += 1
        for i in hands:
            if i[2] >= 70000000:
                count2 += 1
        for i in hands:
            if i[2] < 50000000:
                count3 += 1

        print(f"there are {count}  rare cards")
        print(f"there are {count2}  amazing cards")
        print(f"there are {count3}  booty cards")
        print(f"so there is a {(count/1081)*100}% chance of having a strong")
        print(f"so there is a {(count2/1081)*100}% chance of having a godly hand")
        print(f"so there is a {(count3/1081)*100}% chance of having a low level/basic level hand")
    if type == 2:
        indexer = {"royal-flush":0,"straight-flush":1, "four-of-a-kind":2, "full-house":3,
                  "flush":4, "straight":5, "three-of-a-kind":6,
                  "two-pair":7, "one-pair":8, "high-card":9}
        indexed = {v: k for k, v in indexer.items()}
        points = [0]*10
        for i in hands:
            points[indexer[i[1]]] += 1
        total = 0
        total2 = 0
        total3 = 0
        print(points)
        
        for j,i in enumerate(points):
            
            if j == 0:
                print("\n♛ Best Hands ♛")
            elif j == 6:
                print(f"     ♛ Total Chance for Best Hand is {100*total2/readeval}% ")
                total2 = 0
                print("\n♜ Solid Hands ♜")
            elif j == 8:
                print(f"     ♜ Total Chance for Solid Hand is {100*total2/readeval}% ")
                total2 = 0
                print("\n♟ Regular Hands ♟")
                
            print(f"- {indexed[j]}  was {i} out of {readeval} | This is a {100*(i/readeval)}% chance")
            total += i
            total2 += i
            if j == 9:
                print(f"     ♟ Total Chance for Regular Hand is {100*total2/readeval}% ")
                

                       

        print(f"total is {total} ")
        count = 0
        for i in hands:
            if i[2] >= round(lowestbest[0],-7)+10000000:
                count += 1
        print(f"  ▨   Minimum standard rank is {lowestbest[1]} ")
        print(f"  ▨   Total Chance for A Low Probability Hand (<=2%) is {100*(total-total2)/readeval}% ")
        print(f"  ▨   Total Chance for A Above Community Hand is {100*(count)/readeval}% ")
        total2 = 0
        


def handToOthers():
    pass



if __name__ == '__main__':
    with open('hand_to_row2.pickle', 'rb') as handle:
        hand_to_row = pickle.load(handle)

    """"
    deck = ['2♥', '2♦', '2♣', '2♠', '3♥', '3♦', '3♣', '3♠',
            '4♥', '4♦', '4♣', '4♠', '5♥', '5♦', '5♣', '5♠',
            '6♥', '6♦', '6♣', '6♠', '7♥', '7♦', '7♣', '7♠',
            '8♥', '8♦', '8♣', '8♠', '9♥', '9♦', '9♣', '9♠',
            '10♥', '10♦', '10♣', '10♠', 'j♥', 'j♦', 'j♣', 'j♠',
            'q♥', 'q♦', 'q♣', 'q♠', 'k♥', 'k♦', 'k♣', 'k♠',
            'a♥', 'a♦', 'a♣', 'a♠']
    hand = []
    for i in range(5):
        hand.append(deck.pop(np.random.randint(0,len(deck)-1)))

    card_combinations = list(itertools.combinations(deck, 2))
    print(card_combinations[:20])
    print(len(card_combinations))
    card_combinations = [list(comb)+hand for comb in card_combinations]
    print("donzo")
    print(card_combinations[:20])

    allStrength = []
    for j,i in enumerate(card_combinations):
        options = rank_compare.gameComp(i)
        strongest = rank_compare.strongestHand3(options,hand_to_row)
        #("Sgrog ", strongest)
        for i in strongest:
            allStrength.append([i[0].split(" "),i[1],i[2],j])

    for i in allStrength:
        print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")

    count = 0
    count2 = 0
    count3 = 0
    for i in allStrength:
        if i[2] >= 50000000:
            count += 1
    for i in allStrength:
        if i[2] >= 70000000:
            count2 += 1
    for i in allStrength:
        if i[2] < 50000000:
            count3 += 1

    print(f"there are {count}  rare cards")
    print(f"there are {count2}  amazing cards")
    print(f"there are {count3}  booty cards")
    print(f"so there is a {(count/1081)*100}% chance of having a strong")
    print(f"so there is a {(count2/1081)*100}% chance of having a godly hand")
    print(f"so there is a {(count3/1081)*100}% chance of having a low level/basic level hand")
    """

    #future_eval(allStrength)

    deck1 = ['2♥', '2♦', '2♣', '2♠', '3♥', '3♦', '3♣', '3♠',
            '4♥', '4♦', '4♣', '4♠', '5♥', '5♦', '5♣', '5♠',
            '6♥', '6♦', '6♣', '6♠', '7♥', '7♦', '7♣', '7♠',
            '8♥', '8♦', '8♣', '8♠', '9♥', '9♦', '9♣', '9♠',
            '10♥', '10♦', '10♣', '10♠', 'j♥', 'j♦', 'j♣', 'j♠',
            'q♥', 'q♦', 'q♣', 'q♠', 'k♥', 'k♦', 'k♣', 'k♠',
            'a♥', 'a♦', 'a♣', 'a♠']
    hand1 = []
    for i in range(5):
        hand1.append(deck1.pop(np.random.randint(0,len(deck1)-1)))
    hand2 = []
    for i in range(2):
        hand2.append(deck1.pop(np.random.randint(0,len(deck1)-1)))


    #hand2,hand1 = ['a♣', 'k♣'],['10♠', 'j♠', 'q♠', 'k♠', 'a♠']

    low = lowestBest(hand1,5)
    handscan = futurehand(hand2,hand1,rev=3,convert=False)
    future_eval(handscan[0],readeval=handscan[1],lowestbest=low)

    handscan = futurehand(hand2,hand1,rev=4,convert=False)
    future_eval(handscan[0],readeval=handscan[1],lowestbest=low)

    
    print("community: ",hand1)
    print("hand: ",hand2)
    print(low)