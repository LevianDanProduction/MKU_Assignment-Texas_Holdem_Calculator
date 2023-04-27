
from sys import exit
import os 
import random
import time
import math 
from functools import partial
import numpy as np
import rank_compare
import itertools
import mathymath

class Card():
    suits = ["hearts", "diamonds", "clubs", "spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self,properties,parent):
        self.suit = properties[-1]
        self.value = properties[:-1]
        self.cardval = properties
        self.parentchange(parent)
        #print(f" {self.value} {self.suit} Card:  {self.cardval} ")
                  
    def parentchange(self,newparent):
        self.parent = newparent
        self.place = newparent.cards
        



class Deck():
    deck = ['2♥', '2♦', '2♣', '2♠', '3♥', '3♦', '3♣', '3♠',
        '4♥', '4♦', '4♣', '4♠', '5♥', '5♦', '5♣', '5♠',
        '6♥', '6♦', '6♣', '6♠', '7♥', '7♦', '7♣', '7♠',
        '8♥', '8♦', '8♣', '8♠', '9♥', '9♦', '9♣', '9♠',
        '10♥', '10♦', '10♣', '10♠', 'j♥', 'j♦', 'j♣', 'j♠',
        'q♥', 'q♦', 'q♣', 'q♠', 'k♥', 'k♦', 'k♣', 'k♠',
        'a♥', 'a♦', 'a♣', 'a♠']

    def __init__(self):
        self.name = "deck"
        self.cards = []

    def shuffle(self):
        #self.temp list(zip(self.deck))
        random.shuffle(self.cards)
        #print(self.cards)

    def deckGen(self):
        for i in Deck.deck:
            self.cards.append(Card(i,self))
        self.shuffle()

    
    def getCardPlace(self,card):
        return self.cards.index(card)
    
    def getCardPlace2(self,card):
        index = [i for i, cardv in enumerate(self.cards) if cardv.cardval == card]
        return index[0]


    def drawCard(self,location):
        self.move(self.cards[-1],location)

    def move(self,card,location):
        if self.cards.count(card) > 0:
            card.parentchange(location)
            #print(location.name)
            #Physically changing the cards location
            if location == self:
                self.cards.append(card)
            else:
                location.cards.append(card)
                #print("moved")
            self.cards.remove(card)
            #print(location.cards[0].suit)
            
# p =    [a,b] = *p,  
class Hand():
    Hands = 0
    def __init__(self):
        self.name = "hand"
        self.cards = []
        Hand.Hands += 1

    
    def move(self,card,location):
        if self.cards.count(card) > 0:
            card.parentchange(location)
            #print(location.name)
            #Physically changing the cards location
            if location == self:
                self.cards.append(card)
            else:
                location.cards.append(card)
                #print("moved")
            self.cards.remove(card)
            #print(location.cards[0].suit)
        else:
            #print(f"The selected card to move is not in {self.name}")
            pass
    
    def getCardPlace(self,card):
        return self.cards.index(card)
    def getCardPlace2(self,card):
        index = [i for i, cardv in enumerate(self.cards) if cardv.cardval == card]
        return index[0]


class EHand(Hand):
    def init(self):
        super(Hand,self).__init__(self)


class Community():
    def __init__(self):
        self.name = "community"
        self.cards = []

    def getCardPlace(self,card):
        return self.cards.index(card)
    def getCardPlace2(self,card):
        index = [i for i, cardv in enumerate(self.cards) if cardv.cardval == card]
        return index[0]

    def move(self,card,location):
        if self.cards.count(card) > 0:
            card.parentchange(location)
            #print(location.name)
            #Physically changing the cards location
            if location == self:
                self.cards.append(card)
            else:
                location.cards.append(card)
                #print("moved")
            self.cards.remove(card)
            #print(location.cards[0].suit)
        else:
            #print(f"The selected card to move is not in {self.name}")
            pass

    



class Game():

    def __init__(self):
        self.name = "game"

        self.state = ""
        self.players = 1
        self.part = "Poker"
        self.phase = 0
        self.groups = None
        self.playerHand = None
        self.communityHand = None
        self.handsToUse = []
        self.allStrength = []
        self.rev = 0
        self.processes = False
        self.points = True
        self.evalstats = 0
        self.indexer = {"royal-flush":0,"straight-flush":1, "four-of-a-kind":2, "full-house":3,
                  "flush":4, "straight":5, "three-of-a-kind":6,
                  "two-pair":7, "one-pair":8, "high-card":9}
        self.indexed = {v: k for k, v in self.indexer.items()}
        

    def draw(self,playerhand,otherhands,deck,community):
        self.name = "game"
        deck.drawCard(playerhand)
        deck.drawCard(playerhand)
        for i in otherhands:
            deck.drawCard(i)
            deck.drawCard(i)
        for i in range(5):
            deck.drawCard(community)

    def grabPlayerHand(self):
        self.playerHand = []
        for i in self.groups[0].cards:
            self.playerHand.append((i.suit,i.value))
            #print(i.suit,i.value)
    def grabCommunityHand(self):
        self.communityHand = []
        for i in self.groups[3].cards:
            self.communityHand.append((i.suit,i.value))

    def grabEvaluation(self):
        communityHand = []
        
        for i in self.groups[3].cards:
            communityHand.append(i.cardval)
        playerHand = []
        for i in self.groups[0].cards:
            playerHand.append(i.cardval)
        enemyHands = []
        for j in self.groups[1]:
            temp = []
            for i in j.cards:
                temp.append(i.cardval)
            enemyHands.append(temp+communityHand[:self.rev])
        
        
        playerOptions = playerHand + communityHand[:self.rev]

        #print("mkivmkvkmvs   dfvsv ",playerOptions)
        #print(enemyHands)
        #print(communityHand[:self.rev])
        enemyOptions = []
        self.handsToUse = []
        #for i in enemyHands:
        #    enemyOptions.append(list(i+communityHand))

        options = rank_compare.gameComp(playerOptions)
        #print(options)
        if self.points:
            strongest = rank_compare.strongestHand3(options,hand_to_row)
            #("Sgrog ", strongest)
            for i in strongest:
                self.handsToUse.append([i[0].split(" "),i[1],i[2]])
        else:
            strongest = rank_compare.strongestHand(options)
            #print(strongest)
            for i in strongest[1]:
                self.handsToUse.append([options[i],strongest[2][i][1]])
            #self.handsToUse.append([options[pick],strongest[2][pick][1]])


        #print(self.handsToUse)

    def infoRound(self,allplayers,winner=None):
        if winner:
            return 
        points = [0]*10
        evaluated = []
        for i in allplayers:
            points[self.indexer[i[1]]] += 1
        for j,i in enumerate(points):
            evaluated.append([self.indexed[j],i])
        return evaluated, evaluated.sort(key=lambda x: x[1])

    def finalEvaluation(self):
        communityHand = []
        self.allStrength = []
        for i in self.groups[3].cards:
            communityHand.append(i.cardval)
        playerHand = []
        for i in self.groups[0].cards:
            playerHand.append(i.cardval)
        enemyHands = []
        for j in self.groups[1]:
            temp = []
            for i in j.cards:
                temp.append(i.cardval)
            enemyHands.append(temp+communityHand[:self.rev])

        for j,i in enumerate(enemyHands):
            options = rank_compare.gameComp(i)
            if self.points:
                strongest = rank_compare.strongestHand3(options,hand_to_row)
                #("Sgrog ", strongest)
                for i in strongest:
                    self.allStrength.append([i[0].split(" "),i[1],i[2],j])
        appender = self.handsToUse[0]
        appender.append("player")
        self.allStrength.append(appender)
        max_value = max(sub_list[2] for sub_list in self.allStrength)
        max_lists = [sub_list for sub_list in self.allStrength if sub_list[2] == max_value]
        
        if len(max_lists) == 1:
            if not max_lists[0][3] == "player":
                self.groups[1][max_lists[0][3]]
                #print("this dude has won fr")
                #print("you have ben beanten")
                for i in self.allStrength:
                    #]print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
                    #print["NO:",i[3],"Bhand:",i[0],"type:",i[1]]
                    pass
                self.evalstats = ["loss"]
            else:
                #print("Yay: u won fr ")
                for i in self.allStrength:
                    #print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
                    pass
                self.evalstats = ["win"]
        else:
            for i in max_lists:
                if i[3] == "player":
                    self.evalstats = ["draw"]
                    for i in self.allStrength:
                        print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
                    return 
                else:
                    self.evalstats = ["loss"]
        return 
                

    def phaseGame(self):
        if self.phase == 1:
            #print("\n\n\n\n\n\n\n_____________Pre Flop_____________")
            self.part = "Pre Flop"
            self.draw(*self.groups)
            self.grabPlayerHand()
            self.grabCommunityHand()
            self.rev = 0


        if self.phase == 2:
            #print("\n\n\n\n\n\n\n_____________Flop_____________") 
            self.part = "Flop"
            self.rev = 3
            self.grabEvaluation()

        if self.phase == 3:
            #print("\n\n\n\n\n\n\n_____________Turn_____________") 
            self.part = "Turn"
            self.rev = 4
            self.grabEvaluation()

        if self.phase == 4:
            #print("\n\n\n\n\n\n\n_____________River_____________") 
            self.part = "River"
            self.rev = 5
            self.grabEvaluation()

        if self.phase == 5:
            #print("\n\n\n\n\n\n\n_____________Reveal_____________") 
            self.part = "Reveal"
            self.finalEvaluation()

        if self.phase == 6:
            #print("\n\n\n\n\n\n\n_____________End_____________") 
            self.part = "End"
            self.phase = 0
            self.cleanup(*self.groups)



    def cleanup(self,playerhand,otherhands,deck,community):
        for i in reversed(community.cards):
            community.move(i,deck)
        for i in otherhands:
            for j in reversed(i.cards):
                i.move(j,deck)
        for i in reversed(playerhand.cards):
            playerhand.move(i,deck)



        deck.shuffle()
        #print("\n\n\n\n\n\nCleaned") 

    def round(self):
        self.draw(*self.groups)
        self.rev = 5
        self.grabEvaluation()
        self.finalEvaluation()
        self.cleanup(*self.groups)
    
    def round2(self,playerHand=['8♠', 'k♠'],community=['a♠', '8♣', 'a♣', 'a♥','2♥'],phase=1):
        self.injectGameState(playerHand,community,phase)
        self.rev = 5
        self.grabEvaluation()
        self.finalEvaluation()
        self.cleanup(*self.groups)


    def repPlayer(self,playerHand):
        for i in playerHand:
            deck.move(deck.cards[deck.getCardPlace2(i)],mainhand)
        

    def repComm(self,comm,rev):
        for j,i in enumerate(comm):
            deck.move(deck.cards[deck.getCardPlace2(i)],commune)
            if j == rev-1:
                break

    def randomHidden(self,playerhand,otherhands,deck,community,hand=False):
        if hand:
            deck.drawCard(playerhand)
            deck.drawCard(playerhand)
        self.name = "game"
        for i in otherhands:
            deck.drawCard(i)
            deck.drawCard(i)
        while not len(community.cards) == 5:
            deck.drawCard(community)

#this will set the game up in its current phase
    def injectGameState(self,playerHand=['8♠', 'k♠'],community=['a♠', '8♣', 'a♣', 'a♥','2♥'],phase=1): #inject known game cards and randomise the rest using the deck.
        #assuming there are only cards in the deck
        match phase:
            case 0: # know the community but no hands:
                pass
            case 1: # randomise all but the hand
                self.rev = 0
                self.repPlayer(playerHand)
                self.randomHidden(*self.groups)

            case 2: # all but 2 hand and 3 comm
                self.rev = 3 
                self.repPlayer(playerHand)
                self.repComm(community,self.rev)
                self.randomHidden(*self.groups)
            case 3: # all but 2 hand 4 comm
                self.rev = 4
                self.repPlayer(playerHand)
                self.repComm(community,self.rev)
                self.randomHidden(*self.groups)
            case 4: # all but 2 hand 5 comm 
                self.rev = 5
                self.repPlayer(playerHand)
                self.repComm(community,self.rev)
                self.randomHidden(*self.groups)
            case 5:
                return False
            case 6:
                return False
        print(f"mainhand:{[i.cardval for i in mainhand.cards]} community:{[i.cardval for i in commune.cards]}")





deck = Deck()

mainhand = Hand()
deck.deckGen()
game = Game()
temphand = []
commune = Community()
simtimes = 0
global losses
global wins
wins = 0
losses = 0

class Counter:
    wins = 0
    losses = 0
    type = "slow"
    player = None
    community = None
    phase = None
    draws = 0

def loop():
    #print(mainhand.cards)
    #print(commune.cards)
    #print(i for i in temphand)
    for i in range(6):
        game.phase += 1
        game.phaseGame()
        #print(game.phase)
    return game.evalstats

def loop2():
    game.round()
    return game.evalstats

def loop3():
    game.round2(Counter.player,Counter.community,Counter.phase)
    #game.round2()
    return game.evalstats

import ast
def options():
    slo = input("instant or looped: ")
    sims = int(input("how many simulations: "))
    players = int(input("how many opponents: "))
    if input("Do you have a state to load up?") == "Y":
        phase = int(input("what phase?"))
        phand = input("what is your hand: ")    
        comm = input("what is your community:")
        return {"players":players,"simulations":sims,"speed":slo,"inject":True,
                "phase":phase,"hand":ast.literal_eval(phand),"comm":ast.literal_eval(comm),}
    else:
        return {"players":players,"simulations":sims,"speed":slo,"inject":False}

def loadOpt(opt):
    Counter.wins = 0
    Counter.losses = 0
    Counter.draws = 0
    Counter.type = opt["speed"]
    for i in range(opt["players"]):
        temphand.append(EHand())
    return opt["simulations"],opt

def counter(stats):
    print("stats",stats)
    if stats[0] == "win":
        Counter.wins += 1
    elif stats[0] == "loss":
        Counter.losses += 1
    else:
        Counter.draws += 1
    

def simulateGame(index):
    turn = loop()
    counter(turn)
    #print(index)
def simulateGame2(index):
    turn = loop2()
    counter(turn)
    #print(index)
def simulateGame3(index):
    turn = loop3()
    counter(turn)
    #print(index)

def sim(sim=1,players=2,speed="instant",inject=False,phase=1,hand=['8♠', 'k♠'],comm=['a♠', '8♣', 'a♣', 'a♥','2♥']):
    game.phase = 0
    for i in range(players):
        temphand.append(EHand())
    game.groups = (mainhand,temphand,deck,commune)
    Counter.wins = 0
    Counter.losses = 0
    Counter.draws = 0
    rank_start_time = time.perf_counter() 
    if inject:
        Counter.player = hand
        Counter.community = comm
        Counter.phase = phase
        for i in range(sim):
            simulateGame3(i)
    if speed == "instant":
        for i in range(sim):
            simulateGame2(i)
    else:
        for i in range(sim):
            simulateGame(i)

    rank_end_time = time.perf_counter()
    rank_elapsed = rank_end_time - rank_start_time
    print(f"Time elapsed: {rank_elapsed} seconds")
    print(f"Wins: {Counter.wins} Losses: {Counter.losses} ")


if __name__ == '__main__':
    import pickle   
    import pandas as pd

    with open('hand_to_row.pickle', 'rb') as handle:
        hand_to_row = pickle.load(handle)

    print("created pickle")

    simtimes,settings = loadOpt(options())
    game.phase = 0
    game.groups = (mainhand,temphand,deck,commune)

    rank_start_time = time.perf_counter() 
    if settings["inject"]:
        Counter.player = settings["hand"]
        Counter.community = settings['comm']
        Counter.phase = settings["phase"]
        for i in range(simtimes):
            simulateGame3(i)
    if Counter.type == "instant":
        for i in range(simtimes):
            simulateGame2(i)
    else:
        for i in range(simtimes):
            simulateGame(i)
    rank_end_time = time.perf_counter()
    rank_elapsed = rank_end_time - rank_start_time
    print(f"Time elapsed: {rank_elapsed} seconds")
    print(f"Wins: {Counter.wins} Losses: {Counter.losses} Draws: {Counter.draws} ")

    #what is your hand: ['a♣', 'k♣']
    #what is your community:['10♠', 'j♠', 'q♠', 'k♠', 'a♠']
    