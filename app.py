import streamlit as st
from mpmath import mp, zetazero
from primecount import primepi
import matplotlib.pyplot as plt

# ——————————————————————————————
# ١) تهيئة صفحة Streamlit
st.set_page_config(page_title="Zone‑Pro Enhanced", layout="wide")

# ——————————————————————————————
# ٢) اختيار الصفحة: Calculator أو Dashboard
page = st.sidebar.radio("اختر الصفحة:", ["Calculator", "Dashboard"])

# ——————————————————————————————
# ٣) تهيئة Session State للمقاييس والكاش
if "zeta_count" not in st.session_state:
    st.session_state.zeta_count = 0
if "pi_count" not in st.session_state:
    st.session_state.pi_count = 0
if "zeta_values" not in st.session_state:
    st.session_state.zeta_values = []
if "pi_values" not in st.session_state:
    st.session_state.pi_values = []
if "pi_cache" not in st.session_state:
    st.session_state.pi_cache = {}

# ——————————————————————————————
def get_precision(n: int) -> int:
    # على الأقل 50 خانة، زائد 0.02 لكل صفر
    return max(50, int(n * 0.02) + 20)

# ——————————————————————————————
if page == "Calculator":
    st.title("Zone‑Pro Calculator")

    task = st.radio("اختر الوظيفة:", ["Zeta Zero γₙ", "Prime Count π(x)"])

    if task == "Zeta Zero γₙ":
        # حدّ N حتى 100000
        N = st.number_input(
            "N = رقم الصفر الذي تريد حسابه (1–100000)",
            min_value=1,
            max_value=100000,
            value=1,
            step=1
        )
        plot_zero = st.checkbox("أرسم منحنى الأصفار حتى N", value=False)

        if st.button("احسب"):
            # ضبط الدقة
            mp.dps = get_precision(N)
            zero_n = zetazero(N)

            # تحديث المقاييس
            st.session_state.zeta_count += 1
            st.session_state.zeta_values.append(N)

            # عرض النتيجة
            st.subheader(f"γₙ حيث n = {N}")
            st.write(str(zero_n))

            # الرسم الاختياري مع تقييد النقاط
            if plot_zero:
                max_plot = 2000
                if N > max_plot:
                    st.warning(f"⚠️ N كبير؛ سيتم رسم أول {max_plot} نقطة فقط")
                    plot_range = range(1, max_plot + 1)
                else:
                    plot_range = range(1, N + 1)

                zeros_for_plot = [zetazero(i) for i in plot_range]
                fig, ax = plt.subplots()
                ax.plot(list(plot_range), [z.imag for z in zeros_for_plot], linestyle='-')
                ax.set_xlabel("n")
                ax.set_ylabel("Im(γₙ)")
                ax.set_title(f"الجزء التخيلي للأصفار حتى n = {min(N, max_plot)}")
                st.pyplot(fig)

    else:  # Prime Count π(x)
        # حد X حتى 1e9
        X = st.number_input(
            "X = احسب π(X) حتى (1–1000000000)",
            min_value=1,
            max_value=10**9,
            value=1,
            step=1
        )
        if st.button("احسب"):
            # استخدام كاش لتسريع الحسابات المتكررة
            if X not in st.session_state.pi_cache:
                st.session_state.pi_cache[X] = primepi(X)
            piX = st.session_state.pi_cache[X]

            # تحديث المقاييس
            st.session_state.pi_count += 1
            st.session_state.pi_values.append(X)

            # عرض النتيجة
            st.subheader(f"π({X}) = {piX}")

elif page == "Dashboard":
    st.title("Dashboard إحصائيات الاستخدام")

    # إجمالي العمليات
    st.markdown(f"- **عدد حسابات Zeta Zero**: {st.session_state.zeta_count}")
    st.markdown(f"- **عدد حسابات Prime Count**: {st.session_state.pi_count}")

    # إحصائيات Zeta Zero
    if st.session_state.zeta_count:
        vals = st.session_state.zeta_values
        st.markdown("#### إحصائيات Zeta Zero γₙ")
        st.markdown(f"- أكبر n طلب: {max(vals)}")
        st.markdown(f"- أصغر n طلب: {min(vals)}")
        st.markdown(f"- المتوسط: {sum(vals)/len(vals):.2f}")

    # إحصائيات Prime Count
    if st.session_state.pi_count:
        vals = st.session_state.pi_values
        st.markdown("#### إحصائيات Prime Count π(x)")
        st.markdown(f"- أكبر X طلب: {max(vals)}")
        st.markdown(f"- أصغر X طلب: {min(vals)}")
        st.markdown(f"- المتوسط: {sum(vals)/len(vals):.2f}")

    # رسالة إذا ما في حسابات بعد
    if st.session_state.zeta_count == 0 and st.session_state.pi_count == 0:
        st.info("لم يتم إجراء أي حساب بعد.")
