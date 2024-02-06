import pygame, os
from states.CommonFunc import *

class GeometricFormat:
    def __init__(self, left, top, width, height):
        self.left_ = left
        self.top_ = top
        self.width_ = width
        self.height_ = height
        
class ColorData:
    def __init__(self, r, g, b):
        self.red_ = r
        self.green_ = g
        self.blue_ = b
    def getColor(self):
        return (self.red_, self.green_, self.blue_)
        
class Geometric:
    def __init__(self): pass
    
    def renderRectangle(geo_size: Rect, color_data: ColorData, display, border_size): 
        pygame.draw.rect(display, color_data.getColor(), geo_size.getRect(), 0, border_size)
    
    def renderRectangle2(geo_size: Rect, color_data: ColorData, display, border_size):
        pygame.draw.rect(display, color_data.getColor(), geo_size.getRect(), 0, -1, border_size, -1, border_size, -1)
    
    def renderOutline(self, geo_size: GeometricFormat, color_data: ColorData, display): pass