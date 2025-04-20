import streamlit as st
from mpmath import mp, zetazero, primepi
import matplotlib.pyplot as plt

# ——————————————————————————————
# أول أمر لازم يكون set_page_config
st.set_page_config(page_title="Zone‑Pro Simple", layout="centered")

# ——————————————————————————————
st.title("Zone‑Pro Simplified")

# ——————————————————————————————
st.write("**إعدادات الحساب:**")
cols = st.columns([1,1,1])
with cols[0]:
    N = st.number_input("N = عدد أصفار زيتا", min_value=1, max_value=10000, value=300, step=1)
with cols[1]:
    X = st.number_input("X = احسب π(X) حتى", min_value=1, max_value=1000000, value=10000, step=1)
with cols[2]:
    do_plot = st.checkbox("أرسم منحنى الأصفار", value=False)

# ——————————————————————————————
if st.button("تشغيل"):
    # ضبط الدقة
    mp.dps = max(50, int(N * 0.02) + 20)

    # حساب الأصفار
    zeros = [zetazero(i) for i in range(1, N+1)]
    zeros_str = ", ".join(str(z) for z in zeros)
    st.subheader(f"أول {N} صفر غير تافهة (نص فقط)")
    st.write(zeros_str)

    # حساب π(X)
    piX = primepi(X)
    st.subheader(f"π({X}) = {piX}")

    # زر تنزيل CSV
    csv_data = "n,zero\n" + "\n".join(f"{i},{zeros[i-1]}" for i in range(1, N+1))
    st.download_button(
        label="⬇️ تحميل الأصفار بصيغة CSV",
        data=csv_data.encode("utf-8"),
        file_name=f"zeta_zeros_{N}.csv",
        mime="text/csv"
    )

    # الرسم إذا اختار المستخدم
    if do_plot:
        fig, ax = plt.subplots()
        ax.plot(list(range(1, N+1)), [z.imag for z in zeros], marker="o")
        ax.set_xlabel("n")
        ax.set_ylabel("Im(γₙ)")
        ax.set_title("الجزء التخيلي للأصفار")
        st.pyplot(fig)
