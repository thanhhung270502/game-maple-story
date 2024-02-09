import pygame, os
from states.State import State
from states.Playground import Playground
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
        
        self.vicious_box = pygame.Rect(670, 382, 170, 157)
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

    def update(self, actions, screen):
        self.fps_timer.start()
        self.p_player.handleInputAction(actions)
        
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
            self.item_buyer = "phitieu1"
            self.MP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_buyer.png"))
            self.HP_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_buyer.png"))
            self.phitieu1_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_buyer_active.png"))
            self.phitieu2_item_buyer_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_buyer.png"))
            
        if actions["left"] and self.phitieu2ItemBuyer_box.collidepoint(pygame.mouse.get_pos()):
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
            self.item_seller = "phitieu1"
            self.MP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_seller.png"))
            self.HP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_seller.png"))
            self.phitieu1_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_seller_active.png"))
            self.phitieu2_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_seller.png"))
            
        if actions["left"] and self.phitieu2ItemSeller_box.collidepoint(pygame.mouse.get_pos()):
            self.MP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "MP_item_seller.png"))
            self.HP_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "HP_item_seller.png"))
            self.phitieu1_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu1_item_seller.png"))
            self.phitieu2_item_seller_bg = pygame.image.load(os.path.join(self.game.items_dir, "phitieu2_item_seller_active.png"))
        
        self.game.reset_keys()
        
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
        
        meso_string = str(self.stats["meso"])
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

    def render(self, display):
        display.blit(self.img_background, (0,0))
        display.blit(self.vicious_bg, (670, 382))
        
        self.game_map.loadMap(os.path.join(self.game.map_dir, "henesys.txt"))
        
        map_data = self.game_map.game_map_
        
        self.p_player.doPlayer(map_data)
        
        self.p_player.setMapXY(map_data[0].start_x_[0], map_data[0].start_y_[0])
        self.game_map.setMap(map_data)
        self.game_map.drawMap(display)
        
        self.p_player.show(display)
        
        self.p_player.handleBullet(display)
        
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
        
        
        if self.shop_bg:
            self.renderShop(display)
        
        real_imp_time = self.fps_timer.get_ticks()
        time_one_frame = 1000 / self.FRAME_PER_SECOND
        
        if (real_imp_time < time_one_frame):
            delay_time = time_one_frame - real_imp_time
            if delay_time > 0:
                pygame.time.delay(int(delay_time + 50))
