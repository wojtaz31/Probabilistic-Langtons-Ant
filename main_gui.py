import pygame
import pygame_gui
import sys
import argparse

from ui_rule_builder import UIRuleBuilderWindow
from ui_main_panel import UIMainPanel
from gui_utils import load_config
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE
from grid import Grid
from ant import Ant


def main():
    parser = argparse.ArgumentParser(description="Stochastyczna Mrówka Langtona")
    parser.add_argument("--ruleset", type=str, help="Ścieżka do pliku konfiguracyjnego JSON", default=None)
    args = parser.parse_args()

    pygame.init()
    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Stochastyczna Mrówka Langtona")

    manager = pygame_gui.UIManager(window_size)
    grid = Grid(GRID_SIZE)

    simulation_running = False

    if args.ruleset:
        load_config(args.ruleset, grid)
        simulation_running = True

    main_panel = UIMainPanel(manager, position=(20, 20))
    rule_builder_window = None

    if simulation_running:
        main_panel.btn_toggle_sim.set_text("PAUSE SIMULATION")

    def handle_new_ant(x, y, direction):
        new_ant = Ant(x, y, direction)
        grid.add_ant(new_ant)

    def handle_new_rule(rule):
        grid.add_rule(rule)

    def toggle_simulation():
        nonlocal simulation_running
        simulation_running = not simulation_running
        if simulation_running:
            main_panel.btn_toggle_sim.set_text("PAUSE SIMULATION")
        else:
            main_panel.btn_toggle_sim.set_text("START SIMULATION")

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

        try:
            current_delay = int(main_panel.input_speed.get_text())
            if current_delay < 0:
                current_delay = 0
        except ValueError:
            current_delay = 0

        try:
            steps_per_frame = int(main_panel.input_steps.get_text())
            if steps_per_frame < 1:
                steps_per_frame = 1
        except ValueError:
            steps_per_frame = 1

        if simulation_running and (current_time - last_update_time >= current_delay):
            for _ in range(steps_per_frame):
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
