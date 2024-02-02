import pygame, os
from states.CommonFunc import *
from states.State import State

class ThreatsObject(State, CommonFunc):
    def __init__(self, game):
        State.__init__(self, game)
        CommonFunc.__init__(self)
        
        self.x_val_ = 0
        self.y_val_ = 0
        self.x_pos_ = 0
        self.y_pos_ = 0
        
        self.on_ground_ = True
        self.come_back_time = 0
        self.frame_clip_ = []
        self.width_frame_ = 0
        self.height_frame_ = 0