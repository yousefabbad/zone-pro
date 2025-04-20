import streamlit as st
from mpmath import mp, zetazero, primepi
import matplotlib.pyplot as plt

# ——————————————————————————————
# أول ما يبدأ السكربت لازم يكون set_page_config
st.set_page_config(page_title="Zone‑Pro Simple", layout="centered")

# ——————————————————————————————
st.title("Zone‑Pro Simplified")

# ——————————————————————————————
# اختيار الوظيفة
task = st.radio("اختر الوظيفة:", ["Zeta Zero γₙ", "Prime Count π(x)"])

# ——————————————————————————————
# مدخلات المستخدم
if task == "Zeta Zero γₙ":
    N = st.number_input("N = عدد أصفار زيتا (0–10000)", min_value=0, max_value=10000, value=0, step=1)
    do_plot = st.checkbox("أرسم منحنى الأصفار", value=False)
elif task == "Prime Count π(x)":
    X = st.number_input("X = احسب π(X) حتى (0–1000000)", min_value=0, max_value=1000000, value=0, step=1)

# ——————————————————————————————
# حساب النتائج وعرضها فورًا
if task == "Zeta Zero γₙ" and N > 0:
    # ضبط الدقة بناءً على N
    precision = max(50, int(N * 0.02) + 20)
    mp.dps = precision

    @st.cache_data(show_spinner=False)
    def compute_zeros(count, prec):
        mp.dps = prec
        return [zetazero(i) for i in range(1, count + 1)]

    zeros = compute_zeros(N, precision)
    # عرض الأصفار كنص
    st.subheader(f"أول {N} صفر غير تافهة")
    st.write(", ".join(str(z) for z in zeros))

    # الرسم اختياري
    if do_plot:
        fig, ax = plt.subplots()
        ax.plot(range(1, N+1), [z.imag for z in zeros], marker="o")
        ax.set_xlabel("n")
        ax.set_ylabel("Im(γₙ)")
        ax.set_title("الجزء التخيلي للأصفار")
        st.pyplot(fig)

    # زر تحميل CSV
    csv_data = "n,zero\n" + "\n".join(f"{i},{zeros[i-1]}" for i in range(1, N+1))
    st.download_button(
        label="⬇️ تنزيل الأصفار بصيغة CSV",
        data=csv_data.encode("utf-8"),
        file_name=f"zeta_zeros_{N}.csv",
        mime="text/csv"
    )

elif task == "Prime Count π(x)" and X > 0:
    @st.cache_data(show_spinner=False)
    def compute_pi(x):
        return primepi(x)

    piX = compute_pi(X)
    st.subheader(f"π({X}) = {piX}")
