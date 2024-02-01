class CommonFunc:
    def __init__(self):
        self.SCREEN_WIDTH = 1500
        self.SCREEN_HEIGHT = 720
        self.CHARACTER_WIDTH = 70
        self.CHARACTER_HEIGHT = 70
        self.SCREEN_BPP = 32
        
        self.NUM_OF_FRAME = 4

        self.COLOR_KEY_R = 167
        self.COLOR_KEY_G = 175
        self.COLOR_KEY_B = 180

        self.RENDER_DRAW_COLOR = 255

        self.BLANK_TILE = 0
        self.TILE_SIZE = 60

        self.MAX_MAP_X = 100
        self.MAX_MAP_Y = 12
        self.move = {"right": 0, "left": 1, "up": 2, "down": 3, "jump": 4}

class Input:
    def __init__(self) -> None:
        self.left_ = 0
        self.right_ = 0
        self.up_ = 0
        self.down_ = 0
        self.jump_ = 0
        self.prevStep_ = 0

class Map:
    def __init__(self):
        self.start_x_ = 0
        self.start_y_ = 0
        
        self.max_x_ = 0
        self.max_y_ = 0
        
        self.tile = []
        self.fileName = ""
        
class Rect:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h