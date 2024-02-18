import pygame, os
from states.CommonFunc import *
from states.State import State

class ItemObject(State, CommonFunc):
    def __init__(self, game, x_pos, y_pos, item, num):
        State.__init__(self, game)
        CommonFunc.__init__(self)
        
        self.x_pos_ = x_pos
        self.y_pos_ = y_pos 
        
        self.y_val_ = 0
        
        self.map_x_ = [0]
        self.map_y_ = [0]
        
        self.width_frame_ = self.items[item][0]
        self.height_frame_ = self.items[item][1]
        
        self.num = num
        
        self.item_type = item
        
    def show(self, display):
        rect_x = self.x_pos_ - self.map_x_[0] + self.width_frame_ / 2
        rect_y = self.y_pos_ - self.map_y_[0]
        
        imageName = self.item_type + ".png"
        image = pygame.image.load(os.path.join(self.game.items_dir, imageName))
        display.blit(image, (rect_x, rect_y))
    
    def doPlayer(self, map_data: list[Map]):
        self.y_val_ += self.GRAVITY_SPEED
        
        if self.y_val_ >= self.MAX_FALL_SPEED:
            self.y_val_ = self.MAX_FALL_SPEED
        
        self.checkToMap(map_data)
    
    def checkToMap(self, map_data: list[Map]): 
        x1, x2, y1, y2 = 0, 0, 0, 0
        
        width_min = self.width_frame_ if self.width_frame_ < self.TILE_SIZE else self.TILE_SIZE
        
        x1 = int((self.x_pos_) / self.TILE_SIZE)
        x2 = int((self.x_pos_ + width_min) / self.TILE_SIZE)
        
        y1 = int((self.y_pos_ + self.y_val_) / self.TILE_SIZE)
        y2 = int((self.y_pos_ + self.y_val_ + self.height_frame_ - 1) / self.TILE_SIZE)
        
        if x1 >= 0 and x2 < map_data[0].max_map_x_ and y1 >= 0 and y2 < map_data[0].max_map_y_:
            if self.y_val_ > 0:
                value_1 = map_data[0].tile[y2][x1]
                value_2 = map_data[0].tile[y2][x2]
                if (value_1 > self.BLANK_TILE and value_1 < self.MAP_TILE) or \
                    (value_2 > self.BLANK_TILE and value_2 < self.MAP_TILE):
                    self.y_pos_ = y2 * self.TILE_SIZE
                    self.y_pos_ -= self.height_frame_ + 1
                    self.y_val_ = 0
            elif self.y_val_ < 0:
                value_1 = map_data[0].tile[y1][x1]
                value_2 = map_data[0].tile[y1][x2]
                if (value_1 > self.BLANK_TILE and value_1 < self.MAP_X_TILE) or \
                    (value_2 > self.BLANK_TILE and value_2 < self.MAP_X_TILE):
                    self.x_pos_ = (x1 + 1) * self.TILE_SIZE
                    self.y_val_ = 0
        
        self.y_pos_ += self.y_val_
    
    def setMapXY(self, x, y):
        self.map_x_[0] = x
        self.map_y_[0] = y