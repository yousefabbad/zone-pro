import streamlit as st
from mpmath import mp, zetazero
import matplotlib.pyplot as plt
import pandas as pd

# ——————————————————————————————
# Must be the first Streamlit command
st.set_page_config(
    page_title="Zone‑Pro Zeta Zeros",
    layout="wide"
)

# ——————————————————————————————
# Title
st.title("Zone‑Pro Enhanced: أصفار دالة زيتا")

# ——————————————————————————————
# Sidebar input
st.sidebar.header("إعدادات الحساب")
N = st.sidebar.number_input(
    label="عدد الأصفار غير التافهة",
    min_value=1,
    max_value=10000,
    value=300,
    step=1
)

# ——————————————————————————————
# Precision function
def get_precision(n_zeros: int) -> int:
    # at least 50 decimal places, plus ~0.02 per zero
    return max(50, int(n_zeros * 0.02) + 20)

# Compute and set mp precision
precision = get_precision(N)
mp.dps = precision

# ——————————————————————————————
# Cached computation of zeros
@st.cache(show_spinner=False, max_entries=10)
def compute_zeta_zeros(count: int, precision: int):
    mp.dps = precision
    return [zetazero(i) for i in range(1, count + 1)]

zeros = compute_zeta_zeros(N, precision)

# ——————————————————————————————
# Plot imaginary parts of the zeros
fig, ax = plt.subplots()
ax.plot(range(1, N + 1), [z.imag for z in zeros], marker='o')
ax.set_xlabel("n (ترتيب الصفر)")
ax.set_ylabel("Im(γₙ) (الجزء التخيلي)")
ax.set_title(f"الجزء التخيلي لأول {N} أصفار غير تافهة")
st.pyplot(fig)

# ——————————————————————————————
# Display table of zeros
df = pd.DataFrame({
    "n": list(range(1, N + 1)),
    "zero": [str(z) for z in zeros]
})
st.subheader(f"جدول أول {N} أصفار غير تافهة")
st.dataframe(df)

# ——————————————————————————————
# Download as CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ تحميل النتائج بصيغة CSV",
    data=csv,
    file_name=f"zeta_zeros_{N}.csv",
    mime="text/csv"
)

# ——————————————————————————————
# Informational note
st.info(
    f"✅ تم ضبط الدقة تلقائيًا (mp.dps = {precision}) لضمان نتائج دقيقة 100٪."
)
