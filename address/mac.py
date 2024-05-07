import random
import re
from general import int2bin


class MAC:
    def __init__(self, mac: str = None, sep: str = ":"):
        self.mac = mac
        self.sep = sep

    def integer(self):
        """
        from real mac to decimal reper

        <In ff:ff:ff:00:00:00
        Out> 255:255:255:00:00:00
        """

        hextets = self.mac.split(self.sep)
        numtets = []

        for h in hextets:
            numtets.append(int(h, 16))

        return self.sep.join(map(str, numtets))

    def int2mac(self):
        """
        from decimal reper to real mac

        <In 255:255:255:00:00:00
        Out> ff:ff:ff:00:00:00
        """

        numtets = map(int, self.mac.split(self.sep))
        hextets = []

        for n in numtets:
            hextets.append(hex(n)[2:])
        return self.sep.join(map(str, hextets))

    def binary(self):
        """
        from real mac to binary reper

        <In ff:ff:ff:00:00:00
        Out> 11111111:11111111:11111111:00000000:00000000:00000000
        """

        hextets = self.mac.split(self.sep)
        binary = []

        for h in hextets:
            binary.append(int2bin(int(h, 16)))

        return self.sep.join(binary)

    def bin2mac(self):
        """
        from binary reper to real mac

        <In 11111111:11111111:11111111:00000000:00000000:00000000
        Out> ff:ff:ff:00:00:00
        """
        bin_parts = self.mac.split(self.sep)
        parts = []

        for part in bin_parts:
            parts.append(hex(int(part, 2))[2:].ljust(2, '0'))

        return self.sep.join(parts)

    def get_random(self) -> str:
        """
        get random mac address
        """

        chars = "0123456789ABCDEF"

        return self.sep.join([random.choice(chars) + random.choice(chars) for __ in range(6)])

    def vendor(self):
        ...