from argparse import ArgumentParser

from util import n2i
from util.stylize import colors

"""   
    Converting decimal to ipv4
"""


if "__main__" == __name__:
    version = "n2i (1.0.0v)"

    parser = ArgumentParser(prog="n2i", description="Convert decimal to ipv4")
    parser.add_argument("-n", "--number", type=int, required=True, metavar="<IP>", nargs="+")
    parser.add_argument("-s", "--separator", type=str, default=" ", required=False)
    parser.add_argument("-j", "--justify", type=str, default=" ", required=False)
    parser.add_argument("-v", "--version", version=version, action="version")

    args = parser.parse_args()

    numbers = args.number
    justify = args.justify
    separator = args.separator

    justify = " " if not justify else justify[0]

    for decimal in numbers:
        ip = n2i(decimal=decimal).rjust(15, justify)
        print(f"{colors.GREEN}{decimal}{separator}{colors.WHITE}{ip}{colors.RESET}")
