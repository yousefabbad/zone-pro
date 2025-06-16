# cache_zeros.py
import os, json, numpy as np
from mpmath import mp, zetazero

DATA_DIR  = "data"
NPY_PATH  = os.path.join(DATA_DIR, "zeta_zeros_100k.npy")
JSON_PATH = os.path.join(DATA_DIR, "zeta_zeros_100k.json")
COUNT     = 100_000         # أول مئة ألف صفر

def ensure_zeta_cache():
    """يرجع مصفوفة الأصفار، ويولّدها إذا مفقودة."""
    if os.path.exists(NPY_PATH):
        return np.load(NPY_PATH)

    mp.dps = 50
    print("🔄 جاري حساب الأصفار … قد ياخذ دقائق")
    zeros = np.array([float(zetazero(i).imag) for i in range(1, COUNT + 1)],
                     dtype=np.float64)

    os.makedirs(DATA_DIR, exist_ok=True)
    np.save(NPY_PATH, zeros)
    with open(JSON_PATH, "w") as f:
        json.dump(zeros.tolist(), f)
    print("✅ انتهى الحساب وحفظ الملف")

    return zeros
