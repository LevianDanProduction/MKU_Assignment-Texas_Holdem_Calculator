import pygame
from pygame.locals import *
from sys import exit
import os 
import random
import time

size = 240
width = 960
height = 640
print (os.listdir())
pygame.init()
screen = pygame.display.set_mode((width,height),RESIZABLE)
clock = pygame.time.Clock()

class Screen():
    def __init__(self):
        self.background = pygame.image.load("images/other/bg5.png").convert_alpha()
        self.bg = pygame.image.load("images/other/bg5.png").convert_alpha()
        

class imgEngine():
    def __init__(self):
        self.cardImg = ["card",
           ["hearts","diamonds","clubs","spades"],
           ["A","02","03","04","05","06","07","08","09","10","J","Q","K"]]
        self.deckGen = []
        self.imgDir = "images/Cards (large)/"
        self.otherGen = [(self.imgDir+"card_back.png"),(self.imgDir+"card_empty.png")]
        self.cardGen =[]
        self.deckImgGen()
    
    def deckImgGen(self):
        for i in self.cardImg[1]:
            for j in self.cardImg[2]:
                item = self.imgDir + self.cardImg[0] + "_" + i + "_" + j + ".png"
                item2 = (i,j)
                self.deckGen.append(item)
                self.cardGen.append(item2)
        return (self.deckGen,self.cardGen)

class Card(pygame.sprite.Sprite):
    def __init__(self,properties,frontimg,otherimg,parent,spawnorder=0,place=None):
        pygame.sprite.Sprite.__init__(self)
        self.suit = properties[0]
        self.type = properties[1]
        self.frontimg =  pygame.image.load(frontimg).convert()
        self.backimg = pygame.image.load(otherimg[0])
        self.spawn = spawnorder
        self.place = place
        self.parent = parent
        self.order = 0
        self.display = None
        self.position(self.parent.name)

    def position(self,state):
        if state == "deck":
            self.x = self.parent.x - self.order*0.1
            self.y = self.parent.y - self.order*0.1
            self.display = self.backimg
        else:
            self.display = self.frontimg
            self.x = 32 + 64*(self.spawn % 8)
            self.y = 32 + 64*(self.spawn // 8)

    def update(self):
        if self.parent.name == "deck":
            self.order = self.parent.getCardPlace(self)

        self.position(self.parent.name)
        self.spawn = self.place.index(self)
        screen.blit(self.display,(self.x,self.y))


class Deck():

    def __init__(self):
        self.name = "deck"
        self.sprites = imgEngine()
        self.others = self.sprites.otherGen
        self.spriteSheet1 = self.sprites.deckGen
        self.spriteProp1 = self.sprites.cardGen
        self.cards = []
        self.deckimg = pygame.image.load(self.others[1]).convert()
        self.x = 0
        self.placement()    

    def shuffle(self):
        #self.temp list(zip(self.deck))
        random.shuffle(self.cards)
        print(self.cards)

    def deckGen(self):
        for i in range(0,52):
            self.cards.append(Card(self.spriteProp1[i],self.spriteSheet1[i],self.others,self,i,self.cards))
        self.shuffle()

    def placement(self):
        self.x = 645
        self.y = 20
    
    def getCardPlace(self,card):
        return self.cards.index(card)

    def update(self):
        screen.blit(self.deckimg,(self.x,self.y))

    def drawCard(self,location):
        self.move(self.cards.pop(),location)

    def move(self,card,location):
        if self.cards.count(card) > 0:
            if location == self:
                self.cards.append(card)
            else:
                location.cards.append(card)
            self.cards.remove(card)

class Hand():
    def __init__(self):
        self.name = "hand"
        self.cards = []
    
    def move(self,card,location):
        if self.cards.count(card) > 0:
            if location == self:
                self.cards.append(card)
            else:
                location.cards.append(card)
            self.cards.remove(card)
        else:
            print(f"The selected card to move is not in {self.name}")


class EHand(Hand):
    pass
    
deck = Deck()
window = Screen()
deck.deckGen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        #game code
        screen.blit(window.background,(0,0))
        deck.update()
        for i in deck.cards:
            i.update()
        #print(pygame.mouse.get_pos())




        pygame.display.update()
        clock.tick(60)