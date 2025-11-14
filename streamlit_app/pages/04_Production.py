import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------
# 1) Download Elhub data LIVE from the public CSV API
# ------------------------------------------------------

ELHUB_API_URL = (
    "https://data.elhub.no/download/production_per_group_mba_hour/"
    "production_per_group_mba_hour-all-en-0000-00-00.csv"
)


@st.cache_data(show_spinner="Downloading Elhub production data from API ...")
def load_elhub_2021_from_api() -> pd.DataFrame:
    """
    Download PRODUCTION_PER_GROUP_MBA_HOUR directly from Elhub's
    public CSV API, clean it and return only the columns required
    by the assignment for the year 2021.
    """
    # Raw download (English CSV)
    raw = pd.read_csv(ELHUB_API_URL)

    # The English file currently has these columns:
    # ['START_TIME', 'END_TIME', 'PRICE_AREA',
    #  'PRODUCTION_GROUP', 'VOLUME_KWH']
    rename_map = {
        "START_TIME": "startTime",
        "END_TIME": "endTime",
        "PRICE_AREA": "priceArea",
        "PRODUCTION_GROUP": "productionGroup",
        "VOLUME_KWH": "quantityKwh",
    }
    raw = raw.rename(columns=rename_map)

    # Parse timestamps and keep only 2021
    raw["startTime"] = pd.to_datetime(raw["startTime"], utc=True, errors="coerce")

    df_2021 = raw.loc[
        raw["startTime"].dt.year == 2021,
        ["priceArea", "productionGroup", "startTime", "quantityKwh"],
    ].copy()

    # Make sure quantity is numeric
    df_2021["quantityKwh"] = pd.to_numeric(
        df_2021["quantityKwh"], errors="coerce"
    ).fillna(0.0)

    return df_2021


# ------------------------------------------------------
# 2) Page layout
# ------------------------------------------------------

st.title("Elhub production – 2021")
st.caption(
    "Data from Elhub API "
    "(`PRODUCTION_PER_GROUP_MBA_HOUR`), downloaded live in this app "
    "and filtered to the year **2021**."
)

try:
    df_2021 = load_elhub_2021_from_api()
except Exception as e:
    st.error(
        "❌ Could not download data from the Elhub API.\n\n"
        f"Details: `{type(e).__name__}: {e}`"
    )
    st.stop()

if df_2021.empty:
    st.error("Dataset is empty after filtering to 2021. Please check the API file.")
    st.stop()

price_areas = sorted(df_2021["priceArea"].dropna().unique().tolist())
groups_all = sorted(df_2021["productionGroup"].dropna().unique().tolist())

st.write(f"Available price areas: `{', '.join(price_areas)}`")

col_left, col_right = st.columns(2)


# ------------------------------------------------------
# 3) LEFT COLUMN – Pie chart: total 2021 production per group
# ------------------------------------------------------
with col_left:
    st.subheader("Total yearly production by group")

    price_area_choice = st.radio(
        "Select price area:", price_areas, index=0, horizontal=False
    )

    subset_area = df_2021[df_2021["priceArea"] == price_area_choice]

    yearly_by_group = (
        subset_area.groupby("productionGroup", as_index=False)["quantityKwh"]
        .sum()
        .sort_values("quantityKwh", ascending=False)
    )

    if yearly_by_group.empty:
        st.info("No data available for this price area in 2021.")
    else:
        labels = yearly_by_group["productionGroup"].tolist()
        values = yearly_by_group["quantityKwh"].tolist()

        fig1, ax1 = plt.subplots(figsize=(5, 5))
        wedges, texts, autotexts = ax1.pie(
            values,
            labels=None,  # we'll use legend instead
            autopct="%1.1f%%",
            startangle=90,
        )
        ax1.axis("equal")
        ax1.set_title(f"Total production 2021 – {price_area_choice}")

        # Show legend for readability
        ax1.legend(
            wedges,
            labels,
            title="Production group",
            bbox_to_anchor=(1.05, 0.5),
            loc="center left",
        )

        st.pyplot(fig1)


# ------------------------------------------------------
# 4) RIGHT COLUMN – Line plot for selected month & groups
# ------------------------------------------------------
with col_right:
    st.subheader("Hourly production for a selected month")

    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    month_choice = st.selectbox(
        "Select month:",
        options=list(month_names.keys()),
        format_func=lambda m: month_names[m],
        index=0,
    )

    selected_groups = st.pills(
        "Select production groups (multi-select):",
        options=groups_all,
        selection_mode="multi",
        default=groups_all,
    )

    # Filter data
    mask = (
        (df_2021["priceArea"] == price_area_choice)
        & (df_2021["startTime"].dt.month == month_choice)
        & (df_2021["productionGroup"].isin(selected_groups))
    )
    df_month = df_2021.loc[mask].copy()

    if df_month.empty:
        st.info(
            f"No data available for {price_area_choice} in "
            f"{month_names[month_choice]} 2021 with the selected groups."
        )
    else:
        # Pivot so each production group becomes a separate line
        df_pivot = (
            df_month.pivot_table(
                index="startTime",
                columns="productionGroup",
                values="quantityKwh",
                aggfunc="sum",
            )
            .sort_index()
        )

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        for col in df_pivot.columns:
            ax2.plot(df_pivot.index, df_pivot[col], label=col)

        ax2.set_title(
            f"Hourly production – {month_names[month_choice]} 2021 – {price_area_choice}"
        )
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Production (kWh)")
        ax2.tick_params(axis="x", rotation=45)
        ax2.legend(fontsize=8)

        st.pyplot(fig2)

# ------------------------------------------------------
# 5) Source information
# ------------------------------------------------------
with st.expander("Data source & processing (Elhub)", expanded=False):
    st.markdown(
        """
- **Dataset:** `Production per price range, group and hour (kWh and quantity)`  
  (Elhub data catalogue, dataset `PRODUCTION_PER_GROUP_MBA_HOUR`).
- **API CSV URL used in this app:**  
  `https://data.elhub.no/download/production_per_group_mba_hour/production_per_group_mba_hour-all-en-0000-00-00.csv`
- **Processing steps in the app:**
  1. Download the full CSV from the Elhub API.
  2. Rename the English column names to: `startTime`, `endTime`,
     `priceArea`, `productionGroup`, `quantityKwh`.
  3. Convert `startTime` to timezone-aware timestamps.
  4. Filter rows where the year of `startTime` is **2021**.
  5. Use the cleaned data to:
     - Aggregate total yearly production per group (pie chart).
     - Filter by price area, month and production group and
       plot hourly production as separate time series (line chart).
        """
    )
