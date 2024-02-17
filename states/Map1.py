import pygame, os, random
from states.State import State
from states.CommonFunc import *
from states.Character import Character
from states.ThreatsObject import ThreatsObject
from states.ItemObject import ItemObject
from states.Map2 import Map2
from states.ImpTimer import ImpTimer
from states.Geometric import *
from states.GameMap import *
from RWFile import HandleFile
import random

class Map1(State, CommonFunc):
    def __init__(self, game):
        State.__init__(self,game)
        CommonFunc.__init__(self)
        
        self.game.loginBackground_sound.stop()
        self.game.background_sound.stop()
        self.game.background_sound.play(loops=-1)
        
        self.game = game
        
        self.setMap = False
        
        self.img_background = pygame.image.load(os.path.join(self.game.background_dir, "map1.png"))
        
        self.stats = HandleFile.loadFile(self.game.char_dir, "stats.json")
        self.items = HandleFile.loadFile(self.game.char_dir, "items.json")
        
        self.game_map = GameMap(game)
        self.p_player = Character(game)
        self.fps_timer = ImpTimer()
        
        self.WHITE_COLOR = ColorData(255, 255, 255)
        self.ORANGE_COLOR = ColorData(222, 138, 66)
        
        self.startTimeToCollision = pygame.time.get_ticks()
        self.indexCollision = -1
        
        self.dynamic_threats_list: list[ThreatsObject] = ThreatsObject.makeThreatsList(self)
        self.items_list: list[ItemObject] = []
        self.mesos = 0
        
        self.WHITE_COLOR = ColorData(255, 255, 255)
        self.BLACK_COLOR = ColorData(0, 0, 0)
        self.ORANGE_COLOR = ColorData(222, 138, 66)
        
        # self.bag_bg = pygame.image.load(os.path.join(self.game.items_dir, "bag.png"))
        self.bag_bg = None
        self.items_bag_rect = []
        self.items_rect = []
        self.item_selected = -1
        self.dragging = False
        self.drop = False
        
        self.close_bag_box = pygame.Rect(1268, 117, 19, 19)
        
        # Handle open new map
        self.open_map = False
        self.timeToOpenMap = 0

    def update(self, actions, mouse_pos):
        # Check if the game was paused 
        # if actions["pause"]:
        #     new_state = PauseMenu(self.game)
        #     new_state.enter_state()
        self.fps_timer.start()
        self.p_player.handleInputAction(actions)
        
        if actions["up"]:
            self.p_player.input_type_.up_ = 1
        else:
            self.p_player.input_type_.up_ = 0
        
        if actions["k_i"]:
            if self.bag_bg:
                self.bag_bg = None
                self.item_selected = -1
                self.dragging = False
            else:
                self.bag_bg = pygame.image.load(os.path.join(self.game.items_dir, "bag.png"))
                self.item_selected = -1
                self.dragging = False
        
        if actions["left"] and self.close_bag_box.collidepoint(pygame.mouse.get_pos()):
            self.bag_bg = None
            self.item_selected = -1
            self.dragging = False
        
        if actions["left"] and self.dragging:
            self.drop = True
        
        for i in range(len(self.items_rect)):
            if actions["left"] and self.items_rect[i].collidepoint(pygame.mouse.get_pos()):
                if not self.dragging:
                    self.item_selected = i
                    self.dragging = True

        self.game.reset_keys()

    def handleCollisionBulletAndMonster(self, display):
        for i in range(len(self.p_player.bullet_list_)):
            for j in range(len(self.dynamic_threats_list)):
                object1 = Rect(self.p_player.bullet_list_[i].x_pos_, self.p_player.bullet_list_[i].y_pos_, self.p_player.bullet_list_[i].width_frame_, self.p_player.bullet_list_[i].height_frame_)
                object2 = Rect(self.dynamic_threats_list[j].x_pos_, self.dynamic_threats_list[j].y_pos_, self.dynamic_threats_list[j].width_frame_, self.dynamic_threats_list[j].height_frame_)

                if CommonFunc.checkCollision(object1, object2):
                    damage = 0
                    
                    if self.p_player.bullet_list_[i].name == "star_special":
                        if self.p_player.bullet_list_[i].skill == "ctrl":
                            damage = self.stats["attack"] + 15
                        elif self.p_player.bullet_list_[i].skill == "v":
                            damage = self.stats["skill_2"]["damage"] + 15

                    elif self.p_player.bullet_list_[i].name == "star_normal":
                        if self.p_player.bullet_list_[i].skill == "ctrl":
                            damage = self.stats["attack"]
                        elif self.p_player.bullet_list_[i].skill == "v":
                            damage = self.stats["skill_2"]["damage"]
                    
                    if self.dynamic_threats_list[j].id in self.p_player.bullet_list_[i].numOfHitMonster:
                        continue
                    
                    if self.dynamic_threats_list[j].HP < damage:
                        self.dynamic_threats_list = ThreatsObject.removeMonster(j, self.dynamic_threats_list)
                        # drop pike
                        randProb = random.randint(0, 9)
                        if randProb > 3:
                            pikeName = "pike_drop"
                            item = ItemObject(self.game, object2.x, object2.y, pikeName, 1)
                            self.items_list.append(item)
                        
                    else:
                        self.dynamic_threats_list[j].HP -= damage
                    
                    damage_string = str(damage)
                    damage_text = self.game.huge_font.render(damage_string, True, self.WHITE_COLOR.getColor(), self.ORANGE_COLOR.getColor())
                    damage_pos = (self.dynamic_threats_list[j].x_pos_ + self.MONSTER_WIDTH / 2 - self.dynamic_threats_list[j].map_x_[0], self.dynamic_threats_list[j].y_pos_ - 20 - self.dynamic_threats_list[j].map_y_[0])
                    display.blit(damage_text, damage_pos)
                    
                    
                    if self.p_player.bullet_list_[i].numOfMonster == 1:
                        self.p_player.bullet_list_ = self.p_player.removeBullet(i)
                    else:
                        self.p_player.bullet_list_[i].numOfHitMonster.append(self.dynamic_threats_list[j].id)
                        self.p_player.bullet_list_[i].numOfMonster -= 1
                    return

    def handleCollisionCharacterAndMonster(self):
        object1 = Rect(self.p_player.x_pos_, self.p_player.y_pos_, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT)
        for i in range(len(self.dynamic_threats_list)):
            object2 = Rect(self.dynamic_threats_list[i].x_pos_, self.dynamic_threats_list[i].y_pos_, self.dynamic_threats_list[i].width_frame_, self.dynamic_threats_list[i].height_frame_)
            
            if CommonFunc.checkCollision(object1, object2):
                currentTime = pygame.time.get_ticks() - self.startTimeToCollision
                if currentTime >= 2000:
                    self.stats["HP"] -= 10
                    self.startTimeToCollision = pygame.time.get_ticks()
                    return

    def handleCollisionPickUp(self):
        if self.p_player.input_type_.pickUp_ == 1:
            object1 = Rect(self.p_player.x_pos_, self.p_player.y_pos_, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT)
            for i in range(len(self.items_list)):
                object2 = Rect(self.items_list[i].x_pos_, self.items_list[i].y_pos_, self.items_list[i].width_frame_, self.items_list[i].height_frame_)
                if CommonFunc.checkCollision(object1, object2):
                    if "meso" in self.items_list[i].item_type:
                        self.stats["meso"] += self.items_list[i].num
                        
                    # else:
                    elif "HP" in self.items_list[i].item_type:
                        self.items["HP"] += self.items_list[i].num
                    elif "MP" in self.items_list[i].item_type:
                        self.items["MP"] += self.items_list[i].num
                    elif "star_normal" in self.items_list[i].item_type:
                        self.items["star_normal"] += self.items_list[i].num
                    elif "star_special" in self.items_list[i].item_type:
                        self.items["star_special"] += self.items_list[i].num 
                    elif "key" in self.items_list[i].item_type:
                        self.items["key"] += self.items_list[i].num 
                    elif "sword" in self.items_list[i].item_type:
                        self.items["sword"] += self.items_list[i].num 
                    elif "pike" in self.items_list[i].item_type:
                        self.items["pike"] += self.items_list[i].num 
                    elif "wood" in self.items_list[i].item_type:
                        self.items["wood"] += self.items_list[i].num    
                        
                    self.items_list.pop(i)
                    self.p_player.input_type_.pickUp_ = 0
                    return

    def renderItems(self, display, map_data):
        for item in self.items_list:
            item.setMapXY(map_data[0].start_x_[0], map_data[0].start_y_[0])
            item.show(display)
            
    def renderBag(self, display):
        if self.bag_bg:
            display.blit(self.bag_bg, (1100, 110))
            
            meso_string = CommonFunc.chuyen_chuoi_thanh_chuoi_dinh_dang_so(str(self.stats["meso"]))
            meso_text = self.game.medium_font.render(meso_string, True, self.BLACK_COLOR.getColor())
            meso_pos = (1152, 414)
            display.blit(meso_text, meso_pos)            

            O_x = 1106
            O_y = 205
            index = 0
            self.items_bag_rect = []
            self.items_rect = []
            for key in self.items:
                if self.items[key] != 0:
                    
                    item_rect = Rect(O_x, O_y - 33, 45, 45)
                    self.items_bag_rect.append(item_rect)
                    
                    item_rect = pygame.Rect(O_x, O_y - 33, 45, 45)
                    self.items_rect.append(item_rect)
                    
                    if self.item_selected == index and self.dragging:
                        # Geometric.renderOutline(item_rect, ColorData(105, 147, 255), display, 3, 2)
                        if self.drop:
                            item_rect.x, item_rect.y = self.p_player.x_pos_, self.p_player.y_pos_ - 30
                            self.dragging = False
                            self.item_selected = -1
                            self.drop = False
                            item_drop = ItemObject(self.game, self.p_player.x_pos_, self.p_player.y_pos_ - 35, key + "_drop", self.items[key])
                            self.items[key] = 0
                            self.items_list.append(item_drop)
                            continue
                        else:
                            item_rect.x, item_rect.y = pygame.mouse.get_pos()
                    
                    imageName = str(key) + ".png"
                    image = pygame.image.load(os.path.join(self.game.items_dir, imageName))
                    pos = (item_rect.x, item_rect.y)
                    display.blit(image, pos)
                    
                    string = str(self.items[key])
                    text = self.game.small_med_font.render(string, True, self.BLACK_COLOR.getColor())
                    pos = (O_x, O_y)
                    O_x += 47
                    display.blit(text, pos)
                    index += 1
                
                    if index % 4 == 0:
                        O_x = 1106
                        O_y += 47

    def updateMap_data(self, map_data: list[Map]):
        for i in range(len(map_data[0].tile)):
            for j in range(len(map_data[0].tile[i])):
                if map_data[0].tile[i][j] == 1009:
                    map_data[0].tile[i][j] = 1005
                if map_data[0].tile[i][j] == 1010:
                    map_data[0].tile[i][j] = 1006
                if map_data[0].tile[i][j] == 1011:
                    map_data[0].tile[i][j] = 1007
                if map_data[0].tile[i][j] == 1012:
                    map_data[0].tile[i][j] = 1008
        return map_data
            

    def render(self, display):
        display.blit(self.img_background, (0,0))
        
        if not self.setMap:
            self.game_map.loadMap(os.path.join(self.game.map_dir, "map1.txt"))
            self.setMap = True
        
        map_data = self.game_map.game_map_

        self.p_player.doPlayer(map_data)
        
        self.p_player.setMapXY(map_data[0].start_x_[0], map_data[0].start_y_[0])
        self.game_map.setMap(map_data)
        self.game_map.drawMap(display)
        
        self.p_player.show(display)
            
        for i in range(len(self.dynamic_threats_list)):
            self.dynamic_threats_list[i].impMoveType()
            self.dynamic_threats_list[i].doPlayer(map_data)
            self.dynamic_threats_list[i].setMapXY(map_data[0].start_x_[0], map_data[0].start_y_[0])
            self.dynamic_threats_list[i].show(display)
        
        self.renderItems(display, map_data)
        
        self.p_player.handleBullet(display)
        
        self.handleCollisionBulletAndMonster(display)
        self.handleCollisionCharacterAndMonster()
        self.handleCollisionPickUp()
        
        self.renderBag(display)
        
        HandleFile.saveFile(self.game.char_dir, "stats.json", self.stats)
        HandleFile.saveFile(self.game.char_dir, "items.json", self.items)
        
        Geometric.renderSpecifications(self, display)
        
        if self.p_player.input_type_.up_ == 1:
            x1 = int(self.p_player.x_pos_ / self.TILE_SIZE)
            x2 = int((self.p_player.x_pos_ + self.CHARACTER_WIDTH - 1) / self.TILE_SIZE)
            
            y1 = int(self.p_player.y_pos_ / self.TILE_SIZE)
            y2 = int((self.p_player.y_pos_ + self.CHARACTER_HEIGHT - 1) / self.TILE_SIZE)
            
            if  x1 >= 0 and x2 < map_data[0].max_map_x_ and \
                y1 >= 0 and y2 < map_data[0].max_map_y_:
                value_1 = map_data[0].tile[y1][x1]
                if value_1 > self.MAP_TILE and value_1 <= self.MAP_BACK_TILE:
                    self.exit_state()
                    self.p_player.input_type_.up_ = 0
                elif value_1 > self.MAP_BACK_TILE and value_1 <= self.MAP_NEXT_TILE:
                    new_state = Map2(self.game)
                    new_state.enter_state()
                    self.p_player.input_type_.up_ = 0
        
        for i in range(len(self.items_list)):
            if self.items_list[i].item_type == "pike_drop" and self.items_list[i].num > 20:
                x1 = int(self.items_list[i].x_pos_ / self.TILE_SIZE)
                x2 = int((self.items_list[i].x_pos_ + self.CHARACTER_WIDTH - 1) / self.TILE_SIZE)
                
                y1 = int(self.items_list[i].y_pos_ / self.TILE_SIZE)
                y2 = int((self.items_list[i].y_pos_ + self.CHARACTER_HEIGHT - 1) / self.TILE_SIZE)
                
                if  x1 >= 0 and x2 < map_data[0].max_map_x_ and \
                    y1 >= 0 and y2 < map_data[0].max_map_y_:
                    value_1 = map_data[0].tile[y1][x1]
                    if value_1 > self.MAP_NEXT_TILE:
                        if not self.open_map:
                            self.open_map = True
                            self.timeToOpenMap = pygame.time.get_ticks()
                        if self.open_map and (pygame.time.get_ticks() - self.timeToOpenMap) > 3000:
                            map_data = self.updateMap_data(map_data)
                            self.items_list.pop(i)
                            break
                        
        real_imp_time = self.fps_timer.get_ticks()
        time_one_frame = 1000 / self.FRAME_PER_SECOND
        
        if (real_imp_time < time_one_frame):
            delay_time = time_one_frame - real_imp_time
            if delay_time > 0:
                pygame.time.delay(int(delay_time + 0))
