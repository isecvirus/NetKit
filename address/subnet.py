from ip import IPv4


class METHOD:
    FLSM = "flsm"
    VLSM = "vlsm"
    CLASSFUL = "classful"
    CIDR = "cidr"


DEFAULT_METHOD = METHOD.FLSM


class Subnet:
    def __init__(self, ip: str, cidr: int, method: str = DEFAULT_METHOD):
        self.ip = ip
        self.cidr = cidr
        self.method = method


    def set(self, key: str, value: str | int | None):
        if hasattr(self, key):
            attr_type = type(getattr(self, key))

            if not isinstance(value, attr_type):
                raise ValueError(f"{key!r} isn't of type {type(value)}")

            setattr(self, key, value)
        else:
            raise AttributeError(f"{self.__class__.__name__!r} han no attribute called {key!r}")

    def first(self):
        """
        The first IP in any block is known as the “network address”.
        """
        ipv4 = IPv4(ip=self.ip)

        ...

    def last(self):
        """
        The last IP in any block is known as the “broadcast address”.
        """

        ...

    def available(self):
        ...

    def in_range(self, ip: str):
        ...

    def __len__(self):
        ...

    def __format__(self, format_spec: str):
        match format_spec:
            case "first":
                ...  # get first usable ip
            case "last":
                ...  # get last usable ip
            case "usable":
                ...  # get usable (from, to)
            case "network":
                ...  # get network id
            case "broadcast":
                ...  # get broadcast id
            case "cidr":
                ...  # get cidr
            case _:
                raise ValueError(f"{format_spec!r} isn't a valid formatter")

subnet = Subnet(ip="192.168.100.0", cidr=24)
print(subnet.ip)
subnet.set("cidr", "0.0.0.0")
print(subnet.ip)
