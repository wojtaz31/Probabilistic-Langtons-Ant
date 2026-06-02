import numpy as np
from settings import COLOR_WHITE, COLOR_BLACK

class Grid:
    def __init__(self, size: int):
        self.size = size
        self.board = np.full((size, size, 3), COLOR_WHITE, dtype=np.uint8)

    def color_pixel(self, x: int, y: int, color: tuple = COLOR_BLACK):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.board[x, y] = color

    def get_surface_array(self) -> np.ndarray:
        return self.board