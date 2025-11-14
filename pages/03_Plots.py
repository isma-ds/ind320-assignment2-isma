import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="Plots", page_icon="📈")

st.title("Weather plots")
st.write("Weather time series from the Open-Meteo subset used in part 1.")

# ---------- Load data directly from CSV ----------
@st.cache_data
def load_weather():
    csv_path = Path("data/open-meteo-subset.csv")
    if not csv_path.exists():
        st.error(f"File {csv_path} not found.")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)

    df = df.rename(
        columns={
            "time": "time",
            "temperature_2m (°C)": "temperature_2m",
            "precipitation (mm)": "precipitation",
            "wind_speed_10m (m/s)": "wind_speed_10m",
            "wind_gusts_10m (m/s)": "wind_gusts_10m",
            "wind_direction_10m (°)": "wind_direction_10m",
        }
    )

    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")
    return df


df = load_weather()
if df.empty:
    st.stop()

# ---------- Date range control to keep x-axis readable ----------
min_date = df.index.min().date()
max_date = df.index.max().date()

default_end = min_date + timedelta(days=6)   # default: first 7 days
if default_end > max_date:
    default_end = max_date

start_date, end_date = st.date_input(
    "Select date range:",
    value=(min_date, default_end),
    min_value=min_date,
    max_value=max_date,
)

mask = (df.index.date >= start_date) & (df.index.date <= end_date)
df_range = df.loc[mask].copy()

if df_range.empty:
    st.warning("No data in the selected date range.")
    st.stop()

# ---------- Column selection ----------
available_cols = [
    "temperature_2m",
    "precipitation",
    "wind_speed_10m",
    "wind_gusts_10m",
    "wind_direction_10m",
]

selected = st.multiselect(
    "Select variables to display:",
    options=available_cols,
    default=available_cols,
)

if not selected:
    st.info("Select at least one variable.")
    st.stop()

# ---------- Plot with automatically thinned x-axis ----------
fig, ax = plt.subplots(figsize=(10, 4))

for col in selected:
    ax.plot(df_range.index, df_range[col], label=col)

ax.set_xlabel("Time")
ax.set_ylabel("Value")
ax.legend()

# Choose tick interval so we get ~6–7 labels max
total_days = (end_date - start_date).days + 1
interval = max(1, total_days // 6)

ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %Y"))
fig.autofmt_xdate(rotation=45)

st.pyplot(fig)

st.markdown("© 2025 Isma Sohail | IND320 Portfolio")
