from textwrap import wrap

def transform_color(hex_color):
    try:
        color = [_/255.0 for _ in map(lambda x: int(x, 16), wrap(hex_color, 2))]
    except ValueError as e:
        raise Exception(f"Invalid color format: {hex_color}") from e
    if len(color) != 3:
        raise Exception(f"Invalid color format: {hex_color}")
    return color
