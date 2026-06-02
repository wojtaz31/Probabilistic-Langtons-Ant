import pygame
import sys
from settings import WINDOW_SIZE, GRID_SIZE, COLOR_RED
from grid import Grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Stochastic Langton's Ant")

    grid = Grid(GRID_SIZE)

    center_x, center_y = GRID_SIZE // 2, GRID_SIZE // 2
    grid.color_pixel(center_x, center_y)
    grid.color_pixel(center_x + 1, center_y)
    grid.color_pixel(center_x, center_y + 1)
    grid.color_pixel(center_x + 1, center_y + 1, COLOR_RED)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface = pygame.surfarray.make_surface(grid.get_surface_array())

        scaled_surface = pygame.transform.scale(surface, (WINDOW_SIZE, WINDOW_SIZE))

        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()