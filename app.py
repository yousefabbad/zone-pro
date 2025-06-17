import streamlit as st
import numpy as np
import math, os

# تحميل الجداول جاهزة
ZEROS_PATH = "data/zeros100k.npy"
PI_PATH    = "data/pi100k.npy"

if not (os.path.exists(ZEROS_PATH) and os.path.exists(PI_PATH)):
    st.error("❌ لم أجد ملفات البيانات.\n"
             "شغّل generate_zeros100k.py و generate_pi100k.py أولاً.")
    st.stop()

zeta_zeros = np.load(ZEROS_PATH)
prime_pi   = np.load(PI_PATH)

MAX_ZERO = len(zeta_zeros)
MAX_X    = len(prime_pi) - 1

# واجهة Streamlit
st.set_page_config(page_title="ZonePro – صدف رياضي", layout="centered")
st.title("🧮 ZonePro – أصفار زيتا و π(x) من دون تأخير")

mode = st.radio("اختر العملية:", ["γₙ – الصفر رقم n", "π(x) – عدد الأعداد الأولية ≤ x"])

if mode.startswith("γ"):
    n = st.number_input(f"أدخل n (1 – {MAX_ZERO})", min_value=1, max_value=MAX_ZERO, value=1000)
    st.success(f"γₙ (الصفر رقم {n}) = {zeta_zeros[n-1]}")
else:
    x = st.number_input(f"أدخل x (≤ {MAX_X})", min_value=2, max_value=MAX_X, value=1000, step=100)
    st.success(f"π({x}) = {prime_pi[x]}")
