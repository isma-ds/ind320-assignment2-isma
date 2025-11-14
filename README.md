# IND320 – Assignment 2 Portfolio (Isma Sohail)

This repository contains my solution for **IND320 Project Part 2**, where the goal is to build an end-to-end data workflow and an interactive Streamlit app based on Elhub production data and Open-Meteo weather data.

The project covers:

- Retrieval of hourly production data for all price areas in 2021 using the Elhub API  
  (`PRODUCTION_PER_GROUP_MBA_HOUR`).
- Local storage and optional Spark/Cassandra round-trip for the curated dataset.
- Export of the filtered variables `priceArea`, `productionGroup`, `startTime`,  
  and `quantityKwh` for further use.
- Insertion of curated data into MongoDB Atlas (collection `ind320.elhub_prod_2021`).
- A multi-page Streamlit app that explores both Open-Meteo and Elhub data.

## Project structure

- `app.py` – main entry point for the Streamlit app (multi-page navigation).
- `pages/02_Data_Table.py` – weather data table for the Open-Meteo subset.
- `pages/03_Plots.py` – weather time-series plots with readable date axis and  
  date-range selection.
- `pages/04_Production.py` – production page with:
  - pie chart of total 2021 production by production group for a selected price area,
  - line plot of daily production for a selected month and set of groups,
  - short documentation of the data source in an expander.
- `pages/05_About.py` – short description of the assignment and data pipeline.
- `data/open-meteo-subset.csv` – subset of the Open-Meteo weather dataset.
- `streamlit_app/data/elhub_export_2021.csv` – exported Elhub production data.
- `notebooks/IND320_part1.ipynb` and `IND320_part2.ipynb` – Jupyter notebooks used
  for data collection, Spark/Cassandra work and plotting.

## Running the app locally

```bash
pip install -r requirements.txt
streamlit run app.py
