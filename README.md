# RideWise Customer Analytics — Project Documentation

This document explains the **purpose**, **logic**, and **functionality** of the entire RideWise project. It is intended for onboarding new developers and presenting the system to stakeholders. The project combines **exploratory analysis**, **customer segmentation**, **churn prediction**, and a **production web application** for ride-sharing analytics.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Data Flow Summary](#3-data-flow-summary)
4. [Notebooks Pipeline](#4-notebooks-pipeline)
5. [Web Application](#5-web-application)
6. [Backend API (Churn Prediction)](#6-backend-api-churn-prediction)
7. [How the Pieces Connect](#7-how-the-pieces-connect)
8. [Running the Project](#8-running-the-project)
9. [File and Folder Reference](#9-file-and-folder-reference)

---

## 1. Project Overview

### What Is RideWise?

**RideWise** is a ride-hailing analytics and churn-prediction project. It has two main parts:

- **Jupyter notebooks** — A step-by-step pipeline that explores raw data, engineers features, segments customers (RFMS), defines churn, trains classification models, and produces explainability (SHAP). The notebooks also write the processed datasets and trained models that the app uses.
- **Web dashboard** — A Streamlit frontend plus FastAPI backend that lets users explore trips, demand, revenue, “revenue at risk” by segment, and **predict churn** for one rider or a batch, with recommendations.

**In one sentence:** The project turns ride-hailing data into a clear picture of business health and into actionable churn risk scores so the business can retain customers before they leave.

### Why Each Part Exists

| Component | Purpose |
|----------|--------|
| **Notebooks** | Define how data is cleaned, joined, and modeled; produce the tables and model artifacts the app consumes. They are the single source of truth for logic and reproducibility. |
| **Dashboard** | Give non-technical users a single place to explore metrics and run churn predictions without touching code or notebooks. |

---

## 2. Repository Structure

```
Project 4 - Final/
├── data/                          # Raw and processed data
│   ├── riders.csv, trips.csv, sessions.csv, promotions.csv, drivers.csv  # Raw
│   └── processed_data/            # Outputs from notebooks (see Data Flows)
│       ├── riders_trips.csv       # Trip-level data for dashboard Overview/Demand/Revenue
│       ├── rfm_data.csv           # One row per customer + RFMS segment (Exposure page)
│       ├── riders_trips_rfms_churned.csv  # Churn modeling + RFMS (model training)
│       └── ...                    # Other intermediate files (see Section 3)
├── notebooks/                     # Analysis and modeling pipeline
│   ├── 00_Dataset_Exploration.ipynb
│   ├── 01_EDA of Business/
│   ├── 02_Customer Segmentation/
│   └── 03_Customer Churn Prediction/
├── output/
│   └── webapp/                    # Deployable web application
│       ├── frontend/              # Streamlit app
│       │   ├── Home.py             # Entry point and navigation
│       │   ├── pages/              # One file per page
│       │   ├── data_loader.py      # Loads CSVs for dashboard
│       │   ├── style.py            # Global CSS (sidebar, background, metrics)
│       │   ├── widgets/            # Reusable UI (metric_card, date_card)
│       │   └── data/               # Expected location for riders_trips.csv, rfm_data.csv
│       ├── backend/                # FastAPI churn API
│       │   ├── main.py             # Routes: /health, /predict, /predict/batch
│       │   ├── model_loader.py     # Loads preprocessor + model; prediction + recommendations
│       │   └── schema.py           # Pydantic request/response models
│       ├── model/                  # Expected location for .joblib files (see Section 7)
│       ├── Dockerfile
│       ├── requirements.txt
│       └── render.yaml             # Optional: Render.com deployment config
└── README.md                      # This file
```

---

## 3. Data and Data Flows

### Raw Data (Input)

- **riders.csv** — One row per rider: demographics, loyalty status, signup date, city.
- **trips.csv** — One row per trip: fare, tip, surge, pickup/dropoff time and coordinates, payment, weather.
- **sessions.csv** — App session data (engagement).
- **promotions.csv** — Campaign metadata.
- **drivers.csv** — Driver data (context only).

The **unit of analysis** for the final dashboards and churn model is the **customer (rider)**. Trip- and session-level data are aggregated per rider where needed.

### Processed Data (Produced by Notebooks)

| File | Produced By | Used By | Description |
|------|-------------|---------|-------------|
| **riders_trips.csv** | EDA / feature-engineering notebooks | Frontend: Overview, Demand & Revenue | Trip-level data with rider attributes, pickup time, city, loyalty, fare, tip. One row per trip. |
| **rfm_data.csv** | Customer Segmentation (RFM notebook) | Frontend: Exposure Analysis | One row per customer: recency, frequency, monetary, segments, and related fields. |
| **riders_trips_rfms_churned.csv** | Churn notebooks | Churn model training; 03_SHAP | One row per rider with churn label and RFMS segment; used to train and evaluate the classifier. |

Other files in `data/processed_data/` (e.g. `user_agg_df.csv`, `data_EDA.csv`, `data_modeling.csv`) are intermediate outputs used inside the notebook pipeline.

### Data Expected by the Web App

- **Frontend** (`data_loader.py`): Reads from `frontend/data/` relative to the frontend app:
  - `riders_trips.csv` — for Overview and Demand & Revenue.
  - `rfm_data.csv` — for Exposure Analysis.
- **Backend** (`model_loader.py`): Reads from `output/webapp/model/` (relative to backend’s resolution of project root):
  - `lg_churn_model.joblib` (or equivalent classifier)
  - `lg_churn_model_metadata.joblib` (threshold, feature list)
  - `preprocessor.joblib` (same preprocessing as in 03_SHAP Explainability notebook)

For local runs, ensure these files exist in the expected paths (e.g. copy or symlink from `data/processed_data/` and from wherever the SHAP notebook saves the model).

---

## 4. Notebooks: Analytics & Modeling Pipeline

The notebooks form a **sequential pipeline**. Later notebooks depend on outputs of earlier ones.

---

### 4.1 Notebook 00: Dataset Exploration

**Path:** `notebooks/00_Dataset_Exploration.ipynb`

**Purpose:** Data audit and relationship analysis before any modeling.

**What it does:**

- Loads and inspects the five raw datasets (riders, trips, sessions, promotions, drivers).
- Checks structure, missing values, and duplicates.
- Validates primary and foreign key relationships and defines how tables should be joined.
- Ensures the “one row per rider” concept and join logic are clear for downstream work.

**Why it exists:** Prevents incorrect joins, data leakage, and silent data-quality bugs in later notebooks and in the app.

**Output:** No direct file output; it establishes the **data dictionary and join rules** used in subsequent notebooks.

---

### 4.2 Notebooks 01: EDA of Business

**Path:** `notebooks/01_EDA of Business/`

**Purpose:** Turn raw/joined data into business-ready features and answer high-level business questions.

**01_Feature_Engineering_for_EDA.ipynb**

- Builds a joined/engineered dataset (e.g. from `riders_trips.csv` or equivalent).
- Adds time-based features (year, month, day, hour, weekend, peak hour, etc.) and any other derived columns needed for EDA.

**02_EDA_for_Business_Context.ipynb**

- Explores the data to answer questions such as:
  - Demographics of the customer base
  - When demand is highest
  - Which users are most profitable
  - Which cities to focus on for marketing
  - Effect of surge pricing on churn
  - Relationship of trip distance/duration to price
  - What drives tipping
  - Stability of the customer base (churn)

**Why they exist:** They define which metrics and segments matter for the business and inform what the dashboard shows (e.g. Overview, Demand, Revenue, Exposure).

**Outputs:** Contribute to or produce datasets such as `data_EDA.csv` and the trip-level data that eventually feeds the dashboard (e.g. `riders_trips.csv`).

---

### 4.3 Notebooks 02: Customer Segmentation

**Path:** `notebooks/02_Customer Segmentation/`

**Purpose:** Segment customers using RFM and Surge (RFMS) so the business can target offers and the churn model can use segment as a feature.

**01_Feature Engineering & EDA.ipynb**

- Works with user-level or trip-level data; creates features needed for clustering and RFMS (e.g. recency, frequency, monetary, surge-related).

**02_Data Processing for Clustering Modelling.ipynb**

- Produces a clean, one-row-per-customer table (e.g. `user_agg_df.csv`) with recency, total_trips, spend, avg_surge, tips, ratings, loyalty, city, avg_distance, avg_duration, active_days.

**03_Clustering Model Development.ipynb**

- Runs clustering (e.g. K-means or similar) on RFM(S) dimensions to get segment labels.

**04_RFM_Analysis.ipynb**

- Defines the **RFMS framework**:
  - **R**ecency — days since last trip
  - **F**requency — e.g. total trips
  - **M**onetary — total spend
  - **S**urge — average surge multiplier (price tolerance)
- Maps clusters to named segments (e.g. “At Risk”, “Occasional Riders”, “Core Loyal Riders”, “High-Value Surge-Tolerant”) and produces segment labels per customer.

**Why they exist:** Segments drive the Exposure Analysis page (revenue at risk by segment) and the Churn Predictor (RFMS segment is an input and drives recommendations).

**Outputs:** User-level tables with RFMS segments; one of these (or a derivative) is saved as `rfm_data.csv` for the dashboard and used in churn modeling.

---

### 4.4 Notebooks 03: Customer Churn Prediction

**Path:** `notebooks/03_Customer Churn Prediction/`

**Purpose:** Define churn, build a classification model, and export a preprocessor + model for the API.

**01_Churn_Definition_&_Churn_EDA.ipynb**

- Defines **churn** (e.g. no activity for a fixed number of days or similar rule).
- Creates a binary churn label and explores churn rates and patterns.

**02_Data Processing & Classification Model Development.ipynb**

- Loads the dataset with churn label and RFMS (e.g. `riders_trips_rfms_churned.csv`).
- Splits train/test, handles class imbalance (e.g. SMOTE), builds preprocessing (scaling, encoding).
- Trains and compares classifiers (e.g. Logistic Regression, Random Forest, XGBoost).
- Picks a business threshold and saves the chosen model and metadata.

**03_SHAP Explainability.ipynb**

- Uses the same churn dataset and **same feature set** as the model.
- Builds a **preprocessing pipeline** (ColumnTransformer) that matches the model’s expectations (numeric + categorical encoding).
- Fits the preprocessor on the training data and saves it as `preprocessor.joblib`.
- Optionally runs SHAP for interpretability.
- Ensures the **column order and transformations** used here are exactly what the backend’s `model_loader.py` expects (see `RAW_FEATURE_ORDER` and preprocessor usage).

**Why they exist:** They produce the churn definition, the trained model, the threshold, and the preprocessor that the FastAPI backend loads to serve single and batch predictions.

**Outputs:** Model and metadata (e.g. `lg_churn_model.joblib`, `lg_churn_model_metadata.joblib`) and `preprocessor.joblib`, to be placed in `output/webapp/model/`.

---

## 5. Web Application

The application consists of a **Streamlit frontend** (multi-page) and a **FastAPI backend** (churn prediction only). The frontend uses a top navigation bar; filters are per-page and do not persist when switching pages.

---

### 5.1 Application Architecture

- **Frontend:** `output/webapp/frontend/` — Streamlit. Renders all dashboard pages and calls the backend for churn predictions.
- **Backend:** `output/webapp/backend/` — FastAPI. Exposes `/health`, `/info`, `/predict`, and `/predict/batch`; loads the preprocessor and model at startup.
- **Data:** The frontend reads only from local CSV files (via `data_loader.py`). No database.
- **Churn:** Single and batch predictions are sent as JSON to the backend; the backend runs the preprocessor and model and returns probability, label, risk level, and recommendation.

---

### 5.2 Entry Point and Navigation

**File:** `frontend/Home.py`

**Purpose:** Application entry point and global navigation.

**What it does:**

- Sets page title and layout.
- Injects global sidebar and background styles (`style.py`).
- Defines the **navigation list**: Home, Overview, Demand & Revenue, Exposure Analysis, Churn Predictor.
- Uses `st.navigation(pages, position="top")` so the top bar is the main way to switch pages.
- Does **not** render page content itself; each page module is loaded when the user selects it.

**Why it exists:** Single place to add or reorder pages and to apply app-wide styling.

---

### 5.3 Page: Home (Dashboard)

**File:** `frontend/pages/0_Dashboard.py`

**Purpose:** Landing page and quick description of the app.

**What it does:**

- Shows a short title and project description (e.g. “Rideshare Executive Dashboard” and developer credit).
- Lists what each other page does (Overview, Demand & Revenue, Exposure, Churn Predictor).
- Tells users to use the **top navigation bar** to move between pages.
- Calls `load_data()` so trip data is cached and subsequent pages (Overview, Demand & Revenue) load faster.

**What you see:** Text and bullet list; no charts or filters.

**Why it exists:** Gives new users a clear starting point and reduces perceived load time when opening data-heavy pages.

---

### 5.4 Page: Overview

**File:** `frontend/pages/1_Overview.py`

**Purpose:** Answer: *“What does our rideshare business look like at a glance?”*

**What it does:**

- Loads trip data via `load_data()` (from `frontend/data/riders_trips.csv`).
- **Sidebar filters:** City and Loyalty Tier (each can be “All” or a single value). The dataframe is filtered to the selected cities and loyalty tiers.
- **Metrics row:** Displays Total Users (currently fixed at 10,000 and not filtered), Total Trips, and Revenue over the filtered data.
- **Charts:**
  - **Pie chart:** Share of users in each loyalty tier (Bronze, Silver, Gold, etc.).
  - **Bar chart:** Number of users per city (horizontal bars).
- Uses the shared **metric_card** widget for the three KPIs.

**Data flow:** `data_loader.load_data()` → filter by city and loyalty_status → aggregate for metrics and charts.

**Why it exists:** Quick snapshot of scale (trips, revenue) and mix (loyalty and geography) for reporting and comparison.

---

### 5.5 Page: Demand & Revenue

**File:** `frontend/pages/2_Demand_Revenue.py`

**Purpose:** Answer: *“When do rides happen?”* and *“When does revenue come in?”* on one page with two tabs.

**What it does:**

- Loads the same trip data via `load_data()`.
- **Sidebar filters (shared across both tabs):** Year, Month, City. Each can be “All” or a single option. Data is filtered by `pickup_year`, `pickup_month_num`, and `city`.
- **Shared KPIs (above the tabs):** Total Users, Total Trips, Revenue, Average Fare — all computed on the filtered dataframe.
- **Tab “Demand Analysis”:**
  - Bar chart: trips per hour of the day (`pickup_hour`).
  - Line chart: trips per day over the selected period (daily count by `pickup_time` date).
- **Tab “Revenue Analysis”:**
  - Bar chart: revenue per hour (`total_fare` by `pickup_hour`).
  - Line chart: revenue per day over the selected period.

**Data flow:** `load_data()` → filter by year, month, city → group by hour or by date for charts; sum or count as needed.

**Why it exists:** Lets operations compare demand (trip counts) and revenue (fare) over time to plan driver supply and pricing.

---

### 5.6 Page: Exposure Analysis

**File:** `frontend/pages/4_Exposure_Analysis.py`

**Purpose:** Answer: *“How much revenue could we lose if we don’t re-engage customers who meet an inactivity threshold?”* and *“Who are they, by segment?”*

**What it does:**

- Loads customer-level segment data via `load_data_segments()` from `frontend/data/rfm_data.csv` (drops the `rfm_score` column).
- **Sidebar:** Single control — “Days since last activity” (slider from 7 to 90, step 7). This value is the **inactivity threshold**.
- **At-risk definition in code:** `at_risk_customers = rfm[rfm['recency'] <= inactivity_threshold]`. So the page shows customers whose **recency** (days since last trip) is **less than or equal to** the chosen number. In RFM terms, lower recency means more recently active; thus this selects customers who were active **within** the last N days. (If the product intent is “inactive for N days,” the condition would typically be `recency >= inactivity_threshold`; the current behavior is as implemented.)
- **Metrics:** Revenue at Risk (sum of `monetary` over at-risk customers), Customers Exposed (count), and a date range (min/max of `last_trip_time` for those customers) via **date_card**.
- **Treemap:** Proportion of “Revenue Exposure” by customer **segment** (`segments`). Size and color represent revenue per segment.
- **Table:** List of at-risk customers (dataframe with segment and monetary; `last_trip_time` dropped for display).

**Data flow:** `load_data_segments()` → filter by recency ≤ threshold → aggregate by segment and sum monetary; pass to treemap and table.

**Why it exists:** Supports re-engagement and campaign sizing by quantifying revenue tied to a chosen recency cut and by segment.

---

### 5.7 Page: Churn Predictor

**File:** `frontend/pages/5_Churn_Predictor.py`

**Purpose:** Predict churn risk for one rider or a batch and show a recommended action.

**What it does:**

- **Sidebar:** Calls the backend `/health` endpoint. Shows “API ready” or an error (e.g. “Cannot reach API” or “Model not loaded”).
- **Tabs:**
  - **Single Predict:** Form with 11 inputs: recency, total_trips, avg_spend, total_tip, avg_tip, avg_rating_given, loyalty_status, city, avg_distance, avg_duration, RFMS_segment. On “Predict Churn Risk,” sends a POST to `API_URL/predict` with the payload. Result is shown in a **dialog**: churn probability, risk level (Low/Medium/High), churn/retained label, progress bar, threshold, and **recommendation** text.
  - **Batch Predict:** File upload (CSV) with the same 11 columns. On “Predict batch,” sends POST to `API_URL/predict/batch`. Displays a table of predictions and a download button for the results CSV.
  - **About:** Short description of inputs, outputs, and that the backend uses a preprocessor + trained model.
- **API URL:** Taken from environment variable `API_URL` (default `http://localhost:8000`).

**Data flow:** User input → JSON to FastAPI → `model_loader` runs preprocessor and model → response with probability, label, risk level, recommendation → frontend displays in dialog or table.

**Why it exists:** Puts the trained churn model in the hands of business users for single riders or lists (e.g. from CRM) and ties risk to actionable recommendations.

---

### 5.8 Shared Components

**data_loader.py**

- **load_data():** Reads `frontend/data/riders_trips.csv`, parses `pickup_time`, adds `pickup_year`, `pickup_month_num`, `pickup_month_name`. Cached with `st.cache_data`.
- **load_data_segments():** Reads `frontend/data/rfm_data.csv` and drops `rfm_score`. Used only by Exposure Analysis.

**style.py**

- **inject_background_style():** Sets app background (gradient or image from `frontend/assets/background.png`).
- **inject_sidebar_style():** Injects CSS for sidebar, navigation links, metric cards, viewport, and Churn Predictor–specific styles (risk colors, buttons).

**widgets/metric_card.py**

- **metric_card(title, value, delta=None, prefix="", suffix=""):** Renders a styled KPI card (title, formatted value, optional delta). Used on Overview, Demand & Revenue, and Exposure.

**widgets/date_card.py**

- **date_card(value_min, value_max):** Renders a card showing a date range (e.g. “Date Range: max – min”). Used on Exposure Analysis.

---

### 5.9 Backend API

**main.py**

- **FastAPI app** with CORS enabled for frontend access.
- **GET /health:** Returns `{"status": "ok", "model_loaded": bool}`. Used by the Churn Predictor page to show connection status.
- **GET /info:** Returns version, threshold, feature count; 503 if model not loaded.
- **POST /predict:** Accepts a single `ChurnFeatures` body. Calls `model_service.predict_label()` and `model_service.risk_level()`, then `model_service.recommendation(RFMS_segment, risk)`. Returns `ChurnPredictionResponse` (churn_probability, churn_label, threshold, risk_level, recommendation).
- **POST /predict/batch:** Accepts a list of `ChurnFeatures`. Runs predict for each and returns `{ "predictions": [...], "count": N }`.

**schema.py**

- **ChurnFeatures:** Pydantic model for the 11 raw features (recency, total_trips, avg_spend, total_tip, avg_tip, avg_rating_given, loyalty_status, city, avg_distance, avg_duration, RFMS_segment) with types and constraints.
- **ChurnPredictionResponse:** churn_probability, churn_label, threshold, risk_level, recommendation.

**model_loader.py**

- **ChurnModelService:** On init, loads `lg_churn_model.joblib`, `lg_churn_model_metadata.joblib`, and `preprocessor.joblib` from `output/webapp/model/`. Applies a compatibility patch for tree-based models if needed. Reads business threshold and feature columns from metadata.
- **predict_proba(features_dict):** Builds a one-row DataFrame in `RAW_FEATURE_ORDER`, runs preprocessor, then model `predict_proba`; returns probability of class 1 (churn).
- **predict_label(features_dict):** Returns (label, proba) where label = 1 if proba ≥ threshold else 0.
- **risk_level(proba, threshold, thr_mid):** Maps probability to “Low Risk”, “Medium Risk”, or “High Risk” using threshold and a mid threshold (e.g. 0.65).
- **recommendation(rfms_segment, risk_level):** Returns a fixed recommendation string based on segment and risk (e.g. “Highest priority: churn-prevention package…” for High Risk + At Risk). This is business logic, not ML.
- If model files are missing or loading fails, `model_service` is set to `None` and the API returns 503 on `/predict` and `/info`.

---

## 6. How Pages and Notebooks Connect

- **Notebooks** produce:
  - Trip-level data → copied/symlinked as `frontend/data/riders_trips.csv` → **Overview**, **Demand & Revenue**.
  - Customer-level RFMS data → `frontend/data/rfm_data.csv` → **Exposure Analysis**.
  - Churn dataset + preprocessing + model → saved to `output/webapp/model/` → **Backend** → **Churn Predictor** page.
- **Overview**, **Demand & Revenue** share the same data source and the same `load_data()` cache; they do not share filters across pages.
- **Exposure Analysis** is independent of trip-level filters; it only uses the segment file and the “days since last activity” slider.
- **Churn Predictor** does not use the CSV data; it only talks to the FastAPI backend. The backend expects the same 11 features and the same preprocessor as in **03_SHAP Explainability**.

---

## 7. Deployment and Running the Application

### Prerequisites

- Python 3.11+ (or as in `Dockerfile`).
- Dependencies: see `output/webapp/requirements.txt` (FastAPI, uvicorn, Streamlit, pandas, scikit-learn, joblib, pydantic, requests, etc.).

### Data and Model Setup

1. Run the notebook pipeline so that:
   - `riders_trips.csv` and `rfm_data.csv` exist (or equivalent); place copies in `output/webapp/frontend/data/`.
   - `preprocessor.joblib`, `lg_churn_model.joblib`, and `lg_churn_model_metadata.joblib` are saved from the churn/SHAP notebooks into `output/webapp/model/`.
2. Ensure the backend can resolve the project root so that `model/` points to `output/webapp/model/` (see `model_loader.py`).

### Run Locally

- **Backend:** From `output/webapp/`, run:  
  `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`
- **Frontend:** From `output/webapp/`, run:  
  `streamlit run frontend/Home.py --server.port 8501`  
  (or run from `frontend/` with `streamlit run Home.py` and ensure `API_URL` is set if the API is elsewhere.)
- Set `API_URL` (e.g. `http://localhost:8000`) when the frontend runs on a different host/port than the backend.

### Docker

- The provided `Dockerfile` builds and runs the **API only** by default:  
  `CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]`.  
  For a frontend container, override the command to run Streamlit and ensure `API_URL` points to the API service (e.g. in `render.yaml`).

### Render.com

- `render.yaml` defines two services (API and frontend). Set the frontend’s `API_URL` to the deployed API URL after the first deploy.

---

## 8. Quick Reference

### What Each Page Answers

| Page | Main question | Main actions |
|------|----------------|--------------|
| **Home** | Where do I start? | Read intro; use top nav to open other pages; data preloaded for speed. |
| **Overview** | What does the business look like at a glance? | Filter by city and loyalty tier; view totals and pie/bar charts. |
| **Demand & Revenue** | When do rides and revenue happen? | Filter by year, month, city; switch tabs for demand vs revenue charts. |
| **Exposure Analysis** | How much revenue is at risk and who are those customers? | Set “days since last activity”; view revenue at risk, treemap by segment, customer table. |
| **Churn Predictor** | Is this rider (or list) likely to churn? What should we do? | Single: form → predict → dialog with probability, risk, recommendation. Batch: upload CSV → download predictions. |

### Notebook Pipeline Order

1. **00_Dataset_Exploration** — Audit and relationships.
2. **01_EDA of Business** — Feature engineering and business EDA.
3. **02_Customer Segmentation** — RFMS and segments → `rfm_data.csv` and inputs for churn.
4. **03_Customer Churn Prediction** — Churn definition, model training, SHAP and preprocessor → model and preprocessor for the API.

### Key Files for Onboarding

- **Navigation and entry:** `frontend/Home.py`
- **Data loading:** `frontend/data_loader.py`
- **Churn API:** `backend/main.py`, `backend/model_loader.py`, `backend/schema.py`
- **Preprocessor/feature contract:** Notebook `03_SHAP Explainability.ipynb` and `model_loader.py` (`RAW_FEATURE_ORDER`, preprocessor usage).

---

*This documentation is intended to be production-ready for developer onboarding and stakeholder presentation. For step-by-step user instructions without technical detail, see `output/webapp/frontend/Read Me.md`.*
