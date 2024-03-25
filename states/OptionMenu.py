import pygame, os
from states.State import State
from states.Playground import Playground
from states.Map1 import Map1
from RWFile import HandleFile
from states.CommonFunc import *
from states.Character import Character
from states.ThreatsObject import ThreatsObject
from states.ItemObject import ItemObject
from states.ImpTimer import ImpTimer
from states.Geometric import *
from states.GameMap import *

class OptionMenu(State, CommonFunc):
    def __init__(self, game):
        State.__init__(self, game)
        CommonFunc.__init__(self)
        
        self.game = game
        
        self.img_background = pygame.image.load(os.path.join(self.game.background_dir, "Henesys.png"))
        
        self.stats = HandleFile.loadFile(self.game.char_dir, "stats.json")
        self.items = HandleFile.loadFile(self.game.char_dir, "items.json")
        
        self.game_map = GameMap(game)
        self.p_player = Character(game)
        self.fps_timer = ImpTimer()
        
        self.WHITE_COLOR = ColorData(255, 255, 255)
        self.BLACK_COLOR = ColorData(0, 0, 0)
        self.ORANGE_COLOR = ColorData(222, 138, 66)
        
        self.vicious_box = pygame.Rect(500, 382, 170, 157)
        self.vicious_bg = pygame.image.load(os.path.join(self.game.char_dir, "vicious.png"))
        
        self.shop_bg = None
        self.backFromShop_box = pygame.Rect(583, 129, 160, 30)
        self.buyItem_box = pygame.Rect(583, 169, 160, 30)
        self.sellItem_box = pygame.Rect(904, 144, 160, 30)
        
        self.item_buyer = None
        self.item_seller = None
        
        # Buyer
        self.HP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_buyer.png"))
        self.MP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_buyer.png"))
        self.phitieu1_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_buyer.png"))
        self.phitieu2_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_buyer.png"))
        
        self.HPItemBuyer_box = pygame.Rect(437, 266, 306, 45)
        self.MPItemBuyer_box = pygame.Rect(437, 316, 306, 45)
        self.phitieu1ItemBuyer_box = pygame.Rect(437, 366, 306, 45)
        self.phitieu2ItemBuyer_box = pygame.Rect(437, 416, 306, 45)
        
        # Seller
        self.HP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_seller.png"))
        self.MP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_seller.png"))
        self.phitieu1_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_seller.png"))
        self.phitieu2_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_seller.png"))
        
        self.HPItemSeller_box = pygame.Rect(759, 266, 306, 45)
        self.MPItemSeller_box = pygame.Rect(759, 316, 306, 45)
        self.phitieu1ItemSeller_box = pygame.Rect(759, 366, 306, 45)
        self.phitieu2ItemSeller_box = pygame.Rect(759, 416, 306, 45)
        
        # Jay
        self.jay_bg = pygame.image.load(os.path.join(self.game.char_dir, "jay.png"))
        self.jay_box = pygame.Rect(815, 420, 125, 121)
        
        self.jay_message = None
        self.yes_box = pygame.Rect(900, 465, 50, 20)
        self.no_box = pygame.Rect(955, 465, 50, 20)
        
        # Bag
        self.items_list: list[ItemObject] = []
        
        self.bag_bg = None
        self.items_bag_rect = []
        self.items_rect = []
        self.item_selected = -1
        self.dragging = False
        self.drop = False
        
        self.close_bag_box = pygame.Rect(1268, 117, 19, 19)
        
        # SKILL
        self.skills_bg = None
        
        self.close_skills_box = pygame.Rect(288, 117, 19, 19)
        self.add_skills_box = pygame.Rect(294, 199, 15, 15)

    def update(self, actions, screen):
        
        self.fps_timer.start()
        self.p_player.handleInputAction(actions)
        
        stats = HandleFile.loadFile(self.game.char_dir, "stats.json")
        items = HandleFile.loadFile(self.game.char_dir, "items.json")
        
        if actions["up"]:
            self.p_player.input_type_.up_ = 1
        else:
            self.p_player.input_type_.up_ = 0
            
        if actions["left"] and self.vicious_box.collidepoint(pygame.mouse.get_pos()):
            self.shop_bg = pygame.image.load(os.path.join(self.game.items_dir, "shop.png"))
            self.HP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_buyer.png"))
            self.MP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_buyer.png"))
        
        if actions["left"] and self.backFromShop_box.collidepoint(pygame.mouse.get_pos()):
            self.shop_bg = None
        
        if actions["left"] and self.HPItemBuyer_box.collidepoint(pygame.mouse.get_pos()):
            self.item_buyer = "HP"
            self.HP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_buyer_active.png"))
            self.MP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_buyer.png"))
            self.phitieu1_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_buyer.png"))
            self.phitieu2_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_buyer.png"))
            
        if actions["left"] and self.MPItemBuyer_box.collidepoint(pygame.mouse.get_pos()):
            self.item_buyer = "MP"
            self.MP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_buyer_active.png"))
            self.HP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_buyer.png"))
            self.phitieu1_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_buyer.png"))
            self.phitieu2_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_buyer.png"))
            
        if actions["left"] and self.phitieu1ItemBuyer_box.collidepoint(pygame.mouse.get_pos()):
            self.item_buyer = "star_normal"
            self.MP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_buyer.png"))
            self.HP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_buyer.png"))
            self.phitieu1_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_buyer_active.png"))
            self.phitieu2_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_buyer.png"))
            
        if actions["left"] and self.phitieu2ItemBuyer_box.collidepoint(pygame.mouse.get_pos()):
            self.item_buyer = "star_special"
            self.MP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_buyer.png"))
            self.HP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_buyer.png"))
            self.phitieu1_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_buyer.png"))
            self.phitieu2_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_buyer_active.png"))
        
        # Seller
        if actions["left"] and self.HPItemSeller_box.collidepoint(pygame.mouse.get_pos()):
            self.item_seller = "HP"
            self.HP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_seller_active.png"))
            self.MP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_seller.png"))
            self.phitieu1_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_seller.png"))
            self.phitieu2_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_seller.png"))
            
        if actions["left"] and self.MPItemSeller_box.collidepoint(pygame.mouse.get_pos()):
            self.item_seller = "MP"
            self.MP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_seller_active.png"))
            self.HP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_seller.png"))
            self.phitieu1_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_seller.png"))
            self.phitieu2_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_seller.png"))
            
        if actions["left"] and self.phitieu1ItemSeller_box.collidepoint(pygame.mouse.get_pos()):
            self.item_seller = "star_normal"
            self.MP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_seller.png"))
            self.HP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_seller.png"))
            self.phitieu1_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_seller_active.png"))
            self.phitieu2_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_seller.png"))
            
        if actions["left"] and self.phitieu2ItemSeller_box.collidepoint(pygame.mouse.get_pos()):
            self.item_seller = "star_special"
            self.MP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_seller.png"))
            self.HP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_seller.png"))
            self.phitieu1_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_seller.png"))
            self.phitieu2_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_seller_active.png"))
        
        if actions["left"] and self.buyItem_box.collidepoint(pygame.mouse.get_pos()):
            if self.item_buyer == "HP" and stats["meso"] > 500:
                items["HP"] += 1
                stats["meso"] -= 500
            if self.item_buyer == "MP" and stats["meso"] > 1000:
                items["MP"] += 1
                stats["meso"] -= 1000
            if self.item_buyer == "star_normal" and stats["meso"] > 1000:
                items["star_normal"] += 50
                stats["meso"] -= 1000
            if self.item_buyer == "star_special" and stats["meso"] > 2000:
                items["star_special"] += 50
                stats["meso"] -= 2000
        
        if actions["left"] and self.sellItem_box.collidepoint(pygame.mouse.get_pos()):
            if self.item_seller == "HP" and stats["HP"] > 0:
                items["HP"] -= 1
                stats["meso"] += 250
            if self.item_seller == "MP" and stats["MP"] > 0:
                items["MP"] -= 1
                stats["meso"] += 500
            if self.item_seller == "star_normal" and stats["meso"] > 1000:
                items["star_normal"] -= 50
                stats["meso"] += 500
            if self.item_seller == "star_special" and stats["meso"] > 2000:
                items["star_special"] -= 50
                stats["meso"] += 1000
            
        # Bag
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
        # Skill
        if actions["k_k"]:
            if self.skills_bg:
                self.skills_bg = None
            else:
                self.skills_bg = pygame.image.load(os.path.join(self.game.items_dir, "skills.png"))
        
        if actions["left"] and self.close_skills_box.collidepoint(pygame.mouse.get_pos()):
            self.skills_bg = None
        
        if actions["left"] and self.add_skills_box.collidepoint(pygame.mouse.get_pos()) and stats["point_skill"] > 0:
            stats["point_skill"] -= 1
            stats["skill"]["level"] += 1
            stats["skill"]["damage"] += 100
            stats["skill"]["mana"] += 3
            if stats["skill"]["level"] % 5  == 0:
                stats["skill"]["numOfMonsters"] += 1
        
        
        # Jay
        if actions["left"] and self.jay_box.collidepoint(pygame.mouse.get_pos()):
            self.jay_message = pygame.image.load(os.path.join(self.game.char_dir, "jay_message.png"))
            
        if actions["left"] and self.no_box.collidepoint(pygame.mouse.get_pos()):
            self.jay_message = None
            
        if actions["left"] and self.yes_box.collidepoint(pygame.mouse.get_pos()):
            self.jay_message = None
            self.game.background_sound.stop()
            self.game.map1_sound.play(loops=-1)
            self.game.startTime = pygame.time.get_ticks()
            self.game.inMap = 1
            
            new_state = Map1(self.game)
            new_state.enter_state()
            
        HandleFile.saveFile(self.game.char_dir, "stats.json", stats)
        HandleFile.saveFile(self.game.char_dir, "items.json", items)
        self.game.reset_keys()
    
    def handleCollisionPickUp(self):
        if self.p_player.input_type_.pickUp_ == 1:
            object1 = Rect(self.p_player.x_pos_, self.p_player.y_pos_, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT)
            for i in range(len(self.items_list)):
                object2 = Rect(self.items_list[i].x_pos_, self.items_list[i].y_pos_, self.items_list[i].width_frame_, self.items_list[i].height_frame_)
                if CommonFunc.checkCollision(object1, object2):
                    stats = HandleFile.loadFile(self.game.char_dir, "stats.json")
                    items = HandleFile.loadFile(self.game.char_dir, "items.json")
                    if "meso" in self.items_list[i].item_type:
                        stats["meso"] += self.items_list[i].num
                        
                    # else:
                    elif "HP" in self.items_list[i].item_type:
                        items["HP"] += self.items_list[i].num
                    elif "MP" in self.items_list[i].item_type:
                        items["MP"] += self.items_list[i].num
                    elif "star_normal" in self.items_list[i].item_type:
                        items["star_normal"] += self.items_list[i].num
                    elif "star_special" in self.items_list[i].item_type:
                        items["star_special"] += self.items_list[i].num 
                    elif "key" in self.items_list[i].item_type:
                        items["key"] += self.items_list[i].num 
                    elif "sword" in self.items_list[i].item_type:
                        items["sword"] += self.items_list[i].num 
                    elif "pike" in self.items_list[i].item_type:
                        items["pike"] += self.items_list[i].num 
                    elif "wood" in self.items_list[i].item_type:
                        items["wood"] += self.items_list[i].num    
                        
                    self.items_list.pop(i)
                    self.p_player.input_type_.pickUp_ = 0
                    
                    HandleFile.saveFile(self.game.char_dir, "stats.json", stats)
                    HandleFile.saveFile(self.game.char_dir, "items.json", items)
                    return

    def renderItems(self, display, map_data):
        for item in self.items_list:
            item.doPlayer(map_data)
            item.setMapXY(map_data[0].start_x_[0], map_data[0].start_y_[0])
            item.show(display)

    def renderShop(self, display):
        display.blit(self.shop_bg, (426, 110))
        display.blit(self.HP_item_buyer_bg, (437, 266))
        display.blit(self.MP_item_buyer_bg, (437, 316))
        display.blit(self.phitieu1_item_buyer_bg, (437, 366))
        display.blit(self.phitieu2_item_buyer_bg, (437, 416))
        
        display.blit(self.HP_item_seller_bg, (759, 266))
        display.blit(self.MP_item_seller_bg, (759, 316))
        display.blit(self.phitieu1_item_seller_bg, (759, 366))
        display.blit(self.phitieu2_item_seller_bg, (759, 416))
        
        meso_string = CommonFunc.chuyen_chuoi_thanh_chuoi_dinh_dang_so(str(self.stats["meso"]))
        meso_text = self.game.medium_font.render(meso_string, True, self.BLACK_COLOR.getColor())
        meso_pos = (970, 194)
        display.blit(meso_text, meso_pos)
        
        # for i in range(4):
        HP_string = str(self.items["HP"])
        HP_text = self.game.small_font.render(HP_string, True, self.BLACK_COLOR.getColor())
        HP_pos = (760, 300)
        display.blit(HP_text, HP_pos)
        
        MP_string = str(self.items["MP"])
        MP_text = self.game.small_font.render(MP_string, True, self.BLACK_COLOR.getColor())
        MP_pos = (760, 350)
        display.blit(MP_text, MP_pos)
        
        star_normal_string = str(self.items["star_normal"])
        star_normal_text = self.game.small_font.render(star_normal_string, True, self.BLACK_COLOR.getColor())
        star_normal_pos = (760, 400)
        display.blit(star_normal_text, star_normal_pos)
        
        star_special_string = str(self.items["star_special"])
        star_special_text = self.game.small_font.render(star_special_string, True, self.BLACK_COLOR.getColor())
        star_special_pos = (760, 450)
        display.blit(star_special_text, star_special_pos)

    def renderBag(self, display):
        if self.bag_bg:
            stats = HandleFile.loadFile(self.game.char_dir, "stats.json")
            items = HandleFile.loadFile(self.game.char_dir, "items.json")
            display.blit(self.bag_bg, (1100, 110))
            
            meso_string = CommonFunc.chuyen_chuoi_thanh_chuoi_dinh_dang_so(str(stats["meso"]))
            meso_text = self.game.medium_font.render(meso_string, True, self.BLACK_COLOR.getColor())
            meso_pos = (1152, 414)
            display.blit(meso_text, meso_pos)            

            O_x = 1106
            O_y = 205
            index = 0
            self.items_bag_rect = []
            self.items_rect = []
            for key in items:
                if items[key] != 0:
                    
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
                            item_drop = ItemObject(self.game, self.p_player.x_pos_, self.p_player.y_pos_ - 35, key + "_drop", items[key])
                            items[key] = 0
                            self.items_list.append(item_drop)
                            continue
                        else:
                            item_rect.x, item_rect.y = pygame.mouse.get_pos()
                    
                    imageName = str(key) + ".png"
                    image = pygame.image.load(os.path.join(self.game.items_dir, imageName))
                    pos = (item_rect.x, item_rect.y)
                    display.blit(image, pos)
                    
                    string = str(items[key])
                    text = self.game.small_med_font.render(string, True, self.BLACK_COLOR.getColor())
                    pos = (O_x, O_y)
                    O_x += 47
                    display.blit(text, pos)
                    index += 1
                
                    if index % 4 == 0:
                        O_x = 1106
                        O_y += 47

            HandleFile.saveFile(self.game.char_dir, "stats.json", stats)
            HandleFile.saveFile(self.game.char_dir, "items.json", items)

    def renderSkills(self, display):
        if not self.skills_bg: 
            return
        
        display.blit(self.skills_bg, (120, 110))
        
        point_skill_string = str(self.stats["skill"]["level"])
        point_skill_text = self.game.small_med_font.render(point_skill_string, True, self.BLACK_COLOR.getColor())
        point_skill_pos = (177, 200)
        display.blit(point_skill_text, point_skill_pos)
        
        point_skill_string = str(self.stats["point_skill"])
        point_skill_text = self.game.small_med_font.render(point_skill_string, True, self.BLACK_COLOR.getColor())
        point_skill_pos = (265, 416)
        display.blit(point_skill_text, point_skill_pos)

    def render(self, display):
        display.blit(self.img_background, (0,0))
        
        self.stats = HandleFile.loadFile(self.game.char_dir, "stats.json")
        self.items = HandleFile.loadFile(self.game.char_dir, "items.json")
        
        self.game_map.loadMap(os.path.join(self.game.map_dir, "henesys.txt"))
        
        map_data = self.game_map.game_map_
        
        self.p_player.doPlayer(map_data)
        
        self.p_player.setMapXY(map_data[0].start_x_[0], map_data[0].start_y_[0])
        self.game_map.setMap(map_data)
        self.game_map.drawMap(display)
        
        display.blit(self.vicious_bg, (500, 382))
        display.blit(self.jay_bg, (815, 420))
        
        self.p_player.show(display)
        
        self.renderItems(display, map_data)
        
        self.p_player.handleBullet(display)
        
        self.handleCollisionPickUp()
        
        self.renderBag(display)
        self.renderSkills(display)
        
        # self.stats = HandleFile.loadFile(self.game.char_dir, "stats.json")
        # self.items = HandleFile.loadFile(self.game.char_dir, "items.json")
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
                    new_state = Playground(self.game)
                    new_state.enter_state()
                    self.p_player.input_type_.up_ = 0
        
        if self.jay_message:
            display.blit(self.jay_message, (400, 210))
            
        if self.shop_bg:
            self.renderShop(display)
            
        HandleFile.saveFile(self.game.char_dir, "stats.json", self.stats)
        HandleFile.saveFile(self.game.char_dir, "items.json", self.items)
        
        real_imp_time = self.fps_timer.get_ticks()
        time_one_frame = 1000 / self.FRAME_PER_SECOND
        
        if (real_imp_time < time_one_frame):
            delay_time = time_one_frame - real_imp_time
            if delay_time > 0:
                pygame.time.delay(int(delay_time))
