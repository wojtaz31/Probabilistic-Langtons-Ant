import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIButton, UILabel, UIDropDownMenu, UITextEntryLine, UITextBox
from pygame_gui.windows import UIColourPickerDialog

from action import Action
from rule import Rule
from gui_utils import format_color, parse_color, get_color_options, PLACEHOLDER_OPT, ADD_NEW_COLOR_OPT

ACTION_MAP = {
    "Skręt Lewo (L)": Action.LEFT,
    "Skręt Prawo (R)": Action.RIGHT,
    "Prosto (U)": Action.UP,
    "Bez Zmian (N)": Action.NO_CHANGE
}


class UIRuleBuilderWindow:
    def __init__(self, manager: pygame_gui.UIManager, position: tuple = (50, 50)):
        self.manager = manager

        self.window = UIWindow(
            rect=pygame.Rect(position, (450, 700)),
            manager=self.manager,
            window_display_title="Kreator Reguły (Stochastic Rule)"
        )

        self.known_colors = []
        self.rule_colors = []
        self.current_base_color = None
        self.current_temp_target_color = None
        self.staged_actions = []
        self.staged_colors = []

        self.color_picker = None
        self.picker_target_mode = ""

        self.on_rule_created = None

        self._build_ui()

    def _build_ui(self):
        """Inicjalizuje wszystkie widgety w oknie."""
        y_offset = 10

        UILabel(relative_rect=pygame.Rect((10, y_offset), (400, 25)), text="--- 1. KOLOR BAZOWY REGUŁY ---",
                manager=self.manager, container=self.window)
        y_offset += 30
        self.rect_base_color = pygame.Rect((10, y_offset), (300, 30))
        self.dropdown_base_color = UIDropDownMenu(
            options_list=get_color_options(self.known_colors), starting_option=PLACEHOLDER_OPT,
            relative_rect=self.rect_base_color, manager=self.manager, container=self.window
        )
        y_offset += 40

        UILabel(relative_rect=pygame.Rect((10, y_offset), (400, 25)),
                text="--- 2. MOŻLIWE KIERUNKI (Suma Prawd. = 1.0) ---", manager=self.manager, container=self.window)
        y_offset += 30
        self.dropdown_action = UIDropDownMenu(
            options_list=list(ACTION_MAP.keys()), starting_option="Skręt Lewo (L)",
            relative_rect=pygame.Rect((10, y_offset), (180, 30)), manager=self.manager, container=self.window
        )
        self.input_action_prob = UITextEntryLine(relative_rect=pygame.Rect((200, y_offset), (60, 30)),
                                                 manager=self.manager, container=self.window)
        self.input_action_prob.set_text("1.0")
        self.btn_add_action = UIButton(relative_rect=pygame.Rect((270, y_offset), (150, 30)), text="Dodaj Akcję",
                                       manager=self.manager, container=self.window)
        y_offset += 35
        self.text_staged_actions = UITextBox(html_text="<i>Brak dodanych akcji...</i>",
                                             relative_rect=pygame.Rect((10, y_offset), (410, 60)), manager=self.manager,
                                             container=self.window)
        y_offset += 70

        UILabel(relative_rect=pygame.Rect((10, y_offset), (400, 25)),
                text="--- 3. MOŻLIWE NOWE KOLORY (Suma Prawd. = 1.0) ---", manager=self.manager, container=self.window)
        y_offset += 30
        self.rect_target_color = pygame.Rect((10, y_offset), (180, 30))
        self.dropdown_target_color = UIDropDownMenu(
            options_list=get_color_options(self.known_colors), starting_option=PLACEHOLDER_OPT,
            relative_rect=self.rect_target_color, manager=self.manager, container=self.window
        )
        self.input_color_prob = UITextEntryLine(relative_rect=pygame.Rect((200, y_offset), (60, 30)),
                                                manager=self.manager, container=self.window)
        self.input_color_prob.set_text("1.0")
        self.btn_add_color = UIButton(relative_rect=pygame.Rect((270, y_offset), (150, 30)), text="Dodaj Kolor",
                                      manager=self.manager, container=self.window)
        y_offset += 35
        self.text_staged_colors = UITextBox(html_text="<i>Brak dodanych kolorów...</i>",
                                            relative_rect=pygame.Rect((10, y_offset), (410, 80)), manager=self.manager,
                                            container=self.window)
        y_offset += 90

        self.btn_save_rule = UIButton(relative_rect=pygame.Rect((10, y_offset), (410, 50)),
                                      text="ZAPISZ I WALIDUJ REGUŁĘ", manager=self.manager, container=self.window)

    def _refresh_dropdowns(self):
        """Prywatna metoda hermetyzująca przeładowywanie list rozwijanych."""
        self.dropdown_base_color.kill()
        base_start = format_color(self.current_base_color) if self.current_base_color else PLACEHOLDER_OPT
        self.dropdown_base_color = UIDropDownMenu(
            options_list=get_color_options(self.known_colors), starting_option=base_start,
            relative_rect=self.rect_base_color, manager=self.manager, container=self.window
        )

        self.dropdown_target_color.kill()
        target_start = format_color(
            self.current_temp_target_color) if self.current_temp_target_color else PLACEHOLDER_OPT
        self.dropdown_target_color = UIDropDownMenu(
            options_list=get_color_options(self.known_colors), starting_option=target_start,
            relative_rect=self.rect_target_color, manager=self.manager, container=self.window
        )

    def process_event(self, event):
        """Zewnętrzna metoda, do której przekazujemy eventy z głównej pętli."""

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            selected_val = event.text
            if isinstance(selected_val, tuple): selected_val = selected_val[0]

            if selected_val != PLACEHOLDER_OPT:
                if event.ui_element == self.dropdown_base_color:
                    if selected_val == ADD_NEW_COLOR_OPT:
                        self.picker_target_mode = 'base'
                        self.color_picker = UIColourPickerDialog(rect=pygame.Rect((550, 50), (400, 400)),
                                                                 manager=self.manager,
                                                                 window_title="Wybierz Nowy Kolor do Puli")
                    else:
                        self.current_base_color = parse_color(selected_val)

                elif event.ui_element == self.dropdown_target_color:
                    if selected_val == ADD_NEW_COLOR_OPT:
                        self.picker_target_mode = 'target'
                        self.color_picker = UIColourPickerDialog(rect=pygame.Rect((550, 50), (400, 400)),
                                                                 manager=self.manager,
                                                                 window_title="Wybierz Nowy Kolor do Puli")
                    else:
                        self.current_temp_target_color = parse_color(selected_val)

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_add_action:
                try:
                    prob = float(self.input_action_prob.get_text())
                    selected_val = self.dropdown_action.selected_option
                    if isinstance(selected_val, tuple): selected_val = selected_val[0]

                    self.staged_actions.append((ACTION_MAP[selected_val], prob))
                    html = "<br>".join([f"Kierunek: {a.name}, Prawd: {p}" for a, p in self.staged_actions])
                    self.text_staged_actions.set_text(html)
                except ValueError:
                    print("BŁĄD: Prawdopodobieństwo musi być liczbą!")

            elif event.ui_element == self.btn_add_color:
                selected_val = self.dropdown_target_color.selected_option
                if isinstance(selected_val, tuple): selected_val = selected_val[0]

                if selected_val in [ADD_NEW_COLOR_OPT, PLACEHOLDER_OPT] or self.current_temp_target_color is None:
                    print("BŁĄD: Najpierw wybierz konkretny kolor!")
                else:
                    try:
                        prob = float(self.input_color_prob.get_text())
                        self.staged_colors.append((self.current_temp_target_color, prob))
                        html = "<br>".join([f"Kolor RGB: {c}, Prawd: {p}" for c, p in self.staged_colors])
                        self.text_staged_colors.set_text(html)
                    except ValueError:
                        print("BŁĄD: Prawdopodobieństwo musi być liczbą!")

            elif event.ui_element == self.btn_save_rule:
                selected_base = self.dropdown_base_color.selected_option
                if isinstance(selected_base, tuple): selected_base = selected_base[0]

                if selected_base in [ADD_NEW_COLOR_OPT, PLACEHOLDER_OPT] or self.current_base_color is None:
                    print("BŁĄD ZAPISU: Musisz ustawić poprawny Kolor Bazowy!")
                    return

                if self.current_base_color in self.rule_colors:
                    print(f"BŁĄD ZAPISU: Reguła dla koloru {self.current_base_color} już istnieje!")
                    return

                new_rule = Rule(self.current_base_color)
                for action, prob in self.staged_actions:
                    new_rule.add_action(action, prob)
                for color, prob in self.staged_colors:
                    new_rule.add_next_color(color, prob)

                if new_rule.is_valid():
                    self.rule_colors.append(self.current_base_color)
                    self.staged_actions.clear()
                    self.staged_colors.clear()
                    self.text_staged_actions.set_text("<i>Brak dodanych akcji...</i>")
                    self.text_staged_colors.set_text("<i>Brak dodanych kolorów...</i>")

                    if self.on_rule_created:
                        self.on_rule_created(new_rule)
                else:
                    print("BŁĄD ZAPISU: Suma prawdopodobieństw akcji LUB kolorów nie wynosi 1.0!")

        elif event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            rgb_tuple = (event.colour.r, event.colour.g, event.colour.b)
            if rgb_tuple not in self.known_colors:
                self.known_colors.append(rgb_tuple)

            if self.picker_target_mode == 'base':
                self.current_base_color = rgb_tuple
            elif self.picker_target_mode == 'target':
                self.current_temp_target_color = rgb_tuple

            self._refresh_dropdowns()