import numpy as np

zeros = np.load("data/zeros100k.npy")

def get_zeta_zero(n: int) -> float:
    if 1 <= n <= zeros.shape[0]:
        return float(zeros[n-1])
    raise ValueError(f"n={n} خارج النطاق [1–{zeros.shape[0]}]")
