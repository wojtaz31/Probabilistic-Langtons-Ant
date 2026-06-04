import pygame
import pygame_gui
import sys

from ui_rule_builder import UIRuleBuilderWindow
from ui_main_panel import UIMainPanel
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, COLOR_RED, UPDATE_DELAY_MS
from grid import Grid
from ant import Ant


def main():
    pygame.init()
    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Stochastyczna Mrówka Langtona")

    manager = pygame_gui.UIManager(window_size)
    grid = Grid(GRID_SIZE)

    center_x, center_y = GRID_SIZE // 2, GRID_SIZE // 2
    grid.color_pixel(center_x, center_y)
    grid.color_pixel(center_x + 1, center_y)
    grid.color_pixel(center_x, center_y + 1)
    grid.color_pixel(center_x + 1, center_y + 1, COLOR_RED)

    main_panel = UIMainPanel(manager, position=(20, 20))
    rule_builder_window = None

    simulation_running = False

    def handle_new_ant(x, y, direction):
        new_ant = Ant(x, y, direction)
        grid.add_ant(new_ant)
        print(f"[MAIN] Dodano Mrówkę. Aktualna liczba mrówek: {len(grid.ants)}")

    def handle_new_rule(rule):
        grid.add_rule(rule)
        print(f"[MAIN] Zapisano regułę. Aktualna liczba reguł: {len(grid.rules)}")

    def toggle_simulation():
        nonlocal simulation_running
        simulation_running = not simulation_running
        if simulation_running:
            main_panel.btn_toggle_sim.set_text("PAUSE SIMULATION")
            print("[MAIN] Symulacja URUCHOMIONA.")
        else:
            main_panel.btn_toggle_sim.set_text("START SIMULATION")
            print("[MAIN] Symulacja ZATRZYMANA.")

    main_panel.on_ant_created = handle_new_ant
    main_panel.on_toggle_simulation = toggle_simulation

    def open_rule_builder():
        nonlocal rule_builder_window
        if rule_builder_window is None or not rule_builder_window.window.alive():
            rule_builder_window = UIRuleBuilderWindow(manager, position=(400, 20))
            rule_builder_window.on_rule_created = handle_new_rule

    main_panel.on_open_rule_builder = open_rule_builder

    clock = pygame.time.Clock()
    running = True

    last_update_time = pygame.time.get_ticks()

    while running:
        time_delta = clock.tick(60) / 1000.0
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)
            main_panel.process_event(event)

            if rule_builder_window is not None and rule_builder_window.window.alive():
                rule_builder_window.process_event(event)

        if simulation_running and (current_time - last_update_time >= UPDATE_DELAY_MS):
            grid.step()
            last_update_time = current_time

        manager.update(time_delta)

        surface = pygame.surfarray.make_surface(grid.get_surface_array())
        scaled_surface = pygame.transform.scale(surface, window_size)
        screen.blit(scaled_surface, (0, 0))

        manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()