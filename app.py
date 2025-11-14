import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="IND320 Portfolio — Isma Sohail",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #ffffff;
    font-family: "Inter", sans-serif;
    color: #1a1a1a;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #004b87, #007b83);
    color: white;
}
[data-testid="stSidebar"] a {
    color: #e8f9ff !important;
    font-weight: 500;
}
[data-testid="stSidebarNavLink"] > div:hover {
    background-color: rgba(255,255,255,0.15) !important;
    border-radius: 8px;
}
.banner {
    background: linear-gradient(90deg, #004b87, #00a8a8);
    color: white;
    padding: 30px 40px;
    border-radius: 15px;
    margin-bottom: 25px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.section {
    background-color: rgba(255,255,255,0.85);
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    backdrop-filter: blur(8px);
}
h1, h2, h3 {
    color: #004b87;
    font-weight: 600;
}
.footer {
    text-align: center;
    font-size: 13px;
    color: #666;
    margin-top: 2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar intro text
st.sidebar.title("📂 Navigation")
st.sidebar.info("Use the sidebar to switch between pages.")

# Gradient Header
st.markdown(
    """
<div class="banner">
    <h1 style='margin-bottom:0;'>IND320 Portfolio — Isma Sohail</h1>
    <h4 style='margin-top:5px;'>MSc Data Science | Norwegian University of Life Sciences (NMBU)</h4>
</div>
""",
    unsafe_allow_html=True,
)

# Main Sections
st.markdown(
    """
<div class="section">
<h3>🌟 Welcome</h3>
<p>This portfolio app presents my work for the <b>IND320 – Data to Decision</b> course.
It demonstrates applied data science techniques through reproducible analysis, visual storytelling, and clean interface design.</p>
</div>

<div class="section">
<h3>🔍 Project Overview</h3>
<ul>
<li><b>📊 Data Table:</b> Explore the dataset interactively with row-wise sparklines.</li>
<li><b>📈 Plots:</b> Compare variables over time or by month with dynamic selections.</li>
<li><b>💡 About:</b> Read AI usage, reflection, and learning experiences.</li>
</ul>
</div>

<div class="section">
<h3>🌐 Repository & Deployment</h3>
<ul>
<li>GitHub Repository: <a href="https://github.com/isma-ds/ind320-portfolio-isma" target="_blank">isma-ds/ind320-portfolio-isma</a></li>
<li>Streamlit App: <a href="https://ind320-portfolio-isma.streamlit.app/" target="_blank">ind320-portfolio-isma.streamlit.app</a></li>
</ul>
</div>
""",
    unsafe_allow_html=True,
)

# CSV File Check
data_path = Path("data/open-meteo-subset.csv")
if data_path.exists():
    st.success(f"✅ CSV file detected successfully at: `{data_path}`")
else:
    st.warning(
        "⚠️ Please place `open-meteo-subset.csv` in the `data/` folder before running the app."
    )

# Footer
st.markdown(
    "<div class='footer'>✅ Live Version — Deployed via Streamlit Cloud | © 2025 Isma Sohail | IND320 Data to Decision</div>",
    unsafe_allow_html=True,
)
