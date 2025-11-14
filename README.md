# IND320 Portfolio — Streamlit App (GitHub version)

This repository contains your IND320 portfolio app deployed from **GitHub** (not GitLab).  
It includes:
- A Streamlit app with **4 pages** (Home, Data Table, Plots, About)
- Caching for CSV loading
- Data table with **row‑wise line charts** (first month as sparkline) using `st.column_config.LineChartColumn`
- Plot page with **column selectbox** and **month selection slider**
- A starter Jupyter notebook under `notebooks/` for the **Part 1** hand‑in
- `requirements.txt` for Streamlit Cloud

## Folder Structure
```
ind320-portfolio-isma-github/
├── app.py
├── pages/
│   ├── 02_Data_Table.py
│   ├── 03_Plots.py
│   └── 04_About.py
├── notebooks/
│   └── IND320_part1.ipynb
├── data/
│   └── open-meteo-subset.csv   # ← Put your Canvas CSV here (not committed; ignored by .gitignore)
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Run
1. Place `open-meteo-subset.csv` into the `data/` folder.
2. Create/activate a Python 3.10+ environment.
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```
   - Home: http://localhost:8501/
   - Data Table: http://localhost:8501/Data_Table
   - Plots: http://localhost:8501/Plots
   - About: http://localhost:8501/About

## Deploy to Streamlit Community Cloud
1. Push this repo to GitHub (public).
2. Go to https://share.streamlit.io
3. **New app** → connect to your GitHub repo, select branch, and set **Main file path** to `app.py`.
4. Click **Deploy**. Your app will be available at `https://<your-repo-name>.streamlit.app/`.




