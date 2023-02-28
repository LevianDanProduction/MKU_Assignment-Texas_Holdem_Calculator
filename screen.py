import pygame
from pygame.locals import *
from sys import exit
import os 
import random

size = 240
width = 960
height = 600
print (os.listdir())
pygame.init()
screen = pygame.display.set_mode((width,height),RESIZABLE)
clock = pygame.time.Clock()

class Screen():
    def __init__(self):
        self.background = pygame.image.load("images/other/bg4.png").convert_alpha()
        self.bg = pygame.image.load("images/other/bg01.png").convert_alpha()
        

class imgEngine():
    def __init__(self):
        self.cardImg = ["card",
           ["hearts","diamonds","clubs","spades"],
           ["A","02","03","04","05","06","07","08","09","10","J","Q","K"]]
        self.deckGen = []
        self.otherGen = ["card_back","card_empty"]
        self.imgDir = "images/Cards (large)/"
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
    def __init__(self,properties,frontimg,spawnorder=0):
        pygame.sprite.Sprite.__init__(self)
        self.suit = properties[0]
        self.type = properties[1]
        self.frontimg =  pygame.image.load(frontimg).convert()
        self.x = 32 + 64*(spawnorder % 8)
        self.y = 32 + 64*(spawnorder // 8)

    def update(self):
        screen.blit(self.frontimg,(self.x,self.y))


class Deck():

    def __init__(self):
        self.sprites = imgEngine()
        self.spriteSheet1 = self.sprites.deckGen
        self.spriteProp1 = self.sprites.cardGen
        self.deck = []
    
    def shuffle(self):
        self.deck = random.shuffle(self.deck)

    def deckGen(self):
        for i in range(0,52):
            self.deck.append(Card(self.spriteProp1[i],self.spriteSheet1[i],i))
        deck.shuffle()

class Hand():
    def __init__(self):
        self.cards = []
    
    def drawToHand(self,deck):
        


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
        
        for i in deck.deck:
            i.update()



        pygame.display.update()
        clock.tick(60)