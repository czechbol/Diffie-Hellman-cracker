import CPU_cracking
import BSGS
import random
from Crypto.Util import number
from timeit import default_timer as timer


if __name__ == "__main__":
    start = timer()

    p: int = number.getPrime(12)  # publicly known, generates a random prime number
    g: int = random.randint(1, p - 1)  # publicly known  5#
    a: int = random.randint(1, p)  # only Alice knows this 1398102#
    b: int = random.randint(1, p)  # only Bob knows this  1398103#
    aliceSends = (g ** a) % p
    bobSends = (g ** b) % p
    aliceComputes = (bobSends ** a) % p
    bobComputes = (aliceSends ** b) % p

    print("P is ", p, ", G is ", g)
    print("A is ", a, ", B is ", b)
    print()
    print("Alice sends: ", aliceSends)
    print("Bob sends: ", bobSends)
    print("Bob computes: ", bobComputes)
    print("Alice computes: ", aliceComputes)
    print()
    cracked_a: int = 0

    print("Here is a list of functions:")
    print("1 - Brute-force")
    print("2 - Baby-step giant-step")
    print()
    try:
        a = int(input("Select function to crack with..."))
    except ValueError:
        print("Please use either 1 or 2")
    if 1 == a:
        cracked_CPU = CPU_cracking.calculate_key(p, g, aliceSends, bobSends)
    elif 2 == a:
        cracked_CPU = BSGS.baby_steps_giant_steps(p, g, aliceSends)

    print("Cracked key ", cracked_CPU)
    print()
    print("Cracking took took", timer() - start, "seconds to run")