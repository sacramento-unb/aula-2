# Carbon monitoring classroom prototype

Small Streamlit exercise that compares uploaded GeoParquet tables for soil
carbon and deforestation by year, renders the carbon geometries in Folium and
plots annual totals.

## Expected inputs

The carbon table must contain `ano`, `val`, `area` and a geometry column. The
deforestation table must contain `ano`, `st_area_ha` and geometry metadata
readable by GeoPandas. CRS, units and data provenance are not validated by the
application.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run home.py
```

## Status and limitations

This is an untested teaching prototype, not a maintained monitoring system.
Uploaded data stays in the Streamlit process, but its sensitivity remains the
operator's responsibility. Classification thresholds and metric labels are
hard-coded; no sample dataset or automated test is included.

An existing license file is present. Its applicability and attribution should
be reviewed before redistributing datasets or derivatives.
