import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.sidebar.title("Navigation")
st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/02_Data_Table.py", label="📊 Data Table")
st.sidebar.page_link("pages/03_Plots.py", label="📈 Plots")
st.sidebar.page_link("pages/04_About.py", label="ℹ️ About")

st.title("About This Project")

st.markdown("""
**Course:** IND320 — Data to Decision  
**Student:** Isma Sohail

### AI Usage
An AI assistant helped scaffold the folder structure, write initial Streamlit and Pandas code,
and ensure proper formatting and reproducibility. I reviewed, customized, and tested each section
to align with IND320 requirements. The AI tool accelerated setup and debugging, but all interpretation
and learning outcomes are my own.

### Reflection (≈400 words)
- Describe what you learned about reproducible coding, Streamlit, and Pandas.
- Explain how caching and normalized plotting improved performance and clarity.
- Note how notebooks (exploration) and Streamlit (presentation) complement each other.
- Mention Git workflows (branching, commits, pushing, deploying).

Add your reflection here.
""")
