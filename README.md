# Diffie-Hellman-cracker

Python program that generates and calculates a Diffie-Hellman key and then attacks the simulated exchange by working with variables that would cross between devices.

This program was made as an assignment at FEEC BUT, Applied Cryptography course. Now it's heavily modified from the original version with better optimization.

## There are two modes of attack:

- Multithreaded Brute-force attack (very CPU and time intensive)
- Baby-step Giant-step algorithm (Much faster but very RAM intensive)

## How to use:

Change variables passed to the `DH.generate_from()` method as you need. By default everything gets generated from the bit size of the desired prime number.

Then run the run.py file:
```console
foo@bar $ python3 run.py
```

## Disclaimer

Be careful about using big numbers, the largest number I was able to crack a 55 bit prime and it used over 20GB of RAM (BSGS algoritm).

Multithreaded brute-force attack is time and CPU intensive and I wasn't comfortable with running it longer than an hour (30 bit prime on a 6C/12T CPU)
