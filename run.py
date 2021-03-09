import random
from timeit import default_timer as timer

from functions.cracking import cpu_brute_mt
from functions.cracking import babystep_giantstep
from functions import primes


class DHCryptosystem:
    """Object containing all values of the cryptosystem"""

    def __init__(self, bit_size):
        self.prime = primes.getPrime(bit_size)  # publicly known, generates a random prime number of bit size
        self.generator = random.randint(1, self.prime - 1)  # publicly known
        self.alice_secret = random.randint(1, self.prime)  # only Alice knows this
        self.bob_secret = random.randint(1, self.prime)  # only Bob knows this
        self.alice_sends = pow(self.generator, self.alice_secret, self.prime)  # publicly known
        self.bob_sends = pow(self.generator, self.bob_secret, self.prime)  # publicly known
        self.alice_key = pow(self.bob_sends, self.alice_secret, self.prime)  # only Alice knows this
        self.bob_key = pow(self.alice_sends, self.bob_secret, self.prime)  # only Bob knows this

    def print_info(self):
        print(f"P is {self.prime}, G is {self.generator}")
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
    corr_inp = False
    while not corr_inp:
        try:
            inp = int(input("How many bits should the prime number have? "))
            corr_inp = True
        except ValueError:
            print("Please enter a number")

    DH = DHCryptosystem(inp)
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
