import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIButton, UILabel, UIDropDownMenu, UITextEntryLine, UITextBox
from pygame_gui.windows import UIColourPickerDialog
import sys

from action import Action
from rule import Rule

ACTION_MAP = {
    "Skręt Lewo (L)": Action.LEFT,
    "Skręt Prawo (R)": Action.RIGHT,
    "Prosto (U)": Action.UP,
    "Bez Zmian (N)": Action.NO_CHANGE
}

PLACEHOLDER_OPT = "--- Wybierz ---"
ADD_NEW_COLOR_OPT = "[+ Dodaj Nowy Kolor]"


def format_color(rgb_tuple: tuple) -> str:
    return f"RGB {rgb_tuple}"


def parse_color(color_str: str) -> tuple:
    clean_str = color_str.replace("RGB ", "").replace("(", "").replace(")", "")
    parts = clean_str.split(",")
    return (int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip()))


def get_color_options(known_colors: list) -> list:
    return [PLACEHOLDER_OPT] + [format_color(c) for c in known_colors] + [ADD_NEW_COLOR_OPT]


def main():
    pygame.init()
    window_size = (1000, 800)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Kreator Zaawansowanych Reguł (Rule Builder)")
    manager = pygame_gui.UIManager(window_size)

    config_window = UIWindow(
        rect=pygame.Rect((50, 50), (450, 700)),
        manager=manager,
        window_display_title="Kreator Reguły (Stochastic Rule)"
    )

    known_colors = []
    rule_colors = []

    current_base_color = None
    current_temp_target_color = None

    y_offset = 10

    UILabel(relative_rect=pygame.Rect((10, y_offset), (400, 25)), text="--- 1. KOLOR BAZOWY REGUŁY ---",
            manager=manager, container=config_window)
    y_offset += 30

    rect_base_color = pygame.Rect((10, y_offset), (300, 30))
    dropdown_base_color = UIDropDownMenu(
        options_list=get_color_options(known_colors),
        starting_option=PLACEHOLDER_OPT,
        relative_rect=rect_base_color, manager=manager, container=config_window
    )
    y_offset += 40

    UILabel(relative_rect=pygame.Rect((10, y_offset), (400, 25)),
            text="--- 2. MOŻLIWE KIERUNKI (Suma Prawd. = 1.0) ---", manager=manager, container=config_window)
    y_offset += 30

    dropdown_action = UIDropDownMenu(
        options_list=list(ACTION_MAP.keys()), starting_option="Skręt Lewo (L)",
        relative_rect=pygame.Rect((10, y_offset), (180, 30)), manager=manager, container=config_window
    )
    input_action_prob = UITextEntryLine(relative_rect=pygame.Rect((200, y_offset), (60, 30)), manager=manager,
                                        container=config_window)
    input_action_prob.set_text("1.0")
    btn_add_action = UIButton(relative_rect=pygame.Rect((270, y_offset), (150, 30)), text="Dodaj Akcję",
                              manager=manager, container=config_window)
    y_offset += 35

    text_staged_actions = UITextBox(html_text="<i>Brak dodanych akcji...</i>",
                                    relative_rect=pygame.Rect((10, y_offset), (410, 60)), manager=manager,
                                    container=config_window)
    y_offset += 70

    UILabel(relative_rect=pygame.Rect((10, y_offset), (400, 25)),
            text="--- 3. MOŻLIWE NOWE KOLORY (Suma Prawd. = 1.0) ---", manager=manager, container=config_window)
    y_offset += 30

    rect_target_color = pygame.Rect((10, y_offset), (180, 30))
    dropdown_target_color = UIDropDownMenu(
        options_list=get_color_options(known_colors),
        starting_option=PLACEHOLDER_OPT,
        relative_rect=rect_target_color, manager=manager, container=config_window
    )

    input_color_prob = UITextEntryLine(relative_rect=pygame.Rect((200, y_offset), (60, 30)), manager=manager,
                                       container=config_window)
    input_color_prob.set_text("1.0")
    btn_add_color = UIButton(relative_rect=pygame.Rect((270, y_offset), (150, 30)), text="Dodaj Kolor", manager=manager,
                             container=config_window)
    y_offset += 35

    text_staged_colors = UITextBox(html_text="<i>Brak dodanych kolorów...</i>",
                                   relative_rect=pygame.Rect((10, y_offset), (410, 80)), manager=manager,
                                   container=config_window)
    y_offset += 90

    btn_save_rule = UIButton(relative_rect=pygame.Rect((10, y_offset), (410, 50)), text="ZAPISZ I WALIDUJ REGUŁĘ",
                             manager=manager, container=config_window)

    color_picker = None
    picker_target_mode = ""
    staged_actions = []
    staged_colors = []

    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)

            # obsluga zmiany w dropdoown listach
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                selected_val = event.text
                if isinstance(selected_val, tuple): selected_val = selected_val[0]

                if selected_val == PLACEHOLDER_OPT:
                    continue

                if event.ui_element == dropdown_base_color:
                    if selected_val == ADD_NEW_COLOR_OPT:
                        picker_target_mode = 'base'
                        color_picker = UIColourPickerDialog(rect=pygame.Rect((550, 50), (400, 400)), manager=manager,
                                                            window_title="Wybierz Nowy Kolor do Puli")
                    else:
                        current_base_color = parse_color(selected_val)

                elif event.ui_element == dropdown_target_color:
                    if selected_val == ADD_NEW_COLOR_OPT:
                        picker_target_mode = 'target'
                        color_picker = UIColourPickerDialog(rect=pygame.Rect((550, 50), (400, 400)), manager=manager,
                                                            window_title="Wybierz Nowy Kolor do Puli")
                    else:
                        current_temp_target_color = parse_color(selected_val)

            # obsluga przyciskow
            if event.type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == btn_add_action:
                    try:
                        prob = float(input_action_prob.get_text())
                        selected_val = dropdown_action.selected_option
                        if isinstance(selected_val, tuple): selected_val = selected_val[0]
                        action_enum = ACTION_MAP[selected_val]

                        staged_actions.append((action_enum, prob))
                        html = "<br>".join([f"Kierunek: {a.name}, Prawd: {p}" for a, p in staged_actions])
                        text_staged_actions.set_text(html)
                    except ValueError:
                        print("BŁĄD: Prawdopodobieństwo musi być liczbą!")

                elif event.ui_element == btn_add_color:
                    selected_val = dropdown_target_color.selected_option
                    if isinstance(selected_val, tuple): selected_val = selected_val[0]

                    if selected_val in [ADD_NEW_COLOR_OPT, PLACEHOLDER_OPT] or current_temp_target_color is None:
                        print("BŁĄD: Najpierw wybierz konkretny kolor z listy lub dodaj nowy!")
                    else:
                        try:
                            prob = float(input_color_prob.get_text())
                            staged_colors.append((current_temp_target_color, prob))
                            html = "<br>".join([f"Kolor RGB: {c}, Prawd: {p}" for c, p in staged_colors])
                            text_staged_colors.set_text(html)
                        except ValueError:
                            print("BŁĄD: Prawdopodobieństwo musi być liczbą!")

                elif event.ui_element == btn_save_rule:
                    selected_base = dropdown_base_color.selected_option
                    if isinstance(selected_base, tuple): selected_base = selected_base[0]

                    if selected_base in [ADD_NEW_COLOR_OPT, PLACEHOLDER_OPT] or current_base_color is None:
                        print("BŁĄD ZAPISU: Musisz ustawić poprawny Kolor Bazowy!")
                        continue

                    # sprawdzanie duplikatów
                    if current_base_color in rule_colors:
                        print(f"BŁĄD ZAPISU: Reguła dla koloru {current_base_color} już istnieje!")
                        continue

                    new_rule = Rule(current_base_color)
                    for action, prob in staged_actions:
                        new_rule.add_action(action, prob)
                    for color, prob in staged_colors:
                        new_rule.add_next_color(color, prob)

                    if new_rule.is_valid():
                        print(f"SUKCES! Zapisano regułę dla {current_base_color}.")
                        rule_colors.append(current_base_color)

                        staged_actions.clear()
                        staged_colors.clear()
                        text_staged_actions.set_text("<i>Brak dodanych akcji...</i>")
                        text_staged_colors.set_text("<i>Brak dodanych kolorów...</i>")
                    else:
                        print("BŁĄD ZAPISU: Suma prawdopodobieństw akcji LUB kolorów nie wynosi 1.0!")

            if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                rgb_tuple = (event.colour.r, event.colour.g, event.colour.b)

                if rgb_tuple not in known_colors:
                    known_colors.append(rgb_tuple)

                if picker_target_mode == 'base':
                    current_base_color = rgb_tuple
                elif picker_target_mode == 'target':
                    current_temp_target_color = rgb_tuple

                dropdown_base_color.kill()
                base_start = format_color(current_base_color) if current_base_color else PLACEHOLDER_OPT
                dropdown_base_color = UIDropDownMenu(
                    options_list=get_color_options(known_colors), starting_option=base_start,
                    relative_rect=rect_base_color, manager=manager, container=config_window
                )

                dropdown_target_color.kill()
                target_start = format_color(current_temp_target_color) if current_temp_target_color else PLACEHOLDER_OPT
                dropdown_target_color = UIDropDownMenu(
                    options_list=get_color_options(known_colors), starting_option=target_start,
                    relative_rect=rect_target_color, manager=manager, container=config_window
                )

        manager.update(time_delta)
        screen.fill(pygame.Color("#2b2b2b"))
        manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()