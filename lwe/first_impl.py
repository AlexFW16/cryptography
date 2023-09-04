import numpy as np
import random

# Source:
# https://asecuritysite.com/encryption/lwe2
# TODO check, if this is bullshit and can be easily worked around, because the
# error is always ceil(q/2) or 0. oh, makes sense
# But is the problem only that it is not a random value in that spectrum?
# -> I forgot to add the error

# TODO Next step: step it up, so s is a vector and A a matrix!
# Message
M = 1

# Secret
s = 5

# Prime
q = 100000026691  # 100000026691

# Error distribution (gaussian)
# sqrt(n) <= sigma << q, where n is size of vector (here 1 i think)
# sigma must be a lot smaller than q, log works for big q
mu, sigma = 0, np.log(q) * 10000

# Encryption
# In this case, it sums up everthing
# A = initial equations, part of public key
# B = results of equations with errors, part of public key
# Message bit, 0 or 1

# TODO implement with sample


def encrypt(A, B, M, sample_size=1, debug=False):

    u = 0
    v = 0
    if debug:
        print("Samples:")

    # adds random samples to u and v
    for i in range(0, sample_size):
        index = random.randint(0, len(A)-1)

        u += A[index]
        v += B[index]
        if debug:
            print(str(i) + ": " + str(index))

    v += np.ceil(M * q / 2)
    u, v = u % q, v % q  # Keep modulo q

    return (u, v)


# Different calucation
def encrypt2(A, B, M):
    u = np.sum(A) % q
    error = np.random.normal(mu, sigma)

    # Also add a error from same distribution
    v = (np.sum(B) + np.ceil(M * 1 / 2) + error) % q
    return (u, v)


# Decryption
# u = new equation
# v = new equation result
# s = secret

def decrypt(u, v, s, debug=False):
    dec = (v - s * u) % q

    # Extra step: if the result is e.g. close to zero and negative, it is
    # close to q, hence we need to q - result and check whether > q/2
    dec = (dec + q/4) % q
    if debug:
        print("new dec: " + str(dec))

    if dec > q/2:
        return 1
    else:
        return 0


def decrypt2(u, v, s):
    dec = v - np.dot(s, u)
    dec = dec % q
    print("dec = " + str(dec))

    if dec >= 1/2:
        return 1
    else:
        return 0


def test(runs=1, debug=False, type=0, sample_size=1, error_dist="gauss"):

    # number of succesfull tries
    positives = 0

    print("starting")
    for i in range(0, runs):

        # initialize A with random values and size
        size = random.randint(10, 100)
        A = [0] * size
        for k in range(0, size):
            number = random.randint(0, q)
            A[k] = number

        # set B according to A

        B = [0] * size
        B = [i * s % q for i in A]
        errors = [0] * size

        # TODO add small errors to B
        # TODO add negative errors
        # Errors drawn from gaussian distribution
        for k in range(0, size):
            if error_dist == "gauss":
                error = np.round(np.random.normal(mu, sigma))
            elif error_dist == "pos":
                error = np.abs(np.round(np.random.normal(mu, sigma)))
            else:
                print("No valid error dist")
                exit(0)

            errors[k] = error
            B[k] = B[k] + error

        if debug:
            print("")
            print("--------------")
            print("A: ")
            print(A)
            print("B: ")
            print(B)
            print("")
            print("Errors:")
            print(errors)
            print("--------------")

        for y in range(0, 2):
            if type == 0:
                (u, v) = encrypt(A, B, y, sample_size, debug=debug)
            elif type == 1:
                (u, v) = encrypt2(A, B, y)
            else:
                print("unkown type")
                exit(0)

            if debug:
                print("u: " + str(u))
                print("v: " + str(v))

            if type == 0:
                decryption = decrypt(u, v, s, debug)
            elif type == 1:
                decryption = decrypt2(u, v, s)
            else:
                print("unkown type")
                exit(0)

            if decryption != y:
                print("pos:" + str(positives))
                exit("ERROR")
            else:
                positives += 1

    print("done, " + str(positives) + " succesfull runs without errors.")


for i in range(3, 10):
    print("sample_size: " + str(i))
    test(runs=100, debug=True, type=0, sample_size=i, error_dist="gauss")
    print()
