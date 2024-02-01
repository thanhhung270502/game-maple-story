import pygame, os
from states.State import State
from states.Result import Result
from RWFile import HandleFile
from states.CommonFunc import Map
from states.CommonFunc import CommonFunc
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

    def update(self, actions, mouse_pos):
        # Check if the game was paused 
        # if actions["pause"]:
        #     new_state = PauseMenu(self.game)
        #     new_state.enter_state()
        
        
        self.game.reset_keys()
        pass

    def render(self, display):
        display.blit(self.img_background, (0,0))
        
        self.game_map.loadMap(os.path.join(self.game.map_dir, "map.txt"))
        self.game_map.drawMap(display)



class GameMap (State, CommonFunc):
    def __init__(self, game):
        CommonFunc.__init__(self)
        State.__init__(self, game)
        self.game_map_ = Map()
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
                    if (j > self.game_map_.max_x_):
                        self.game_map_.max_x_ = j
                    if (i > self.game_map_.max_y_):
                        self.game_map_.max_y_ = i
            # print(tile)
            self.game_map_.tile.append(tile)
        self.game_map_.max_x_ = (self.game_map_.max_x_ + 1) * self.TILE_SIZE
        self.game_map_.max_y_ = (self.game_map_.max_y_ + 1) * self.TILE_SIZE
        
        self.game_map_.start_x_ = 0
        self.game_map_.start_y_ = 0
        
        self.game_map_.fileName = fileName
        
    def drawMap(self, display):
        x1, x2, y1, y2 = 0, 0, 0, 0

        map_x = int(self.game_map_.start_x_ / self.TILE_SIZE)
        x1 = (self.game_map_.start_x_ % self.TILE_SIZE) * (-1)
        x2 = x1 + self.SCREEN_WIDTH + (self.TILE_SIZE if x1 != 0 else 0)
        
        map_y = int(self.game_map_.start_y_ / self.TILE_SIZE)
        y1 = (self.game_map_.start_y_ % self.TILE_SIZE) * (-1)
        y2 = y1 + self.SCREEN_HEIGHT + (self.TILE_SIZE if y1 != 0 else 0)
        
        i = y1
        while(i < y2):
            map_x = int(self.game_map_.start_x_ / self.TILE_SIZE)
            j = x1
            while(j < x2):
                val = int(self.game_map_.tile[map_y][map_x])
                if val > 0:
                    imageName = str(val) + ".png"
                    image = pygame.image.load(os.path.join(self.game.map_dir, imageName))
                    imagePos = (j, i)
                    display.blit(image, imagePos)
                map_x += 1
                j += self.TILE_SIZE
            map_y += 1
            i += self.TILE_SIZE