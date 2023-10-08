import numpy as np

def pollard(n):
    a, b = 2, 2 # 2 pointers for finding the cycle
    d = 1 # gcd
    i = 1
    running = True

    while running:
        a = f(a) % n # tortoise (floyd algo)
        b = f(f(b)) % n # hare (- || -)

        d = np.gcd(a - b, n)

        if d > 1 and d < n:
            return d
        elif d == n:
            return -1



# f: S \to S, on a finite set S
c = 1 # can be replaced with int > 0 (I think)
def f(x):
    return np.power(x, 2) + c


def pollard_recursive(n):
    factorization = []

    while is_composite(n):
        factor = pollard(n)
        factorization.append(factor)
        n = int(n / factor)

    # No need to check if n == 1, because pollard does not work on prime numbers
    factorization.append(n)
    return factorization
    
def is_composite(n):
    for i in range(2, n):
        if n % i == 0:
            return True
    return False


