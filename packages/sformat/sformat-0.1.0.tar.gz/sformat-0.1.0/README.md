# Section-character format

This tool and library convert simple formatting codes that are based on the section character (`§`) to standard [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code).

These formatting codes are inspired by the ones used in [Minecraft](https://minecraft.fandom.com/wiki/Formatting_codes).

## Formatting codes

16 colors are available:

![colors](https://raw.githubusercontent.com/fr-Pursuit/sformat/master/colors.png)

To set the background color, prefix the color letter with `g` (ex: `§g1` for a blue background)

In addition to color codes, several other formatting codes are available:

- `§l` - Bold text
- `§u` - Underlined text
- `§v` - Reverse the background and foreground color
- `§r` - Reset the formatting

## Installation

This project can be installed via `pip`:

    pip install sformat

## Tool usage

The `sformat` tool can be used to format text by piping it to its standard input:

    $ echo "§aHello §bWorld§r!" | sformat
    Hello World! (in color)

## Library usage

Simply use the `format` function from `sformat.formatter`:

```python
from sformat.formatter import format

raw_text = "§aHello §bWorld§r!"
colored_text = format(raw_text)
print(colored_text)  # The text will be displayed in color
```

## License

This project is licensed under the [GNU GPLv3 license](/./LICENSE).
