import streamlit as st
from mpmath import mp, zetazero, primepi
import matplotlib.pyplot as plt

# ——————————————————————————————
# 1) ضبط صفحة Streamlit
st.set_page_config(page_title="Zone‑Pro Enhanced", layout="centered")
st.title("Zone‑Pro Enhanced")

# ——————————————————————————————
# 2) اختيار الوظيفة
task = st.radio("اختر الوظيفة:", ["Zeta Zero γₙ", "Prime Count π(x)"])

# ——————————————————————————————
if task == "Zeta Zero γₙ":
    # مدخل N ما بين 1 و100000
    N = st.number_input(
        "N = رقم الصفر المراد حسابه (1–100000)",
        min_value=1, max_value=100000, value=1, step=1
    )
    plot_zero = st.checkbox("أرسم منحنى الأصفار حتى N", value=False)

    if st.button("احسب"):
        # ضبط دقة الحساب تلقائيًا
        mp.dps = max(50, int(N * 0.02) + 20)
        zero_n = zetazero(N)

        # عرض النتيجة
        st.subheader(f"γₙ حيث n = {N}")
        st.write(str(zero_n))

        # إذا طلب المستخدم الرسم
        if plot_zero:
            max_plot = 2000
            if N > max_plot:
                st.warning(f"⚠️ N كبير؛ سيتم رسم أول {max_plot} نقطة فقط")
                rng = range(1, max_plot + 1)
            else:
                rng = range(1, N + 1)

            zeros = [zetazero(i) for i in rng]
            fig, ax = plt.subplots()
            ax.plot(list(rng), [z.imag for z in zeros], linestyle='-')
            ax.set_xlabel("n")
            ax.set_ylabel("Im(γₙ)")
            ax.set_title(f"الجزء التخيلي للأصفار حتى n = {min(N, max_plot)}")
            st.pyplot(fig)

elif task == "Prime Count π(x)":
    # مدخل X ما بين 1 و10,000,000
    X = st.number_input(
        "X = احسب π(X) حتى (1–10000000)",
        min_value=1, max_value=10_000_000, value=1, step=1
    )
    if st.button("احسب"):
        # حساب عدد الأوليات باستخدام mpmath
        piX = primepi(X)

        # عرض النتيجة
        st.subheader(f"π({X}) = {piX}")
