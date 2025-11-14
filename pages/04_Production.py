import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pymongo import MongoClient

st.set_page_config(page_title="Production", page_icon="⚡")

st.title("Power production – 2021")
st.write("This page shows curated production data by price area and production group.")


@st.cache_data
def load_production_data():
    """
    Try to load data from MongoDB (ind320.elhub_prod_2021).
    If that fails or MONGO_URI is not set, fall back to the CSV
    exported from the Jupyter Notebook.
    """
    # 1) Try MongoDB
    mongo_uri = os.environ.get("MONGO_URI", "").strip()
    if mongo_uri:
        try:
            client = MongoClient(mongo_uri)
            db = client["ind320"]
            coll = db["elhub_prod_2021"]
            docs = list(coll.find({}, {"_id": 0}))
            if docs:
                df = pd.DataFrame(docs)
                df["startTime"] = pd.to_datetime(df["startTime"], utc=True)
                return df, "MongoDB collection ind320.elhub_prod_2021"
        except Exception as e:
            st.warning(f"MongoDB not available, falling back to CSV. Reason: {type(e).__name__}")

    # 2) Fallback to CSV
    csv_path = "streamlit_app/data/elhub_export_2021.csv"
    if not os.path.exists(csv_path):
        st.error(f"Could not find CSV at {csv_path}. Please export it from the notebook.")
        return pd.DataFrame(), f"Missing CSV file: {csv_path}"

    df = pd.read_csv(csv_path)
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True)
    return df, f"CSV file {csv_path}"


df, source_label = load_production_data()

if df.empty:
    st.stop()

# Prepare lists for controls
price_areas = sorted(df["priceArea"].dropna().unique())
groups_all = sorted(df["productionGroup"].dropna().unique())
months_all = sorted(df["startTime"].dt.month.unique())

# Layout: two columns
left_col, right_col = st.columns(2)

# ------------------------ LEFT:PIE CHART ------------------------
with left_col:
    st.subheader("Total production by group")

    # Price area selector (radio, as required)
    selected_area = st.radio(
        "Price area",
        options=price_areas,
        index=0,
        horizontal=True,
    )

    pie_df = (
        df[df["priceArea"] == selected_area]
        .groupby("productionGroup", as_index=False)["quantityKwh"]
        .sum()
        .sort_values("quantityKwh", ascending=False)
    )

    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.pie(
        pie_df["quantityKwh"].values,
        labels=pie_df["productionGroup"].values,
        autopct="%1.1f%%",
        startangle=90,
    )
    ax1.axis("equal")
    ax1.set_title(f"Total 2021 production – {selected_area}")
    st.pyplot(fig1)

# ------------------------ RIGHT: LINE PLOT ------------------------
with right_col:
    st.subheader("Monthly profile by group")

    # HERE is the important part: st.pills WITHOUT the 'selection=' argument
    selected_groups = st.pills("Production groups", options=groups_all)
    # On some versions, this returns None or a single value; normalise to a list
    if not selected_groups:
        selected_groups = groups_all
    elif isinstance(selected_groups, str):
        selected_groups = [selected_groups]

    # Month selector
    month_name_map = {
        m: datetime(2021, m, 1).strftime("%B")
        for m in months_all
    }
    month_labels = [month_name_map[m] for m in months_all]
    selected_month_label = st.selectbox("Month", options=month_labels, index=0)
    # Reverse map label -> month number
    label_to_month = {v: k for k, v in month_name_map.items()}
    selected_month = label_to_month[selected_month_label]

    # Filter data
    mask = (
        (df["priceArea"] == selected_area)
        & (df["startTime"].dt.month == selected_month)
        & (df["productionGroup"].isin(selected_groups))
    )
    jan_df = df.loc[mask].copy()

    if jan_df.empty:
        st.info("No data for this combination of price area, month and groups.")
    else:
        # Aggregate by day to make the x-axis readable
        jan_df["date"] = jan_df["startTime"].dt.date
        daily = (
            jan_df.groupby(["date", "productionGroup"], as_index=False)["quantityKwh"]
            .sum()
            .rename(columns={"quantityKwh": "kWh"})
        )

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        for group, gdf in daily.groupby("productionGroup"):
            ax2.plot(
                pd.to_datetime(gdf["date"]),
                gdf["kWh"],
                marker=".",
                label=group,
            )

        ax2.set_title(f"Daily production – {selected_area}, {selected_month_label} 2021")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("kWh")
        ax2.grid(True, alpha=0.3)
        ax2.legend(title="Production group")

        ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        fig2.autofmt_xdate()

        st.pyplot(fig2)

# ------------------------ EXPANDER ------------------------
with st.expander("Data source and processing"):
    st.markdown(
        f"""
        - Data shown on this page is based on **Elhub production per group MBA hour** for the year 2021.
        - Raw hourly data was imported in the IND320 Jupyter Notebook, filtered to the columns
          `priceArea`, `productionGroup`, `startTime` and `quantityKwh`, and then written via Spark/Cassandra.
        - The curated dataset used here is loaded from **{source_label}**.
        - This page lets you explore:
          - Total annual production per group (pie chart, left), and
          - Daily values for a chosen month, price area and set of production groups (line plot, right).
        """
    )
