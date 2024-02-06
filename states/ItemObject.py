import pygame, os
from states.CommonFunc import *
from states.State import State

class ItemObject(State, CommonFunc):
    def __init__(self, game, x_pos, y_pos, item):
        State.__init__(self, game)
        CommonFunc.__init__(self)
        
        self.x_pos_ = x_pos + 25
        self.y_pos_ = y_pos + 80
        
        self.map_x_ = [0]
        self.map_y_ = [0]
        
        self.width_frame_ = self.items[item][0]
        self.height_frame_ = self.items[item][1]
        
        self.item = item
        
    def show(self, display):
        rect_x = self.x_pos_ - self.map_x_[0]
        rect_y = self.y_pos_ - self.map_y_[0]
        
        imageName = self.item + ".png"
        image = pygame.image.load(os.path.join(self.game.items_dir, imageName))
        display.blit(image, (rect_x, rect_y))
    
    def setMapXY(self, x, y):
        self.map_x_[0] = x
        self.map_y_[0] = y