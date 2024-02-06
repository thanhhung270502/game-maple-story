import pygame, os, random
from states.State import State
from states.Result import Result
from RWFile import HandleFile
from states.CommonFunc import *
from states.Character import Character
from states.ThreatsObject import ThreatsObject
from states.ItemObject import ItemObject
from states.ImpTimer import ImpTimer
from states.Geometric import *
import random
import json
# from states.PauseMenu import PauseMenu

class Playground(State, CommonFunc):
    def __init__(self, game, level, weapon):
        State.__init__(self,game)
        CommonFunc.__init__(self)
        self.COLORWHITE = (255, 255, 255)
        
        self.game = game
        
        self.img_background = pygame.image.load(os.path.join(self.game.background_dir, "Henesys.png"))
        self.actions = []
        self.startGame = False
        self.startTime = pygame.time.get_ticks()
        self.countdown = 6
        self.countdownTime = self.countdown
        self.weapon = weapon
        self.level = level
        self.game_map = GameMap(game)
        
        self.p_player = Character(game)
        self.fps_timer = ImpTimer()
        
        self.startTimeToCollision = pygame.time.get_ticks()
        self.indexCollision = -1
        
        self.HP = 900
        self.HP_max_ = 1000
        self.MP = 400
        self.MP_max_ = 500
        
        self.EXP = 1500
        self.EXP_max_ = 15000
        
        self.specifications_rect_ = Rect(550, 680, 400, 40)
        self.HP_rect_ = Rect(560, 696, 120, 20)
        self.MP_rect_ = Rect(690, 696, 120, 20)
        self.EXP_rect_ = Rect(820, 696, 120, 20)
        
        self.whiteColor_ = ColorData(255, 255, 255)
        
        # self.threats_list: [ThreatsObject] = []
        
        self.dynamic_threats_list: [ThreatsObject] = self.makeThreatsList()
        self.items_list: [ItemObject] = []
        self.mesos = 0
        
    def makeThreatsList(self):
        dynamic_threats_list: [ThreatsObject] = []
        
        for i in range(10):
            p_threat = ThreatsObject(self.game, 500 + i * 300, 200, "squid") 
            p_threat.animation_a_ = p_threat.x_pos_ - 200
            p_threat.animation_b_ = p_threat.x_pos_ + 200
            p_threat.type_move_ = self.type_move["move_in_space_threat"]
            p_threat.input_type_.left_ = 1
            dynamic_threats_list.append(p_threat)
        
        # for i in range(10):
        #     p_threat = ThreatsObject(self.game, 700 + i * 1200, 200)
        #     p_threat.type_move_ = self.type_move["static_threat"]
        #     p_threat.input_type_.left_ = 0
        #     dynamic_threats_list.append(p_threat)

        return dynamic_threats_list

    def update(self, actions, mouse_pos):
        # Check if the game was paused 
        # if actions["pause"]:
        #     new_state = PauseMenu(self.game)
        #     new_state.enter_state()
        self.fps_timer.start()
        self.p_player.handleInputAction(actions)
        
        self.game.reset_keys()
        pass

    def removeMonster(self, index):
        size = len(self.dynamic_threats_list)
        if size > 0 and index < size:
            self.dynamic_threats_list.pop(index)
        return self.dynamic_threats_list
    
    def handleCollisionBulletAndMonster(self):
        for i in range(len(self.p_player.bullet_list_)):
            for j in range(len(self.dynamic_threats_list)):
                object1 = Rect(self.p_player.bullet_list_[i].x_pos_, self.p_player.bullet_list_[i].y_pos_, self.p_player.bullet_list_[i].width_frame_, self.p_player.bullet_list_[i].height_frame_)
                object2 = Rect(self.dynamic_threats_list[j].x_pos_, self.dynamic_threats_list[j].y_pos_, self.dynamic_threats_list[j].width_frame_, self.dynamic_threats_list[j].height_frame_)

                if CommonFunc.checkCollision(object1, object2):
                    self.p_player.bullet_list_ = self.p_player.removeBullet(i)
                    
                    if self.dynamic_threats_list[j].HP < self.p_player.damage:
                        self.dynamic_threats_list = self.removeMonster(j)
                        meso = "meso1"
                        if self.dynamic_threats_list[j].monster == "squid":
                            meso = "meso3"
                        item = ItemObject(self.game, object2.x, object2.y, meso)
                        self.items_list.append(item)
                    else:
                        self.dynamic_threats_list[j].HP -= self.p_player.damage
                    
                    return
                
    def handleCollisionCharacterAndMonster(self):
        object1 = Rect(self.p_player.x_pos_, self.p_player.y_pos_, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT)
        for i in range(len(self.dynamic_threats_list)):
            object2 = Rect(self.dynamic_threats_list[i].x_pos_, self.dynamic_threats_list[i].y_pos_, self.dynamic_threats_list[i].width_frame_, self.dynamic_threats_list[i].height_frame_)
            
            if CommonFunc.checkCollision(object1, object2):
                currentTime = pygame.time.get_ticks() - self.startTimeToCollision
                if currentTime >= 2000:
                    self.HP -= 10
                    self.startTimeToCollision = pygame.time.get_ticks()
                    return

    def handleCollisionPickUp(self):
        if self.p_player.input_type_.pickUp_ == 1:
            object1 = Rect(self.p_player.x_pos_, self.p_player.y_pos_, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT)
            for i in range(len(self.items_list)):
                object2 = Rect(self.items_list[i].x_pos_, self.items_list[i].y_pos_, self.items_list[i].width_frame_, self.items_list[i].height_frame_)
                if CommonFunc.checkCollision(object1, object2):
                    print("here")
                    meso = 0
                    if self.items_list[i].item == "meso1":
                        meso = random.randint(50, 200)
                    elif self.items_list[i].item == "meso2":
                        meso = random.randint(200, 500)
                    elif self.items_list[i].item == "meso3":
                        meso = random.randint(500, 1000)
                    elif self.items_list[i].item == "meso4":
                        meso = random.randint(1000, 5000)
                    
                    self.mesos += meso
                    self.items_list.pop(i)
                    self.p_player.input_type_.pickUp_ = 0
                    return
                        

    def renderSpecifications(self, display):
        font = pygame.font.SysFont("Arial", 10, True)
        Geometric.renderRectangle(self.specifications_rect_, ColorData(43, 54, 57), display, 5)
        
        # HP
        Geometric.renderRectangle(self.HP_rect_, ColorData(255, 255, 255), display, 3)
        
        HP_rect = Rect(560, 696, 120, 20)
        if self.HP != self.HP_max_:
            HP_rect.w = int((self.HP / self.HP_max_) * 120)
        Geometric.renderRectangle(HP_rect, ColorData(248, 4, 2), display, 3)
        
        HP_string = "HP : [ " + str(self.HP) + " / " + str(self.HP_max_) + " ]" 
        HP_text = font.render(HP_string, True, self.whiteColor_.getColor())
        HP_position = (560, 684)
        display.blit(HP_text, HP_position)
        
        # MP
        Geometric.renderRectangle(self.MP_rect_, ColorData(255, 255, 255), display, 3)
        
        MP_rect = Rect(690, 696, 120, 20)
        if self.MP != self.MP_max_:
            MP_rect.w = int((self.MP / self.MP_max_) * 120)
        Geometric.renderRectangle(MP_rect, ColorData(0, 133, 249), display, 3)
        
        MP_string = "MP : [ " + str(self.MP) + " / " + str(self.MP_max_) + " ]" 
        MP_text = font.render(MP_string, True, self.whiteColor_.getColor())
        MP_position = (690, 684)
        display.blit(MP_text, MP_position)
        
        # Exp
        Geometric.renderRectangle(self.EXP_rect_, ColorData(255, 255, 255), display, 3)
        
        EXP_rect = Rect(820, 696, 120, 20)
        if self.EXP != self.EXP_max_:
            EXP_rect.w = int((self.EXP / self.EXP_max_) * 120)
        Geometric.renderRectangle(EXP_rect, ColorData(228, 242, 58), display, 3)
        
        exp_percent = float(self.EXP / self.EXP_max_)
        EXP_string = "EXP : " + str(self.EXP) + " [" + str(exp_percent) +  "%]" 
        EXP_text = font.render(EXP_string, True, self.whiteColor_.getColor())
        EXP_position = (820, 684)
        display.blit(EXP_text, EXP_position)

    def renderItems(self, display, map_data):
        for item in self.items_list:
            item.setMapXY(map_data[0].start_x_[0], map_data[0].start_y_[0])
            item.show(display)

    def render(self, display):
        display.blit(self.img_background, (0,0))
        
        self.game_map.loadMap(os.path.join(self.game.map_dir, "map.txt"))
        
        map_data = self.game_map.game_map_
        
        self.p_player.doPlayer(map_data)
        
        self.p_player.setMapXY(map_data[0].start_x_[0], map_data[0].start_y_[0])
        self.game_map.setMap(map_data)
        self.game_map.drawMap(display)
        
        for i in range(len(self.dynamic_threats_list)):
            self.dynamic_threats_list[i].impMoveType()
            self.dynamic_threats_list[i].doPlayer(map_data)
            self.dynamic_threats_list[i].setMapXY(map_data[0].start_x_[0], map_data[0].start_y_[0])
            self.dynamic_threats_list[i].show(display)

        self.p_player.show(display)
        self.renderItems(display, map_data)
        
        self.p_player.handleBullet(display)
        
        self.handleCollisionBulletAndMonster()
        # self.handleCollisionCharacterAndMonster()
        self.handleCollisionPickUp()
        
        self.renderSpecifications(display)
        
        
        real_imp_time = self.fps_timer.get_ticks()
        time_one_frame = 1000 / self.FRAME_PER_SECOND
        
        if (real_imp_time < time_one_frame):
            delay_time = time_one_frame - real_imp_time
            if delay_time > 0:
                pygame.time.delay(int(delay_time + 50))
        # pygame.time.delay(30)
        

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
                    if val < 5: 
                        imageName = str(val) + ".png"
                        image = pygame.image.load(os.path.join(self.game.map_dir, imageName))
                        imagePos = (j, i)
                        display.blit(image, imagePos)
                map_x += 1
                j += self.TILE_SIZE
            map_y += 1
            i += self.TILE_SIZE