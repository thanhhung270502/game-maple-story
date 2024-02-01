import pygame, os
from states.State import State
from states.Result import Result
from RWFile import HandleFile
from states.CommonFunc import *
from states.Character import Character
import random
import json
# from states.PauseMenu import PauseMenu

class Playground(State):
    def __init__(self, game, level, weapon):
        State.__init__(self,game)
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.COLORWHITE = (255, 255, 255)
        
        self.img_background = pygame.image.load(os.path.join(self.game.background_dir, "Henesys.png"))
        self.actions = []
        self.startGame = False
        self.startTime = pygame.time.get_ticks()
        self.countdown = 6
        self.countdownTime = self.countdown
        self.weapon = weapon
        self.level = level
        self.game_map = GameMap(game)
        
        self.p_player = Character(game)

    def update(self, actions, mouse_pos):
        # Check if the game was paused 
        # if actions["pause"]:
        #     new_state = PauseMenu(self.game)
        #     new_state.enter_state()
        self.p_player.handleInputAction(actions)
        
        self.game.reset_keys()
        pass

    def render(self, display):
        display.blit(self.img_background, (0,0))
        
        map_data = self.game_map.game_map_
        
        self.game_map.loadMap(os.path.join(self.game.map_dir, "map.txt"))
        
        self.p_player.doPlayer(map_data)
        self.p_player.show(display)
        
        self.game_map.drawMap(display)
        pygame.time.delay(10)
        



class GameMap (State, CommonFunc):
    def __init__(self, game):
        CommonFunc.__init__(self)
        State.__init__(self, game)
        self.game_map_ = [Map()]
        self.tile_mat = []
        
    def loadMap(self, fileName):
        with open(fileName, 'rb') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            tile = []
            for j in range(len(lines[i].split())):
                val = int(lines[i].split()[j])
                tile.append(val)
                if val > 0:
                    if (j > self.game_map_[0].max_x_):
                        self.game_map_[0].max_x_ = j
                    if (i > self.game_map_[0].max_y_):
                        self.game_map_[0].max_y_ = i
            # print(tile)
            self.game_map_[0].tile.append(tile)
        self.game_map_[0].max_x_ = (self.game_map_[0].max_x_ + 1) * self.TILE_SIZE
        self.game_map_[0].max_y_ = (self.game_map_[0].max_y_ + 1) * self.TILE_SIZE
        
        self.game_map_[0].start_x_ = 0
        self.game_map_[0].start_y_ = 0
        
        self.game_map_[0].fileName = fileName
        
    def drawMap(self, display):
        x1, x2, y1, y2 = 0, 0, 0, 0

        map_x = int(self.game_map_[0].start_x_ / self.TILE_SIZE)
        x1 = (self.game_map_[0].start_x_ % self.TILE_SIZE) * (-1)
        x2 = x1 + self.SCREEN_WIDTH + (self.TILE_SIZE if x1 != 0 else 0)
        
        map_y = int(self.game_map_[0].start_y_ / self.TILE_SIZE)
        y1 = (self.game_map_[0].start_y_ % self.TILE_SIZE) * (-1)
        y2 = y1 + self.SCREEN_HEIGHT + (self.TILE_SIZE if y1 != 0 else 0)
        
        i = y1
        while(i < y2):
            map_x = int(self.game_map_[0].start_x_ / self.TILE_SIZE)
            j = x1
            while(j < x2):
                val = int(self.game_map_[0].tile[map_y][map_x])
                if val > 0:
                    imageName = str(val) + ".png"
                    image = pygame.image.load(os.path.join(self.game.map_dir, imageName))
                    imagePos = (j, i)
                    display.blit(image, imagePos)
                map_x += 1
                j += self.TILE_SIZE
            map_y += 1
            i += self.TILE_SIZE