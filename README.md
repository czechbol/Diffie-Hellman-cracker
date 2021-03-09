# Diffie-Hellman-cracker

Python program that generates and calculates a Diffie-Hellman key and then attacks the simulated exchange by working with variables that would cross between devices.

This program was made as an assignment at FEEC BUT, Applied Cryptography course

## There are two modes of attack:

- Multithreaded Brute-force attack (very CPU and time intensive)
- Baby-step Giant-step algorithm (Much faster but very RAM intensive)

## How to use:

Pass variables to the `DH.generate_from()` method as you need. By default everything gets generated from the bit size of the desired prime number.

Then run the run.py file.

## Disclaimer

Be careful about using big numbers, the largest number I was able to crack a 55 bit generator and it used over 20GB of RAM (BSGS algoritm).

Multithreaded Bruteforce is time intensive and I wasn't comfortable with running it longer than an hour (30 bit generator on a 6C/12T CPU)
