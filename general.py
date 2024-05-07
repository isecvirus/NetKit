def int2bin(decimal: int, fill: bool = True) -> str:
    """
    :param decimal: number
    :param fill: pad zeros to the left to the length of 8
    :return:
    """

    binary_octet = ""

    while decimal > 0:
        remainder = decimal % 2
        binary_octet = str(remainder) + binary_octet

        decimal //= 2

    return binary_octet.zfill(8) if fill else binary_octet


def bin2int(binary: str) -> int:
    """
    :param binary: binary to integer
    :return:
    """

    decimal = 0

    for digit in binary:
        decimal = decimal * 2 + int(digit)

    return decimal


