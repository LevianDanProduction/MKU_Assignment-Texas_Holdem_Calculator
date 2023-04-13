import pygame
from pygame.locals import *
from sys import exit
import os 
import random
import time
import math 
from functools import partial
from pygame.math import Vector2
import numpy as np


size = 240
width = 960
height = 640
fps = 60
print (os.listdir())
pygame.init()
pygame.mixer.init

screen = pygame.display.set_mode((width,height),RESIZABLE)
clock = pygame.time.Clock()

class Screen():
    def __init__(self):
        self.background = pygame.image.load("images/other/bg06.jpg").convert_alpha()
        self.background2 = pygame.image.load("images/other/bg5.png").convert_alpha()
        self.bg = pygame.image.load("images/other/bg5.png").convert_alpha()
        
class ImgEngine():
    def __init__(self):
        self.cardImg = ["card",
           ["hearts","diamonds","clubs","spades"],
           ["A","02","03","04","05","06","07","08","09","10","J","Q","K"]]
        self.deckGen = []
        self.imgDir = "images/Cards (large)/"
        self.pregame = "images/other/pre game.png"
        self.otherGen = [(self.imgDir+"card_back.png"),(self.imgDir+"card_empty.png")]
        self.cardGen =[]
        self.deckImgGen()
        self.pot = "images/other/pot.png"
        self.title = "images/other/title.png"
        self.textFont_s = pygame.font.Font("images/font/pio.otf",24)
        self.textFont_m = pygame.font.Font("images/font/pio.otf",36)
        self.images = []
        self.imgGen()
    
    def deckImgGen(self):
        for i in self.cardImg[1]:
            for j in self.cardImg[2]:
                item = self.imgDir + self.cardImg[0] + "_" + i + "_" + j + ".png"
                item2 = (i,j)
                self.deckGen.append(item)
                self.cardGen.append(item2)
        return (self.deckGen,self.cardGen)
    
    def imgGen(self):
        for file in os.listdir("images/ui"):
            if file.endswith(".jpg") or file.endswith(".png"):
                self.images.append((file[:-4],pygame.image.load("images/ui/" + file)))
    
    def getImg(self,img):
        for i in self.images:
            if img == i[0]:
                return i[1].convert_alpha()

    
class MusicEngine():
    def __init__(self):
        self.music = []
        self.sound = []
        self.soundDir = "sound/"
        self.musicDir = "sound/music"
        self.otherext = ".mp3"
        self.soundGen()
        self.currentMusic = None
    
    def soundGen(self):
        for file in os.listdir(self.musicDir):
            self.music.append(os.path.join(self.musicDir, file))
        
        for file in os.listdir(self.soundDir):
            if file.endswith(".mp3") or file.endswith(".wav"):
                self.sound.append((file[:-4],pygame.mixer.Sound(self.soundDir + file)))

    
    def musicPlay(self,music,loop=0):
        for i in self.music:
            print(i[12:-4])
            if i[12:-4] == music:
                self.currentMusic = i
                pygame.mixer.music.load(i)
                pygame.mixer.music.play(loops=loop)

    def musicStop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload(self.currentMusic)

    def soundPlay(self,music):
        for i in self.sound:
            if music == i[0]:
                i[1].play()
                print("soundplayed")

class Card(pygame.sprite.Sprite):
    suits = ["hearts", "diamonds", "clubs", "spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self,properties,frontimg,otherimg,parent,spawnorder=0,place=None):
        pygame.sprite.Sprite.__init__(self)
        self.suit = properties[0]
        self.value = properties[1]
        self.frontimg =  pygame.image.load(frontimg).convert()
        self.backimg = pygame.image.load(otherimg[0]).convert()
        self.spawn = spawnorder
        self.parentchange(parent)
        self.order = 0
        self.display = self.backimg
        self.x = self.parent.x
        self.y = self.parent.y
        self.tx = 0
        self.ty = 0
        self.positionSet(self.parent.name)
        self.x = self.tx
        self.y = self.ty
        self.focus = [False,"hide"]
        self.pos = Vector2((self.x,self.y))
        self.rect = self.display.get_rect(center = (self.x,self.y))
        self.target = (self.tx,self.ty)
        self.change = (self.x,self.y)
        # positions
        self.changevect = Vector2(self.change)
        self.targetvect = Vector2(self.target) 
        self.direction = self.changevect - self.targetvect
        self.speed = 8 # changing this changes the direction the sprite moves
        self.moving = False
        self.hover =[0,0]
        
        self.rect.center = (round(self.tx), round(self.ty))

    def targetSet(self):
        self.target = (self.tx,self.ty)
        self.targetvect = Vector2(self.target) 
        self.direction = self.changevect - self.targetvect

    def positionSet(self,state,order=0):

        if state == "deck":
            self.tx = self.parent.x - order*0.1
            self.ty = self.parent.y - order*0.1
            self.target =[self.tx,self.ty]

        elif state == "hand":
            #print(self.parent.x,self.parent.y)
            print(self.order)
            self.tx = (self.parent.x -32) + order*32 
            self.ty = (self.parent.y-64)
        elif state == "community":
            #print(self.parent.x,self.parent.y)
            print(self.order)
            self.tx = (self.parent.x) + order*64 
            self.ty = (self.parent.y)

        try:
            self.targetSet()
        except:
            print("init stare")
        


    def position(self,state,order=0):
        if state == "deck":
            self.x = self.parent.x - order*0.8
            self.y = self.parent.y - order*0.8

        elif state == "hand":
            #print(self.parent.x,self.parent.y)
            self.x = ((self.parent.x -32) + order*32 ) + 16
            self.y = (self.parent.y-64) 
            self.hoverCheck()
        elif state == "community":
            self.x = (self.parent.x) + order*42 
            self.y = (self.parent.y)
        else:
            self.x = 480
            self.y = 320
        try:
            self.targetSet()
        except:
            print("init stare")
        
        
        self.rect.center = (round(self.x), round(self.y))
    
    def handCheck(self):
        if self.focus[0] == True:
            if self.focus[1] == "hide":
                self.display = self.backimg
                return
            elif self.focus[1] == "show":
                self.display = self.frontimg
                return     
                  
        if self.parent.handState == "hide":
            self.display = self.backimg
            return
        elif self.parent.handState == "show":
            self.display = self.frontimg
            return
    def handFlip(self,active=False,state="hide"):
        self.focus[0] = active
        self.focus[1] = state

    def hoverCheck(self):
        mouse = pygame.mouse.get_pos()
        temprect = pygame.Rect(self.rect.centerx,self.rect.centery,self.display.get_width(),self.display.get_height())
        if temprect.collidepoint(mouse):
            self.hover = [0,-7]
        else:
            self.hover = [0,0]
    def update(self):

        self.spawn = self.place.index(self)

        #if self.moving:
        #    self.pos += self.direction.normalize() * self.speed 
        #    self.rect.center = (round(self.pos.x), round(self.pos.y))
        #else:
        #    self.position(self.parent.name)
            #print("idle")
        
        if self.moving:
            self.target = (self.tx,self.ty)
            self.targetvect = Vector2(self.target) 
            self.direction = self.changevect - self.targetvect

            self.pos -= self.direction.normalize() * self.speed 
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            self.change = (self.rect.center[0],self.rect.center[1])
            self.changevect = Vector2((self.rect.center[0],self.rect.center[1]))
            if (self.rect.center[0] + self.speed) > self.target[0]:
                if (self.rect.center[1] + self.speed) > self.target[1]:
                    self.moving = False
        else:
            self.position(self.parent.name,order=self.parent.getCardPlace(self))
        self.handCheck()
        #print(self.rect.center)
        screen.blit(self.display,(self.rect.center[0]+self.hover[0],self.rect.center[1]+self.hover[1]))
        

    def parentchange(self,newparent):
        self.parent = newparent
        self.place = newparent.cards
        
    def cardMove(self,newparent):
        self.moving = True
        self.positionSet(newparent.name,order=self.parent.getCardPlace(self))
        print("moving 1")




class Deck(pygame.sprite.Sprite):

    def __init__(self,images,sound):
        pygame.sprite.Sprite.__init__(self)
        self.name = "deck"
        self.sprites = images
        self.sound = sound
        self.others = self.sprites.otherGen
        self.spriteSheet1 = self.sprites.deckGen
        self.spriteProp1 = self.sprites.cardGen
        self.cards = []
        self.handState = "hide"
        self.deckimg = pygame.image.load(self.others[1]).convert()
        self.x = 0
        self.y = 0
        self.placement()    

    def shuffle(self):
        #self.temp list(zip(self.deck))
        random.shuffle(self.cards)
        print(self.cards)

    def deckGen(self):
        for i in range(0,52):
            self.cards.append(Card(self.spriteProp1[i],self.spriteSheet1[i],self.others,self,i))
        self.shuffle()
        self.sound.soundPlay("cardDraw"+str(np.random.randint(1,5)))

    def placement(self):
        self.x = 645
        self.y = 20
    
    def getCardPlace(self,card):
        return self.cards.index(card)

    def update(self):
        screen.blit(self.deckimg,(self.x,self.y))

    def drawCard(self,location):
        self.sound.soundPlay("cardDraw"+str(np.random.randint(1,5)))
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
                print("moved")
            self.cards.remove(card)
            card.cardMove(location)
            print(location.cards[0].suit)
            
# p =    [a,b] = *p,  
class Hand(pygame.sprite.Sprite):
    Hands = 0
    rad = 2*math.pi
    radius = math.sqrt(48000)
    centre = (320,310)
    

    def __init__(self,images,sound,handstate=None):
        self.sprites = images
        self.sound = sound
        self.potimg = pygame.image.load(images.pot).convert_alpha()
        self.name = "hand"
        self.cards = []
        self.position = Hand.Hands
        self.handState = handstate
        Hand.Hands += 1
        self.placement()

    
    def move(self,card,location):
        if self.cards.count(card) > 0:
            card.parentchange(location)
            #print(location.name)
            #Physically changing the cards location
            if location == self:
                self.cards.append(card)
            else:
                location.cards.append(card)
                print("moved")
            self.cards.remove(card)
            card.cardMove(location)
            print(location.cards[0].suit)
        else:
            print(f"The selected card to move is not in {self.name}")

    def placement(self):
        self.x = Hand.centre[0]+ Hand.radius * math.sin(Hand.rad*(self.position/Hand.Hands))
        self.y = Hand.centre[1]+ Hand.radius * math.cos(Hand.rad*(self.position/Hand.Hands))
        #print(self.x,self.y)
        
    
    def getCardPlace(self,card):
        return self.cards.index(card)

    def update(self):
        self.placement()
        screen.blit(self.potimg,(self.x,self.y))
    


class EHand(Hand,pygame.sprite.Sprite):
    def init(self,images,):
        super(Hand,self).__init__(self,images,"hide")
        super(pygame.sprite.Sprite,self).__init__(self)
        Hands += 1

class Community():
    def __init__(self,images,sound):
        self.sprites = images
        self.sound = sound
        self.name = "community"
        self.cards = []
        self.handState = "hide"
        self.placement()

    def placement(self):
        self.x = 240
        self.y = 280

    def getCardPlace(self,card):
        return self.cards.index(card)
    
    def flipCards(self,cardrange):
        for i in self.cards[cardrange[0]:cardrange[1]]:
            i.handFlip(True,"show")

    def move(self,card,location):
        if self.cards.count(card) > 0:
            card.parentchange(location)
            #print(location.name)
            #Physically changing the cards location
            if location == self:
                self.cards.append(card)
            else:
                location.cards.append(card)
                print("moved")
            self.cards.remove(card)
            card.cardMove(location)
            print(location.cards[0].suit)
        else:
            print(f"The selected card to move is not in {self.name}")

    def update(self):
        self.placement()
        #screen.blit(self.potimg,(self.x,self.y))
    


class PokerFunc():

    def changeVal(value,change):
        value = value + change
        print(value)
        return value
        
    
class Menu():
    def __init__(self,image,sound,parent):
        self.name = "menu"
        self.img = image
        self.sound = sound
        self.parent = parent
        self.state = self.parent.state
        self.currentText = []
        self.currentObj = []
        self.func = PokerFunc
        self.currentScreen = None
        self.stateFunctions = None
    def blank(self):
        pass
    def add_player(self):
        self.parent.players += 1
        self.sound.soundPlay("ajust")
        print(self.parent.players)
    def subtract_player(self):
        self.parent.players -= 1
        self.sound.soundPlay("ajust")
        print(self.parent.players)
    def start_game(self):
        self.sound.soundPlay("submit")
        self.stateFunctions.setState("mainGame")
    def proceed(self):
        self.parent.phase += 1
        self.parent.phaseGame()

    def preGame(self):
        temp = pygame.image.load(self.img.pregame).convert_alpha()
        #self.currentText.append((self.img.getImg("button_right"),(870,250)))
        #self.currentText.append((self.img.getImg("button_left"),(740,250)))
        #self.currentObj.append(ImgButton(self.img.getImg("button_right"),870,250,onclickFunction=self.func.changeValue(self.parent.players,1)))
        self.currentObj.append(ImgButton(self.img.getImg("button_right"),870,250,onclickFunction=self.add_player,name="select"))
        self.currentObj.append(ImgButton(self.img.getImg("button_left"),740,250,onclickFunction=self.subtract_player,name="select"))
        self.currentText.append((temp,(731,30)))
        self.currentText.append([self.img.textFont_m.render("Players",False,(255,255,255)),(760,140),False])
        self.currentText.append([self.img.textFont_m.render(str(self.parent.players),False,(255,255,255)),(830,255),True])
        self.currentObj.append(ImgButton(self.img.getImg("start"),760,500,onclickFunction=self.start_game,name="select",onePress=True))
        #self.currentText.append
    def mainGame(self):
        self.currentObj.append(ImgButton(self.img.getImg("proceed"),760,530,onclickFunction=self.blank,name="select",onePress=True))
    def noScreen(self):
        pass

    def displayText(self):
        for i in self.currentText:
                screen.blit(i[0],i[1])
        
    def updateObj(self):
        for i in self.currentObj:
            if i.name == "select":
                i.update()
            else:
                i.update()
        
    def update(self,state):
        self.currentText = []
        self.currentObj = []
        self.currentScreen = self.noScreen
        self.stateFunctions = state
        if state.state == "preGame":
            self.currentScreen = self.preGame
        if state.state == "mainGame":
            self.currentScreen = self.mainGame
        if self.currentScreen:
            self.currentScreen()
        self.displayText()
        self.updateObj()

class ImgButton():
    def __init__(self,img, x, y, buttonText='Button', onclickFunction=None, onePress=False, imagedim=None,name=None):
        self.x = x
        self.y = y
        self.name = name
        self.dim = imagedim
        self.img = img
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonRect = pygame.Rect(self.x,self.y,self.img.get_width(),self.img.get_height())

    def update(self):
        mouse = pygame.mouse.get_pos()
        if self.buttonRect.collidepoint(mouse):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        screen.blit(self.img,(self.x,self.y))

class Game():

    def __init__(self,image,sound):
        self.name = "game"
        self.img = image
        self.sound = sound
        self.title = pygame.image.load(image.title).convert_alpha()
        self.state = ""
        self.menu = Menu(image,sound,self)
        self.players = 1
        self.phase = 0
        self.groups = None
        #self.menu.preGame()

    def draw(self,playerhand,otherhands,deck,community):
        self.name = "game"
        deck.drawCard(playerhand)
        deck.drawCard(playerhand)
        for i in otherhands:
            deck.drawCard(i)
            deck.drawCard(i)
        for i in range(5):
            deck.drawCard(community)

    def phaseGame(self):
        if self.phase == 1:
            print("\n\n\n\n\n\n\n_____________Pre-Flop_____________")
            self.draw(*self.groups)
            self.sound.soundPlay("round")

        if self.phase == 2:
            print("\n\n\n\n\n\n\n_____________Flop_____________") 
            self.groups[3].flipCards((0,3))
            self.sound.soundPlay("card-flip-3")
        if self.phase == 3:
            print("\n\n\n\n\n\n\n_____________Turn_____________") 
            self.groups[3].flipCards((0,4))
            self.sound.soundPlay("card-flip-3")

        if self.phase == 4:
            print("\n\n\n\n\n\n\n_____________River_____________") 
            self.groups[3].flipCards((0,5))
            self.sound.soundPlay("card-flip-3")

        if self.phase == 5:
            print("\n\n\n\n\n\n\n_____________Reveal_____________") 
            self.groups[3].flipCards((0,5))
            for i in self.groups[1]:
                for j in reversed(i.cards):
                    j.handFlip(True,"show")
            self.sound.soundPlay("card-flip-3")

        if self.phase == 6:
            print("\n\n\n\n\n\n\n_____________End_____________") 
            self.phase = 0
            self.cleanup(*self.groups)
            self.sound.soundPlay("round")


    def cleanup(self,playerhand,otherhands,deck,community):
        for i in reversed(playerhand.cards):
            playerhand.move(i,deck)
        for i in otherhands:
            for j in reversed(i.cards):
                i.move(j,deck)
        for i in reversed(community.cards):
            community.move(i,deck)
        for i in deck.cards:
            i.handFlip(False,"hide")
        deck.shuffle()
        print("\n\n\n\n\n\nCleaned") 

    
    def stateChange(self,state):
        self.stateC = state
    
    def update(self,state):
        self.state = state.state
        if self.state == "mainMenu":
            screen.blit(self.title,(0,0))

        
class Program():
    def __init__(self):
        self.tempState = "mainMenu"
        self.state = "mainMenu"
        self.test = 0
        self.run = True
        mainMenu(self)
    
    def setState(self,state):
        self.state = state
        return state
    
    def stateCheck(self):
        if self.tempState != self.state:
            self.tempState = self.state
            self.stateChange()
            return True

    def stateChange(self):
        if self.state == "mainMenu":
            mainMenu(self)
        if self.state == "preGame":
            preGame(self)
        if self.state == "mainGame":
            mainGame(self)

        

        

        


imageEngine = ImgEngine()
musicEngine = MusicEngine()
deck = Deck(imageEngine,musicEngine)
window = Screen()
mainhand = Hand(imageEngine,musicEngine,"show")
deck.deckGen()
game = Game(imageEngine,musicEngine)
musicEngine.musicPlay("main-h",-1)
temphand = []
commune = Community(imageEngine,musicEngine)


def mainMenu(program):
    while program.run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #game code
            screen.fill("white")
            screen.blit(window.background,(0,0))
            screen.fill((29, 39, 63))
            #print(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    game.state = ""
                    musicEngine.soundPlay("submit")
                    program.test += 1
                    program.setState("preGame")
                    print(program.test)

            game.update(program)
            update = game.menu.update(program)
            if program.stateCheck():
                return
            pygame.display.update()
            clock.tick(fps)
        
            

def preGame(program):
    while program.run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            screen.fill("white")
            #game code
            screen.blit(window.bg,(0,0))

            print(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    game.state = ""
                    musicEngine.soundPlay("submit")
                    program.test += 1
                    print(program.test)
                if event.key == pygame.K_j:
                    game.players += 1
                    print(game.players)

            game.update(program)
            game.menu.update(program)
            if program.stateCheck():
                return
            pygame.display.update()
            clock.tick(fps)
            

def mainGame(program):
    for i in range(game.players-1):
        temphand.append(EHand(imageEngine,musicEngine,"hide"))
    game.phase = 0
    game.groups = (mainhand,temphand,deck,commune)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #game code
            
            #print(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    #deck.drawCard(mainhand)
                    #print(deck.cards)
                    print(mainhand.cards)
                    print("card drew")
                    musicEngine.soundPlay("card-blip")
                if event.key == pygame.K_b:
                    #for i in mainhand.cards:
                        #print(i.x,i.y)
                    print("cards")
                if event.key == pygame.K_s:
                    temphand.append(EHand(imageEngine,musicEngine))
                if event.key == pygame.K_d:
                    #game.draw(mainhand,temphand,deck,commune)
                    print("all cards drawn")
                if event.key == pygame.K_f:
                    #game.state = ""
                    game.menu.proceed()
                    #musicEngine.soundPlay("submit")
                if event.key == pygame.K_u:
                    commune.flipCards((0,5))
                    musicEngine.soundPlay("submit")
                    # Check if mouse button is down
                if pygame.mouse.get_pressed()[0]:
                    # Wait for mouse button to be released
                    while pygame.mouse.get_pressed()[0]:
                        pygame.time.delay(10)

        screen.blit(window.bg,(0,0))
        game.update(program)
        update = game.menu.update(program)
        if program.stateCheck():
            return
        
        deck.update()
        mainhand.update()
        commune.update()
        for i in deck.cards:
            i.update()
            
        for i in mainhand.cards:
            i.update()
            
        for i in temphand:
            for j in i.cards:
                j.update()
            i.update()
        for i in commune.cards:
            i.update()

        pygame.display.update()
        clock.tick(fps)


Program()

"""
#Boiler page


def Example(program):
    while program.run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            screen.fill("white")
            #game code
            

            #game code

            game.update(program.state)
            game.menu.update(program.state)
            if program.stateCheck():
                return
            pygame.display.update()
            clock.tick(fps)


"""