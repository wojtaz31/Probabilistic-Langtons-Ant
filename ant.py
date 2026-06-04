from action import Action

DIR_OFFSETS = {
    "UP": (0, -1),
    "RIGHT": (1, 0),
    "DOWN": (0, 1),
    "LEFT": (-1, 0)
}

DIR_ORDER = list(DIR_OFFSETS.keys())


class Ant:
    def __init__(self, x: int, y: int, direction: str):
        self.x = x
        self.y = y
        self.direction = direction

    def rotate(self, action: Action):
        idx = DIR_ORDER.index(self.direction)
        if action == Action.LEFT:
            idx = (idx - 1) % 4
        elif action == Action.RIGHT:
            idx = (idx + 1) % 4

        self.direction = DIR_ORDER[idx]

    def move(self):
        dx, dy = DIR_OFFSETS[self.direction]
        self.x += dx
        self.y += dy
