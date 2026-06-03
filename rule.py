from typing import List, Tuple
from action import Action


class Rule:
    def __init__(self, color: tuple):
        self.color = color
        self.actions: List[Tuple[Action, float]] = []
        self.next_colors: List[Tuple[tuple, float]] = []

    def add_action(self, action: Action, probability: float):
        self.actions.append((action, probability))

    def add_next_color(self, next_color: tuple, probability: float):
        self.next_colors.append((next_color, probability))