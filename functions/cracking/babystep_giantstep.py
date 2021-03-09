import math


def calculate_key(crack_me) -> int or None:
    """Discrete logarithm problem solution using the Baby-step Giant-step algorithm. RAM intensive.

    Args:
        crack_me (CrackMeDH object): Object containing the publicly know values of the cryptosystem.

    Returns:
        int or None: int if a key was found, else None
    """
    N = 1 + int(math.sqrt(crack_me.prime))

    baby_steps_tabulka = {}
    baby_step = 1
    for i in range(N + 1):
        baby_steps_tabulka[baby_step] = i
        baby_step = baby_step * crack_me.generator % crack_me.prime

    inverzni_k_N = pow(crack_me.generator, (crack_me.prime - 2) * N, crack_me.prime)
    giant_step = crack_me.alice_sends

    for j in range(N + 1):
        if giant_step in baby_steps_tabulka:
            temp = j * N + baby_steps_tabulka[giant_step]
            log = pow(crack_me.generator, temp, crack_me.prime)
            if log == crack_me.alice_sends:
                cracked_key = pow(crack_me.bob_sends, temp, crack_me.prime)
                print(f"Found possible Alice's secret: {temp}")
            if log == crack_me.bob_sends:
                cracked_key = pow(crack_me.alice_sends, temp, crack_me.prime)
                print(f"Found possible Bob's secret: {temp}")
            return cracked_key
        else:
            giant_step = giant_step * inverzni_k_N % crack_me.prime
    return None
