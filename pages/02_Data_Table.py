import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Data Table", page_icon="📊", layout="wide")

# --- Styling ---
st.markdown(
    """
<style>
.section {
    background-color: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.footer {
    text-align: center;
    font-size: 13px;
    color: #777;
    margin-top: 2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Sidebar Navigation ---
st.sidebar.title("📂 Navigation")
st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/02_Data_Table.py", label="📊 Data Table")
st.sidebar.page_link("pages/03_Plots.py", label="📈 Plots")
st.sidebar.page_link("pages/04_About.py", label="ℹ️ About")

st.title("📊 Data Table")
st.markdown("### Interactive Dataset View with Sparklines")


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df["year_month"] = df["time"].dt.to_period("M").astype(str)
    return df


csv_path = Path("data/open-meteo-subset.csv")

if not csv_path.exists():
    st.error(
        "❌ CSV file not found. Please add `open-meteo-subset.csv` to your data folder."
    )
    st.stop()

df = load_data(csv_path)

with st.container():
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📅 Overview of Dataset")
    st.write(f"Total rows: {len(df)} | Total columns: {len(df.columns)}")
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📈 Variable Trends (First Month Sparklines)")

    if "year_month" in df.columns and df["year_month"].notna().any():
        first_month = sorted(df["year_month"].dropna().unique())[0]
        first_month_df = df[df["year_month"] == first_month].copy()
    else:
        first_month_df = df.head(720).copy()

    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    rows = [
        {"Variable": c, "Trend": first_month_df[c].dropna().tolist()}
        for c in numeric_cols
    ]

    table_df = pd.DataFrame(rows)
    st.dataframe(
        table_df,
        column_config={
            "Variable": st.column_config.TextColumn(width="medium"),
            "Trend": st.column_config.LineChartColumn(width="large"),
        },
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='footer'>© 2025 Isma Sohail | IND320 Portfolio</div>",
    unsafe_allow_html=True,
)
