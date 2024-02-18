import pygame, os
from states.State import State
from states.OptionMenu import OptionMenu
from states.Playground import Playground
from states.Map1 import Map1
from states.Map2 import Map2
from states.Map3 import Map3
from states.Shop import Shop

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        # self.play_box = pygame.Rect(450, 305, 380, 110)
        self.start_box = pygame.Rect(1125, 360, 150, 90)
        self.img_background = None

    def update(self, actions, screen):
        if actions["start"] or actions["left"] and self.start_box.collidepoint(pygame.mouse.get_pos()):
            new_state = OptionMenu(self.game)
            # new_state = Map1(self.game)
            # new_state = Map2(self.game)
            # new_state = Map3(self.game)
            # new_state = Playground(self.game)
            new_state.enter_state()
        # elif actions["start"] or actions["left"] and self.shop_box.collidepoint(pygame.mouse.get_pos()):
        #     new_state = Shop(self.game)
        #     new_state.enter_state()
        # elif self.start_box.collidepoint(pygame.mouse.get_pos()):
        #     pygame.mouse.set_cursor(pygame.cursors.broken_x)
        #     self.img_background = pygame.image.load(os.path.join(self.game.background_dir, "BG2.png"))
        # elif self.shop_box.collidepoint(pygame.mouse.get_pos()):
        #     pygame.mouse.set_cursor(pygame.cursors.broken_x)
        #     self.img_background = pygame.image.load(os.path.join(self.game.background_dir, "BG3.png"))
        # elif not self.start_box.collidepoint(pygame.mouse.get_pos()) and not self.shop_box.collidepoint(pygame.mouse.get_pos()):
        #     pygame.mouse.set_cursor(pygame.cursors.broken_x)
        #     self.img_background = pygame.image.load(os.path.join(self.game.background_dir, "BG1.png"))

        self.game.reset_keys()
        
    def render(self, display):
        if self.img_background is None:
            self.img_background = pygame.image.load(os.path.join(self.game.background_dir, "background.png"))
        display.blit(self.img_background, (0,0))
