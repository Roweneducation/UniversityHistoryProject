import streamlit as st
st.set_page_config(page_title="Legend Test", layout="wide")

st.title("Century Color Legend - Minimal Test")

century_colors = {
    11: "#e0f7fa", 12: "#b2ebf2", 13: "#81d4fa", 14: "#4fc3f7",
    15: "#29b6f6", 16: "#03a9f4", 17: "#039be5", 18: "#0288d1",
    19: "#0277bd", 20: "#01579b", 21: "#003c8f"
}

legend_items = []
for c, color in century_colors.items():
    century_start = (c - 1) * 100 + 1
    century_end = c * 100
    legend_items.append(
    f'<div style="display:flex;align-items:center;margin-right:18px;margin-bottom:6px;">'
    f'<div style="width:18px;height:18px;background:{color};margin-right:7px;border-radius:4px;border:1px solid #ccc"></div>'
    f'<span style="color:white;font-size:1rem;">{c}th century ({century_start}–{century_end})</span>'
    f'</div>'
)

legend_html = f'<div style="display:flex;flex-wrap:wrap;">{" ".join(legend_items)}</div>'
st.markdown(legend_html, unsafe_allow_html=True)
