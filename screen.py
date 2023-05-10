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
import itertools

import mathymath
import screenSim
import rank_compare
import settings as setmenu
import predictor




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
        self.textFont_xs = pygame.font.Font("images/font/pio.otf",16)
        self.textFont_s = pygame.font.Font("images/font/pio.otf",24)
        self.textFont_m = pygame.font.Font("images/font/pio.otf",36)
        self.textFont_num_xs = pygame.font.Font("images\\font\\pau.ttf",16)
        self.textFont_num_s = pygame.font.Font("images\\font\\pau.ttf",24)
        self.images = []
        self.imgGen("ui")
        #self.imgGen("Cards (small)")
        self.imgGen("Cards (medium)")
    
    def deckImgGen(self):
        for i in self.cardImg[1]:
            for j in self.cardImg[2]:
                item = self.imgDir + self.cardImg[0] + "_" + i + "_" + j + ".png"
                item2 = (i,j)
                self.deckGen.append(item)
                self.cardGen.append(item2)
        return (self.deckGen,self.cardGen)
    
    def cardToImg(self,cardinfo):
        for i in self.cardImg[1]:
            for j in self.cardImg[2]:
                if cardinfo == (i,j):
                    return self.cardImg[0] + "_" + i + "_" + j 
    
    def imgGen(self,area):
        for file in os.listdir("images/"+area):
            if file.endswith(".jpg") or file.endswith(".png"):
                self.images.append((file[:-4],pygame.image.load("images/"+area+"/" + file)))
    
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
            self.x = self.parent.x - order*0.4
            self.y = self.parent.y - order*0.4

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
        #random.Random(4).shuffle(self.cards)
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
    
    def imagechange(self,img):
        self.potimg = self.sprites.getImg(img)
    
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
    

class CustomImg:
    def __init__(self,image,sound,parent,name="img",imgname="dice_1",imginfo=None,offset=(0,0)):
        self.name = name
        if name == "card":
            self.cardId = imginfo
        else:
            self.cardId = None
        self.img = image
        self.sound = sound
        self.x = 0
        self.y = 0
        self.displacement = offset
        self.imgname = imgname
        self.front = None
        self.parent = parent
        self.imgSet()

    def imgSet(self):
        if self.cardId:
            self.front = self.img.getImg(self.img.cardToImg((self.cardId[0],self.cardId[1])))
        else:
            self.front = self.img.getImg(self.imgname)
    
    def positionType(self):
        if self.parent.name == "info":
            self.x = self.parent.x + 21*self.displacement[0]
            self.y = self.parent.y 
    
    def update(self):
        #print(self.front,self.cardId)
        self.positionType()
        screen.blit(self.front,(self.x,self.y))

class PokerFunc():

    def __init__(self,image,sound,place=(0,0),player=None,comm=False,parent=None):
        self.name = "info"
        self.img = image
        self.sound = sound
        self.imagecards = []
        self.x = place[0]
        self.y = place[1]
        self.parent = parent
        self.comm = comm
        if player:
            self.genSet(player)
        else:
            self.genSet()
    
    def genSet(self,cards=[]): # test=[("hearts","A"),("hearts","09"),("clubs","Q")])
        temp = 0
        for i in cards:
            self.imagecards.append(CustomImg(self.img,self.sound,self,name="card",imginfo=(i[0],i[1]),offset=(temp,0)))
            temp += 1

    def update(self):
        for j,i in enumerate(self.imagecards):
            if self.comm:
                if j == self.parent.rev:
                    break
            i.update()
        
    
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
        self.currentText.append([self.img.textFont_m.render(self.parent.part,False,(255,255,255)),(740,20),False])
        if not self.parent.processes:
            self.currentText.append([self.img.textFont_xs.render("Press F to progress",False,(255,255,255)),(750,590),False])
        else:
            self.currentText.append([self.img.textFont_xs.render("Processing",False,(255,255,255)),(750,590),False])
        self.currentText.append([self.img.textFont_xs.render("Player Hand",False,(255,255,255)),(740,70),False])
        self.currentText.append([self.img.textFont_xs.render("Community",False,(255,255,255)),(740,130),False])
        self.currentObj.append(PokerFunc(self.img,self.sound,(740,90),player=self.parent.playerHand))
        self.currentObj.append(PokerFunc(self.img,self.sound,(740,150),player=self.parent.communityHand,comm=True,parent=self.parent))
        if self.parent.handsToUse or not self.parent.handsToUse == []:
            #print("added eval",self.parent.handsToUse)
            for j,i in enumerate(self.parent.handsToUse):
                #print("mkobmibmi    ",i)
                #print("lalalala   ",i[1])

                #print("hand:    ", i)
                #print("Format:   ",rank_compare.fromFormatHand(i[0]))
                self.currentObj.append(PokerFunc(self.img,self.sound,(740,(220 + 50*j)),player=rank_compare.fromFormatHand(i[0])))
                self.currentText.append([self.img.textFont_xs.render(i[1].replace('-',' '),False,(255,255,255)),(755,250+50*j),False])
                self.currentText.append([self.img.textFont_num_xs.render(str(mathymath.poker_probabilitie(i[1])),False,(255,255,255)),(860,230+50*j),False])
                if j == 0:
                    break
        self.currentText.append([self.img.textFont_xs.render("Best Hands",False,(255,255,255)),(740,200),False])
        self.currentText.append([self.img.textFont_num_s.render("Win Chance",False,(255,255,255)),(775,275),False])
        self.currentText.append([self.img.textFont_xs.render("Future Hands",False,(255,255,255)),(740,310),False])
        #self.currentText.append([self.img.textFont_xs.render("Future Hands",False,(255,255,255)),(740,400),False])
        #self.currentObj.append(ImgButton(self.img.getImg("proceed"),760,530,onclickFunction=self.blank,name="select",onePress=True))
        self.currentObj.append(BButton(790, 350, 80, 30, "gray", "lightblue", self.img.textFont_xs, "Start", "Start the predictor", ToolTip(self.img.textFont_xs)))
    def noScreen(self):
        pass

    def displayText(self):
        for i in self.currentText:
                screen.blit(i[0],i[1])
        
    def updateObj(self):
        for i in self.currentObj:
            if i.name == "customdrawb":
                i.update(self.parent.eventlist)
                i.draw()
                i.tool_tip.update()
                i.tool_tip.draw()
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

    def screen_update(self):
        self.currentText = []
        self.currentObj = []
        self.currentScreen = self.noScreen
        if self.parent.state == "preGame":
            self.currentScreen = self.preGame
        if self.parent.state == "mainGame":
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

class ToolTip():
    def __init__(self, font):
        self.name = "customdrawb"
        self.font = font 
        self.tip_text = None
        self.current_text = None
        self.rect = None
        self.image = None

    def set_text(self, tip_text):
        self.tip_text = tip_text

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.tip_text != self.current_text:
            self.current_text = self.tip_text
            if self.current_text == None:
                self.image = None
                self.rect = None
            else:
                self.image = self.font.render(self.tip_text, True, (0, 0, 0))
                self.rect = self.image.get_rect().inflate(6, 2)
        if self.rect:
            self.rect.topright = mouse_pos[0]-16, mouse_pos[1]

    def draw(self):
        if self.rect and self.image:
            pygame.draw.rect(screen, (255, 255, 0), self.rect)
            screen.blit(self.image, self.image.get_rect(center = self.rect.center))

class BBox():
    def __init__(self, x, y, w, h, font, color=pygame.Color('white'), text=None):
        self.game = game
        self.name = "customdrawb"
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.image = font
        self.hover = False
        self.texton = text
    def update():
        pass
    def draw(self):
        color = self.color if self.hover  else self.highlight_color
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.image, self.image.get_rect(center = self.rect.center))
        if self.texton:
            blit_text(self.rect, self.texton, (self.rect.x,self.rect.y), self.font, color=pygame.Color('black'))


        
class BButton():
    def __init__(self, x, y, w, h, color, highlight_color, font, text, tip_text=None, tool_tip=None):
        self.game = game
        self.name = "customdrawb"
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.highlight_color = highlight_color
        self.image = font.render(text, True, (0, 0, 0))
        self.hover = False
        self.tip_text = tip_text
        self.tool_tip = tool_tip
        self.btext = ""
        self.bdisplay = BBox(50,50,700,600,font,text=self.btext)
        self.displayposs = False
        
    def update(self,event_list):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        if self.hover and self.tool_tip:
            self.tool_tip.set_text(self.tip_text)
            self.displayposs = True
        
        #if event_list

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.game.rev == 5:
                        continue

                        predictor.lowestBest(communityHand)

                    playerHand = []
                    communityHand = []
                    for i in self.game.groups[3].cards:
                        communityHand.append(rank_compare.toFormat((i.value,i.suit)))
                    for i in self.game.groups[0].cards:
                        playerHand.append(rank_compare.toFormat((i.value,i.suit)))
                    if self.game.rev == 3 or self.game.rev == 4:    
                        handscan = predictor.futurehand(playerHand,communityHand,rev=self.game.rev,convert=False)
                        self.btext = "\n".join(predictor.future_eval(handscan[0],type=3,readeval=handscan[1]))
                        predictor.future_eval(handscan[0],type=2,readeval=handscan[1])


                    
                    
    def draw(self):
        color = self.color if self.hover  else self.highlight_color
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.image, self.image.get_rect(center = self.rect.center))
        if self.displayposs:
            self.bdisplay.draw

        

class Game():

    def __init__(self,image,sound):
        self.name = "game"
        self.img = image
        self.sound = sound
        self.title = pygame.image.load(image.title).convert_alpha()
        self.state = ""
        self.menu = Menu(image,sound,self)
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
        self.eventlist = None
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

    def grabPlayerHand(self):
        self.playerHand = []
        for i in self.groups[0].cards:
            self.playerHand.append((i.suit,i.value))
            print(i.suit,i.value)
    def grabCommunityHand(self):
        self.communityHand = []
        for i in self.groups[3].cards:
            self.communityHand.append((i.suit,i.value))

    def grabEvaluation(self):
        communityHand = []
        
        for i in self.groups[3].cards:
            communityHand.append(rank_compare.toFormat((i.value,i.suit)))
        playerHand = []
        for i in self.groups[0].cards:
            playerHand.append(rank_compare.toFormat((i.value,i.suit)))
        enemyHands = []
        for j in self.groups[1]:
            temp = []
            for i in j.cards:
                temp.append(rank_compare.toFormat((i.value,i.suit)))
            enemyHands.append(temp+communityHand[:self.rev])
        
        
        playerOptions = playerHand + communityHand[:self.rev]

        print("mkivmkvkmvs   dfvsv ",playerOptions)
        print(enemyHands)
        print(communityHand[:self.rev])
        enemyOptions = []
        self.handsToUse = []
        #for i in enemyHands:
        #    enemyOptions.append(list(i+communityHand))
        self.processes = True
        self.menu.screen_update()

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


        print(self.handsToUse)

    def finalEvaluation(self):
        communityHand = []
        self.allStrength = []
        for i in self.groups[3].cards:
            communityHand.append(rank_compare.toFormat((i.value,i.suit)))
        playerHand = []
        for i in self.groups[0].cards:
            playerHand.append(rank_compare.toFormat((i.value,i.suit)))
        enemyHands = []
        for j in self.groups[1]:
            temp = []
            for i in j.cards:
                temp.append(rank_compare.toFormat((i.value,i.suit)))
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
                print("you have ben beanten")
                for i in self.allStrength:
                    print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
                    #print["NO:",i[3],"Bhand:",i[0],"type:",i[1]]
                    return self.groups[1][max_lists[0][3]]
            else:
                print("Yay: u won fr ")
                for i in self.allStrength:
                    print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
                    return self.groups[0]
        else:
            for i in max_lists:
                if i[3] == "player":
                    print("Joe Drew a Dewy Stew u Drew ")
                    for i in self.allStrength:
                        print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
                    return 
                else:
                    print("you have ben beanten")
                    print(f"NO:{i[3]},   Bhand:{i[0]},  type:{i[1]}, score:{i[2]}")
        return 
        
                
    def revealWin(self,winner=None):
        if winner:
            for i in self.groups[1]:
                i.imagechange("losepot") 
            self.groups[0].imagechange("losepot") 
            winner.imagechange("winpot")


    def resetWin(self):
        for i in self.groups[1]:
            i.imagechange("pot") 
        self.groups[0].imagechange("pot") 

    def phaseGame(self):
        if self.phase == 1:
            print("\n\n\n\n\n\n\n_____________Pre Flop_____________")
            self.part = "Pre Flop"
            self.draw(*self.groups)
            self.grabPlayerHand()
            self.grabCommunityHand()
            self.sound.soundPlay("round")
            self.rev = 0


        if self.phase == 2:
            print("\n\n\n\n\n\n\n_____________Flop_____________") 
            self.part = "Flop"
            self.groups[3].flipCards((0,3))
            self.sound.soundPlay("card-flip-3")
            self.rev = 3
            self.grabEvaluation()
            self.processes = False

        if self.phase == 3:
            print("\n\n\n\n\n\n\n_____________Turn_____________") 
            self.part = "Turn"
            self.groups[3].flipCards((0,4))
            self.sound.soundPlay("card-flip-3")
            self.rev = 4
            self.grabEvaluation()
            self.processes = False

        if self.phase == 4:
            print("\n\n\n\n\n\n\n_____________River_____________") 
            self.part = "River"
            self.groups[3].flipCards((0,5))
            self.sound.soundPlay("card-flip-3")
            self.rev = 5
            self.grabEvaluation()
            self.processes = False

        if self.phase == 5:
            print("\n\n\n\n\n\n\n_____________Reveal_____________") 
            self.part = "Reveal"
            self.groups[3].flipCards((0,5))
            for i in self.groups[1]:
                for j in reversed(i.cards):
                    j.handFlip(True,"show")
            self.sound.soundPlay("card-flip-3")
            self.revealWin(self.finalEvaluation())

        if self.phase == 6:
            print("\n\n\n\n\n\n\n_____________End_____________") 
            self.part = "End"
            self.phase = 0
            self.cleanup(*self.groups)
            self.sound.soundPlay("round")
            self.resetWin()


    def cleanup(self,playerhand,otherhands,deck,community):
        for i in reversed(community.cards):
            community.move(i,deck)
        for i in otherhands:
            for j in reversed(i.cards):
                i.move(j,deck)
        for i in reversed(playerhand.cards):
            playerhand.move(i,deck)

        for i in deck.cards:
            i.handFlip(False,"hide")

        #deck.cards = []
        #deck.deckGen()
        deck.shuffle()
        print("\n\n\n\n\n\nCleaned") 

    
    def stateChange(self,state):
        self.stateC = state
    
    def update(self,state,event):
        self.eventlist = event
        self.state = state.state
        if self.state == "mainMenu":
            screen.blit(self.title,(0,0))
    
    def playerBal(self,bal):
        self.players = bal #5 goal 8
        enemyamm = len(self.groups[1]) #7 current
        while not self.players == enemyamm+1:
            if self.players > enemyamm+1:
                self.groups[1].append(EHand(imageEngine,musicEngine))
            else:
                self.groups[1].pop(-1)

        
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

def preprocess_df(df):
    hand_to_row = {}
    for index, row in df.iterrows():
        hand_to_row[row['hand']] = row.to_dict()
        
    return hand_to_row

def preprocess_df2(df):
    hand_to_row = df.groupby('hand').apply(lambda x: x.iloc[0].to_dict()).to_dict()
    return hand_to_row


def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

import pickle   
import pandas as pd
import ast        
#df2 = pd.read_csv('cards6.csv')

rank_start_time = time.perf_counter()       





#uncomment 1068,1069,1070 if you dont have the pickle

#hand_to_row = preprocess_df2(df2)
#with open('hand_to_row2.pickle', 'wb') as handle:
#    pickle.dump(hand_to_row, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open('hand_to_row2.pickle', 'rb') as handle:
    hand_to_row = pickle.load(handle)

predictor.hand_to_row = hand_to_row

rank_end_time = time.perf_counter()
rank_elapsed = rank_end_time - rank_start_time
print(f"Time elapsed: {rank_elapsed} seconds")

print("created pickle")

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
        event_list = pygame.event.get()
        for event in event_list:
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

            game.update(program,event_list)
            update = game.menu.update(program)
            if program.stateCheck():
                return
            pygame.display.update()
            clock.tick(fps)
        
            

def preGame(program):
    while program.run == True:
        event_list = pygame.event.get()
        for event in event_list:
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

            game.update(program,event_list)
            game.menu.update(program)
            if program.stateCheck():
                return
            pygame.display.update()
            clock.tick(fps)

def mainGame(program):
    settings_menu = setmenu.SettingsMenu(screen,game) 

    for i in range(game.players-1):
        temphand.append(EHand(imageEngine,musicEngine,"hide"))
    game.phase = 0
    game.groups = (mainhand,temphand,deck,commune)
    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #game code

            if event.type == pygame.MOUSEBUTTONDOWN:
                if setmenu.cog_icon_rect.collidepoint(pygame.mouse.get_pos()):
                    settings_menu.show()
            
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
                    if not game.processes:
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
        game.update(program,event_list)
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
            i.update()

        for i in temphand:
            for j in i.cards:
                j.update()
            
            
        for i in commune.cards:
            i.update()

        screen.blit(setmenu.cog_icon, setmenu.cog_icon_rect.topleft)

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