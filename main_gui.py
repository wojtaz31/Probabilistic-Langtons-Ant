# main_gui.py
import pygame
import pygame_gui
import sys

# Importujemy naszą nową, kulturalną klasę okna
from ui_rule_builder import UIRuleBuilderWindow


def handle_new_rule(rule):
    """
    To jest Callback. Zostanie wywołany automatycznie przez obiekt GUI,
    gdy użytkownik poprawnie zapisze i zwaliduje nową regułę.
    """
    print("\n--- ODEBRANO NOWĄ REGUŁĘ W MAIN.PY ---")
    print(f"Kolor bazowy: {rule.color}")
    print(f"Akcje: {rule.actions}")
    print(f"Przejścia kolorów: {rule.next_colors}")
    print("--------------------------------------\n")
    # Tutaj w przyszłości dodasz tę regułę do obiektu symulacji/planszy!


def main():
    pygame.init()
    window_size = (1000, 800)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Symulator - Test Modułowego GUI")

    manager = pygame_gui.UIManager(window_size)

    # 1. Tworzymy instancję naszego okna GUI
    rule_builder_ui = UIRuleBuilderWindow(manager, position=(50, 50))

    # 2. Podpinamy naszą funkcję odbiorczą pod obiekt okna
    rule_builder_ui.on_rule_created = handle_new_rule

    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Przekazujemy event do managera i do naszej klasy okna
            manager.process_events(event)
            rule_builder_ui.process_event(event)

        manager.update(time_delta)

        screen.fill(pygame.Color("#2b2b2b"))
        manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()