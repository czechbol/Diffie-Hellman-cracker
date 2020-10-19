import math


def calculate_key(p, g, A):
    # vypocitame strop
    N = 1 + int(math.sqrt(p))

    # vytvorime baby step tabulku, ktera obsahuje vždy pár (g^i ; i)
    baby_steps_tabulka = {}
    baby_step = 1
    for i in range(N + 1):
        # vytvarime tabulku párů
        baby_steps_tabulka[baby_step] = i
        # nemusime umocnovat, staci kazdy loop vynasobit predchozi hodnotu generatorem
        baby_step = baby_step * g % p

    # print(baby_steps_tabulka)

    # fermatovou malou vetou vypocitame g^-N (inverzni prvek)
    inverzni_k_N = pow(g, (p - 2) * N, p)
    giant_step = A
    # podíváme se jestli se giant_step nachazi v tabulce baby_steps na prvnim miste
    # ANO - logaritmus se rovna q * N + hodnota z tabulky baby_steps na druhem miste (ten iterator i)
    # NE - giant_step vynasobime inverznim prvkem mod p a tim ziskame novou hodnotu giant_step, zkousime dal
    for j in range(N + 1):
        if giant_step in baby_steps_tabulka:
            return j * N + baby_steps_tabulka[giant_step]
        else:
            giant_step = giant_step * inverzni_k_N % p
    return "No Match"
