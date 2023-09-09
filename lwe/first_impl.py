import numpy as np
import random

# Source:
# https://asecuritysite.com/encryption/lwe2
# TODO check, if this is bullshit and can be easily worked around, because the
# error is always ceil(q/2) or 0. oh, makes sense
# But is the problem only that it is not a random value in that spectrum?
# -> I forgot to add the error


# TODO: creating of v is not right yet (vectors)

# TODO Next step: step it up, so s is a vector and A a matrix!
# Message
M = 1
# length of vectors
n = 4


# Prime
q = 100000026691  # 100000026691
# q = 97

# Error distribution (gaussian)
# sqrt(n) <= sigma << q, where n is size of vector (here 1 i think)
# sigma must be a lot smaller than q, log works for big q
# TODO: check for size of vector
mu, sigma = 0, np.log(q)

# Secret
s = 5
s_vec = [random.randint(0, q-1) for _ in range(0, n)]

# Encryption
# ------------------------------------------

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

    # encrypt message bit m
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

# Encryption, but A is a matrix


def encrypt_vec(A, B, M, sample_size=1, debug=False):

    # TODO check if this is the rigth dimension
    u = [0] * len(A[0])
    v = 0

    if debug:
        print("A: " + str(A))
        print("B: " + str(B))
    # Creating the u and v vector, adding up random rows (equations) of A and
    # of the vector B

    samples = [0] * sample_size  # debug

    for i in range(0, sample_size):
        index = random.randint(0, len(A)-1)

        if debug:
            samples[i] = index

        u = np.add(u, A[index])
        u = [i % q for i in u]
        v += B[index] % q

        # error = np.round(np.random.normal(mu, sigma))
        # TODO add error
    if debug:
        print("v pre encoding: " + str(v))

    # Encoding the message bit
    v += np.ceil(M * q/2)

    # Keep modulo q
    v = v % q
    u = [i % q for i in u]

    if debug:
        print("sample index: " + str(samples))
        print("u: " + str(u))
        print("v: " + str(v))

    return (u, v)


# Decryption
# -------------------------------

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


def decrypt_vec(u, v, s, debug=False):

    dec = (v - np.dot(s, u)) % q
    dec = (dec + q/4) % q

    if debug:
        print("dec: " + str(dec))
    if dec >= q * 1/2:
        return 1
    else:
        return 0


# Uses guass, and has no 2 types of encryption
def test_vec(s, runs=1, debug=False, sample_size=1,  max_equ_num=100,
             min_equ_num=10):

    # number of succesfull tries
    positives = 0

    print("starting...")
    for _ in range(0, runs):

        # initialize A
        size = random.randint(min_equ_num, max_equ_num)  # number of equations
        A = [[0] * n] * size  # 1st index = rows (k), 2nd index = cols (n)
        if debug:
            print("s: " + str(s))

        A = [[np.random.randint(0, q-1) for _ in range(0, n)]
             for _ in range(0, size)]

       # dimension of B must equal the number of rows of A (K)
        B = [np.dot(a, s) % q for a in A]
        errors = [np.round(np.random.normal(mu, sigma)) for _ in B]

        if debug:
            print("----------------")
            print("B without err: " + str(B))
            print("errors: " + str(errors))
            print("")

        B = np.add(B, errors)

        if debug:
            print("A: " + str(A))
            print("B (after): " + str(B))
            print("errors: " + str(errors))
            print()

        for m in range(0, 2):
            (u, v) = encrypt_vec(A, B, m, sample_size=sample_size, debug=debug)

            if debug:
                print("u: " + str(u))
                print("v: " + str(v))
            decryption = decrypt_vec(u, v, s, debug)

            if debug:
                print("final decryption: " + str(decryption))

            if decryption != m:
                print("ERROR")
                print("positives: " + str(positives))
                exit(0)
            else:
                positives += 1
    print("Success")


def test(runs=1, debug=False, type=0, sample_size=1, error_dist="gauss"):

    # number of succesfull tries
    positives = 0

    print("starting")
    for _ in range(0, runs):

        # initialize A with random values and size (size of A = length of B)
        size = random.randint(10, 100)
        A = [0] * size
        for k in range(0, size):
            number = random.randint(0, q-1)
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


# for i in range(3, 20):
#     print("sample_size: " + str(i))
#     test(runs=100, debug=False, type=0, sample_size=i, error_dist="gauss")
#     print()

for i in range(3, 20):
    print("sample_size: " + str(i))
    test_vec(s_vec, runs=100, debug=False, sample_size=i,
             max_equ_num=10, min_equ_num=3)

# test_vec(s_vec, runs=1, debug=True, sample_size=2,
    # max_equ_num=4, min_equ_num=2)
