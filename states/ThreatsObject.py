import pygame, os
from states.CommonFunc import *
from states.State import State

class ThreatsObject(State, CommonFunc):
    def __init__(self, game, x_pos, y_pos, monster, id):
        State.__init__(self, game)
        CommonFunc.__init__(self)
        
        self.monsters = HandleFile.loadFile(self.game.monster_dir, "statsOfMonster.json")
        
        self.x_val_ = 0
        self.y_val_ = 0
        self.x_pos_ = x_pos
        self.y_pos_ = y_pos
        self.id = id
        
        self.map_x_ = [0]
        self.map_y_ = [0]
        
        self.on_ground_ = True
        self.come_back_time_ = 0
        
        self.frame_clip_ = []
        self.frame_ = 0
        
        self.width_frame_ = self.monsters[monster]["width"]
        self.height_frame_ = self.monsters[monster]["height"]
        
        self.attack = self.monsters[monster]["attack"]
        
        self.HP = self.monsters[monster]["HP"]
        self.monster = monster
        
        self.imageName = ""
        if monster == "squid":
            self.imageName = "left_" + str(monster)
        elif monster == "boss":
            self.imageName = str(monster) + "_left_"
        elif monster == "box":
            self.imageName = str(monster)
        
        self.type_move_ = self.type_move["static_threat"]
        self.animation_a_ = 0
        self.animation_b_ = 0
        self.input_type_ = Input()
        self.input_type_.left_ = 1
        
        self.startTimeToStuck = -1

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
            
            if self.type_move_ == self.type_move["move_in_space_threat"]:
                imageName = self.imageName + str(self.frame_) + ".png"
                image = pygame.image.load(os.path.join(self.game.monster_dir, imageName))
            else:
                imageName = self.imageName + ".png"
                image = pygame.image.load(os.path.join(self.game.monster_dir, imageName))
            display.blit(image, (rect_x, rect_y))
            
    def doPlayer(self, map_data: list[Map]):
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
            
            if self.come_back_time_ == 0:
                self.initial()
    
    def checkToMap(self, map_data: list[Map]): 
        x1, x2, y1, y2 = 0, 0, 0, 0
        
        # Check horizontal position
        height_min = self.height_frame_ if self.height_frame_ < self.TILE_SIZE else self.TILE_SIZE
        
        # print(self.x_pos_)
        x1 = int((self.x_pos_ + self.x_val_) / self.TILE_SIZE)
        x2 = int((self.x_pos_ + self.x_val_ + self.width_frame_ - 1) / self.TILE_SIZE)
        
        y1 = int((self.y_pos_) / self.TILE_SIZE)
        y2 = int((self.y_pos_ + height_min - 1) / self.TILE_SIZE)
        
        if x1 >= 0 and x2 < map_data[0].max_map_x_ and y1 >= 0 and y2 < map_data[0].max_map_y_:
            if self.x_val_ > 0:
                value_1 = map_data[0].tile[y1][x2]
                value_2 = map_data[0].tile[y2][x2]
                # print("value_1: ", value_1, "; value_2: ", value_2)
                if (value_1 > self.BLANK_TILE and value_1 < self.MAP_X_TILE) or \
                    (value_2 > self.BLANK_TILE and value_2 < self.MAP_X_TILE):
                    self.x_pos_ = x2 * self.TILE_SIZE
                    self.x_pos_ -= self.width_frame_ + 1
                    self.x_val_ = 0
                    
                    if self.startTimeToStuck == -1:
                        self.startTimeToStuck = pygame.time.get_ticks()
                    
                    if (pygame.time.get_ticks() - self.startTimeToStuck) > 4000:
                        if self.input_type_.left_ == 1:
                            self.input_type_.right_ = 1
                            self.input_type_.left_ = 0
                            self.imageName = "right_" + str(self.monster)
                        elif self.input_type_.right_ == 1:
                            self.input_type_.left_ = 1
                            self.input_type_.right_ = 0
                            self.imageName = "left_" + str(self.monster)
                        self.startTimeToStuck = -1
            elif self.x_val_ < 0:
                value_1 = map_data[0].tile[y1][x1]
                value_2 = map_data[0].tile[y2][x1]
                if (value_1 > self.BLANK_TILE and value_2 < self.MAP_X_TILE) or \
                    (value_2 > self.BLANK_TILE and value_2 < self.MAP_X_TILE):
                    self.x_pos_ = (x1 + 1) * self.TILE_SIZE
                    self.x_val_ = 0
                if self.startTimeToStuck == -1:
                    self.startTimeToStuck = pygame.time.get_ticks()
                
                if (pygame.time.get_ticks() - self.startTimeToStuck) > 4000:
                    if self.input_type_.left_ == 1:
                        self.input_type_.right_ = 1
                        self.input_type_.left_ = 0
                        if self.monster == "boss":
                            self.imageName = str(self.monster)+ "_right_"
                        elif self.monster == "squid":
                            self.imageName = "right_" + str(self.monster)
                    elif self.input_type_.right_ == 1:
                        self.input_type_.left_ = 1
                        self.input_type_.right_ = 0
                        if self.monster == "boss":
                            self.imageName = str(self.monster)+ "_left_"
                        elif self.monster == "squid":
                            self.imageName = "left_" + str(self.monster)
                    self.startTimeToStuck = -1
        
        # Check vertical position
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
                    self.on_ground_ = True
            elif self.y_val_ < 0:
                value_1 = map_data[0].tile[y1][x1]
                value_2 = map_data[0].tile[y1][x2]
                if (value_1 > self.BLANK_TILE and value_1 < self.MAP_X_TILE) or \
                    (value_2 > self.BLANK_TILE and value_2 < self.MAP_X_TILE):
                    self.x_pos_ = (x1 + 1) * self.TILE_SIZE
                    self.y_val_ = 0
                    self.on_ground_ = False
        
        self.x_pos_ += self.x_val_
        self.y_pos_ += self.y_val_
        
        if self.x_pos_ < 0:
            self.x_pos_ = 0
        elif self.x_pos_ + self.width_frame_ > map_data[0].max_x_:
            self.x_pos_ = map_data[0].max_x_ - self.width_frame_ - 1
            
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
                    if self.monster == "squid":
                        self.imageName = "left_squid"
                    elif self.monster == "boss":
                        self.imageName = "boss_left_"
                elif self.x_pos_ < self.animation_a_:
                    self.input_type_.left_ = 0
                    self.input_type_.right_ = 1
                    if self.monster == "squid":
                        self.imageName = "right_squid"
                    elif self.monster == "boss":
                        self.imageName = "boss_right_"
            else:
                if self.input_type_.left_ == 1:
                    if self.monster == "squid":
                        self.imageName = "left_squid"
                    elif self.monster == "boss":
                        self.imageName = "boss_left_"
    
    def makeThreatsList(self):
        dynamic_threats_list: list[ThreatsObject] = []
        
        for i in range(20):
            p_threat = ThreatsObject(self.game, 500 + i * 300, 200, "squid", self.id_monsters) 
            self.id_monsters += 1
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
    
    def makeBoxList(self):
        box_list: list[ThreatsObject] = []
        
        p_threat = ThreatsObject(self.game, 30, 0, "box", self.id_monsters)
        self.id_monsters += 1
        p_threat.type_move_ = self.type_move["static_threat"]
        p_threat.input_type_.left_ = 0
        box_list.append(p_threat)
        
        p_threat = ThreatsObject(self.game, 450, 0, "box", self.id_monsters)
        self.id_monsters += 1
        p_threat.type_move_ = self.type_move["static_threat"]
        p_threat.input_type_.left_ = 0
        box_list.append(p_threat)
        
        p_threat = ThreatsObject(self.game, 900, 0, "box", self.id_monsters)
        self.id_monsters += 1
        p_threat.type_move_ = self.type_move["static_threat"]
        p_threat.input_type_.left_ = 0
        box_list.append(p_threat)
        
        return box_list
    
    def makeBoss(self):
        dynamic_threats_list: list[ThreatsObject] = []

        p_threat = ThreatsObject(self.game, 640, 0, "boss", self.id_monsters) 
        self.id_monsters += 1
        p_threat.animation_a_ = p_threat.x_pos_ - 500
        p_threat.animation_b_ = p_threat.x_pos_ + 500
        p_threat.type_move_ = self.type_move["move_in_space_threat"]
        p_threat.input_type_.left_ = 1
        dynamic_threats_list.append(p_threat)
        
        return dynamic_threats_list
    
    def spamMonster(self, monsters_list):
        for i in range(10):
            p_threat = ThreatsObject(self.game, 200 + i * 100, 200, "squid", self.id_monsters) 
            self.id_monsters += 1
            p_threat.animation_a_ = p_threat.x_pos_ - 400
            p_threat.animation_b_ = p_threat.x_pos_ + 400
            p_threat.type_move_ = self.type_move["move_in_space_threat"]
            p_threat.input_type_.left_ = 1
            monsters_list.append(p_threat)
        
        return monsters_list

    
    def removeMonster(index, dynamic_threats_list):
        size = len(dynamic_threats_list)
        if size > 0 and index < size:
            dynamic_threats_list.pop(index)
        return dynamic_threats_list