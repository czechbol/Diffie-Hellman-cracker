import random
from timeit import default_timer as timer

from functions.cracking import cpu_brute_mt
from functions.cracking import babystep_giantstep
from functions import prime


if __name__ == "__main__":
    p: int = prime.getPrime(22)  # publicly known, generates a random prime number of bit size
    g: int = random.randint(1, p - 1)  # publicly known
    a: int = random.randint(1, p)  # only Alice knows this
    b: int = random.randint(1, p)  # only Bob knows this
    aliceSends = pow(g, a, p)
    bobSends = pow(g, b, p)
    aliceComputes = pow(bobSends, a, p)
    bobComputes = pow(aliceSends, b, p)

    print("P is ", p, ", G is ", g)
    print("a is ", a, ", b is ", b)
    print()
    print("Alice sends: " + str(aliceSends) + ", Bob sends: " + str(bobSends))
    print("Alice computes: " + str(aliceComputes) + ", Bob computes: " + str(bobComputes))
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

    start = timer()

    if 1 == a:
        cracked_key = cpu_brute_mt.calculate_key(p, g, aliceSends, bobSends)
    elif 2 == a:
        temp = babystep_giantstep.calculate_key(p, g, aliceSends)
        log = pow(g, temp, p)
        if log == aliceSends:
            cracked_key = pow(bobSends, temp, p)
            print("Found A: ", temp)
        if log == bobSends:
            cracked_key = pow(aliceSends, temp, p)
            print("Found B: ", temp)

    print("Cracked key ", cracked_key)
    print()
    print("Cracking took took", timer() - start, "seconds to run")
