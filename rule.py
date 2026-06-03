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

    def is_valid(self) -> bool:
        if not self.actions or not self.next_colors:
            return False

        action_prob_sum = sum(prob for _, prob in self.actions)
        color_prob_sum = sum(prob for _, prob in self.next_colors)

        return abs(action_prob_sum - 1.0) < 1e-6 and abs(color_prob_sum - 1.0) < 1e-6
