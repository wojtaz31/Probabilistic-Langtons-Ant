import pygame
import pygame_gui
import sys

from ui_rule_builder import UIRuleBuilderWindow
from ui_main_panel import UIMainPanel


def handle_new_ant(x, y, direction):
    print(f"\n[MAIN] Dodano Mrówkę! Pozycja: ({x}, {y}), Zwrot: {direction}")


def handle_new_rule(rule):
    print(f"\n[MAIN] Zapisano nową regułę dla koloru: {rule.color}")
    print(f"Akcje: {rule.actions} | Przejścia: {rule.next_colors}")


def main():
    pygame.init()
    window_size = (1200, 800)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Stochastyczna Mrówka Langtona - UI")

    manager = pygame_gui.UIManager(window_size)

    main_panel = UIMainPanel(manager, position=(20, 20))
    main_panel.on_ant_created = handle_new_ant

    rule_builder_window = None

    def open_rule_builder():
        nonlocal rule_builder_window
        if rule_builder_window is None or not rule_builder_window.window.alive():
            rule_builder_window = UIRuleBuilderWindow(manager, position=(400, 20))
            rule_builder_window.on_rule_created = handle_new_rule
        else:
            print("[INFO] Kreator Reguł jest już otwarty!")

    main_panel.on_open_rule_builder = open_rule_builder

    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)
            main_panel.process_event(event)

            if rule_builder_window is not None and rule_builder_window.window.alive():
                rule_builder_window.process_event(event)

        manager.update(time_delta)

        screen.fill(pygame.Color("#2b2b2b"))
        manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()