from argparse import ArgumentParser
from util.stylize import colors
from util import i2i, i2n, i2b

"""   
    Converting decimal to ipv4
"""


if "__main__" == __name__:
    version = "i2i (1.0.0v)"

    parser = ArgumentParser(prog="i2i", description="Convert decimal to ipv4")
    parser.add_argument("-f", "--from", type=str, default="0.0.0.0", required=False, metavar="<IP-FROM>", dest="_from")
    parser.add_argument("-t", "--to", type=str, default="0.0.0.255", required=False, metavar="<IP-TO>")
    parser.add_argument("-v", "--version", version=version, action="version")

    args = parser.parse_args()

    _from = args._from
    to = args.to

    ips = i2i(_from=_from, to=to)
    for ip in ips:
        decimal = str(i2n(ip))
        binary = i2b(ip)

        print(f"{colors.GREEN}{ip.rjust(15, ' ')}{colors.RESET}"
              f"{colors.MAGENTA}{decimal.rjust(11, ' ')}{colors.RESET}"
              f"{colors.CYAN}{binary.rjust(36, ' ')}{colors.RESET}")
