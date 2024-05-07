from variable import MAX_IP, MAX_CIDR

class CIDR:
    def __init__(self, cidr:int=None):
        self.cidr = cidr

    def ip(self, cidr:int=None, sep:str="."):
        """
        CIDR to ip address

        <In 16
        Out> 255.255.0.0

        :param cidr:
        """

        if cidr is None:
            cidr = self.cidr

        rest_cidr = MAX_CIDR - cidr
        decimal = MAX_IP - (1 << rest_cidr)

        octets = []

        for c in range(3, -1, -1):
            cidr = c << 3  # 24, 16, 8
            octet = str(decimal >> cidr & 255)
            octets.append(octet)

        return sep.join(octets)



cidr = CIDR()
print(cidr.ip(16))