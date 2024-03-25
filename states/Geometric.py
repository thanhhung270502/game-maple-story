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
    
    def renderOutline(geo_size: Rect, color_data: ColorData, display, border_size, border_width): 
        pygame.draw.rect(display, color_data.getColor(), geo_size.getRect(), border_width, -1, border_size, -1, border_size, -1)
    
    def renderSpecifications(self, display):
        self.small_font = pygame.font.SysFont("Arial", 10, True)
        self.medium_font = pygame.font.SysFont("Arial", 15, True)
        self.large_font = pygame.font.SysFont("Arial", 20, True)
        Geometric.renderRectangle(self.specifications_rect_, ColorData(43, 54, 57), display, 5)
        
        # HP
        Geometric.renderRectangle(self.HP_rect_, ColorData(255, 255, 255), display, 3)
        
        HP_rect = self.HP_rect_.copy()
        if self.stats["HP"] != self.stats["HP_max"]:
            HP_rect.w = int((self.stats["HP"] / self.stats["HP_max"]) * 120)
        Geometric.renderRectangle(HP_rect, ColorData(248, 4, 2), display, 3)
        
        HP_string = "HP : [ " + str(self.stats["HP"]) + " / " + str(self.stats["HP_max"]) + " ]" 
        HP_text = self.small_font.render(HP_string, True, self.WHITE_COLOR.getColor())
        HP_position = (self.HP_rect_.x, self.HP_rect_.y - 12)
        display.blit(HP_text, HP_position)
        
        # MP
        Geometric.renderRectangle(self.MP_rect_, ColorData(255, 255, 255), display, 3)
        
        MP_rect = self.MP_rect_.copy()
        if self.stats["MP"] != self.stats["MP_max"]:
            MP_rect.w = int((self.stats["MP"] / self.stats["MP_max"]) * 120)
        Geometric.renderRectangle(MP_rect, ColorData(0, 133, 249), display, 3)
        
        MP_string = "MP : [ " + str(self.stats["MP"]) + " / " + str(self.stats["MP_max"]) + " ]" 
        MP_text = self.small_font.render(MP_string, True, self.WHITE_COLOR.getColor())
        MP_position = (self.MP_rect_.x, self.MP_rect_.y - 12)
        display.blit(MP_text, MP_position)
        
        # Exp
        Geometric.renderRectangle(self.EXP_rect_, ColorData(255, 255, 255), display, 3)
        
        EXP_rect = self.EXP_rect_.copy()
        if self.stats["EXP"] != self.stats["EXP_max"]:
            EXP_rect.w = int((self.stats["EXP"] / self.stats["EXP_max"]) * 120)
        Geometric.renderRectangle(EXP_rect, ColorData(228, 242, 58), display, 3)
        
        exp_percent = float(self.stats["EXP"] / self.stats["EXP_max"])
        exp_percent = round(exp_percent, 4) * 100
        EXP_string = "EXP : " + str(self.stats["EXP"]) + " [" + str(exp_percent) +  "%]" 
        EXP_text = self.small_font.render(EXP_string, True, self.WHITE_COLOR.getColor())
        EXP_position = (self.EXP_rect_.x, self.EXP_rect_.y - 12)
        display.blit(EXP_text, EXP_position)
        
        # Level
        Geometric.renderRectangle(self.LEVEL_rect_, ColorData(30, 30, 39), display, 3)
        
        LEVEL_string = "Level. " + str(self.stats["level"]) 
        LEVEL_text = self.medium_font.render(LEVEL_string, True, self.ORANGE_COLOR.getColor())
        LEVEL_position = (self.LEVEL_rect_.x + 7, self.LEVEL_rect_.y + 7)
        display.blit(LEVEL_text, LEVEL_position)
        
        # Footbar
        footbar_image = pygame.image.load(os.path.join(self.game.background_dir, "footbar.png"))
        display.blit(footbar_image, (485, 678))
    
    def renderHPBoss(self, display, boss):
        display.blit(self.boss_image, (750, 0))
        Geometric.renderRectangle(self.bossHP_rect_, ColorData(255, 255, 255), display, 5)
        
        HP_rect = self.bossHP_rect_.copy()
        print(boss.HP, self.monsters["boss"]["HP"])
        if boss.HP < self.monsters["boss"]["HP"]:
            HP_rect.w = int((boss.HP / self.monsters["boss"]["HP"]) * 800)
        Geometric.renderRectangle(HP_rect, ColorData(206, 0, 0), display, 5)
        
    def renderTimeLeft(self, display):
        if self.game.startTime >= 0:
            timeLeft_bg = pygame.image.load(os.path.join(self.game.background_dir, "time_left.png"))
            display.blit(timeLeft_bg, (515, 65))
            
            # huge_font = pygame.font.SysFont('comicsansms', 72) 
            
            self.game.countdownTime = int(self.game.countdown - (pygame.time.get_ticks() - self.game.startTime) / 1000)
            
            if self.game.countdownTime > 2:
                minutes = (self.game.countdownTime - 2) // 60
                remaining_seconds = (self.game.countdownTime - 2) % 60
                countdownString = str(minutes) + " : " + str(remaining_seconds)
                
                countdownText = self.game.Huge_font.render(str(countdownString), True, self.COLORWHITE)
                countdownPosition = countdownText.get_rect()
                countdownPosition.center = (750, 120)
                display.blit(countdownText, countdownPosition)
            
            else:
                # if self.game.inMap == 1:
                self.exit_state()