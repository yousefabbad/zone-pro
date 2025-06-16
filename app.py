# app.py  —  واجهة Streamlit لتحليل مفاتيح RSA بأصفار زيتا محفوظة

import streamlit as st, numpy as np, math
from Crypto.PublicKey import RSA
from scipy.stats import chisquare
from cache_zeros import ensure_zeta_cache   # ← يستدعي الكاش أو يولّد

# يُحمَّل الملف أو يولَّد مرة واحدة
ZETA_ZEROS = ensure_zeta_cache()     # مصفوفة NumPy بطول 100k

# ░░ واجهة ░░
st.set_page_config(page_title="ZonePro Zeta-RSA", layout="centered")
st.title("🔐 ZonePro – تحليل مفاتيح RSA بأصفار زيتا")

# اختيار إدخال المفتاح
mode = st.radio("اختر إدخال المفتاح:", ("رفع ملف PEM", "توليد داخل الأداة"))
bits = st.selectbox("طول المفتاح عند التوليد:", [512, 1024, 2048, 4096], index=2)

pem_bytes = None
if mode == "رفع ملف PEM":
    up = st.file_uploader("📎 ارفع المفتاح العام", type=["pem"])
    if up: pem_bytes = up.read()
else:
    if st.button("🎲 توليد مفتاح RSA"):
        pem_bytes = RSA.generate(bits).publickey().export_key()

if not pem_bytes:
    st.stop()

# استخراج n و e
try:
    key = RSA.import_key(pem_bytes)
    n = key.n; e = key.e
except Exception as err:
    st.error(f"خطأ في قراءة المفتاح: {err}")
    st.stop()

st.success(f"Bit-length: {n.bit_length()} بت | e = {e}")

# عدد الأصفار المستخدمة
count = st.select_slider("اختر عدد الأصفار للتحليل",
                         options=[100, 1000, 10000, 100000], value=1000)
gamma = ZETA_ZEROS[:count]

# التحليل
ratios = ((n % (gamma * 1e9).astype(np.int64)) / (gamma * 1e9))
sigma   = float(ratios.std())
hist, _ = np.histogram(ratios, bins=20, range=(0.,1.))
chi2, _ = chisquare(hist, np.full_like(hist, hist.sum()/20))
prob    = hist / hist.sum()
entropy = -float(np.sum(prob * np.log2(prob, where=prob>0)))

# العرض
st.markdown(f"""
**σ:** `{sigma:.6f}`  
**χ²:** `{chi2:.2f}`  
**Entropy:** `{entropy:.3f}` / max≈`{math.log2(20):.3f}`
""")
st.bar_chart(hist)

# التقييم
if chi2 > 30 or entropy < 3.5:
    st.error("❌ المفتاح يحتمل أنه ضعيف التوليد")
else:
    st.success("✅ المفتاح يبدو جيّد التوليد")
