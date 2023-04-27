import pandas as pd
import itertools
from collections import Counter
import ast


df = pd.read_csv('cards6.csv')



def card_power(card):
    rank = card[:-1]
    print(card)
    print(rank)
    power_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}

    return power_map[rank]

def card_powers(card):
    card = card.strip()
    rank_value = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
    suit_value = {'♠': 1, '♣': 2, '♦': 3, '♥': 4}
    return (suit_value[card[-1]], rank_value[card[:-1].lower()])

def sort_hand(hand):
    return sorted(hand, key=card_powers)

power_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
suit = {'♥':1 ,'♦':2 ,'♣':3 ,'♠':4}
def power_mapper(power):
    return power_map[str(power)]

def handpower(hand):
    handpower = {"royal-flush":0,"straight-flush":1, "four-of-a-kind":2, "full-house":3,
                  "flush":4, "straight":5, "three-of-a-kind":6,
                  "two-pair":7, "one-pair":8, "high-card":9}
    return handpower[hand[1]]

def toFormat(card):
    suits = {"hearts":"♥", 
             "diamonds":"♦", 
             "clubs":"♣", 
             "spades":"♠"}
    values = {"2":"2", 
              "3":"3", 
              "4":"4", 
              "5":"5", 
              "6":"6", 
              "7":"7", 
              "8":"8", 
              "9":"9", 
              "10":"10", 
              "J":"j", 
              "Q":"q", 
              "K":"k", 
              "A":"a",
              "02":"2", 
              "03":"3", 
              "04":"4", 
              "05":"5", 
              "06":"6", 
              "07":"7", 
              "08":"8", 
              "09":"9", 
              "10":"10",}
    return values[card[0]] + suits[card[1]]

def fromFormatHand(hand):
    suits = {"♥":"hearts", 
             "♦":"diamonds", 
             "♣":"clubs", 
             "♠":"spades"}
    values = {"j":"J", 
              "q":"Q", 
              "k":"K", 
              "a":"A",
              "2":"02", 
              "3":"03", 
              "4":"04", 
              "5":"05", 
              "6":"06", 
              "7":"07", 
              "8":"08", 
              "9":"09", 
              "10":"10",}
    handy =[]
    #print("g: ",hand)
    for i in hand:
        handy.append((suits[i[-1]],values[i[:-1]]))
    return handy

def gameComp(option):
    sort = sorted(option,key=card_powers)
    return list(itertools.combinations(sort, 5))


def compressHand(hand):
    temp = ""
    temp = " ".join(hand)
    return temp.strip()

def strongestHand(hands):
    handnow = hands
    rankerhands = list()
    finalHand = list()
    for j,i in enumerate(handnow):
        
        current = compressHand(sort_hand(i))
        #print(current)
        selected_row = df.loc[df['hand'] == current]
        #print("Search1: ",selected_row)
        row_info = selected_row.iloc[0].to_dict()
        

        #print(row_info)
        handy = row_info["hand"]
        rank = row_info["rank"]
        info = ast.literal_eval(row_info["tie"])
        group = [handy,rank,info,j]
        rankerhands.append(group)
        finalHand.append([handnow,j])
        #print(rankerhands,finalHand)

    #print(rankerhands)
    unorder = rankerhands
    order = sorted(rankerhands,key=handpower)
    #print("order")
    high = order[0][1]
    order2 = [item for item in order if item[1] == high]

    orderbreak = order2.copy()
    biggest = orderbreak[0][2]
    bigaf = orderbreak[0]
    for i in range(len(orderbreak[0][2])-1):
        for j in orderbreak:
            if power_mapper(j[2][i]) > power_mapper(biggest[i]):
                biggest = j[2]
                bigaf = j
                orderbreak = [item for item in orderbreak if item[2][i]==biggest[i]]
                print(len(orderbreak),":order:    ",orderbreak)
    if orderbreak == []:
        orderbreak = [bigaf]
        print("big:    ",biggest)

    print ("best hand is",orderbreak)
    checkhand = [item[3] for item in orderbreak]
    #print(checkhand)
    finalHand = [item for item in finalHand if item[1] in checkhand]
    #print(finalHand)
    return (orderbreak,checkhand,unorder)
            

def strongestHand2(hands):
    handnow = hands
    rankerhands = list()
    finalHand = list()
    for j,i in enumerate(handnow):
        
        current = compressHand(sort_hand(i))
        #print(current)
        selected_row = df.loc[df['hand'] == current]
        #print("Search1: ",selected_row)
        row_info = selected_row.iloc[0].to_dict()
        

        #print(row_info)
        handy = row_info["hand"]
        rank = row_info["rank"]
        tie = row_info["points"]
        info = ast.literal_eval(row_info["tie"])
        group = [handy,rank,info,j,tie]
        rankerhands.append(group)
        finalHand.append([handnow,j])
        #print(rankerhands,finalHand)

    #leader = rankerhands[0]

    #for i in rankerhands:
    #    if i[4] > leader[4]:
    #        leader = i
    max_value = max(sub_list[4] for sub_list in rankerhands)
    max_lists = [sub_list for sub_list in rankerhands if sub_list[4] == max_value]
    print(i)
    return ([[i[0],i[1],i[4]] for i in max_lists])      

def strongestHand3(hands, hand_to_row):
    rankerhands = []

    for j, i in enumerate(hands):
        current = compressHand(sort_hand(i))
        selected_row = hand_to_row[current]
        row_info = selected_row

        handy = row_info["hand"]
        rank = row_info["rank"]
        tie = row_info["points"]
        info = ast.literal_eval(row_info["tie"])
        group = [handy, rank, info, j, tie]
        rankerhands.append(group)

    max_value = float('-inf')
    max_lists = []

    for i in rankerhands:
        if i[4] > max_value:
            max_value = i[4]
            max_lists = [i]
        elif i[4] == max_value:
            max_lists.append(i)

    result = [[i[0], i[1], i[4]] for i in max_lists]
    return result


def compareHands(h1,h2):
    if h1[2]>h2[2]:
        return h1
    else:
        return h2