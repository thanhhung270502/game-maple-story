import pygame, os
from states.CommonFunc import *
from states.State import State

class ThreatsObject(State, CommonFunc):
    def __init__(self, game, x_pos, y_pos):
        State.__init__(self, game)
        CommonFunc.__init__(self)
        
        self.x_val_ = 0
        self.y_val_ = 0
        self.x_pos_ = x_pos
        self.y_pos_ = y_pos
        
        self.map_x_ = [0]
        self.map_y_ = [0]
        
        self.on_ground_ = True
        self.come_back_time_ = 0
        
        self.frame_clip_ = []
        self.frame_ = 0
        
        self.width_frame_ = 0
        self.height_frame_ = 0
        
        self.imageName = "left_squid"
        
        self.type_move_ = self.type_move["static_threat"]
        self.animation_a_ = 0
        self.animation_b_ = 0
        self.input_type_ = Input()
        self.input_type_.left_ = 1

    def initial(self):
        self.x_val_ = 0
        self.y_val_ = 0
        
        if self.x_pos_ > 256:
            self.x_pos_ = 256
            self.animation_a_ -= 256
            self.animation_b_ -= 256
        else:
            self.x_pos_ = 0
            
        self.y_pos_ = 0
        self.come_back_time_ = 0
        self.input_type_.left_ = 1

    def show(self, display):
        if self.come_back_time_ == 0:
            rect_x = self.x_pos_ - self.map_x_[0]
            rect_y = self.y_pos_ - self.map_y_[0]
            self.frame_ += 1
            
            if self.frame_ >= 8:
                self.frame_ = 0
            
            imageName = self.imageName + str(self.frame_) + ".png"
            image = pygame.image.load(os.path.join(self.game.monster_dir, imageName))
            display.blit(image, (rect_x, rect_y))
            
    def doPlayer(self, map_data: [Map]):
        if self.come_back_time_ == 0:
            self.x_val_= 0
            self.y_val_ += self.GRAVITY_SPEED
            
            if self.y_val_ >= self.MAX_FALL_SPEED:
                self.y_val_ = self.MAX_FALL_SPEED
                
            if self.input_type_.left_ == 1:
                self.x_val_ -= self.MONSTER_SPEED
            elif self.input_type_.right_ == 1:
                self.x_val_ += self.MONSTER_SPEED
            
            self.checkToMap(map_data)
        elif self.come_back_time_ > 0:
            self.come_back_time_ -= 1
            
            self.checkToMap(map_data)
            
            if self.come_back_time_ == 0:
                self.initial()
    
    def checkToMap(self, map_data: [Map]): 
        x1, x2, y1, y2 = 0, 0, 0, 0
        
        # Check horizontal position
        height_min = self.MONSTER_HEIGHT if self.MONSTER_HEIGHT < self.TILE_SIZE else self.TILE_SIZE
        
        # print(self.x_pos_)
        x1 = int((self.x_pos_ + self.x_val_) / self.TILE_SIZE)
        x2 = int((self.x_pos_ + self.x_val_ + self.MONSTER_WIDTH - 1) / self.TILE_SIZE)
        
        y1 = int((self.y_pos_) / self.TILE_SIZE)
        y2 = int((self.y_pos_ + height_min - 1) / self.TILE_SIZE)
        
        print("x1: ", x1, "; x2: ", x2)
        
        if x1 >= 0 and x2 < self.MAX_MAP_X and y1 >= 0 and y2 < self.MAX_MAP_Y:
            if self.x_val_ > 0:
                value_1 = map_data[0].tile[y1][x2]
                value_2 = map_data[0].tile[y2][x2]
                # print("value_1: ", value_1, "; value_2: ", value_2)
                if value_1 > self.BLANK_TILE or \
                    value_2 > self.BLANK_TILE:
                    self.x_pos_ = x2 * self.TILE_SIZE
                    self.x_pos_ -= self.MONSTER_WIDTH + 1
                    self.x_val_ = 0
            elif self.x_val_ < 0:
                value_1 = map_data[0].tile[y1][x1]
                value_2 = map_data[0].tile[y2][x1]
                if value_1 > self.BLANK_TILE or \
                    value_2 > self.BLANK_TILE:
                    self.x_pos_ = (x1 + 1) * self.TILE_SIZE
                    self.x_val_ = 0
        
        # Check vertical position
        width_min = self.MONSTER_WIDTH if self.MONSTER_WIDTH < self.TILE_SIZE else self.TILE_SIZE
        
        x1 = int((self.x_pos_) / self.TILE_SIZE)
        x2 = int((self.x_pos_ + width_min) / self.TILE_SIZE)
        
        y1 = int((self.y_pos_ + self.y_val_) / self.TILE_SIZE)
        y2 = int((self.y_pos_ + self.y_val_ + self.MONSTER_HEIGHT - 1) / self.TILE_SIZE)
        
        # print(x1, y1, x2, y2)
        
        if x1 >= 0 and x2 < self.MAX_MAP_X and y1 >= 0 and y2 < self.MAX_MAP_Y:
            if self.y_val_ > 0:
                value_1 = map_data[0].tile[y2][x1]
                value_2 = map_data[0].tile[y2][x2]
                if value_1 > self.BLANK_TILE or value_2 > self.BLANK_TILE:
                    self.y_pos_ = y2 * self.TILE_SIZE
                    self.y_pos_ -= self.MONSTER_HEIGHT + 1
                    self.y_val_ = 0
                    self.on_ground_ = True
            elif self.y_val_ < 0:
                value_1 = map_data[0].tile[y1][x1]
                value_2 = map_data[0].tile[y1][x2]
                if value_1 > self.BLANK_TILE or value_2 > self.BLANK_TILE:
                    self.x_pos_ = (x1 + 1) * self.TILE_SIZE
                    self.y_val_ = 0
                    self.on_ground_ = False
        
        
        self.x_pos_ += self.x_val_
        self.y_pos_ += self.y_val_
        
        if self.x_pos_ < 0:
            self.x_pos_ = 0
        elif self.x_pos_ + self.MONSTER_WIDTH > map_data[0].max_x_:
            self.x_pos_ = map_data[0].max_x_ - self.MONSTER_WIDTH - 1
            
        if self.y_pos_ > map_data[0].max_y_:
            self.come_back_time_ = 60
    
    def setMapXY(self, x, y):
        self.map_x_[0] = x
        self.map_y_[0] = y
        
    def impMoveType(self):
        if self.type_move_ == self.type_move["static_threat"]:
            pass
        else:
            if self.on_ground_ == True:
                if self.x_pos_ > self.animation_b_:
                    self.input_type_.left_ = 1
                    self.input_type_.right_ = 0
                    self.imageName = "left_squid"
                elif self.x_pos_ < self.animation_a_:
                    self.input_type_.left_ = 0
                    self.input_type_.right_ = 1
                    self.imageName = "right_squid"
            else:
                if self.input_type_.left_ == 1:
                    self.imageName = "left_squid"
    