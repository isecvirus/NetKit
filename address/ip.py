from general import bin2int, int2bin
from variable import MAX_CIDR, MAX_IP

TYPE = {
    "private": {},
    "internet": {},
    "documentation": {},
    "subnet": {},
    "host": {},
    "n/a": {}
}


class IPv4:
    def __init__(self, ip: str | int | bytes = None, sep: str = "."):
        """
        __INIT__ method, set the initial ip address

        :param ip:
        :param sep: ip separator
        """

        self.ip = ip
        self.sep = sep

    def binary(self, ip: str = None) -> str:
        """
        full ip to binary

        <In 192.168.10.1
        Out> 11000000.10101000.00001010.00000001
        """

        if ip is None:
            ip = self.ip
        octets = []
        for o in ip.split(self.sep):
            octet = int(o)
            octets.append(int2bin(octet))

        return self.sep.join(octets)

    def bin2ip(self, ip: str = None) -> str:
        """
        binary to full ip address

        <In 11000000.10101000.00001010.00000001
        Out> 192.168.10.1
        """

        if ip is None:
            ip = self.ip
        binary_octets = ip.split(self.sep)
        octets = []

        for o in binary_octets:
            octets.append(str(bin2int(o)))

        return self.sep.join(octets)

    def pack(self, ip: str = None) -> bytes:
        """
        pack ip address to bytes

        <In 192.168.10.1
        Out> \xc0\xa8\n\x01
        """

        if ip is None:
            ip = self.ip
        pack_array = bytearray(4)
        octets = ip.split(self.sep)

        for i in range(4):
            pack_array[i] = int(octets[i])

        return bytes(pack_array)

    def unpack(self, ip: bytes = None) -> str:
        """
        unpack packed ip address

        <In \xc0\xa8\n\x01
        Out> 192.168.10.1
        """

        if ip is None:
            ip = self.ip
        return self.sep.join([o for o in map(str, ip)])

    def integer(self, ip: str = None) -> int:
        """
        ip to decimal reper

        <In 192.168.10.1
        Out> 3232238081
        """

        if ip is None:
            ip = self.ip
        m = map(int, ip.split(self.sep))
        octets = list(m)

        o1 = octets[0] << 24
        o2 = octets[1] << 16
        o3 = octets[2] << 8
        o4 = octets[3]

        decimal = o1 | o2 | o3 | o4

        return decimal

    def int2ip(self, ip: int = None) -> str:
        """
        decimal to ip address

        <In 3232238081
        Out> 192.168.10.1
        """

        if ip is None:
            ip = self.ip

        octets = []

        for c in range(3, -1, -1):
            cidr = c << 3  # 24, 16, 8
            octet = str(ip >> cidr & 255)
            octets.append(octet)

        return self.sep.join(octets)

    def pool(self, to: str, _from: str = None) -> list[str]:
        """
        pool of ip addresses from range x to range y

        <In 192.168.10.1-192.168.10.3
        Out> ['192.168.10.1', '192.168.10.2', '192.168.10.3']

        :param to:
        :param _from:
        """

        if not _from:
            _from = self.ip

        ips = []

        for decimal in range(self.integer(_from), self.integer(to) + 1):
            ip = self.int2ip(decimal)
            ips.append(ip)

        return ips

    def cidr(self, ip: str = None):
        """
        get ip cidr using ip

        <In 255.255.0.0
        Out> 16

        :param ip:
        """

        if ip is None:
            ip = self.ip

        return self.binary(ip).count("1")

    def range_cidr(self, end:str, start:str=None):
        """
        ip range to cidr

        :param end:
        :param start:

        <In start=192.168.10.0, end=192.168.10.16
        Out> 27

        :return:
        """

        if start is None:
            start = self.ip

        start_int = self.integer(start)
        end_int = self.integer(end)

        cidr = 32
        while (start_int ^ end_int) >> (MAX_CIDR - cidr):
            cidr -= 1

        return cidr

    def range(self, ip: str=None, cidr: int = None) -> tuple[str, str]:
        """
        range to range (using cidr)

        <In 192.168.0.0/24
        Out> ('192.168.10.0', '192.168.10.255')

        :param ip:
        """

        if ip is None:
            ip = self.ip

        parts = ip.split("/")
        network_address = parts[0]  # ip
        if cidr is None:
            cidr = int(parts[1])  # cidr

        network_int = self.integer(network_address)
        rest_cidr = MAX_CIDR - cidr
        mask_int = MAX_IP - (1 << rest_cidr)

        first_int = network_int & mask_int
        last_int = first_int | (2 ** (32 - cidr) - 1)

        return self.int2ip(first_int), self.int2ip(last_int)

    def type(self, ip: str = None):
        """
        get the ip type private, public

        <In 192.168.100.13
        Out> private

        :param ip:
        """

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
        - Public:
            ip/cidr     = 192.88.99.0/24
            mask        = 255.255.255.0
            range       = 192.88.99.0 - 192.88.99.255
            scope       = public
            rfc         = 3068
            description = 6to4 Relay Anycast
            ----------------------------
            ip/cidr     = 224.0.0.0/4
            mask        = 240.0.0.0
            range       = 224.0.0.0 - 239.255.255.255
            scope       = public
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

        if ip is None:
            ip = self.ip


ipv4 = IPv4("192.168.10.0")
# print(ipv4.range())
print(ipv4.range_cidr(end="192.168.10.224"))
print(ipv4.type())
