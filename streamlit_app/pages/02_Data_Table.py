# streamlit_app/pages/02_Data_Table.py
# ---------------------------------------------------------
# Data Table page – uses LIVE data from the Open-Meteo API
# instead of a local CSV file.
# ---------------------------------------------------------

import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Data Table – Open-Meteo API", page_icon="📊", layout="wide")

st.markdown("## 📊 Data Table")
st.caption(
    "Interactive dataset view using **live hourly weather data** from the "
    "Open-Meteo API for a location near Ås, Norway. "
    "The data are downloaded with Python directly in this app "
    "(no CSV file needed)."
)


# -----------------------------
# 1) Helper: call Open-Meteo API
# -----------------------------
@st.cache_data(ttl=60 * 60)  # cache for 1 hour
def load_open_meteo_data(past_days: int = 7) -> pd.DataFrame:
    """
    Download hourly weather data from the Open-Meteo API.

    We request ERA5 reanalysis / forecast for a point near Ås, Norway.
    Only standard, public, no-auth data are used.
    """
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 59.66,   # approx. Ås / Oslo region
        "longitude": 10.79,
        "hourly": ",".join(
            [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
            ]
        ),
        "past_days": past_days,
        "forecast_days": 0,
        "timezone": "Europe/Oslo",
    }

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])

    if not times:
        raise ValueError("Open-Meteo API returned no hourly data.")

    df = pd.DataFrame({"time": pd.to_datetime(times)})

    for key in ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"]:
        if key in hourly:
            df[key] = hourly[key]

    # Add convenient date / hour columns
    df["date"] = df["time"].dt.date
    df["hour"] = df["time"].dt.hour

    return df


# -----------------------------
# 2) Load data safely
# -----------------------------
with st.spinner("Downloading hourly weather data from Open-Meteo API..."):
    try:
        df = load_open_meteo_data(past_days=7)
    except Exception as e:
        st.error(
            "❌ Could not download data from the Open-Meteo API.\n\n"
            f"Error: `{type(e).__name__}: {e}`"
        )
        st.stop()

st.success(f"✅ Loaded {len(df)} hourly observations from the last 7 days.")


# -----------------------------
# 3) Sidebar filters
# -----------------------------
st.sidebar.markdown("### 🔎 Data Table Filters")

dates_available = sorted(df["date"].unique())
selected_date = st.sidebar.selectbox("Select date", options=dates_available, index=len(dates_available) - 1)

variables_all = [
    ("temperature_2m", "Temperature (°C)"),
    ("relative_humidity_2m", "Relative humidity (%)"),
    ("precipitation", "Precipitation (mm)"),
    ("wind_speed_10m", "Wind speed (m/s)"),
]

default_vars = ["temperature_2m", "precipitation"]

var_labels = {k: label for k, label in variables_all}
var_keys = [k for k, _ in variables_all]

selected_vars = st.sidebar.multiselect(
    "Variables to display / plot",
    options=var_keys,
    default=default_vars,
    format_func=lambda k: var_labels[k],
)

# Filter DataFrame for the selected date
df_day = df[df["date"] == selected_date].copy()

st.markdown(f"### 📅 Data for {selected_date}")

# -----------------------------
# 4) Show table
# -----------------------------
if df_day.empty:
    st.warning("No observations for this date.")
else:
    # Order columns: time, hour, selected variables
    cols = ["time", "hour"] + selected_vars
    st.dataframe(
        df_day[cols].reset_index(drop=True),
        height=400,
        use_container_width=True,
    )

    # -----------------------------
    # 5) Line plot for selected variables
    # -----------------------------
    if selected_vars:
        st.markdown("### 📈 Hourly profile for selected variables")

        plot_df = df_day.set_index("time")[selected_vars]

        st.line_chart(
            plot_df,
            use_container_width=True,
        )
    else:
        st.info("Select at least one variable in the sidebar to see a line plot.")

# -----------------------------
# 6) Documentation expander
# -----------------------------
with st.expander("ℹ️ Data source & processing details"):
    st.markdown(
        """
        **Source**

        * Data are fetched directly from the public **Open-Meteo API**  
          using the `/v1/forecast` endpoint with `past_days=7` and
          the timezone set to `Europe/Oslo`.

        **Variables**

        * `temperature_2m` – air temperature 2 m above ground (°C)  
        * `relative_humidity_2m` – relative humidity (%)  
        * `precipitation` – total precipitation per hour (mm)  
        * `wind_speed_10m` – wind speed 10 m above ground (m/s)

        **Processing steps in this page**

        1. Python sends a HTTP GET request to the Open-Meteo API.  
        2. The JSON response is converted to a Pandas DataFrame.  
        3. Timestamps are parsed to proper `datetime` objects and split into
           `date` and `hour` columns.  
        4. The dataset is displayed as an interactive table, and line plots
           are created based on the variables selected in the sidebar.

        The data are cached in Streamlit for one hour (`@st.cache_data`)
        to avoid unnecessary repeated API calls.
        """
    )
