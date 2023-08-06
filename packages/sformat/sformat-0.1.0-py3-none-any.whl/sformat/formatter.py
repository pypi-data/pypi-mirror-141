FORMATTING_CODES = {
    "0": 30,    # Black
    "1": 34,    # Blue
    "2": 32,    # Green
    "3": 36,    # Cyan
    "4": 31,    # Red
    "5": 35,    # Magenta
    "6": 33,    # Yellow
    "7": 37,    # Light Gray
    "8": 90,    # Dark Gray
    "9": 94,    # Light Blue
    "a": 92,    # Light Green
    "b": 96,    # Light Cyan
    "c": 91,    # Light Red
    "d": 95,    # Light Magenta
    "e": 93,    # Light Yellow
    "f": 97,    # White
    "g0": 40,   # Black
    "g1": 44,   # Blue
    "g2": 42,   # Green
    "g3": 46,   # Cyan
    "g4": 41,   # Red
    "g5": 45,   # Magenta
    "g6": 43,   # Yellow
    "g7": 47,   # Light Gray
    "g8": 100,  # Dark Gray
    "g9": 104,  # Light Blue
    "ga": 102,  # Light Green
    "gb": 106,  # Light Cyan
    "gc": 101,  # Light Red
    "gd": 105,  # Light Magenta
    "ge": 103,  # Light Yellow
    "gf": 107,  # White
    "l": 1,     # Bold
    "u": 4,     # Underline
    "v": 7,     # Reversed
    "r": 0      # Reset
}

def format(text: str) -> str:
    formatted = text
    for code, formatting in FORMATTING_CODES.items():
        formatted = formatted.replace(f"§{code}", f"\u001b[{formatting}m")
    return formatted
