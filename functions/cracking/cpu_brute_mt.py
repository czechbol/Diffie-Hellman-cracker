import psutil
import multiprocessing
import math
from itertools import count, islice


def chunker(num_chunks: int, prime: int) -> list:
    """Splits the range into num_cpus size list of subranges.

    Args:
        num_chunks (int): Number of chunks to create
        prime (int): Prime number to get the range from

    Returns:
        list: List of iterators
    """

    chunk_size = int(math.ceil(prime / num_chunks))
    prev_chunk = 0
    chunks = []
    for i in range(num_chunks):
        this_chunk_start = prev_chunk
        remaining = prime - chunk_size
        if remaining < chunk_size:
            chunks.append(islice(count(this_chunk_start), remaining))
        else:
            chunks.append(islice(count(this_chunk_start), chunk_size))
        prev_chunk = this_chunk_start + chunk_size

    return chunks


def calculate_key(crack_me) -> int or None:
    """Calculates the DHCryptosystem key by utilizing multiprocessing enhanced brute force. CPU intensive

    Args:
        crack_me (CrackMeDH object): Object containing the publicly know values of the cryptosystem.

    Returns:
        int or None: int if a key was found, else None
    """

    max_num_cpus: int = psutil.cpu_count(logical=True)
    corr_inp = False
    while not corr_inp:
        try:
            num_cpus = int(input(f"How many cores should be utilized? (1-{max_num_cpus}): "))
            if not 1 <= num_cpus <= max_num_cpus:
                raise ValueError
            corr_inp = True
        except ValueError:
            print(f"Please choose a number between 1 and {max_num_cpus}")

    chunks = chunker(num_cpus, crack_me.prime)
    key = multi_cracking(crack_me, chunks)  # Deals with multiprocessing, returns found key

    return key


def multi_cracking(crack_me, chunks: list) -> int or None:
    """Used for spawning cracker process for each subrange if the prime

    Args:
        crack_me (CrackMeDH object): Object containing the publicly know values of the cryptosystem.
        chunks (list): List of iterators

    Returns:
        int or None: int if a key was found, else None
    """

    jobs = []
    key = multiprocessing.Value("i", -1)
    for chunk in chunks:
        process = multiprocessing.Process(target=cracker, args=(crack_me, chunk, key))
        process.start()
        jobs.append(process)
    for process in jobs:
        process.join()
    return key.value if not key.value == -1 else None


def cracker(crack_me, chunk: islice, key: multiprocessing.Value):
    """Where the magic of brute force happens

    Args:
        crack_me (CrackMeDH object): Object containing the publicly know values of the cryptosystem.
        chunk (islice): iterator through which we loop
        key (multiprocessing.Value): thread safe variable used to save the foud key
    """

    for i in chunk:
        if key.value != -1:
            return

        test = pow(crack_me.generator, i, crack_me.prime)
        if test == crack_me.alice_sends:
            with key.get_lock():
                key.value = pow(crack_me.bob_sends, i, crack_me.prime)
            print(f"Found possible Alice's secret: {i}")
            break
        if test == crack_me.bob_sends:
            with key.get_lock():
                key.value = pow(crack_me.alice_sends, i, crack_me.prime)
            print(f"Found possible Bob's secret: {i}")
            break
