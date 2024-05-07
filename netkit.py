import json
import random
import re
import threading
from enum import Enum
from socket import AF_INET, socket, SOCK_STREAM
from general import int2bin, bin2int

class ipTYPES(Enum):
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


_all_ = ['b2i', 'b2m', 'c2i', 'c2n', 'i2b', 'i2c', 'i2i', 'i2n', 'i2p', 'i2t', 'isipv4', 'm2b', 'm2n',
         'n2c', 'n2i', 'n2m', 'p2i', 'r2c', 'r2r', 't2i', 'v2a', 'p2d']


class IPGenerator:
    def private(self):
        ...

    def public(self):
        ...

    def loopback(self):
        ...

    def link_local(self):
        ...

    def multicast(self):
        ...

    def reserved(self):
        ...

    def reserved_iana(self):
        # reserved for IANA
        ...

    def ietf(self):
        # IETF Protocol Assignment
        ...

    def carrier_grade_nat(self):
        # Carrier-grade NAT
        ...

    def test_net1(self):
        # TEST-NET-1
        ...


class PacketGenerator:
    ...


class Detector:
    """ ToDo: detect types """
    ...



class IPGenerator:
    """ ToDo: ip by type and so on (: """
    ...


class Convertor:
    ...


class Validator:
    def __init__(self):
        ...

    def ipv4(self, ip: str, sep: str = ".") -> bool:
        """
        * Check if the given ip is valid ipv4

        Example:
            :param ip: 0.0.0.0
            :param sep: by default "."
            :return: True
        """

        try:
            dots = ip.count(sep) == 3
            octets = list(map(int, ip.split(sep)))
            bits = [0 <= o <= 255 for o in octets]

            return dots == (len(octets) == 4) == list(set(bits))[0]
        except (IndexError, ValueError, TypeError) as error:
            return False

    def ipv6(self, ip: str, sep: str = ":"):
        ...

    def mac(self, mac: str, sep: str = ":"):
        """
        Validate the mac address true/false format

        <In ff:ff:ff:00:00:00
        Out> true
        """
        return re.match("^([0-9A-Fa-f]{2}" + sep + "){5}[0-9A-Fa-f]{2}$", string=mac) is not None

    def port(self, port: int) -> bool:
        """
        * Check if the given port is in the range MIN_PORT - MAX_PORT

        :param port: 145
        :return: True
        """

        is_num = isinstance(port, int)
        in_range = MIN_PORT <= port <= MAX_PORT

        return is_num and in_range

    def cidr(self, n: int) -> bool:
        ...

    def url(self, url: str) -> bool:
        ...

    def status_code(self, code: int) -> bool:
        ...

    def vlan(self, id: int) -> bool:
        """
        Based on the IEEE 802.1Q standard
        VLAN Ranges:
            reserved = 0, 4095
                ~ Can't be seen or used.
            normal:
                1
                    ~ Default VLAN.
                    ~ Can't be deleted.
                2-1001
                    ~ Used for Ethernet.
                    ~ Can be created/deleted.
                1002-1005
                    ~ Default for FDDI (Fiber Distributed Data Interface) and token ring.
                    ~ Can't be deleted.
            extended: 1006-4094
                ~ Used only for ethernet VLANs.

        reference: https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4500/12-2/25ew/configuration/guide/conf/vlans.pdf

        * Check if the given vlan id is in the range MIN_VLAN - MAX_VLAN

        :param id: 20
        :return: True
        """

        is_num = isinstance(id, int)
        in_range = MIN_VLAN <= id <= MAX_VLAN

        return is_num and in_range

print(Validator().mac("01:23:45:ab:cd:fg"))


def t2c():  # ToDo: status code type to code
    ...


def c2t():  # ToDo: code to type
    ...


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
        >> 192.168.1.1
        "private"
        >> 8.8.8.8
        "public"
        >> 127.0.0.1
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


def t2i(type: str = ipTYPES.PRIVATE):  # type to random ip
    """
    ipv4 type to random ip

    - Private:
        ip/cidr     = 0.0.0.0/8
        mask        = 255.0.0.0
        range       = 0.0.0.0 - 0.255.255.255
        scope       = private
        rfc         = 1122
        description = RFC 1122, Section 3.2.1.3
        ----------------------------
        ip/cidr     = 10.0.0.0/8
        mask        = 255.0.0.0
        range       = 10.0.0.0 - 10.255.255.255
        scope       = private
        rfc         = 1918
        description =
        ----------------------------
        ip/cidr     = 100.64.0.0/10
        mask        = 255.192.0.0
        range       = 100.64.0.0 - 100.127.255.255
        scope       = private
        rfc         = 6598
        description =
        ----------------------------
        ip/cidr     = 172.16.0.0/12
        mask        = 255.240.0.0
        range       = 172.16.0.0 - 172.31.255.255
        scope       = private
        rfc         = 1918
        description =
        ----------------------------
        ip/cidr     = 192.168.0.0/24
        mask        = 255.255.255.0
        range       = 192.0.0.0 - 192.0.0.255
        scope       = private
        rfc         = 5736
        description = IETF Protocol Assignments
        ----------------------------
        ip/cidr     = 192.168.0.0/16
        mask        = 255.255.0.0
        range       = 192.168.0.0 - 192.168.255.255
        scope       = private
        rfc         = 1918
        description =
        ----------------------------
        ip/cidr     = 192.18.0.0/15
        mask        = 255.254.0.0
        range       = 192.18.0.0 - 192.19.255.255
        scope       = private
        rfc         = 2544
        description = Network Interconnect Device Benchmark Testing
    - Internet:
        ip/cidr     = 192.88.99.0/24
        mask        = 255.255.255.0
        range       = 192.88.99.0 - 192.88.99.255
        scope       = internet
        rfc         = 3068
        description = 6to4 Relay Anycast
        ----------------------------
        ip/cidr     = 224.0.0.0/4
        mask        = 240.0.0.0
        range       = 224.0.0.0 - 239.255.255.255
        scope       = internet
        rfc         = 3171
        description = Multicast
    - Documentation:
        ip/cidr     = 192.0.2.0/24
        mask        = 255.255.255.0
        range       = 192.0.2.0 - 192.0.2.255
        scope       = documentation
        rfc         = 5737
        description = TEST-NET-1
        ----------------------------
        ip/cidr     = 198.51.100.0/24
        mask        = 255.255.255.0
        range       = 198.51.100.0 - 198.51.100.255
        scope       = documentation
        rfc         = 5737
        description = TEST-NET-2
        ----------------------------
        ip/cidr     = 203.0.113.0/24
        mask        = 255.255.255.0
        range       = 203.0.113.0 - 203.0.113.255
        scope       = documentation
        rfc         = 5737
        description = TEST-NET-3
    - Subnet:
        ip/cidr     = 169.254.0.0/16
        mask        = 255.255.0.0
        range       = 169.254.0.0 - 169.254.255.255
        scope       = subnet
        rfc         = 3927
        description = Link Local
    - Host:
        ip/cidr     = 127.0.0.0/8
        mask        = 255.0.0.0
        range       = 127.0.0.0 - 127.255.255.255
        scope       = host
        rfc         = 1122
        description = Loopback (RFC 1122, Section 3.2.1.3)
    - n/a:
        ip/cidr     = 240.0.0.0/4
        mask        = 240.0.0.0
        range       = 240.0.0.0 - 255.255.255.255
        scope       = n/a
        rfc         = 1122
        description = Reserved for Future Use (RFC 1112, Section 4)
        ----------------------------
        ip/cidr     = 255.255.255.255/32
        mask        = 255.255.255.255
        range       = 255.255.255.255 - 255.255.255.255
        scope       = n/a
        rfc         = 919, 922
        description = Limited Broadcast (RFC 919, Section 7, RFC 922, Section 7)

    :param type: ipv4.type
    :return: x.x.x.x (ip based on the type)
    """
    rand = lambda f, t: str(random.choice(list(range(f, t + 1))))
    TYPES = {
        "private": random.choice(
            [
                "10." + '.'.join([rand(0, 255) for p1 in range(3)]),
                "172." + '.'.join([rand(16, 31) for p2 in range(3)]),
                "192.168." + '.'.join([rand(0, 255) for p2 in range(2)])
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



def r2c(start: str, end: str) -> int:  # range to cidr
    """
    Example:
        :param start: 192.168.10.0
        :param end: 192.168.10.16
        :return: 27
    """

    start_int = i2n(start)
    end_int = i2n(end)

    prefix_length = 32
    while (start_int ^ end_int) >> (32 - prefix_length):
        prefix_length -= 1

    return prefix_length


def v2a(vi: str):  # vendor id to address
    with open("organizations.json", "r") as ouis:
        oui = json.loads(ouis.read())
        vi = vi.replace(":", "").replace("-", "").replace(" ", "")
        if vi in oui:
            return oui[vi]
        else:
            return {}



def ports(ips: list[str], ports_range: range = range(0, 65536), timeout: int = 1):  # ports or port scan
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


print(r2r("255.255.255.255/32"))
print(c2i(32))
