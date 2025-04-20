import streamlit as st
from mpmath import mp, zetazero, primepi
import matplotlib.pyplot as plt

# ——————————————————————————————
# ضروري يكون أول سطر
st.set_page_config(page_title="Zone‑Pro Simple", layout="centered")
st.title("Zone‑Pro Simplified")

# ——————————————————————————————
# اختيار الوظيفة
task = st.radio("اختر الوظيفة:", ["Zeta Zero γₙ", "Prime Count π(x)"])

# ——————————————————————————————
if task == "Zeta Zero γₙ":
    # رقم الصفر N من 0-10000، الافتراضي 0 عشان المستخدم يدخل بنفسه
    N = st.number_input("N = رقم الصفر الذي تريد حسابه (0–10000)", min_value=0, max_value=10000, value=0, step=1)
    # خيار الرسم اختياري
    plot_zero = st.checkbox("أرسم منحنى الأصفار حتى N", value=False)

    # إذا المستخدم أدخل N>0 نفّذ الحساب فورًا
    if N > 0:
        # ضبط الدقة بناءً على N
        mp.dps = max(50, int(N * 0.02) + 20)
        # حساب الصفر رقم N
        zero_n = zetazero(N)

        # عرض النتيجة كنص
        st.subheader(f"النتيجة: γₙ حيث n = {N}")
        st.write(str(zero_n))

        # رسم التوزيع إذا فعّل المستخدم
        if plot_zero:
            zeros = [zetazero(i) for i in range(1, N+1)]
            fig, ax = plt.subplots()
            ax.plot(range(1, N+1), [z.imag for z in zeros], marker="o")
            ax.set_xlabel("n")
            ax.set_ylabel("Im(γₙ)")
            ax.set_title(f"الجزء التخيلي للأصفار حتى n = {N}")
            st.pyplot(fig)

        # زر تنزيل CSV للنتيجة
        csv_data = f"n,zero\n{N},{zero_n}"
        st.download_button(
            label="⬇️ تنزيل نتيجة الصفر بصيغة CSV",
            data=csv_data.encode("utf-8"),
            file_name=f"zeta_zero_{N}.csv",
            mime="text/csv"
        )

elif task == "Prime Count π(x)":
    # قيمة X من 0-1,000,000، الافتراضي 0
    X = st.number_input("X = احسب π(X) حتى (0–1000000)", min_value=0, max_value=1000000, value=0, step=1)

    # إذا المستخدم أدخل X>0 نفّذ الحساب فورًا
    if X > 0:
        piX = primepi(X)
        st.subheader(f"النتيجة: π({X}) = {piX}")

        # زر تنزيل CSV للنتيجة
        csv_data = f"x,pi(x)\n{X},{piX}"
        st.download_button(
            label="⬇️ تنزيل نتيجة π(X) بصيغة CSV",
            data=csv_data.encode("utf-8"),
            file_name=f"pi_count_{X}.csv",
            mime="text/csv"
        )
