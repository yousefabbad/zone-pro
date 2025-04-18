import streamlit as st
from zeros_zones import get_zeta_zero
from pi_zones import get_pi

st.set_page_config(page_title="Zone Pro Edition", layout="centered")
st.title("Zone Modeling – Pro Edition")

mode = st.radio("اختر وظيفة", ["Zeta Zero γₙ", "Prime Count π(x)"])

if mode == "Zeta Zero γₙ":
    n = st.number_input("أدخل n بين 1 و 100000", min_value=1, max_value=100000, step=1)
    if st.button("احسب γₙ"):
        try:
            z = get_zeta_zero(int(n))
            st.success(f"γₙ ≈ {z:.12f}")
        except Exception as e:
            st.error(f"خطأ: {e}")

else:
    x = st.number_input("أدخل x (حتى 100k عبر Lookup، أكبر يحسب)", min_value=1, step=1)
    if st.button("احسب π(x)"):
        try:
            p = get_pi(int(x))
            st.success(f"π({x}) = {p}")
        except Exception as e:
            st.error(f"خطأ: {e}")
