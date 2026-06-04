import json

from action import Action
from rule import Rule
from ant import Ant

PLACEHOLDER_OPT = "--- Wybierz ---"
ADD_NEW_COLOR_OPT = "[+ Dodaj Nowy Kolor]"

STR_TO_ACTION = {
    "LEFT": Action.LEFT,
    "RIGHT": Action.RIGHT,
    "UP": Action.UP,
    "NO_CHANGE": Action.NO_CHANGE
}


def format_color(rgb_tuple: tuple) -> str:
    return f"RGB {rgb_tuple}"


def parse_color(color_str: str) -> tuple:
    clean_str = color_str.replace("RGB ", "").replace("(", "").replace(")", "")
    parts = clean_str.split(",")
    return (int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip()))


def get_color_options(known_colors: list) -> list:
    return [PLACEHOLDER_OPT] + [format_color(c) for c in known_colors] + [ADD_NEW_COLOR_OPT]


def load_config(filepath, grid):
    with open(filepath, 'r') as f:
        data = json.load(f)

    for ant_data in data.get("ants", []):
        new_ant = Ant(ant_data["x"], ant_data["y"], ant_data["direction"])
        grid.add_ant(new_ant)
        print(f"[LOAD] Dodano mrówkę z configu: ({new_ant.x}, {new_ant.y})")

    for rule_data in data.get("rules", []):
        base_color = tuple(rule_data["base_color"])
        rule = Rule(base_color)

        for action_str, prob in rule_data.get("actions", []):
            rule.add_action(STR_TO_ACTION[action_str], prob)

        for color_list, prob in rule_data.get("next_colors", []):
            rule.add_next_color(tuple(color_list), prob)

        if rule.is_valid():
            grid.add_rule(rule)
            print(f"[LOAD] Załadowano regułę dla koloru: {base_color}")
        else:
            print(f"[BŁĄD LOAD] Reguła dla {base_color} w JSON jest niepoprawna (sumy != 1.0)!")
