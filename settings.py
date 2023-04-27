import pygame
import pygame_menu
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Load cog icon
cog_icon_path = 'images\Cards (medium)\dice_decorated_question.png'  # Replace with the path to your cog icon
cog_icon = pygame.image.load(cog_icon_path)
cog_icon_rect = cog_icon.get_rect()
cog_icon_rect.topleft = (10, 10)

class SettingsMenu:
    def __init__(self, screen,game):
        self.screen = screen
        self.game = game
        self.menu = pygame_menu.Menu(title='Settings', width=screen.get_width(), height=screen.get_height(), theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input('Player Name: ', default='Player')
        self.menu.add.selector('Players: ', [(str(i)) for i in range(1,11)], default=self.game.players)
        self.menu.add.button('Back', self.close_menu)
        self.menu.add.button('Apply', self.close_menu)
    
    def playerChange(self,val):
        self.game.playerBal(int(val[0]))

    def show(self):
        self.menu.enable()
        self.menu.mainloop(self.screen)

    def close_menu(self):
        self.menu.disable()

    def apply(self):
        #applied feats
        self.close_menu()
