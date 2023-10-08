from pollards_rho import pollard_recursive
from trial_div import trial_division
import time

prime = 346349 * 3465317

start = time.time()
print(pollard_recursive(prime))

end = time.time()
print("pollard: " + str(end - start))


start = time.time()

print(trial_division(prime))
end = time.time()
print("trial div:" + str(end - start))

