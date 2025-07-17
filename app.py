import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="University Foundings Over Time",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="Slide10-removebg-preview.png",
)

# --- CUSTOM BRANDING CSS (optional, keep as you wish) ---
st.markdown("""
    <style>
    @media (max-width: 800px) {
        section[data-testid="stSidebar"] {
            display: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
<style>
/* Make sidebar wider */
section[data-testid="stSidebar"] {
    min-width: 380px !important;
    max-width: 480px !important;
    width: 380px !important;
}
@media (min-width: 1400px) {
    section[data-testid="stSidebar"] {
        min-width: 440px !important;
        max-width: 520px !important;
        width: 440px !important;
    }
}
section[data-testid="stSidebar"] > div:first-child {
    padding-right: 18px !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
section[data-testid="stSidebar"] > div:first-child {
    padding-right: 32px !important;
}
div[data-baseweb="slider"] {
    margin-right: 16px !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: #f8f9fa !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .st-cf,
section[data-testid="stSidebar"] .st-bb {
    color: #15325b !important;
    font-weight: bold;
}
.css-1n76uvr, .css-1fv8s86, .css-1r7ky0e, .css-x78sv8, .css-1e3tf61 {
    background-color: #eab32a !important;
    border: 2px solid #15325b !important;
    color: #15325b !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
}
.css-1n76uvr .css-12a93b, .css-1fv8s86 .css-12a93b, .css-1r7ky0e .css-12a93b, .css-x78sv8 .css-12a93b, .css-1e3tf61 .css-12a93b {
    color: #15325b !important;
}
div[data-baseweb="select"] .css-1wy0on6 {
    color: #eab32a !important;
}
div[data-baseweb="select"] .css-1pahdxg-control {
    border-color: #eab32a !important;
}
div[data-baseweb="slider"] .css-14g5y82 .css-1uixxvy,
div[data-baseweb="slider"] .css-1n4twyz,
div[data-baseweb="slider"] .css-1eoe787,
div[data-baseweb="slider"] .css-1a90xhh,
div[data-baseweb="slider"] .css-1g6gooi {
    background: #eab32a !important;
    border-color: #eab32a !important;
}
div[data-baseweb="slider"] .css-1ljl6o7 {
    color: #eab32a !important;
}
span[data-testid="stSliderValue"] {
    color: #eab32a !important;
    font-weight: bold;
}
.st-expander {
    border: 2px solid #eab32a !important;
    border-radius: 8px !important;
}
.st-expanderHeader {
    background: #f8f9fa !important;
    color: #15325b !important;
    font-weight: bold;
}
.century-legend-box {
    border: 2px solid #eab32a !important;
}
.century-legend-label {
    color: #15325b !important;
    font-weight: 600;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("universities_cleaned.csv")
    df = df[df['year'] >= 1000]
    df['year'] = df['year'].astype(int)
    df['century'] = ((df['year'] - 1) // 100 + 1)
    century_colors = {
        11: "#e0f7fa", 12: "#b2ebf2", 13: "#81d4fa", 14: "#4fc3f7",
        15: "#29b6f6", 16: "#03a9f4", 17: "#039be5", 18: "#0288d1",
        19: "#0277bd", 20: "#01579b", 21: "#003c8f"
    }
    df["color"] = df["century"].map(century_colors).fillna("#888888")
    return df

df = load_data()

# Get year and country range for both modes
year_min = int(df["year"].min())
year_max = int(df["year"].max())
countries = sorted(df["country"].dropna().unique())

# ---- Mobile/desktop toggle ----
is_mobile = st.checkbox("Mobile mode (hide sidebar and show filters here)", value=False)

if is_mobile:
    st.image("Slide9-removebg-preview.png", use_container_width=True)
    st.title("Filters")
    year_range = st.slider(
        "Founding Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        step=1
    )
    selected_countries = st.multiselect(
        "Country",
        countries,
        default=countries
    )
else:
    st.sidebar.image("Slide9-removebg-preview.png", use_container_width=True)
    st.sidebar.title("Filters")
    year_range = st.sidebar.slider(
        "Founding Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        step=1
    )
    selected_countries = st.sidebar.multiselect(
        "Country",
        countries,
        default=countries
    )

# Filter DataFrame
df_filtered = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["country"].isin(selected_countries))
]

# --- Build Plotly Figure ---
fig = go.Figure()

fig.add_trace(go.Scattergeo(
    lon=df_filtered['longitude'],
    lat=df_filtered['latitude'],
    text=df_filtered['university'] + " (" + df_filtered['year'].astype(str) + ")",
    mode='markers',
    marker=dict(size=6, color=df_filtered['color']),
    hoverinfo='text'
))

fig.update_layout(
    geo=dict(
        projection_type="natural earth",
        showland=True,
        landcolor="black",
        bgcolor="black",
        showocean=True,
        oceancolor="black",
        showcountries=True,
        countrycolor="gray",
        countrywidth=0.8
    ),
    paper_bgcolor="black",
    plot_bgcolor="black",
    font=dict(color="white"),
    title=f"Universities Founded {year_range[0]} - {year_range[1]}",
    title_font_color="white",
    margin={"r":0,"t":30,"l":0,"b":0}
)

# --- Display in Streamlit ---
st.title("University Foundings Over Time")
with st.expander("ℹ️ About This App (click to expand)"):
    st.markdown("""
This interactive map visualizes the founding of universities across the world from the year 1000 onward.  
- **Each blue dot** represents a university, colored by the century in which it was founded (see the legend below the map).
- **Filters on the left** allow you to narrow the display by country and by founding year range.
- **Hover over a dot** to see the university’s name and founding year.
- **Expand the table** below the map to see a list of all universities currently shown.

**Where does the data come from?**  
The data were collected by web scraping public university directories and Wikipedia lists of oldest universities in continuous operation.  
Every effort has been made to ensure accuracy, but some founding years or locations may be imprecise or disputed due to historical changes, renamings, or differing definitions of what constitutes a “university.”  
If you notice errors or missing universities, please let us know!

**Project goals:**  
- Make the global history of higher education visually explorable.
- Encourage transparency by showing sources and limitations.

**Disclosure:** 
Disclaimer:
The data presented here is by no means complete or fully accurate. 
Not all universities are included, and some information may be missing or imprecise. 
Please do not take these listings as exhaustive or fully authoritative—they are intended for exploration and general reference only.

_Data sources include Wikipedia, university official pages, and aggregated directories. The data are for educational and visualization purposes only._
""")

st.plotly_chart(fig, use_container_width=True)
st.markdown(f"Universities displayed: **{len(df_filtered)}**")

# --- Century Color Legend ---
st.markdown("### Century Color Legend")
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
        f'<div class="century-legend-box" style="width:18px;height:18px;background:{color};margin-right:7px;border-radius:4px;border:2px solid #eab32a"></div>'
        f'<span class="century-legend-label">{c}th century ({century_start}–{century_end})</span>'
        f'</div>'
    )
legend_html = f'<div style="display:flex;flex-wrap:wrap;">{" ".join(legend_items)}</div>'
st.markdown(legend_html, unsafe_allow_html=True)

# --- Optionally show Data Table ---
with st.expander("Show data table"):
    st.dataframe(df_filtered)
