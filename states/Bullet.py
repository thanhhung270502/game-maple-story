import pygame, os
from states.CommonFunc import *
from states.State import State

class Bullet(CommonFunc, State):
    def __init__(self, game, x_pos, y_pos, bullet_dir):
        CommonFunc.__init__(self)
        State.__init__(self, game)
        
        self.x_pos_ = x_pos
        self.y_pos_ = y_pos
        self.x_val_ = self.BULLET_SPEED
        self.y_val_ = 0
        
        self.map_x_ = [0]
        self.map_y_ = [0]
        
        self.is_move_ = False 
        self.bullet_dir_ = bullet_dir
        
    def handleMove(self, x_border, y_border):
        if self.bullet_dir_ == self.move["right"]:
            self.x_pos_ += self.x_val_
            
            if self.x_pos_ > x_border:
                self.is_move_ = False
        else:
            self.x_pos_ -= self.x_val_
            if self.x_pos_ < 0:
                self.is_move_ = False
                
    def setMapXY(self, x, y):
        self.map_x_[0] = x
        self.map_y_[0] = y
