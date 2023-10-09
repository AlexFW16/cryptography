# returns the next bigger prime number
def get_next_prime(prime):
    n = prime + 1

    while is_composite(n):
        n += 1
    return n


# returns true if given integer is a composite
def is_composite(n):
    for i in range(2, n):
        if n % i == 0:
            return True
    return False

# computes a^k (mod) n
def repeated_squaring(a, k, n):
    b = 1
    A = a

    if k == 0:
        return b

    # the binary representation of k (cut of the 'b0' prefix)
    binary = bin(k)[2:]

    if binary[len(binary) - 1] == 1: # check if the lowest bit is 1
        b = a


    for bit in reversed(binary[:len(binary) - 1]): # skip the lowest bit
        A = (A * A) % n

        if bit == "1": # apparently, this iterates over the string representation of the binary
            b = (A * b) % n

    return b

        





