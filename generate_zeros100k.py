import numpy as np, mpmath as mp
mp.mp.dps = 50
N = 100000
zeros = np.empty(N, float)
for n in range(1, N+1):
    zeros[n-1] = float(mp.zetazero(n).imag)
np.save("data/zeros100k.npy", zeros)
print("zeros100k.npy generated")
