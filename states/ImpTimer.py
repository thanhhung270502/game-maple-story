import pygame, os
from states.CommonFunc import *

class ImpTimer(CommonFunc):
    def __init__(self):
        CommonFunc.__init__(self)
        
        self.started_tick_ = 0
        self.paused_tick_ = 0
        
        self.is_paused_ = False
        self.is_started_ = False
        
    def start(self):
        self.is_started_ = True
        self.is_paused_ = False
        self.started_tick_ = pygame.time.get_ticks()
        
    def stop(self):
        self.is_started_ = False
        self.is_paused_ = False
    
    def pause(self):
        if self.is_started_ and not self.is_paused_:
            # self.is_started_ = False
            self.is_paused_ = True
            self.paused_tick_ = pygame.time.get_ticks()
        
    def unPause(self):
        if self.is_paused_:
            self.is_paused_ = False
            self.started_tick_ = pygame.time.get_ticks() - self.paused_tick_
            self.paused_tick_ = 0
            
    def get_ticks(self):
        if self.is_started_:
            if self.is_paused_:
                return self.paused_tick_
            else:
                return pygame.time.get_ticks() - self.started_tick_
            
        return 0
    