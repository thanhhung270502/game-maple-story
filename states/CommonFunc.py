from RWFile import HandleFile

class Rect:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
    
    def getRect(self):
        return (self.x, self.y, self.w, self.h)
        
    def print_rect(self):
        print("x: ", self.x, "; y: ", self.y)
        print("w: ", self.w, "; h: ", self.h)
    def copy(self):
        return Rect(self.x, self.y, self.w, self.h)
class CommonFunc():
    def __init__(self):
        self.SCREEN_WIDTH = 1500
        self.SCREEN_HEIGHT = 720
        
        self.CHARACTER_WIDTH = 70
        self.CHARACTER_HEIGHT = 70
        
        self.MONSTER_WIDTH = 60
        self.MONSTER_HEIGHT = 105
        
        self.SCREEN_BPP = 32
        
        self.NUM_OF_FRAME = 8

        self.COLOR_KEY_R = 167
        self.COLOR_KEY_G = 175
        self.COLOR_KEY_B = 180
        
        self.COLORWHITE = (255, 255, 255)

        self.RENDER_DRAW_COLOR = 255

        self.BLANK_TILE = 0
        self.MAP_TILE = 1000
        self.MAP_X_TILE = 500
        
        self.MAP_BACK_TILE = 1004
        self.MAP_NEXT_TILE = 1008
        
        self.TILE_SIZE = 60

        self.MAX_MAP_X = 25
        self.MAX_MAP_Y = 12
        self.move = {"right": 0, "left": 1, "up": 2, "down": 3}
        
        self.type_move = {"static_threat": 0, "move_in_space_threat": 1}
        self.items = {"meso1": (21, 20), "meso2": (21, 20), "meso3": (21, 20), "meso4": (21, 20), 
                      "HP_drop": (25, 25), "MP_drop": (25, 25), "star_normal_drop": (25, 25), "star_special_drop": (25, 25),
                      "pike_drop": (25, 25), "sword_drop": (25, 25), "wood_drop": (25, 25), "key_drop": (25, 25)}
        
        self.GRAVITY_SPEED = 10
        self.PLAYER_SPEED = 8
        self.MONSTER_SPEED = 4
        self.BULLET_SPEED = 24
        self.MAX_FALL_SPEED = 30
        self.PLAYER_JUMP = 32
        self.DISTANCE_OF_BULLET = 400
        
        self.FRAME_PER_SECOND = 1000      # fps
        
        self.id_monsters = 0
        
        # self.specifications_rect_ = Rect(550, 680, 400, 40)
        # self.HP_rect_ = Rect(560, 696, 120, 20)
        # self.MP_rect_ = Rect(690, 696, 120, 20)
        # self.EXP_rect_ = Rect(820, 696, 120, 20)
        
        self.specifications_rect_ = Rect(0, 680, 485, 40)
        self.HP_rect_ = Rect(95, 696, 120, 20)
        self.MP_rect_ = Rect(225, 696, 120, 20)
        self.EXP_rect_ = Rect(355, 696, 120, 20)
        self.LEVEL_rect_ = Rect(5, 685, 80, 30)
        
        self.bossHP_rect_ = Rect(800, 0, 700, 30)
        
    def checkCollision(object1: Rect, object2: Rect):
        left_a = object1.x
        right_a = object1.x + object1.w
        top_a = object1.y
        bottom_a = object1.y + object1.h
        
        left_b = object2.x
        right_b = object2.x + object2.w
        top_b = object2.y
        bottom_b = object2.y + object2.h
        
        # Case 1: size object 1 < size object 2
        if (left_a > left_b and left_a < right_b):
            if (top_a > top_b and (top_a < bottom_b)):
                return True
        
            if (bottom_a > top_b and bottom_a < bottom_b):
                return True
        
        if (right_a > left_b and right_a < right_b):
            if (top_a > top_b and top_a < bottom_b):
                return True
        
            if (bottom_a > top_b and bottom_a < bottom_b):
                return True
        
        # Case 2: size object 1 < size object 2
        if (left_b > left_a and left_b < right_a):
            if (top_b > top_a and top_b < bottom_a):
                return True
        
        if (left_b > left_a and left_b < right_a):
            if (bottom_b > top_a and bottom_b < bottom_a):
                return True

        if (right_b > left_a and right_b < right_a):
            if (top_b > top_a and top_b < bottom_a):
                return True
        
        if (right_b > left_a and right_b < right_a):
            if (bottom_b > top_a and bottom_b < bottom_a):
                return True
        
        # Case 3: size object 1 = size object 2
        if (top_a == top_b and right_a == right_b and bottom_a == bottom_b):
            return True
        
        return False

    def chuyen_chuoi_thanh_chuoi_dinh_dang_so(chuoi):
        # Chuyển chuỗi thành số nguyên
        so_nguyen = int(chuoi)
        
        # Sử dụng định dạng f-string để thêm dấu phẩy vào giữa các chữ số
        chuoi_ket_qua = f"{so_nguyen:,}"
        
        return str(chuoi_ket_qua)


class Input:
    def __init__(self) -> None:
        self.left_ = 0
        self.right_ = 0
        self.up_ = 0
        self.down_ = 0
        self.jump_ = 0
        self.prevStep_ = 0
        self.pickUp_ = 0
        self.menu_ = 0

class Map:
    def __init__(self):
        self.start_x_ = [0]
        self.start_y_ = [0]
        
        self.max_x_ = 0
        self.max_y_ = 0
        
        self.tile = []
        self.fileName = ""
        
        self.max_map_x_ = 0
        self.max_map_y_ = 0