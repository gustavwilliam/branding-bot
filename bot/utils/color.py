from PIL import ImageColor
from contextlib import suppress

RGB_COLOR = tuple[int, int, int]
RGBA_COLOR = tuple[int, int, int, int]


def parse_color(raw_color: str) -> RGB_COLOR | RGBA_COLOR:
    """Get an RGB representation of the given color."""
    with suppress(ValueError):
        return ImageColor.getrgb(raw_color)
    with suppress(ValueError):
        return ImageColor.getrgb(f"#{raw_color}")

    raise ValueError(f"The provided color ({raw_color}) is invalid.")


def rgb_to_hex(color: RGB_COLOR | RGBA_COLOR) -> str:
    """Returns the hexadecimal represenation of an RGB color."""
    if not all(0 <= value <= 255 for value in color):
        raise ValueError(f"The provided color ({color}) is invalid.")

    return "#%02x%02x%02x" % color
