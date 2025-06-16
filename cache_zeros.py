# cache_zeros.py – حساب أصفار ريمان بدقة عالية وتخزينها

import os, numpy as np
from mpmath import zetazeros, mp

CACHE_PATH = "data/zeta_zeros_100k.npy"
COUNT = 100_000

def ensure_zeta_cache():
    if os.path.exists(CACHE_PATH):
        return np.load(CACHE_PATH)

    # دقة عالية
    mp.dps = 50
    print("🔄 جاري حساب الأصفار … قد يستغرق دقائق")

    # نحسب أول 100,000 صفر (الجزء التخيلي فقط)
    zeros = np.array([float(z.imag) for z in zetazeros(COUNT)])

    os.makedirs("data", exist_ok=True)
    np.save(CACHE_PATH, zeros)
    print("✅ تم حفظ الملف:", CACHE_PATH)
    return zeros
