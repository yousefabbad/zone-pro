import streamlit as st
from mpmath import mp, zetazero, primepi
import matplotlib.pyplot as plt

# ——————————————————————————————
MAX_PI_INTERACTIVE = 10_000_000  # أقصى قيمة تفاعلية مقترحة

st.set_page_config(page_title="Zone‑Pro Enhanced", layout="centered")
st.title("Zone‑Pro Enhanced")

task = st.radio("اختر الوظيفة:", ["Zeta Zero γₙ", "Prime Count π(x)"])

if task == "Zeta Zero γₙ":
    N = st.number_input("N = رقم الصفر (1–100000)", 1, 100_000, 1, 1)
    plot_zero = st.checkbox("أرسم منحنى حتى N", False)
    if st.button("احسب"):
        mp.dps = max(50, int(N * 0.02) + 20)
        zero_n = zetazero(N)
        st.subheader(f"γₙ حيث n = {N}")
        st.write(str(zero_n))
        if plot_zero:
            rng = range(1, min(N,2000)+1)
            if N>2000: st.warning("رسم أول 2000 نقطة لتفادي البطء")
            zeros = [zetazero(i) for i in rng]
            fig,ax = plt.subplots(); ax.plot(rng,[z.imag for z in zeros],"-")
            st.pyplot(fig)

else:  # Prime Count π(x)
    X = st.number_input(f"X = احسب π(X) حتى (1–{MAX_PI_INTERACTIVE:,})", 
                        1, 1_000_000_000, 1, 1)
    if st.button("احسب"):
        if X > MAX_PI_INTERACTIVE:
            st.error(f"⚠️ الحد التفاعلي هنا هو {MAX_PI_INTERACTIVE:,}. لقيم أكبر، يمكن تستخدم جهاز أقوى أو خدمة مخصصة.")
        else:
            with st.spinner("⏳ جاري حساب π(x)…"):
                # تخزين مؤقت للنتائج
                if "pi_cache" not in st.session_state:
                    st.session_state.pi_cache = {}
                if X not in st.session_state.pi_cache:
                    st.session_state.pi_cache[X] = primepi(X)
                piX = st.session_state.pi_cache[X]
            st.subheader(f"π({X}) = {piX}")
