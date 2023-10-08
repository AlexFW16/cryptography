import numpy as np


# naive implementation, divides by ascending prime numbers and
# tests for primality each time.
def trial_division(n):
    prime = 2  # primes by which n is divided
    is_composite = True  # primality check of the newly obtained number
    factorization = []  # the wanted factorization

    while is_composite:
        if n % prime == 0:
            factorization.append(prime)
            n = int(n / prime)

            is_composite = isComposite(n)
        else:
            prime = getNextPrime(prime)

    if n != 1:  # otherwise, n was prime and 1 would be appended
        factorization.append(n)

    return factorization


def getNextPrime(prime):
    n = prime + 1

    while isComposite(n):
        n += 1
    return n


def isComposite(n):
    for i in range(2, n):
        if n % i == 0:
            return True
    return False
