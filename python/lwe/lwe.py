import numpy as np
import random

# Source:
# https://asecuritysite.com/encryption/lwe2
# TODO check, if this is bullshit and can be easily worked around, because the
# error is always ceil(q/2) or 0. oh, makes sense
# But is the problem only that it is not a random value in that spectrum?
# -> I forgot to add the error

# TODO try to break it
# TODO why does it break with n too big


# length of vectors
n = 55

# Prime
# q = 100000026691  # 100000026691
q = 9737333  # if too big, it immediately breaks

# Error distribution (gaussian)
# sqrt(n) <= sigma << q, where n is size of vector (here 1 i think)
# sigma must be a lot smaller than q, log works for big q
# TODO: check for size of vector
mu, sigma = 0, np.log(q)

# Secret
s_vec = [random.randint(0, q-1) for _ in range(0, n)]

# Encryption
# ------------------------------------------

# In this case, it sums up everthing
# A = initial equations, part of public key
# B = results of equations with errors, part of public key
# Message bit, 0 or 1

# TODO implement with sample

# Encryption, but A is a matrix


def encrypt_vec(A, B, M, sample_size=1, debug=False):

    # TODO check if this is the rigth dimension
    u = [0] * len(A[0])
    v = 0

    if debug:
        print("A: " + str(A))
        print("B: " + str(B))
        print("M :" + str(M))
    # Creating the u and v vector, adding up random rows (equations) of A and
    # of the vector B

    samples = [0] * sample_size  # debug

    for i in range(0, sample_size):
        index = random.randint(0, len(A)-1)

        samples[i] = index

        u = np.add(u, A[index])
        u = [i % q for i in u]
        v += B[index] % q

        # error = np.round(np.random.normal(mu, sigma))
        # TODO add error
    v = v % q

    if debug:
        print("v pre encoding: " + str(v))

    # Encoding the message bit
    error = np.round(np.random.normal(mu, sigma))
    v += np.ceil(M * q/2) + error

    # Keep modulo q
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
def test_vec(s, n=1, runs=1, debug=False, sample_size=1,  max_equ_num=100,
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

        m = random.randint(0, 1)
        (u, v) = encrypt_vec(A, B, m, sample_size=sample_size, debug=debug)

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


for i in range(3, 20):
    print("sample_size: " + str(i))
    test_vec(s_vec, n, runs=100, debug=False, sample_size=i,
             max_equ_num=1000, min_equ_num=100)
