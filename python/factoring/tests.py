from pollards_rho import pollard_recursive
from trial_div import trial_division
from pollard_p_minus_1 import pollard_p_minus_1
from util import repeated_squaring
import time

prime = 346349 * 3465317

def test_1():
    start = time.time()
    print(pollard_recursive(prime))

    end = time.time()
    print("pollard: " + str(end - start))


    start = time.time()

    print(trial_division(prime))
    end = time.time()
    print("trial div:" + str(end - start))

def test_2():
    input = 19048567
    out = pollard_p_minus_1(input, 19)
    print(out)
    print(str(input / out))


test_2()



