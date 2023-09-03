import numpy as np

# Source: lwe2cryptione.com/enuritysit://asechttps
# TODO check, if this is bullshit and can be easily worked around, because the
# error is always ceil(q/2) or 0. oh, makes sense
# But is the problem only that it is not a random value in that spectrum?

# TODO Next step: step it up, so s is a vector and A a matrix!
# Message
M = 1

# Secret
s = 5

# Prime
q = 89

# Public Key
A = [14, 34, 55, 32, 95, 69, 56, 24, 11, 20, 4]
B = [i * s % q for i in A]


samples = (0, 1, 3)

# Encryption
# In this case, it sums up everthing
# A = initial equations
# B = results of equations with errors
# Message bit, 0 or 1

# TODO implement with sample


def encrypt(A, B, M):

    u = np.sum(A) % q
    v = (np.sum(B) + np.ceil(M * q / 2)) % q
    return (u, v)

# Decryption
# u = new equation
# v = new equation result
# s = secret


def decrypt(u, v, s):
    dec = v - np.dot(s, u)
    dec = dec % q
    print("dec: " + str(dec))

    if dec >= q/2:
        return 1
    else:
        return 0


(u, v) = encrypt(A, B, M)
print(decrypt(u, v, s))
