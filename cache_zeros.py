# cache_zeros.py – يولّد أصفار ريمان ويخزنها محلياً كـ NumPy
import numpy as np, os, json
from mpmath import zetazero, mp

COUNT = 1000  # عدّل العدد إذا تبي أكثر أو أقل
CACHE_FILE = "data/zeta_zeros_1000.npy"

def generate_zeta_zeros(count):
    mp.dps = 50  # عدد المنازل العشرية للدقة
    zeros = []
    for i in range(1, count + 1):
        try:
            z = float(zetazero(i).imag)
            zeros.append(z)
        except Exception as e:
            print(f"⚠️ خطأ في الصفر رقم {i}: {e}")
            break
    return np.array(zeros)

def ensure_zeta_cache():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(CACHE_FILE):
        return np.load(CACHE_FILE)
    zeros = generate_zeta_zeros(COUNT)
    np.save(CACHE_FILE, zeros)
    return zeros
