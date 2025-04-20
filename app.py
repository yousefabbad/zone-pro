import streamlit as st
from mpmath import mp, zetazero, primepi
import matplotlib.pyplot as plt

# 1) لازم أول سطر
st.set_page_config(page_title="Zone‑Pro Simple", layout="centered")
st.title("Zone‑Pro Simplified")

# 2) اختار الوظيفة
task = st.radio("اختر الوظيفة:", ["Zeta Zero γₙ", "Prime Count π(x)"])

# 3) حسب الاختيار حط الخانة المناسبة
if task == "Zeta Zero γₙ":
    N = st.number_input("N = عدد أصفار زيتا", min_value=1, max_value=10000, value=300, step=1)
elif task == "Prime Count π(x)":
    X = st.number_input("X = احسب π(X) حتى", min_value=1, max_value=1000000, value=10000, step=1)

# 4) خيار الرسم للأصفار لو اخترتها
do_plot = False
if task == "Zeta Zero γₙ":
    do_plot = st.checkbox("أرسم منحنى الأصفار", value=False)

# 5) زر التشغيل
if st.button("تشغيل"):
    mp.dps = 50  # دقة ثابتة أو تشغّل دالة get_precision لو حاب

    if task == "Zeta Zero γₙ":
        zeros = [zetazero(i) for i in range(1, N+1)]
        st.write("أول", N, "أصفار غير تافهة:")
        st.write(", ".join(str(z) for z in zeros))
        if do_plot:
            fig, ax = plt.subplots()
            ax.plot(list(range(1, N+1)), [z.imag for z in zeros], marker="o")
            ax.set_xlabel("n")
            ax.set_ylabel("Im(γₙ)")
            st.pyplot(fig)
        csv_data = "n,zero\n" + "\n".join(f"{i},{zeros[i-1]}" for i in range(1, N+1))
        st.download_button("⬇️ تنزيل CSV للأصفار", csv_data, file_name=f"zeros_{N}.csv")

    else:  # Prime Count
        piX = primepi(X)
        st.write(f"π({X}) =", piX)
