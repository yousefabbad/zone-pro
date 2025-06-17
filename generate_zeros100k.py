"""
تشغيل هذا الملف مرّة واحدة فقط:
    python generate_zeros100k.py
سيولّد data/zeros100k.npy في حوالي 3-5 دقائق (حسب الجهاز).
"""
import os, numpy as np
from mpmath import zetazero, mp

COUNT = 100_000
SAVE_PATH = "data/zeros100k.npy"

os.makedirs("data", exist_ok=True)
if os.path.exists(SAVE_PATH):
    print("ملف الأصفار موجود بالفعل – لا حاجة لإعادة الحساب.")
    quit()

mp.dps = 50
print(f"🔄 حساب أول {COUNT:,} صفر غير تافه بدقة 50…")
zeros = np.array([float(zetazero(i).imag) for i in range(1, COUNT + 1)],
                 dtype=np.float64)
np.save(SAVE_PATH, zeros)
print("✅ تم الحفظ في", SAVE_PATH)
