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
