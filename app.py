import streamlit as st, numpy as np, math
from Crypto.PublicKey import RSA
from scipy.stats import chisquare
from cache_zeros import ensure_zeta_cache

ZETA = ensure_zeta_cache()
OPTIONS = [100, 1_000, 10_000, 100_000]

st.set_page_config(page_title="ZonePro Zeta-RSA", layout="centered")
st.title("🔐 ZonePro – تحليل مفاتيح RSA بأصفار زيتا")

mode = st.radio("طريقة الإدخال", ("رفع PEM", "توليد"))
bits = st.selectbox("طول عند التوليد", [512, 1024, 2048, 4096], 2)

pem = None
if mode == "رفع PEM":
    up = st.file_uploader("📎 ارفع PEM", ["pem"])
    if up: pem = up.read()
else:
    if st.button("🎲 توليد مفتاح"):
        pem = RSA.generate(bits).publickey().export_key()

if not pem:
    st.stop()

try:
    key = RSA.import_key(pem); n, e = key.n, key.e
except Exception as err:
    st.error("خطأ PEM: " + str(err)); st.stop()

st.success(f"Bit-len: {n.bit_length()} | e: {e}")

count = st.select_slider("أصفار زيتا", options=OPTIONS, value=1_000)
γ = ZETA[:count]; den = γ * 1e9
ratios = np.array([(n % int(d)) / d for d in den])

σ = float(ratios.std())
hist, _ = np.histogram(ratios, bins=20, range=(0.,1.))
χ2, _ = chisquare(hist, np.full_like(hist, hist.sum()/20))
prob = hist / hist.sum()
entropy = -float(np.sum(prob * np.log2(prob, where=prob>0)))
rel = σ / math.log2(n)

st.markdown(f"""
**σ:** `{σ:.6f}`  
**σ/log₂(n):** `{rel:.6f}`  
**χ²:** `{χ2:.2f}`  
**Entropy:** `{entropy:.3f}` / `4.322`
""")
st.bar_chart(hist)

# 🟢 تقييم أكثر صرامة
good = (n.bit_length() >= 2048 and e == 65537 and 8 <= χ2 <= 28
        and entropy >= 4.10 and rel > 0.002)

if good:
    st.success("✅ المفتاح جيّد التوليد رياضياً")
else:
    st.error("❌ المفتاح مشبوه أو ضعيف")
