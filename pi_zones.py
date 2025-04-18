import numpy as np

pi_lookup = np.load("data/pi100k.npy")

def segmented_sieve_count(x: int) -> int:
    import math
    limit = int(math.sqrt(x)) + 1
    sieve = [True] * (limit + 1)
    primes = []
    for num in range(2, limit):
        if sieve[num]:
            primes.append(num)
            for multiple in range(num*num, limit, num):
                sieve[multiple] = False
    low = 100001
    high = min(x, low + 100000)
    count = int(pi_lookup[-1])
    while low <= x:
        mark = [True] * (high - low + 1)
        for p in primes:
            start = ((low + p - 1) // p) * p
            for m in range(start, high+1, p):
                mark[m-low] = False
        for i, is_prime in enumerate(mark):
            if is_prime and (low + i) >= 2:
                count += 1
        low = high + 1
        high = min(x, low + 100000)
    return count

def get_pi(x: int) -> int:
    if 1 <= x < pi_lookup.shape[0]:
        return int(pi_lookup[x])
    elif x >= pi_lookup.shape[0]:
        return segmented_sieve_count(x)
    raise ValueError(f"x={x} خارج النطاق")
