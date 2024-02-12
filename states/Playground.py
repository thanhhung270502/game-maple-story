import pygame, os, random
from states.State import State
from states.CommonFunc import *
from states.Character import Character
from states.ThreatsObject import ThreatsObject
from states.ItemObject import ItemObject
from states.ImpTimer import ImpTimer
from states.Geometric import *
from states.GameMap import *
from RWFile import HandleFile
import random

class Playground(State, CommonFunc):
    def __init__(self, game):
        State.__init__(self,game)
        CommonFunc.__init__(self)
        
        self.game.loginBackground_sound.stop()
        self.game.background_sound.stop()
        self.game.background_sound.play(loops=-1)
        
        self.game = game
        
        self.img_background = pygame.image.load(os.path.join(self.game.background_dir, "huntingArea.png"))
        
        self.stats = HandleFile.loadFile(self.game.char_dir, "stats.json")
        
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
                            print(damage)
                        elif self.p_player.bullet_list_[i].skill == "v":
                            damage = self.stats["skill_2"]["damage"] + 15

                    elif self.p_player.bullet_list_[i].name == "star_normal":
                        if self.p_player.bullet_list_[i].skill == "ctrl":
                            damage = self.stats["attack"]
                            print(damage)
                        elif self.p_player.bullet_list_[i].skill == "v":
                            damage = self.stats["skill_2"]["damage"]
                    
                    if self.dynamic_threats_list[j].HP < damage:
                        self.dynamic_threats_list = ThreatsObject.removeMonster(j, self.dynamic_threats_list)
                        meso = "meso1"
                        if self.dynamic_threats_list[j].monster == "squid":
                            meso = "meso3"
                        item = ItemObject(self.game, object2.x, object2.y, meso)
                        self.items_list.append(item)
                    else:
                        self.dynamic_threats_list[j].HP -= damage
                    
                    damage_string = str(damage)
                    damage_text = self.game.huge_font.render(damage_string, True, self.WHITE_COLOR.getColor(), self.ORANGE_COLOR.getColor())
                    damage_pos = (self.dynamic_threats_list[j].x_pos_ + self.MONSTER_WIDTH / 2, self.dynamic_threats_list[j].y_pos_ - 20)
                    display.blit(damage_text, damage_pos)
                    
                    if self.p_player.bullet_list_[i].numOfMonster == 1 and self.dynamic_threats_list[j].id not in self.p_player.bullet_list_[i].numOfHitMonster:
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
        
        self.handleCollisionBulletAndMonster(display)
        self.handleCollisionCharacterAndMonster()
        self.handleCollisionPickUp()
        
        Geometric.renderSpecifications(self, display)
        
        if self.p_player.input_type_.up_ == 1:
            x1 = int(self.p_player.x_pos_ / self.TILE_SIZE)
            x2 = int((self.p_player.x_pos_ + self.CHARACTER_WIDTH - 1) / self.TILE_SIZE)
            
            y1 = int(self.p_player.y_pos_ / self.TILE_SIZE)
            y2 = int((self.p_player.y_pos_ + self.CHARACTER_HEIGHT - 1) / self.TILE_SIZE)
            
            if  x1 >= 0 and x2 < map_data[0].max_map_x_ and \
                y1 >= 0 and y2 < map_data[0].max_map_y_:
                value_1 = map_data[0].tile[y1][x1]
                if value_1 > self.MAP_TILE:
                    self.exit_state()
                    self.p_player.input_type_.up_ = 0
        
        real_imp_time = self.fps_timer.get_ticks()
        time_one_frame = 1000 / self.FRAME_PER_SECOND
        
        if (real_imp_time < time_one_frame):
            delay_time = time_one_frame - real_imp_time
            if delay_time > 0:
                pygame.time.delay(int(delay_time + 50))
