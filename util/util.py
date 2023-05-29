import json
import random
import threading
from socket import AF_INET, socket, SOCK_STREAM

"""

What is "&"?:
    The & operator compares each bit and set it to 1 if both are 1,
    otherwise it is set to 0:

    Example: 6 & 3 = 2

    6 = 00000110
    3 = 00000011
    --------------------
    2 = 00000010


What is "|"?:
    The | operator compares each bit and set it to 1 if one or both is 1,
    otherwise it is set to 0:

    Example: 6 | 3 = 7

    6 = 00000110
    3 = 00000011
    --------------------
    7 = 00000111


What is "^"?:
    The ^ operator compares each bit and set it to 1 if only one is 1,
    otherwise (if both are 1 or both are 0) it is set to 0:

    Example: 6 ^ 3 = 5

    6 = 00000110
    3 = 00000011
    --------------------
    5 = 00000101


What is ">>" and "<<"?:
    The >> operator moves each bit the specified number of times to the right.
    Empty holes at the left are filled with 0's.

    Example: 8 >> 2 = 2

    If you move each bit 2 times to the right, 8 becomes 2:
        8 = 00001000
    becomes:
        2 = 00000010

"""

PRIVATE = "private"
PUBLIC = "public"
LOOPBACK = "loopback"
LINK_LOCAL = "link-local"
MULTICAST = "multicast"
RESERVED = "reserved"
RESERVED_FOR_IANA = "Reserved for IANA"
IETF_PROTOCOL_ASSIGNMENT = "IETF Protocol Assignment"
CARRIER_GRADE_NAT = "Carrier-grade NAT"
TEST_NET_1 = "TEST-NET-1"

MIN_PORT = 0
MAX_PORT = 2 ** 16 - 1
isMAX_PORT = lambda port: port if port <= 2 ** 16 - 1 else 2 ** 16 - 1

_all_ = ['b2i', 'b2m', 'c2h', 'c2i', 'c2n', 'h2c', 'i2b', 'i2c', 'i2i', 'i2n', 'i2p', 'i2t', 'isipv4', 'm2b', 'm2n',
         'n2c', 'n2i', 'n2m', 'p2i', 'r2c', 'r2r', 't2i', 'v2a', 'p2d']


def binary_to_number(binary: str) -> int:
    decimal = 0

    for digit in binary:
        decimal = decimal * 2 + int(digit)
    return decimal


def number_to_binary(decimal: int, fill: bool = True) -> str:
    binary_octet = ""

    while decimal > 0:
        remainder = decimal % 2
        binary_octet = str(remainder) + binary_octet
        decimal //= 2
    return binary_octet.zfill(8) if fill else binary_octet


def isipv4(ipv4: str | list, sep: str = ".") -> bool | dict:  # is ipv4
    if isinstance(ipv4, str):
        try:
            dots = ipv4.count(sep) == 3
            octets = list(map(int, ipv4.split(sep)))
            bits = [0 <= o <= 255 for o in octets]

            return dots == (len(octets) == 4) == list(set(bits))[0]
        except (IndexError, ValueError, TypeError) as error:
            return False
    elif isinstance(ipv4, list):
        validation = {}
        for ip in ipv4:
            validation[ip] = isipv4(ip, sep)
        return validation


def i2t(ip: str):  # ip to type
    """
    Returns the type of IPv4 address as a string.

    :param ip: A string representing an IPv4 address in the form "xxx.xxx.xxx.xxx"
    :return: A string representing the type of the IPv4 address, which can be one of:
             "private" for private addresses (e.g., 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
             "public" for public addresses (e.g., all other addresses)
             "loopback" for loopback addresses (e.g., 127.0.0.1)
             "link-local" for link-local addresses (e.g., 169.254.0.0/16)
             "multicast" for multicast addresses (e.g., 224.0.0.0/4)
             "broadcast" for broadcast addresses (e.g., 255.255.255.255)

    Examples:
        >>> i2t("192.168.1.1")
        "private"
        >>> i2t("8.8.8.8")
        "public"
        >>> i2t("127.0.0.1")
        "loopback"
    """
    octets = ip.split(".")

    if octets[0] == "10" or (octets[0] == "172" and int(octets[1]) in range(16, 32)) or \
            (octets[0] == "192" and octets[1] == "168"):
        return "private"  # 10.0.0.1, 192.168.0.1, 172.16.0.1
    elif octets[0] == "127":
        return "loopback"  # 127.0.0.1, 127.0.1.1, 127.255.255.255
    elif octets[0] == "169" and octets[1] == "254":
        return "link-local"  # 169.254.0.1, 169.254.0.5, 169.254.255.255
    elif int(octets[0]) in range(224, 240):
        return "multicast"  # 224.0.0.1, 239.255.255.255, 224.0.1.1
    elif octets[0] == "255":
        if all(o == "255" for o in octets[1:]):
            return "broadcast"  # 255.255.255.255, 192.168.0.255, 172.16.0.255
        else:
            return "reserved"
    elif octets[0] == "0":
        return "unassigned"
    elif octets[0] == "192" and octets[1] == "31" and octets[2] == "196":
        return "Reserved for IANA"
    elif octets[0] == "192" and octets[1] == "0" and octets[2] == "0":
        return "IETF Protocol Assignment"
    elif octets[0] == "100" and int(octets[1]) in range(64, 128):
        return "Carrier-grade NAT"
    elif octets[0] == "192" and octets[1] == "0" and octets[2] == "2":
        return "TEST-NET-1"
    else:
        return "public"  # 8.8.8.8, 52.95.132.29, 104.18.34.196


def t2i(type: str = "private"):  # type to random ip
    rand = lambda f, t: str(random.choice(list(range(f, t + 1))))
    TYPES = {
        "private": random.choice(
            [
                "10." + '.'.join([rand(0, 255) for p1 in range(3)]),
                "172." + '.'.join([rand(16, 31) for p2 in range(3)])
            ]
        ),
        "public": rand(1, 224) + '.' + '.'.join([rand(0, 255) for p1 in range(3)]),
        "loopback": "127." + '.'.join([rand(0, 255) for p1 in range(3)]),
        "link-local": "169.254." + '.'.join([rand(0, 255) for p1 in range(2)]),
        "multicast": str(random.randint(224, 240)) + '.' + '.'.join([rand(0, 255) for p1 in range(3)]),
        "reserved": "255." + '.'.join([rand(0, 255) for p1 in range(3)]),
        "Reserved for IANA": "192.31.196." + rand(0, 255),
        "IETF Protocol Assignment": "192.0.0." + rand(0, 255),
        "Carrier-grade NAT": "100." + rand(64, 128) + '.' + '.'.join([rand(0, 255) for p1 in range(2)]),
        "TEST-NET-1": "192.0.2." + rand(64, 128)
    }

    return TYPES[type]


def i2i(_from: str, to: str) -> list[str]:
    ips = []

    for decimal in range(i2n(_from), i2n(to) + 1):
        ip = n2i(decimal)
        ips.append(ip)
    return ips


def i2n(ip: str) -> int:
    m = map(int, ip.split("."))
    octets = list(m)

    o1 = octets[0] << 24
    o2 = octets[1] << 16
    o3 = octets[2] << 8
    o4 = octets[3]

    decimal = o1 | o2 | o3 | o4

    return decimal


def n2i(decimal: int) -> str:
    octets = []
    for c in range(3, -1, -1):
        cider = c << 3  # 24, 16, 8
        octet = str(decimal >> cider & 255)
        octets.append(octet)
    return '.'.join(octets)


def i2b(ip: str, sep: str = ".", ret_sep: str = ".", _as: str = str) -> str | list[str]:
    octets = []
    for o in ip.split(sep):
        octet = int(o)
        octets.append(number_to_binary(octet))

    if _as == str:
        return ret_sep.join(octets)
    elif _as == list:
        return octets


def b2i(binray: str, sep: str = "."):
    binary_octets = binray.split(sep)
    octets = []

    for o in binary_octets:
        octets.append(str(binary_to_number(o)))

    return '.'.join(octets)


def i2p(ip: str) -> bytes:  # ip to packed binary representation
    pack_array = bytearray(4)
    octets = ip.split('.')

    for i in range(4):
        pack_array[i] = int(octets[i])
    return bytes(pack_array)


def p2i(bytes_array: bytes) -> str:  # packed binary to ip
    return '.'.join([o for o in map(str, bytes_array)])


def c2n(cidr: int) -> int:  # cidr to decimal
    max_ip = 2 ** 32
    max_cidr = 32
    return (max_ip - 1) << (max_cidr - cidr)


def c2i(cidr: int) -> str:  # cidr to mask
    return n2i(c2n(cidr))


def i2c(mask: str, sep: str = ".") -> int:  # mask to cidr
    return i2b(mask, sep).count("1")


def r2r(ipv4: str) -> list[str]:  # cidr to range
    parts = ipv4.split("/")
    network_address = parts[0]
    prefix_length = int(parts[1])

    network_int = i2n(network_address)
    mask_int = c2n(prefix_length)

    first_int = network_int & mask_int
    last_int = first_int | (2 ** (32 - prefix_length) - 1)

    return [n2i(first_int), n2i(last_int)]


def n2c(decimal: int) -> int:
    ip = n2i(decimal)
    return i2c(ip)


def r2c(start: str, end: str) -> int:
    start_int = i2n(start)
    end_int = i2n(end)

    prefix_length = 32
    while (start_int ^ end_int) >> (32 - prefix_length):
        prefix_length -= 1

    return prefix_length  # range to cidr


def c2h(cidr: int) -> int:  # cidr to host
    return 2 ** (32 - cidr) - 2


def h2c(hosts: int) -> int:
    net_bits = 1

    while ((2 ** net_bits) - 2) < hosts:
        net_bits += 1

    return 32 - net_bits


def m2n(mac: str, sep: str = ":"):
    hextets = mac.split(sep)
    numtets = []
    for h in hextets:
        numtets.append(int(h, 16))
    return sep.join(map(str, numtets))


def n2m(decimal_mac: str, sep: str = ":"):
    numtets = map(int, decimal_mac.split(sep))
    hextets = []
    for n in numtets:
        hextets.append(hex(n)[2:])
    return sep.join(map(str, hextets))


def m2b(mac: str, sep: str = ":"):
    hextets = mac.split(sep)
    binary = []
    for h in hextets:
        binary.append(number_to_binary(int(h, 16)))
    return sep.join(binary)


def b2m(binary: str, sep: str = ":"):
    binary_parts = binary.split(sep)
    hextets = []
    for b in binary_parts:
        hextets.append(hex(binary_to_number(b))[2:])
    return sep.join(map(str, hextets))


def v2a(vi: str):  # vendor id to address
    with open("oui.json", "r") as ouis:
        oui = json.loads(ouis.read())
        vi = vi.replace(":", "").replace("-", "").replace(" ", "")
        if vi in oui:
            return oui[vi]
        else:
            return {}

def p2d(ips: list[str], ports_range: range = range(0, 65536), timeout: int = 0.1):  # port to detect
    result = {}

    def scan(i: str, p: int):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(timeout)
        response = sock.connect_ex((i, p))

        if response == 0:
            result.setdefault(ip, [])
            result[ip].append(port)
        sock.close()

    processes = []
    for ip in ips:
        for port in ports_range:
            process = threading.Thread(target=scan, args=(ip, port))
            processes.append(process)
            process.start()

    for p in processes:
        p.join()

    return result