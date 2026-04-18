def ansi(f):
    """
    Takes a directive (f) and returns the corresponding ansi value for text formatting.

    Directive types :\n
    - "0" : Resets formatting\n
    - "#RRGGBB" : Converts a hex color to a 24-bit RGB escape sequence\n
    - "&NAME" : Returns a predefined color from DEFAULT_COLORS\n
    - "_" : Returns a greyed out color (for frozen/secondary text appearance)

    :param f: The formatting directive
    :type f: str
    :return: The ansi escape sequence ready to be inserted into a string
    :rtype: str
    """

    def hex_to_ansi(hex_color: str) -> str:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"

    default_colors = {
        'PURPLE': 'B470FF',
        'BLUE': '7072FF',
        'PINK': 'FD70FF',
        'RED': 'FF7072',
        'GREEN': '70FFB5',
        'YELLOW': 'FFFD70',
        'ORANGE': 'FFB570',
        'CYAN': '70FFFD'
        }

    try:
        match f[0]:
            case '0':return '\033[0m'
            case '#':return hex_to_ansi(f[1:])
            case '&':return hex_to_ansi(default_colors[f[1:]])
            case '_':return hex_to_ansi('888888')
            case _:return ''
    except Exception:return ''