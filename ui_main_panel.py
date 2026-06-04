import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIButton, UILabel, UIDropDownMenu, UITextEntryLine
from settings import GRID_SIZE


class UIMainPanel:
    def __init__(self, manager: pygame_gui.UIManager, position: tuple = (20, 20)):
        self.manager = manager
        self.window = UIWindow(
            rect=pygame.Rect(position, (350, 460)),
            manager=self.manager,
            window_display_title="Główny Panel Symulacji"
        )
        self.on_ant_created = None
        self.on_open_rule_builder = None
        self.on_toggle_simulation = None
        self._build_ui()

    def _build_ui(self):
        y_offset = 10
        UILabel(relative_rect=pygame.Rect((10, y_offset), (300, 25)), text="--- NOWA MRÓWKA ---", manager=self.manager,
                container=self.window)
        y_offset += 35

        UILabel(relative_rect=pygame.Rect((10, y_offset), (40, 30)), text="X:", manager=self.manager,
                container=self.window)
        self.input_x = UITextEntryLine(relative_rect=pygame.Rect((50, y_offset), (80, 30)), manager=self.manager,
                                       container=self.window)

        UILabel(relative_rect=pygame.Rect((140, y_offset), (40, 30)), text="Y:", manager=self.manager,
                container=self.window)
        self.input_y = UITextEntryLine(relative_rect=pygame.Rect((180, y_offset), (80, 30)), manager=self.manager,
                                       container=self.window)

        center_val = str(GRID_SIZE // 2)
        self.input_x.set_text(center_val)
        self.input_y.set_text(center_val)

        y_offset += 40
        UILabel(relative_rect=pygame.Rect((10, y_offset), (100, 30)), text="Kierunek:", manager=self.manager,
                container=self.window)
        self.dropdown_dir = UIDropDownMenu(
            options_list=["UP", "RIGHT", "DOWN", "LEFT"],
            starting_option="UP",
            relative_rect=pygame.Rect((120, y_offset), (160, 30)),
            manager=self.manager, container=self.window
        )
        y_offset += 40
        self.btn_add_ant = UIButton(relative_rect=pygame.Rect((10, y_offset), (280, 40)),
                                    text="Dodaj Mrówkę na planszę", manager=self.manager, container=self.window)
        y_offset += 60
        UILabel(relative_rect=pygame.Rect((10, y_offset), (300, 25)), text="--- ZARZĄDZANIE REGUŁAMI ---",
                manager=self.manager, container=self.window)
        y_offset += 35
        self.btn_open_rule_builder = UIButton(relative_rect=pygame.Rect((10, y_offset), (280, 40)),
                                              text="[+] Otwórz Kreator Reguł", manager=self.manager,
                                              container=self.window)
        y_offset += 60
        self.btn_toggle_sim = UIButton(relative_rect=pygame.Rect((10, y_offset), (280, 50)), text="START SIMULATION",
                                       manager=self.manager, container=self.window)

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_add_ant:
                if self.on_ant_created:
                    try:
                        x = int(self.input_x.get_text())
                        y = int(self.input_y.get_text())
                        d = self.dropdown_dir.selected_option
                        if isinstance(d, tuple): d = d[0]
                        self.on_ant_created(x, y, d)
                    except ValueError:
                        print("BŁĄD: Współrzędne X i Y muszą być liczbami całkowitymi!")
            elif event.ui_element == self.btn_open_rule_builder:
                if self.on_open_rule_builder:
                    self.on_open_rule_builder()
            elif event.ui_element == self.btn_toggle_sim:
                if self.on_toggle_simulation:
                    self.on_toggle_simulation()