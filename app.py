# app.py — ZonePro (إصدار خالٍ من OverflowError)
import streamlit as st
import numpy as np
import math
from Crypto.PublicKey import RSA
from scipy.stats import chisquare
from cache_zeros import ensure_zeta_cache  # يحضر الأصفار أو يولّدها

# حمِّل أصفار زيتا (100k) من الكاش
ZETA_ZEROS = ensure_zeta_cache()
ZERO_OPTIONS = [100, 1_000, 10_000, 100_000]

st.set_page_config(page_title="ZonePro – Zeta RSA Analyzer", layout="centered")
st.title("🔐 ZonePro – تحليل مفاتيح RSA باستخدام أصفار زيتا")

# 1) إدخال المفتاح
mode = st.radio("طريقة الإدخال:", ("رفع ملف PEM", "توليد داخل الأداة"))
bits = st.selectbox("طول المفتاح عند التوليد", [512, 1024, 2048, 4096], index=2)

pem_bytes = None
if mode == "رفع ملف PEM":
    uploaded = st.file_uploader("📎 ارفع المفتاح العام (PEM)", type=["pem"])
    if uploaded:
        pem_bytes = uploaded.read()
else:
    if st.button("🎲 توليد مفتاح RSA"):
        pem_bytes = RSA.generate(bits).publickey().export_key()

if not pem_bytes:
    st.stop()

# 2) استخراج n و e
try:
    key = RSA.import_key(pem_bytes)
    n = key.n
    e = key.e
except Exception as err:
    st.error(f"خطأ في قراءة المفتاح: {err}")
    st.stop()

st.success(f"Bit-length: {n.bit_length()} بت | e = {e}")

# 3) اختيار عدد الأصفار
count = st.select_slider("عدد أصفار زيتا المستخدمة", options=ZERO_OPTIONS, value=1_000)
gamma = ZETA_ZEROS[:count]

# 4) التحليل مع معالجة الأعداد الضخمة بدون Overflow
denoms = [g * 1e9 for g in gamma]                          # المقامات
ratios = np.array([(n % int(d)) / d for d in denoms])      # البواقي كنِسب

sigma = float(ratios.std())
hist, _ = np.histogram(ratios, bins=20, range=(0.0, 1.0))
chi2, _ = chisquare(hist, np.full_like(hist, hist.sum() / 20))
prob = hist / hist.sum()
entropy = -float(np.sum(prob * np.log2(prob, where=prob > 0)))

# 5) عرض النتائج
st.subheader("📊 إحصائيات التحليل")
st.write(f"- **σ (std):** `{sigma:.6f}`")
st.write(f"- **χ² (19 dof):** `{chi2:.2f}`")
st.write(f"- **Entropy:** `{entropy:.3f}` / max≈`{math.log2(20):.3f}`")

st.subheader("📈 توزيع البواقي (Histogram)")
st.bar_chart(hist)

# 6) التقييم
if chi2 > 30 or entropy < 3.5:
    st.error("❌ المفتاح يحتمل أنه ضعيف التوليد")
else:
    st.success("✅ المفتاح يبدو جيد التوليد")
