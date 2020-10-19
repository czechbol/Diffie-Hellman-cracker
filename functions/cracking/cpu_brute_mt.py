import psutil
import multiprocessing
import math
import time


def calculate_key(n: int, g: int, alicesends: int, bobsends: int):
    n: int = n  # publicly known
    g: int = g  # publicly known
    alicesends: int = alicesends  # publicly known
    bobsends: int = bobsends  # publicly known

    num_cpus: int = psutil.cpu_count(logical=True)
    print("Number of CPU threads being used: ", num_cpus)
    print("Number of parallel processes used in cracking: ", num_cpus)
    print()

    parts = math.ceil(n / num_cpus)
    startvalue = 1
    args = []

    for a in range(0, int(num_cpus)):
        args.append([n, g, alicesends, bobsends, startvalue, parts * (a + 1), 1])
        startvalue = parts * a

    key: int = multi(num_cpus, args)

    return key


def multi(num_cpus, args):
    # Create Event
    event = multiprocessing.Event()

    jobs = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=crack, args=args[i] + [event])
        p.start()
        jobs.append(p)
    while True:
        if event.is_set():
            print("Exiting all child processess..")
            print()
            for i in jobs:
                # Terminate each process
                i.terminate()
            # Terminating main process
            f = open("temp.txt", "r")
            key = int(f.read())
            return key
        time.sleep(2)
    for i in jobs:
        i.join()
    f = open("temp.txt", "r")
    key = int(f.read())
    return key


def crack(n: int, g: int, alicesends: int, bobsends: int, a: int, x: int, inc: int, event):
    key: int = 0
    for i in range(a, x, inc):
        log = (g ** i) % n
        if log == alicesends:
            key = pow(bobsends, i, n)
            f = open("temp.txt", "w+")
            f.write(str(key))
            f.close()
            print("Found A: ", i)
            event.set()
            break
        if log == bobsends:
            key = pow(alicesends, i, n)
            f = open("temp.txt", "w+")
            f.write(str(key))
            f.close()
            print("Found B: ", i)
            event.set()
            break

    return key
