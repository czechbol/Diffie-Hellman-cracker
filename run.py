from random import randint
from timeit import default_timer as timer

from functions.cracking import cpu_brute_mt
from functions.cracking import babystep_giantstep
from functions import primes


class DHCryptosystem:
    """Object containing all values of the cryptosystem"""

    def __init__(self):
        self.prime = None  # publicly known
        self.generator = None  # publicly known
        self.alice_secret = None  # only Alice knows this
        self.bob_secret = None  # only Bob knows this
        self.alice_sends = None  # publicly known
        self.bob_sends = None  # publicly known
        self.alice_key = None  # only Alice knows this
        self.bob_key = None  # only Bob knows this

    def generate_from(
        self,
        bit_size: int = None,
        prime: int = None,
        generator: int = None,
        alice_secret: int = None,
        bob_secret: int = None,
        alice_sends: int = None,
        bob_sends: int = None,
        key: int = None,
    ):
        """Generates the DHCryptosystem values (If not passed == if they are None) or assigns them

        Args:
            bit_size (int, optional): Bit size of the prime. Not necessary if prime also passed. Defaults to None.
            prime (int, optional): Prime number base of the cryptosystem. Defaults to None.
            generator (int, optional): Generator of the cryptosystem. Defaults to None.
            alice_secret (int, optional): Alice's secret. Defaults to None.
            bob_secret (int, optional): Bob's secret. Defaults to None.
            alice_sends (int, optional): Alice sends. Defaults to None.
            bob_sends (int, optional): Bob sends. Defaults to None.
            key (int, optional): Established key. Defaults to None.

        Raises:
            ValueError: If neither bit_size or prime is passed. One of these is required
        """
        if prime is None and bit_size is None:
            raise ValueError("Either prime or bit_size must be specified")

        self.prime = prime if prime is not None else primes.getPrime(bit_size)
        self.generator = generator if generator is not None else randint(1, self.prime - 1)  # nosec
        self.alice_secret = alice_secret if alice_secret is not None else randint(1, self.prime)  # nosec
        self.bob_secret = bob_secret if bob_secret is not None else randint(1, self.prime)  # nosec
        self.alice_sends = (
            alice_sends if alice_sends is not None else pow(self.generator, self.alice_secret, self.prime)
        )
        self.bob_sends = (
            bob_sends if bob_sends is not None else pow(self.generator, self.bob_secret, self.prime)
        )
        self.alice_key = key if key is not None else pow(self.bob_sends, self.alice_secret, self.prime)
        self.bob_key = key if key is not None else pow(self.alice_sends, self.bob_secret, self.prime)

    def print_info(self):
        print(f"Prime is {self.prime}, Generator is {self.generator}")
        print(f"Alice's secret is {self.alice_secret}, Bob's secret is {self.bob_secret}")
        print()
        print(f"Alice sends: {self.alice_sends}, Bob sends: {self.bob_sends}")
        print(f"Alice's key: {self.alice_key}, Bob's key: {self.bob_key}")
        print()


class CrackMeDH:
    """used just for passing variables to crackers more conveniently"""

    def __init__(self, prime, generator, alice_sends, bob_sends):
        self.prime = prime
        self.generator = generator
        self.alice_sends = alice_sends
        self.bob_sends = bob_sends


if __name__ == "__main__":
    DH = DHCryptosystem()
    corr_inp = False
    while not corr_inp:
        try:
            bit_size = int(input("How many bits should the prime number have? "))
            corr_inp = True
        except ValueError:
            print("Please enter a number")

    DH.generate_from(bit_size=bit_size)
    DH.print_info()

    print("Here is a list of available functions:")
    print("1 - Brute-force")
    print("2 - Baby-step giant-step")
    print()

    corr_inp = False

    while not corr_inp:
        try:
            inp = int(input("Select function to crack with..."))
            if inp not in [1, 2]:
                raise ValueError
            corr_inp = True
        except ValueError:
            print("Please use either 1 or 2")

    start = timer()

    if 1 == inp:
        cracked_key = cpu_brute_mt.calculate_key(
            CrackMeDH(DH.prime, DH.generator, DH.alice_sends, DH.bob_sends)
        )
    elif 2 == inp:
        cracked_key = babystep_giantstep.calculate_key(
            CrackMeDH(DH.prime, DH.generator, DH.alice_sends, DH.bob_sends)
        )
    if cracked_key is None:
        cracked_key = "Key not found"

    print(f"Cracked key {cracked_key}")
    print()
    print("Cracking took", timer() - start, "seconds to run")
