import numpy as np
import random
from settings import COLOR_WHITE, COLOR_BLACK


class Grid:
    def __init__(self, size: int):
        self.size = size
        self.board = np.full((size, size, 3), COLOR_WHITE, dtype=np.uint8)
        self.rules = {}
        self.ants = []

    def color_pixel(self, x: int, y: int, color: tuple = COLOR_BLACK):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.board[x, y] = color

    def add_rule(self, rule):
        self.rules[rule.color] = rule

    def add_ant(self, ant):
        self.ants.append(ant)

    def get_surface_array(self) -> np.ndarray:
        return self.board

    def step(self):
        for ant in self.ants:
            if 0 <= ant.x < self.size and 0 <= ant.y < self.size:

                raw_color = self.board[ant.x, ant.y]
                current_color = (int(raw_color[0]), int(raw_color[1]), int(raw_color[2]))

                if current_color in self.rules:
                    rule = self.rules[current_color]

                    actions = [a[0] for a in rule.actions]
                    action_probs = [a[1] for a in rule.actions]
                    chosen_action = random.choices(actions, weights=action_probs, k=1)[0]

                    colors = [c[0] for c in rule.next_colors]
                    color_probs = [c[1] for c in rule.next_colors]
                    chosen_color = random.choices(colors, weights=color_probs, k=1)[0]

                    self.board[ant.x, ant.y] = chosen_color

                    ant.rotate(chosen_action)

            ant.move()