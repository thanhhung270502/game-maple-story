import pygame, os
from states.CommonFunc import *
from states.State import State
from states.Bullet import Bullet
from RWFile import HandleFile

class Character(State, CommonFunc):
    def __init__(self, game):
        State.__init__(self, game)
        CommonFunc.__init__(self)
        
        self.game = game
        
        self.x_val_ = 0
        self.y_val_ = 0
        
        self.x_pos_ = 0
        self.y_pos_ = 0
        
        self.map_x_ = [0]
        self.map_y_ = [0]
        
        self.frame_clip_ = []

        self.input_type_ = Input()
        
        self.frame_ = 0
        self.status_ = 0
        
        self.on_ground_ = False
        
        self.imageName = "moveRight"
        
        self.stats = HandleFile.loadFile(self.game.char_dir, "stats.json")
        
        self.mesos = 0
        
        self.bullet_list_: [Bullet] = []
        
        self.damage = 2
    
    def setMapXY(self, x, y):
        self.map_x_[0] = x
        self.map_y_[0] = y

    def show(self, display):
        self.updateImagePlayer()
        
        # When moving, this frame will increase
        if self.input_type_.left_ == 1 or self.input_type_.right_ == 1:
            self.frame_ += 1
        else:
            self.frame_ = 0
            
        if self.frame_ >= self.NUM_OF_FRAME:
            self.frame_ = 0
        
        rect_x = self.x_pos_ - self.map_x_[0]
        rect_y = self.y_pos_ - self.map_y_[0]
        
        imageName = self.imageName + str(self.frame_) + ".png"
        image = pygame.image.load(os.path.join(self.game.char_dir, imageName))
        display.blit(image, (rect_x, rect_y))

    def updateImagePlayer(self):
        if self.on_ground_:
            if self.status_ == self.move["left"]:
                self.imageName = "moveLeft"
            else:
                self.imageName = "moveRight"
        else:
            if self.status_ == self.move["left"]:
                self.imageName = "jumpLeft"
            else:
                self.imageName = "jumpRight"

    def handleInputAction(self, actions):
        if actions["moveLeft"]:
            self.status_ = self.move["left"]
            self.input_type_.left_ = 1
            self.input_type_.right_ = 0
        elif actions["moveRight"]:
            self.status_ = self.move["right"]
            self.input_type_.left_ = 0
            self.input_type_.right_ = 1
        else:
            self.input_type_.left_ = 0
            self.input_type_.right_ = 0

        if actions["moveJump"]:
            self.input_type_.jump_ = 1
        else:
            self.input_type_.jump_ = 0

        if actions["normalAttack"]:
            bullet = Bullet(self.game, self.x_pos_ + int(self.CHARACTER_WIDTH / 2), self.y_pos_ + int(self.CHARACTER_HEIGHT / 2), self.status_, self.stats["bullet"], "ctrl")
            bullet.is_move_ = True
            self.bullet_list_.append(bullet)
        elif actions["k_v"]:
            bullet = Bullet(self.game, self.x_pos_ + int(self.CHARACTER_WIDTH / 2), self.y_pos_ + int(self.CHARACTER_HEIGHT / 3), self.status_, self.stats["bullet"], "v")
            bullet.is_move_ = True
            self.bullet_list_.append(bullet)
        
        if actions["k_3"]:
            self.stats["bullet"] = "star_normal"
            HandleFile.saveFile(self.game.char_dir, "stats.json", self.stats)
        elif actions["k_4"]:
            self.stats["bullet"] = "star_special"
            HandleFile.saveFile(self.game.char_dir, "stats.json", self.stats)
            # bullet = Bullet(self.game, self.x_pos_ + int(self.CHARACTER_WIDTH / 2), self.y_pos_ + int(self.CHARACTER_HEIGHT / 3), self.status_, self.stats["bullet"], "v")
            # bullet.is_move_ = True
            # self.bullet_list_.append(bullet)
            
        if actions["pickUp"]:
            self.input_type_.pickUp_ = 1
        else:
            self.input_type_.pickUp_ = 0

    def handleBullet(self, display):
        length = len(self.bullet_list_)
        i = 0
        while(i < length):
            if self.bullet_list_[i].is_move_:
                self.bullet_list_[i].handleMove(self.x_pos_ + self.DISTANCE_OF_BULLET, self.x_pos_ - self.DISTANCE_OF_BULLET)
                image = pygame.image.load(os.path.join(self.game.bullet_dir, "phitieu1_1.png"))
                
                if self.bullet_list_[i].name == "star_special":
                    if self.bullet_list_[i].skill == "ctrl" or self.bullet_list_[i].skill == "c":
                        image = pygame.image.load(os.path.join(self.game.bullet_dir, "phitieu2_1.png"))
                    elif self.bullet_list_[i].skill == "v":
                        image = pygame.image.load(os.path.join(self.game.bullet_dir, "phitieu2_2.png"))
                
                elif self.bullet_list_[i].name == "star_normal":
                    if self.bullet_list_[i].skill == "v":
                        image = pygame.image.load(os.path.join(self.game.bullet_dir, "phitieu1_2.png"))
                
                rect_x = self.bullet_list_[i].x_pos_ - self.map_x_[0]
                rect_y = self.bullet_list_[i].y_pos_ - self.map_y_[0]
                
                display.blit(image, (rect_x, rect_y))
                i += 1
            else:
                self.bullet_list_.pop(i)
                length -= 1

    def removeBullet(self, index):
        size = len(self.bullet_list_)
        if size > 0 and index < size:
            self.bullet_list_.pop(index)
            
        return self.bullet_list_

    def doPlayer(self, map_data: [Map]):
        self.x_val_= 0
        self.y_val_ += self.GRAVITY_SPEED
        
        if self.y_val_ >= self.MAX_FALL_SPEED:
            self.y_val_ = self.MAX_FALL_SPEED
        
        if self.input_type_.left_ == 1:
            self.x_val_ -= self.PLAYER_SPEED
        elif self.input_type_.right_ == 1:
            self.x_val_ += self.PLAYER_SPEED
        if self.input_type_.jump_ == 1:
            if (self.on_ground_ == True):
                self.y_val_ = -self.PLAYER_JUMP
                self.input_type_.jump_ = 0
                self.on_ground_ = False
                
        
        self.checkToMap(map_data)
        self.centerCharacterOnMap(map_data)

    def centerCharacterOnMap(self, map_data: [Map]):
        if self.x_pos_ + (self.SCREEN_WIDTH / 2) < (map_data[0].max_map_x_ * self.TILE_SIZE):
            map_data[0].start_x_[0] = self.x_pos_ - (self.SCREEN_WIDTH / 2)
            if map_data[0].start_x_[0] < 0:
                map_data[0].start_x_[0] = 0
            elif (map_data[0].start_x_[0] + self.SCREEN_WIDTH >= map_data[0].max_x_):
                map_data[0].start_x_[0] = map_data[0].max_x_ - self.SCREEN_WIDTH
        else:
            map_data[0].start_x_[0] = map_data[0].max_map_x_ * self.TILE_SIZE - self.SCREEN_WIDTH
        # map_data[0].start_y_[0] = self.y_pos_ - (self.SCREEN_HEIGHT / 2)
        # if map_data[0].start_y_[0] < 0:
        #     map_data[0].start_y_[0] = 0
        # elif (map_data[0].start_y_[0] + self.SCREEN_HEIGHT >= map_data[0].max_y_ * 2):
        #     map_data[0].start_y_[0] = map_data[0].max_y_ - self.SCREEN_HEIGHT

    def checkToMap(self, map_data: [Map]):
        x1, x2, y1, y2 = 0, 0, 0, 0
        
        # Check horizontal position
        height_min = self.CHARACTER_HEIGHT if self.CHARACTER_HEIGHT < self.TILE_SIZE else self.TILE_SIZE
        
        x1 = int((self.x_pos_ + self.x_val_) / self.TILE_SIZE)
        x2 = int((self.x_pos_ + self.x_val_ + self.CHARACTER_WIDTH - 1) / self.TILE_SIZE)
        
        y1 = int((self.y_pos_) / self.TILE_SIZE)
        y2 = int((self.y_pos_ + height_min - 1) / self.TILE_SIZE)
        
        if x1 >= 0 and x2 < map_data[0].max_map_x_ and y1 >= 0 and y2 < map_data[0].max_map_y_:
            if self.x_val_ > 0:
                value_1 = map_data[0].tile[y1][x2]
                value_2 = map_data[0].tile[y2][x2]
                if (value_1 > self.BLANK_TILE and value_1 < self.MAP_TILE) or \
                    (value_2 > self.BLANK_TILE and value_2 < self.MAP_TILE):
                    self.x_pos_ = x2 * self.TILE_SIZE
                    self.x_pos_ -= self.CHARACTER_WIDTH + 1
                    self.x_val_ = 0
            elif self.x_val_ < 0:
                value_1 = map_data[0].tile[y1][x1]
                value_2 = map_data[0].tile[y2][x1]
                if (value_1 > self.BLANK_TILE and value_2 < self.MAP_TILE) or \
                    (value_2 > self.BLANK_TILE and value_2 < self.MAP_TILE):
                    self.x_pos_ = (x1 + 1) * self.TILE_SIZE
                    self.x_val_ = 0
        
        # Check vertical position
        width_min = self.CHARACTER_WIDTH if self.CHARACTER_WIDTH < self.TILE_SIZE else self.TILE_SIZE
        
        x1 = int((self.x_pos_) / self.TILE_SIZE)
        x2 = int((self.x_pos_ + width_min) / self.TILE_SIZE)
        
        y1 = int((self.y_pos_ + self.y_val_) / self.TILE_SIZE)
        y2 = int((self.y_pos_ + self.y_val_ + self.CHARACTER_HEIGHT - 1) / self.TILE_SIZE)
        
        if x1 >= 0 and x2 < map_data[0].max_map_x_ and y1 >= 0 and y2 < map_data[0].max_map_y_:
            if self.y_val_ > 0:
                value_1 = map_data[0].tile[y2][x1]
                value_2 = map_data[0].tile[y2][x2]
                if (value_1 > self.BLANK_TILE and value_1 < self.MAP_TILE) or \
                    (value_2 > self.BLANK_TILE and value_2 < self.MAP_TILE):
                    self.y_pos_ = y2 * self.TILE_SIZE
                    self.y_pos_ -= self.CHARACTER_HEIGHT + 1
                    self.y_val_ = 0
                    self.on_ground_ = True
            elif self.y_val_ < 0:
                value_1 = map_data[0].tile[y1][x1]
                value_2 = map_data[0].tile[y1][x2]
                if (value_1 > self.BLANK_TILE and value_1 < self.MAP_TILE) or \
                    (value_2 > self.BLANK_TILE and value_2 < self.MAP_TILE):
                    self.x_pos_ = (x1 + 1) * self.TILE_SIZE
                    self.y_val_ = 0
                    self.on_ground_ = False
        
        self.x_pos_ += self.x_val_
        self.y_pos_ += self.y_val_
        
        if self.x_pos_ < 0:
            self.x_pos_ = 0
        elif self.x_pos_ + self.CHARACTER_WIDTH > map_data[0].max_x_:
            self.x_pos_ = map_data[0].max_x_ - self.CHARACTER_WIDTH - 1