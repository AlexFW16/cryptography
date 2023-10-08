### How to factor efficiently

1. Apply trial division by small primes $< b_1$
2. Apply Pollard's rho algorithm for small primes $< b_2 > b_1$
3. Apply ellitpic curve factoring algorithm for primes $< b_3 > b_2$
4. Apply one of the more powerful general-purpose algorithms (quadratic sieve or general number field sieve)