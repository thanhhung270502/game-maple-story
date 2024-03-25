import os, time, pygame
# Load our scenes
from states.Title import Title
from states.CommonFunc import CommonFunc

class Game(CommonFunc):
    def __init__(self):
        CommonFunc.__init__(self)
        pygame.init()
        pygame.mixer.init()

        self.CHARACTER_WIDTH = 80
        self.CHARACTER_HEIGHT = 90
        self.GAME_TITLE = 'Zombie Game'
        self.FPS = 120
        self.CHARACTER_WIDTH = 150
        self.CHARACTER_HEIGHT = 150
        self.FONT_TOP_MARGIN = 30
        self.LEVEL_SCORE_GAP = 4

        self.game_canvas = pygame.Surface((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))

        self.running, self.playing = True, True
        self.actions = {"left": False, "right": False, "up": False,
                        "pause" : False, "start" : False, 
                        "moveLeft": False, "moveRight": False, "moveUp": False, "moveDown": False,
                        "moveJump": False, "normalAttack": False, "pickUp": False,
                        "k_1": False, "k_2": False, "k_3": False, "k_4": False,
                        "k_c": False, "k_v": False, "k_b": False,
                        "k_i": False, "dragging": False, "k_k": False}
        self.mouse_pos = (0,0)
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.dragging = False
        
        self.countdown = 12
        self.countdownTime = self.countdown
        self.startTime = -1
        self.inMap = 0
        
        self.load_assets()
        self.load_states()

    def game_loop(self):
        self.load_sounds()
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()
                if mouse_click[0]:
                    self.actions['left'] = True
                    if self.play_pickup_sound:
                        self.pickup_sound.play()
                if mouse_click[2]:
                    self.actions['right'] = True
                    if self.play_pickup_sound:
                        self.pickup_sound.play()  # Play click sound
                self.mouse_pos = pygame.mouse.get_pos()
                
                self.dragging = not self.dragging
            self.actions["dragging"] = self.dragging
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.actions['pause'] = True
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True
                if event.key == pygame.K_LCTRL:
                    self.actions['normalAttack'] = True
                if event.key == pygame.K_SPACE:
                    self.actions['moveJump'] = True
                    self.jump_sound.play()
                if event.key == pygame.K_z:
                    self.actions['pickUp'] = True
                if event.key == pygame.K_UP:
                    self.actions["up"] = True
                if event.key == pygame.K_1:
                    self.actions["k_1"] = True
                if event.key == pygame.K_2:
                    self.actions["k_2"] = True
                if event.key == pygame.K_3:
                    self.actions["k_3"] = True
                if event.key == pygame.K_4:
                    self.actions["k_4"] = True
                if event.key == pygame.K_c:
                    self.actions["k_c"] = True
                if event.key == pygame.K_v:
                    self.actions["k_v"] = True
                if event.key == pygame.K_b:
                    self.actions["k_b"] = True
                if event.key == pygame.K_i:
                    self.actions["k_i"] = True
                if event.key == pygame.K_k:
                    self.actions["k_k"] = True
                self.mouse_pos = (0,0)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click = pygame.mouse.get_pressed()
                if mouse_click[0]:
                    self.actions['left'] = False
                if mouse_click[2]:
                    self.actions['right'] = False
                    
                # self.actions["dragging"] = False
                self.mouse_pos = pygame.mouse.get_pos()
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_ESCAPE:
            #         self.actions['pause'] = False   
            #     if event.key == pygame.K_RETURN:
            #         self.actions['start'] = False
            #     if event.key == pygame.K_LEFT:
            #         self.actions['moveLeft'] = False
            #     if event.key == pygame.K_RIGHT:
            #         self.actions['moveRight'] = False
            #     if event.key == pygame.K_UP:
            #         self.actions['moveUp'] = False
            #     if event.key == pygame.K_DOWN:
            #         self.actions['moveDown'] = False
            #     if event.key == pygame.K_BACKSPACE:
            #         self.actions['moveJump'] = False
            #     self.mouse_pos = (0,0)

        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_LEFT]:
            self.actions["moveLeft"] = True
        if userInput[pygame.K_RIGHT]:
            self.actions["moveRight"] = True
        # if userInput[pygame.K_SPACE]:
        #     print("backspace")
        #     self.actions['moveJump'] = True

    def update(self):
        self.state_stack[-1].update(self.actions, self.screen)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        # Render current state to the screen
        self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        #text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        # Create pointers to directories 
        self.assets_dir = os.path.join("./assets")
        self.map_dir = os.path.join(self.assets_dir, "map")
        self.char_dir = os.path.join(self.assets_dir, "characters")
        self.monster_dir = os.path.join(self.assets_dir, "monster")
        self.items_dir = os.path.join(self.assets_dir, "items")
        self.bullet_dir = os.path.join(self.assets_dir, "bullet")
        self.background_dir = os.path.join(self.assets_dir, "background")
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "fonts")
        self.sound_dir = os.path.join(self.assets_dir, "sounds")
        # self.huge_font = pygame.font.Font(os.path.join(self.font_dir, "font.ttf"), 70)
        # self.large_font = pygame.font.Font(os.path.join(self.font_dir, "font.ttf"), 50)
        # self.medium_font = pygame.font.Font(os.path.join(self.font_dir, "font.ttf"), 30)
        # self.medium_rare_font = pygame.font.Font(os.path.join(self.font_dir, "font.ttf"), 25)
        # self.small_font = pygame.font.Font(os.path.join(self.font_dir, "font.ttf"), 15)
        self.small_font = pygame.font.SysFont("Arial", 10, True)
        self.small_med_font = pygame.font.SysFont("Arial", 12, True)
        self.medium_font = pygame.font.SysFont("Arial", 15, True)
        self.large_font = pygame.font.SysFont("Arial", 20, True)
        self.huge_font = pygame.font.SysFont("Arial", 30, True)
        self.Huge_font = pygame.font.SysFont("Verdana", 70, True)
        
        # Courier New

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def load_sounds(self):
        self.background_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "henesys.mp3"))
        self.loginBackground_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "login.mp3"))

        self.play_pickup_sound = True
        self.pickup_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "pickup.wav"))
        
        self.punch_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "punch.wav"))
        self.explosion_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "explosion.wav"))
        self.wrong_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "wrong.mp3"))
        
        self.map1_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "map1.mp3"))
        self.map2_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "map2.mp3"))
        self.map3_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "map3.mp3"))

        self.jump_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "jump.mp3"))
        self.hit_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "hit.mp3"))

        self.loginBackground_sound.play(loops=-1)


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()