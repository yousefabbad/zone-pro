import numpy as np
N = 100000
s = np.ones(N+1, bool)
s[:2] = False
for p in range(2, int(N**0.5)+1):
    if s[p]:
        s[p*p::p] = False
pi = np.cumsum(s.astype(int))
np.save("data/pi100k.npy", pi)
print("pi100k.npy generated")
