"""
يشغَّل مرّة واحدة:
    python generate_pi100k.py
يولّد جدول π(x) من 0 إلى 10,000,000 ويحفظه NumPy.
"""
import os, numpy as np, math

LIMIT = 10_000_000
SAVE_PATH = "data/pi100k.npy"
os.makedirs("data", exist_ok=True)
if os.path.exists(SAVE_PATH):
    print("جدول π(x) موجود بالفعل.")
    quit()

# غربلة بسيطة
sieve = bytearray(b"\x01") * (LIMIT + 1)
sieve[:2] = b"\x00\x00"   # 0 و 1 غير أوليين
for p in range(2, int(math.isqrt(LIMIT)) + 1):
    if sieve[p]:
        sieve[p*p: LIMIT+1: p] = b"\x00" * ((LIMIT - p*p)//p + 1)

# بناء جدول π(x)
pi_table = np.frombuffer(sieve, dtype=np.uint8).cumsum(dtype=np.uint32)
np.save(SAVE_PATH, pi_table)
print("✅ جدول π(x) حُفِظ في", SAVE_PATH)
