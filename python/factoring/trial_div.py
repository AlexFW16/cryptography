import numpy as np
from util import is_composite, get_next_prime


# naive implementation, divides by ascending prime numbers and
# tests for primality each time.
def trial_division(n):
    prime = 2  # primes by which n is divided
    # is_composite = True  # primality check of the newly obtained number
    factorization = []  # the wanted factorization

    while is_composite(n):

        if n % prime == 0:
            factorization.append(prime)
            n = int(n / prime)

        else:
            prime = get_next_prime(prime)

    if n != 1:  # otherwise, n was prime and 1 would be appended
        factorization.append(n)

    return factorization

