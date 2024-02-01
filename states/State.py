class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        
        self.MAX_MAP_X = 160
        self.MAX_MAP_Y = 40

    def update(self, delta_time, actions):
        pass
    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()