import streamlit as st

st.set_page_config(
    page_title="IND320 Portfolio — Isma Sohail",
    page_icon="📘",
    layout="wide",
)

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("Navigation")

    st.page_link("app.py", label="🏠 Home", icon="🏡")
    st.page_link("pages/02_Data_Table.py", label="📊 Data Table")
    st.page_link("pages/03_Plots.py", label="📈 Plots")
    st.page_link("pages/04_Production.py", label="⚡ Production")
    st.page_link("pages/05_About.py", label="ℹ️ About")

st.markdown(
    """
    <div style='background: linear-gradient(90deg, #004b8d, #00a8cc); 
                padding: 40px; border-radius: 12px; margin-bottom: 30px;'>
        <h1 style='color: white; text-align: center;'>
            IND320 Portfolio — Isma Sohail
        </h1>
        <h3 style='color: white; text-align: center; margin-top: -10px;'>
            MSc Data Science | Norwegian University of Life Sciences (NMBU)
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# WELCOME
# ----------------------------
st.subheader("🌟 Welcome")
st.write(
    """
This portfolio app presents my work for the **IND320 – Data to Decision** course.
It demonstrates applied data science techniques through reproducible analysis,
visual storytelling, API usage, Spark/Cassandra processing, and clean interface design.
"""
)

# ----------------------------
# PROJECT OVERVIEW (one time only!)
# ----------------------------
st.subheader("🔍 Project Overview")

st.markdown(
    """
- **📊 Data Table:** Explore the dataset interactively with row-wise sparklines.  
- **📈 Plots:** Compare variables over time or by month with dynamic selections.  
- **⚡ Production:** Visualise 2021 electricity production by price area & group  
  using **Elhub API data processed via the notebook**.  
- **💡 About:** Read AI usage, reflection, and learning experiences.
"""
)

# ----------------------------
# REPOSITORY & DEPLOYMENT
# ----------------------------
st.subheader("🌐 Repository & Deployment")
st.markdown(
    """
- **GitHub Repository:**  
  [isma-ds/ind320-portfolio-isma](https://github.com/isma-ds/ind320-portfolio-isma)  
- **Streamlit App:**  
  [ind320-portfolio-isma.streamlit.app](https://ind320-portfolio-isma.streamlit.app)
"""
)

st.markdown(
    """
<br><br>
<div style='text-align: center; font-size: 14px; color: gray;'>
🟢 Live Version — Deployed via Streamlit Cloud  
<br>
© 2025 Isma Sohail | IND320 Data to Decision
</div>
""",
    unsafe_allow_html=True
)
