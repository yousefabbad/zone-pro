import streamlit as st
from mpmath import mp, zetazero
import primesieve
import matplotlib.pyplot as plt

# ——————————————————————————————
# Page config
st.set_page_config(page_title="Zone‑Pro Enhanced", layout="centered")
st.title("Zone‑Pro Enhanced")

# ——————————————————————————————
# اختيار الوظيفة
task = st.radio("اختر الوظيفة:", ["Zeta Zero γₙ", "Prime Count π(x)"])

# ——————————————————————————————
if task == "Zeta Zero γₙ":
    N = st.number_input(
        "N = رقم الصفر المراد حسابه (1–100000)",
        min_value=1, max_value=100000, value=1, step=1
    )
    plot_zero = st.checkbox("أرسم منحنى الأصفار حتى N", value=False)

    if st.button("احسب"):
        # دقة mpmath حسب N
        mp.dps = max(50, int(N*0.02)+20)
        zero_n = zetazero(N)

        st.subheader(f"γₙ حيث n = {N}")
        st.write(str(zero_n))

        if plot_zero:
            max_plot = 2000
            if N > max_plot:
                st.warning(f"⚠️ N كبير؛ سيتم رسم أول {max_plot} نقطة فقط")
                plot_range = range(1, max_plot+1)
            else:
                plot_range = range(1, N+1)

            zeros = [zetazero(i) for i in plot_range]
            fig, ax = plt.subplots()
            ax.plot(list(plot_range), [z.imag for z in zeros], linestyle='-')
            ax.set_xlabel("n")
            ax.set_ylabel("Im(γₙ)")
            ax.set_title(f"الجزء التخيلي للأصفار حتى n = {min(N, max_plot)}")
            st.pyplot(fig)

elif task == "Prime Count π(x)":
    X = st.number_input(
        "X = احسب π(X) حتى (1–1000000000)",
        min_value=1, max_value=10**9, value=1, step=1
    )
    if st.button("احسب"):
        # primesieve.count_primes(start, stop) يعطي عدد الأوليات in [start, stop)
        piX = primesieve.count_primes(1, X+1)

        st.subheader(f"π({X}) = {piX}")
