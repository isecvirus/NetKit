from argparse import ArgumentParser

from util import i2n, i2b
from util.stylize import colors

"""   
    Converting ipv4 to decimal	    
"""

if "__main__" == __name__:
    version = "i2n (1.0.0v)"

    parser = ArgumentParser(prog="i2n", description="Convert ipv4 to decimal")
    parser.add_argument("-i", "--ip", type=str, default="0.0.0.0", required=True, metavar="<IP>", nargs="+")
    parser.add_argument("-m", "--mode", type=str, default="ip", required=False, choices=["ip", "bin"])
    parser.add_argument("-s", "--separator", type=str, default=" ", required=False)
    parser.add_argument("-j", "--justify", type=str, default=" ", required=False)
    parser.add_argument("-o", "--output", type=str, required=False)
    parser.add_argument("-v", "--version", version=version, action="version")

    args = parser.parse_args()

    ips = args.ip
    mode = args.mode
    justify = args.justify
    separator = args.separator
    output = args.output

    output_list = []
    for ip in ips:
        ip_just = 15
        dec_just = 10
        justify = " " if not justify else justify[0]
        decimal = i2n(ip=ip)

        if mode == "ip":
            ip = ip
        elif mode == "bin":
            ip = i2b(ip)


        decimal = str(decimal).rjust(dec_just, justify)
        ip = ip.rjust(ip_just, justify)
        output_list.append(f"{ip}{decimal}")

        print(f"{colors.GREEN}{ip}{colors.RESET}{separator}{colors.WHITE}{decimal}{colors.RESET}")

    if output:
        try:
            o = open(output, "w")
            o.write('\n'.join(output_list))
            o.close()
        except Exception as error:
            print(f"\n{colors.RED+colors.BOLD}{error}{colors.RESET}")