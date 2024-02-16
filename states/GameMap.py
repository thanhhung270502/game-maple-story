import pygame, os
from states.CommonFunc import *
from states.State import *

class GameMap (State, CommonFunc):
    def __init__(self, game):
        CommonFunc.__init__(self)
        State.__init__(self, game)
        self.game_map_ = [Map()]
        self.tile_mat = []
        
    def loadMap(self, fileName):
        self.game_map_[0].tile = []
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
        
        self.game_map_[0].start_x_[0] = 0
        self.game_map_[0].start_y_[0] = 0
        
        self.game_map_[0].fileName = fileName
        self.game_map_[0].max_map_x_ = len(lines[0].split())
        self.game_map_[0].max_map_y_ = len(self.game_map_[0].tile)
    
    def setMap(self, map_data):
        self.game_map_[0].start_x_[0] = map_data[0].start_x_[0]
        self.game_map_[0].start_y_[0] = map_data[0].start_y_[0]
        
        self.game_map_[0].max_x_ = map_data[0].max_x_
        self.game_map_[0].max_y_ = map_data[0].max_y_
        
        self.game_map_[0].tile = map_data[0].tile
        self.game_map_[0].fileName = map_data[0].fileName

    def drawMap(self, display):
        x1, x2, y1, y2 = 0, 0, 0, 0
        
        map_x = int(self.game_map_[0].start_x_[0] / self.TILE_SIZE)
        x1 = (self.game_map_[0].start_x_[0] % self.TILE_SIZE) * (-1)
        x2 = x1 + self.SCREEN_WIDTH + (self.TILE_SIZE if x1 != 0 else 0)
        
        map_y = int(self.game_map_[0].start_y_[0] / self.TILE_SIZE)
        y1 = (self.game_map_[0].start_y_[0] % self.TILE_SIZE) * (-1)
        y2 = y1 + self.SCREEN_HEIGHT + (self.TILE_SIZE if y1 != 0 else 0)
        
        i = y1
        while(i < y2):
            map_x = int(self.game_map_[0].start_x_[0] / self.TILE_SIZE)
            j = x1
            while(j < x2):
                val = int(self.game_map_[0].tile[map_y][map_x])
                if val > 0:
                    if val < 10000: 
                        imageName = str(val) + ".png"
                        image = pygame.image.load(os.path.join(self.game.map_dir, imageName))
                        imagePos = (j, i)
                        display.blit(image, imagePos)
                map_x += 1
                j += self.TILE_SIZE
            map_y += 1
            i += self.TILE_SIZE