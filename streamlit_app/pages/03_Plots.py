# streamlit_app/pages/03_Plots.py
# ---------------------------------------------------------
# Plots page – visualises LIVE weather data from
# the Open-Meteo API (no local CSV needed).
# ---------------------------------------------------------

import streamlit as st
import pandas as pd
import requests
import altair as alt


st.markdown("## 📉 Plots")
st.caption(
    "Visualising **hourly weather data** downloaded on-the-fly from the "
    "public Open-Meteo API for a location near Ås, Norway."
)


# -----------------------------
# 1) Helper: call Open-Meteo API
# -----------------------------
@st.cache_data(ttl=60 * 60)
def load_open_meteo_data(past_days: int = 7) -> pd.DataFrame:
    """
    Download hourly weather data from the Open-Meteo API
    for the last `past_days` days near Ås / Oslo.
    """
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 59.66,
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

    df["date"] = df["time"].dt.date
    df["hour"] = df["time"].dt.hour

    return df


# -----------------------------
# 2) Sidebar controls
# -----------------------------
st.sidebar.markdown("### 📉 Plot controls (Open-Meteo)")

days = st.sidebar.slider("History (days back)", min_value=3, max_value=30, value=7, step=1)

agg_mode = st.sidebar.radio(
    "Time resolution",
    options=["Hourly", "Daily"],
    index=0,
    help="Daily aggregates use mean for temperature, humidity and wind, and sum for precipitation.",
)

variables_all = [
    ("temperature_2m", "Temperature (°C)"),
    ("relative_humidity_2m", "Relative humidity (%)"),
    ("precipitation", "Precipitation (mm)"),
    ("wind_speed_10m", "Wind speed (m/s)"),
]
var_labels = {k: v for k, v in variables_all}
var_keys = [k for k, _ in variables_all]

selected_vars = st.sidebar.multiselect(
    "Variables to plot",
    options=var_keys,
    default=["temperature_2m", "precipitation"],
    format_func=lambda k: var_labels[k],
)

if not selected_vars:
    st.warning("Select at least one variable in the sidebar to see a plot.")
    st.stop()


# -----------------------------
# 3) Load data
# -----------------------------
with st.spinner(f"Downloading last {days} days from the Open-Meteo API..."):
    try:
        df = load_open_meteo_data(past_days=days)
    except Exception as e:
        st.error(
            "❌ Could not download data from the Open-Meteo API.\n\n"
            f"Error: `{type(e).__name__}: {e}`"
        )
        st.stop()

st.success(f"✅ Loaded {len(df)} hourly observations from the last {days} days.")


# -----------------------------
# 4) Prepare data for plotting
# -----------------------------
if agg_mode == "Daily":
    st.markdown("### 📆 Daily aggregates")

    agg_dict = {
        "temperature_2m": "mean",
        "relative_humidity_2m": "mean",
        "wind_speed_10m": "mean",
        "precipitation": "sum",
    }

    df_daily = df.groupby("date").agg(agg_dict).reset_index()
    df_plot = df_daily[["date"] + selected_vars].copy()
    time_col = "date"
else:
    st.markdown("### ⏱ Hourly profile")
    df_plot = df[["time"] + selected_vars].copy()
    time_col = "time"

# Long format for Altair
long_df = df_plot.melt(
    id_vars=[time_col],
    value_vars=selected_vars,
    var_name="variable",
    value_name="value",
)

long_df["variable_label"] = long_df["variable"].map(var_labels)


# -----------------------------
# 5) Build Altair line chart
# -----------------------------
x_title = "Date" if time_col == "date" else "Time"

chart = (
    alt.Chart(long_df)
    .mark_line()
    .encode(
        x=alt.X(f"{time_col}:T", title=x_title),
        y=alt.Y("value:Q", title="Value"),
        color=alt.Color("variable_label:N", title="Variable"),
        tooltip=[
            alt.Tooltip(f"{time_col}:T", title=x_title),
            alt.Tooltip("variable_label:N", title="Variable"),
            alt.Tooltip("value:Q", title="Value", format=".2f"),
        ],
    )
    .properties(height=400)
    .interactive()
)

st.altair_chart(chart, use_container_width=True)


# -----------------------------
# 6) Quick stats
# -----------------------------
with st.expander("📌 Summary statistics for selected variables"):
    stats = (
        df_plot[selected_vars]
        .describe()
        .T.rename(columns={"50%": "median"})
        [["mean", "median", "min", "max"]]
    )
    stats.index = [var_labels[i] for i in stats.index]
    st.dataframe(stats.style.format("{:.2f}"), use_container_width=True)


# -----------------------------
# 7) Documentation
# -----------------------------
with st.expander("ℹ️ Details about this page"):
    st.markdown(
        """
        **What this page shows**

        * Line plots of **temperature, humidity, precipitation and wind speed**  
          from the Open-Meteo API for a point near Ås / Oslo.
        * You can:
          - Choose the **time window** (3–30 days).  
          - Switch between **hourly** and **daily** resolution.  
          - Select which **variables** to include in the plot.

        **How the processing is done (Python)**

        1. Use the `requests` library to call the public `/v1/forecast` endpoint.  
        2. Convert the JSON response to a Pandas DataFrame.  
        3. Parse timestamps and create `date` / `hour` helper columns.  
        4. Optionally aggregate to daily level (mean for temperature, humidity, wind;
           sum for precipitation).  
        5. Reshape the table to a long format and visualise it with **Altair** line charts.

        This fits the course requirement of using **APIs with Python** to fetch,
        process and visualise real data in a Streamlit app.
        """
    )
