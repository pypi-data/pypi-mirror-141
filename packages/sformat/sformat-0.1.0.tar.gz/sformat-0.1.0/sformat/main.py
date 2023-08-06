from typing import Sequence
import fileinput
from sformat.formatter import format

#######################################
# Section-character format by Pursuit #
#######################################


def main(argv: Sequence[str] = None) -> None:
    for line in fileinput.input():  # Read input from standard input
        print(format(line), end="")  # Write output to standard output
