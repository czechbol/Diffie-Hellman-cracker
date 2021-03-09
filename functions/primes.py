from random import randint, getrandbits


def isProbablePrime(num: int, rounds: int = 5) -> bool:
    """Fermat's primality test

    Args:
        num (int): Number to be tested
        rounds (int, optional): How many rounds of tests should be performed. Defaults to 5.

    Returns:
        bool: True if prime else False
    """

    if num - 1 < 5:
        rounds = num - 1
    tries = 0

    for x in range(rounds):
        tester = randint(2, num - 2)  # nosec
        res = pow(tester, num - 1, num)
        if res != 1:
            return False
        tries += 1

    return True


def getPrime(bit_size: int) -> int:
    """Get a n-bit prime

    Args:
        bit_size (int): Bit size of the desired prime number

    Returns:
        int: desired prime number
    """
    prime = getrandbits(bit_size)  # nosec
    while not isProbablePrime(prime):
        prime = getrandbits(bit_size)
        if int(repr(prime)[-1]) % 2 == 0 or int(repr(prime)[-1]) % 5 == 0:
            # skip if last digit is divisible by 2 or 5
            continue
    return prime
