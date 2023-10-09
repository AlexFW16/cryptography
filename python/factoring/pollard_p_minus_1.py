import numpy as np
from util import get_next_prime
from util import repeated_squaring

# in: composite integer n, that is not a prime power
# in: Smoothness bound B
# Returns a non-trivial factor of n

def pollard_p_minus_1(n, B):
    a = np.random.randint(2, n)
    d = np.gcd(a, n)

    if d >= 2:
        return d
    
    prime = get_next_prime(2)
    while prime <= B:
        l = np.floor(np.log(n) / np.log(prime))
        a = repeated_squaring(a, repeated_squaring(prime, int(l), n), n)
        # a = (np.power(a, np.power(prime, l))) % n # TODO Replace by algorithm 2.143

        prime = get_next_prime(prime)
    
    d = np.gcd(a-1, n)
    if d == 1 or d == n:
        return -1
    else:
        return d





