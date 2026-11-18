# 🛰️ Punjab GeoGuardian – Urban Expansion & Farmland Loss Detection
AIRI Team PITB – AI Internship Task 3

> Learning prototype, **not** an official government monitoring system. Results are *estimated / possible* changes.

## Overview
Detects possible conversion of agricultural/vegetation land to built-up land by comparing Sentinel-2 imagery of two years.

- **AOI:** Lahore peri-urban zone (Raiwind Road corridor)
- **Years:** 2019 vs 2025 (Jan 15 – Mar 31, same season)
- **Data:** Sentinel-2 SR Harmonized (10 m), cloud < 20 %, SCL mask, median composite
- **Method:** NDVI + NDBI + MNDWI → rule-based baseline + Random Forest → change detection → area stats → hotspots
- **Key result:** `<converted sq km>` sq km (`<x>`%) possible conversion; validation accuracy `<xx>`% on `<n>` points *(fill from outputs)*

## Repository contents
| File | Purpose |
|---|---|
| `PunjabGeoGuardian_Colab.ipynb` | Full pipeline (run in Google Colab) |
| `app.py` | Streamlit dashboard |
| `requirements.txt` | Dependencies |
| `outputs/` | Maps, CSV tables, interactive map, report (copy from Drive) |

## How to run
1. Open the notebook in Colab, set `EE_PROJECT` in the CONFIG cell, run Steps 1–5.
2. Label the generated training/validation CSVs using the Google satellite links, upload them (Step 6), run Steps 7–12.
3. Dashboard: copy the `outputs/` folder next to `app.py`, then `pip install -r requirements.txt && streamlit run app.py`.

## Outputs (9 maps + extras)
RGB, NDVI, NDBI, land-cover (both years), change map, area chart, hotspots (CSV/GeoJSON), area stats (CSV), validation table, error analysis, interactive layer-toggle map, report, LinkedIn text.

## Limitations
10 m resolution (mixed pixels), dry fields/bare soil vs built-up confusion, tree-covered housing, seasonal effects, limited manual samples. No claims are made about any specific housing society or private development.

## Data sources
Copernicus Sentinel-2 via Google Earth Engine (`COPERNICUS/S2_SR_HARMONIZED`); Google satellite basemap for manual labelling.
