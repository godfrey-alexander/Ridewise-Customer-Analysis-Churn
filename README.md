# RideWise Customer Analytics — Project Documentation

This document explains the **purpose**, **logic**, and **functionality** of the entire RideWise project. It is intended for onboarding new developers and presenting the system to stakeholders. The project combines **exploratory analysis**, **customer segmentation**, **churn prediction**, and a **production web application** for ride-sharing analytics.

---

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

**RideWise** is a fictional ride-hailing company. This repository implements an end-to-end **customer analytics and churn prediction** system for such a business.

### Business Problem

The company faces:

- **High customer churn** (riders stopping use of the service).
- Lack of a **unified, data-driven** way to:
  - Understand customer behavior.
  - Segment customers meaningfully.
  - Predict churn before it happens.
  - Design retention and promotion strategies.

### What This Project Delivers

1. **Notebooks** — A reproducible pipeline that:
   - Audits and joins raw data (riders, trips, sessions, etc.).
   - Builds features for business EDA and clustering.
   - Segments customers using **RFMS** (Recency, Frequency, Monetary, Surge).
   - Defines churn and trains **classification models** to predict it.
   - Adds **SHAP explainability** and saves a **preprocessor + model** for production.

2. **Web application** — A Streamlit dashboard that:
   - Shows **overview** metrics, **demand** and **revenue** patterns, and **exposure** (revenue at risk).
   - Offers a **Churn Predictor** (single and batch) that calls a FastAPI backend to score riders and return **risk level** and **recommendations**.

3. **Backend API** — A FastAPI service that loads the saved model and preprocessor, accepts rider features, and returns churn probability, label, risk level, and a text recommendation.

### Unit of Analysis

Throughout the project, the **unit of analysis is the customer (rider)**. Trip- and session-level data are aggregated **per rider** for segmentation and churn modeling.

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RAW DATA (data/)                                   │
│  riders.csv, trips.csv, sessions.csv, promotions.csv, drivers.csv            │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     NOTEBOOKS PIPELINE (notebooks/)                           │
│  00 → 01_EDA (feature eng) → 02_EDA (business)                               │
│  02_Segmentation (feature eng → clustering → RFMS) → 03_Churn (define →      │
│  train → SHAP → save model/preprocessor)                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          ▼                             ▼                             ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│ data/processed_data/ │   │ output/webapp/model/ │   │ frontend/data/       │
│ riders_trips.csv     │   │ preprocessor.joblib │   │ (copy of CSVs for    │
│ riders_trips_rfms    │   │ lg_churn_model*     │   │  dashboard)           │
│ _churned.csv, etc.   │   │                     │   │ riders_trips.csv     │
└─────────────────────┘   └─────────────────────┘   │ rfm_data.csv         │
          │                             │            └─────────────────────┘
          │                             │                       │
          ▼                             ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     WEB APPLICATION (output/webapp/)                          │
│  Frontend (Streamlit): Home, Overview, Demand & Revenue, Exposure, Churn     │
│  Backend (FastAPI): /health, /info, /predict, /predict/batch                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

- **Notebooks** produce processed CSVs and (from the churn pipeline) the **model** and **preprocessor** used by the API.
- The **frontend** reads from its own `data/` (e.g. `riders_trips.csv`, `rfm_data.csv`) for dashboards; the **backend** reads from `model/` for predictions.

---

## 3. Data Flow Summary

### Processed Data Files (from notebooks)

| File | Produced By | Consumed By | Purpose |
|------|-------------|-------------|---------|
| `riders_trips.csv` | 00_Dataset_Exploration | 01_Feature_Engineering (EDA), frontend | Riders joined with trips (one row per trip). |
| `riders_trips_sessions.csv` | 00_Dataset_Exploration | Optional churn paths | Riders + trips + sessions. |
| `data_EDA.csv` | 01_Feature_Engineering_for_EDA | 02_EDA_for_Business_Context, 02_Segmentation/01 | Trip-level data with time/distance/fare features for EDA. |
| `user_agg_df.csv` | 02_Segmentation/01_Feature Engineering & EDA | 02_Segmentation/02, 04_RFM_Analysis | One row per rider: recency, trips, spend, tips, loyalty, city, etc. |
| `data_preprocessed.csv` | 02_Segmentation/02_Data Processing | 02_Segmentation/03_Clustering | Scaled/encoded features for clustering. |
| `riders_trips_rfms.csv` | 02_Segmentation/04_RFM_Analysis | 03_Churn/01_Churn_Definition | Riders with RFMS segment (no churn label yet). |
| `riders_trips_rfms_churned.csv` | 03_Churn/01_Churn_Definition | 03_Churn/02, 03_SHAP; backend training | Riders with RFMS + churn label; used to train churn model. |

### Model Artifacts (used by backend)

- **Preprocessor** — `model/preprocessor.joblib`: ColumnTransformer (ordinal + one-hot for categories; optional numeric scaling) fitted in **03_SHAP Explainability**.
- **Model** — `model/lg_churn_model.joblib`: Trained classifier (e.g. Logistic Regression) from the same pipeline.
- **Metadata** — `model/lg_churn_model_metadata.joblib`: e.g. `business_threshold`, `feature_columns`, for the API.

The **frontend** does not use the raw `data/processed_data/` path directly; it uses copies (or the same structure) under `output/webapp/frontend/data/` (`riders_trips.csv` for trip-level dashboards, `rfm_data.csv` for exposure/segment views).

---

## 4. Notebooks Pipeline

Notebooks are under `notebooks/`. Execution order and dependencies are as below.

---

### 4.1 Notebook 00 — Dataset Exploration

**Path:** `notebooks/00_Dataset_Exploration.ipynb`

**Purpose:**  
Perform a **data audit** and define **table relationships** before any modeling. Ensures joins are correct and avoids data leakage or duplicate rows.

**What it does:**

1. Loads five raw datasets: `riders.csv`, `trips.csv`, `sessions.csv`, `promotions.csv`, `drivers.csv` from `data/`.
2. Inspects structure, dtypes, and basic stats of each table.
3. Validates primary and foreign keys and defines how tables should be joined (e.g. riders ↔ trips via `user_id`).
4. Builds a **riders–trips** join (one row per trip, with rider attributes) and saves:
   - `data/processed_data/riders_trips.csv`
5. Optionally builds **riders–trips–sessions** and saves:
   - `data/processed_data/riders_trips_sessions.csv`

**Outputs:**  
`riders_trips.csv`, `riders_trips_sessions.csv` (optional).

**Why it exists:**  
All downstream work assumes a clear, correct join. This notebook is the single source of truth for “how rider and trip data are combined.”

---

### 4.2 Notebooks 01 — EDA of Business

**Folder:** `notebooks/01_EDA of Business/`

#### 4.2.1 — 01_Feature_Engineering_for_EDA.ipynb

**Purpose:**  
Create a **trip-level** dataset rich enough for business EDA (time of day, duration, distance, fare, surge, weather, etc.).

**What it does:**

1. Reads `data/processed_data/riders_trips.csv`.
2. Parses dates and adds time-based features: year, month, day, hour, weekend, peak hour, night, season.
3. Computes trip metrics: duration (e.g. minutes), distance (e.g. haversine km), total fare (with surge), total fare with tip, tip percentage, surge flag, weather/surge interaction, etc.
4. Saves the enriched trip-level table as:
   - `data/processed_data/data_EDA.csv`

**Outputs:**  
`data_EDA.csv`.

**Why it exists:**  
Business questions (demand by hour, revenue by day, impact of surge/weather) require these features; this notebook creates them once for EDA and for the segmentation feature-engineering step.

#### 4.2.2 — 02_EDA_for_Business_Context.ipynb

**Purpose:**  
Answer **business questions** using the EDA dataset: demographics, demand patterns, profitability, city focus, surge vs churn, distance/time vs price, tipping, and churn stability.

**What it does:**

1. Loads `data/processed_data/data_EDA.csv`.
2. Uses visualizations and summary stats to explore:
   - Customer demographics and loyalty/city mix.
   - When demand is highest (hour, day).
   - Who is most profitable.
   - Which cities to focus on.
   - Surge vs churn, trip distance/time vs price, tipping behavior, and churn distribution.

**Outputs:**  
None (analysis only). Feeds business understanding used in segmentation and churn strategy.

**Why it exists:**  
To turn the engineered dataset into clear, stakeholder-ready insights before building segments and models.

---

### 4.3 Notebooks 02 — Customer Segmentation

**Folder:** `notebooks/02_Customer Segmentation/`

#### 4.3.1 — 01_Feature Engineering & EDA.ipynb

**Purpose:**  
Build a **rider-level** (one row per user) aggregated dataset for clustering and RFMS.

**What it does:**

1. Reads `data/processed_data/data_EDA.csv` (trip-level).
2. Aggregates per `user_id`: recency, total_trips, total_spend, avg_spend, avg_surge, total_tip, avg_tip, avg_rating_given, loyalty_status, city, avg_distance, avg_duration, active_days, etc.
3. Saves:
   - `data/processed_data/user_agg_df.csv`

**Outputs:**  
`user_agg_df.csv`.

**Why it exists:**  
Segmentation and churn models need one row per rider; this is the first rider-level dataset in the pipeline.

#### 4.3.2 — 02_Data Processing for Clustering Modelling.ipynb

**Purpose:**  
Prepare the rider-level data for **clustering**: handle outliers (e.g. Yeo-Johnson), encode categories, scale, and produce a numeric matrix.

**What it does:**

1. Reads `data/processed_data/user_agg_df.csv`.
2. Transforms numeric columns (e.g. Yeo-Johnson) and encodes categorical (e.g. city one-hot).
3. Saves the preprocessed matrix as:
   - `data/processed_data/data_preprocessed.csv`

**Outputs:**  
`data_preprocessed.csv`.

**Why it exists:**  
Clustering (e.g. K-Means) requires a single scaled/encoded numeric table; this notebook creates it.

#### 4.3.3 — 03_Clustering Model Development.ipynb

**Purpose:**  
Run **clustering** (e.g. K-Means) on the preprocessed matrix, choose number of clusters (e.g. silhouette, Davies–Bouldin), and optionally use PCA for visualization.

**What it does:**

1. Reads `data/processed_data/data_preprocessed.csv`.
2. Fits clustering (e.g. K-Means), evaluates cluster count, assigns cluster labels.
3. May attach cluster labels back to rider-level data for interpretation.

**Outputs:**  
Cluster assignments (and possibly saved objects). The next notebook (04) uses rider-level aggregates and builds RFMS on top of this logic or a similar schema.

**Why it exists:**  
To find natural rider groups that will later be refined or summarized by the RFMS framework.

#### 4.3.4 — 04_RFM_Analysis.ipynb

**Purpose:**  
Define the **RFMS** framework (Recency, Frequency, Monetary, Surge) and assign each rider to an **RFMS segment** used for targeting and churn modeling.

**What it does:**

1. Reads `data/processed_data/user_agg_df.csv`.
2. Defines R (e.g. days since last trip), F (e.g. total_trips), M (e.g. total_spend), S (e.g. avg_surge).
3. Computes scores/weights and assigns segments, e.g.:
   - At Risk  
   - Occasional Riders  
   - Core Loyal Riders  
   - High-Value Surge-Tolerant  
4. Saves a rider-level table with segment labels:
   - `data/processed_data/riders_trips_rfms.csv`

**Outputs:**  
`riders_trips_rfms.csv` (no churn label yet).

**Why it exists:**  
RFMS segments are the business-facing way to group riders and are **inputs** to the churn model and to the app’s exposure and recommendation logic.

---

### 4.4 Notebooks 03 — Customer Churn Prediction

**Folder:** `notebooks/03_Customer Churn Prediction/`

#### 4.4.1 — 01_Churn_Definition_&_Churn_EDA.ipynb

**Purpose:**  
Define **churn** (e.g. no trip in the last N days or similar rule) and add a binary **churned** label to the RFMS dataset.

**What it does:**

1. Reads `data/processed_data/riders_trips_rfms.csv`.
2. Applies a churn rule (e.g. recency > threshold → churned = 1).
3. Performs EDA on churn (rates by segment, city, etc.).
4. Saves the final modeling dataset:
   - `data/processed_data/riders_trips_rfms_churned.csv`

**Outputs:**  
`riders_trips_rfms_churned.csv`.

**Why it exists:**  
Churn prediction needs a single definition and one labeled dataset; this notebook creates it.

#### 4.4.2 — 02_Data Processing & Classification Model Development.ipynb

**Purpose:**  
Train **churn classification models** (e.g. Logistic Regression, Random Forest, XGBoost), tune and evaluate them, and compare with churn-appropriate metrics (e.g. precision-recall, ROC-AUC).

**What it does:**

1. Reads `data/processed_data/riders_trips_rfms_churned.csv`.
2. Defines feature set and target `churned`.
3. Splits train/test, handles class imbalance (e.g. SMOTE) if used.
4. Trains and evaluates multiple classifiers; selects a preferred model (e.g. Logistic Regression).
5. May save an initial model or pass the chosen config to the next notebook.

**Outputs:**  
Trained model(s) and evaluation results. The **production** model and preprocessor are saved in **03_SHAP Explainability**.

**Why it exists:**  
To choose and validate the classifier that will be deployed in the API.

#### 4.4.3 — 03_SHAP Explainability.ipynb

**Purpose:**  
Explain the chosen model with **SHAP**, define a **preprocessing pipeline** that matches the API, and **save** the preprocessor and model for production.

**What it does:**

1. Reads `data/processed_data/riders_trips_rfms_churned.csv` and drops columns not used as features (e.g. active_days, total_spend, avg_surge).
2. Defines **numeric** and **categorical** features; builds a **ColumnTransformer**:
   - Ordinal encoding for `loyalty_status` and `RFMS_segment` (fixed order).
   - One-hot for `city`.
   - Optional numeric scaling (e.g. RobustScaler).
3. Fits the preprocessor and the final model (e.g. Logistic Regression) on the same data.
4. Runs SHAP (e.g. TreeExplainer or KernelExplainer) for interpretability.
5. Saves to `model/` (relative to project or `output/webapp/`):
   - `preprocessor.joblib`
   - `lg_churn_model.joblib` (or `rf_churn_model.joblib`)
   - `lg_churn_model_metadata.joblib` (e.g. `business_threshold`, `feature_columns`)

**Outputs:**  
`preprocessor.joblib`, `*_churn_model.joblib`, `*_churn_model_metadata.joblib`.

**Why it exists:**  
The API must use the **exact** same features and preprocessing as training; this notebook is the single place that defines and saves that pipeline and the model the backend loads.

---

## 5. Web Application

The app lives under `output/webapp/`. The **frontend** is Streamlit; the **backend** is FastAPI. The frontend reads CSV data from `frontend/data/` and calls the backend for churn predictions.

---

### 5.1 Entry Point and Navigation

**File:** `output/webapp/frontend/Home.py`

**Purpose:**  
Set up the Streamlit app and **top navigation** for all pages.

**What it does:**

1. Sets page title “RideWise Dashboard” and wide layout.
2. Injects global **sidebar** and **background** styles (from `style.py`).
3. Defines the **navigation** list:
   - **Home** → `pages/0_Dashboard.py`
   - **Overview** → `pages/1_Overview.py`
   - **Demand & Revenue** → `pages/2_Demand_Revenue.py`
   - **Exposure Analysis** → `pages/4_Exposure_Analysis.py`
   - **Churn Predictor** → `pages/5_Churn_Predictor.py`
4. Uses `st.navigation(pages, position="top")` and `pg.run()` so the top bar switches between these pages.

**No page 3** in the list; numbering is intentional (e.g. legacy or reserved).

---

### 5.2 Shared Components and Styling

#### 5.2.1 — `frontend/style.py`

**Purpose:**  
Central place for **CSS** and **visual** behavior used across pages.

**What it does:**

- **`inject_background_style()`** — Sets app background (gradient or image from `frontend/assets/background.png`).
- **`inject_sidebar_style()`** — Injects a large block of CSS:
  - Sidebar nav link size and padding.
  - Caption and dataframe styling.
  - Reduced padding above title and around metric blocks.
  - Responsive behavior (e.g. smaller nav on narrow screens).
  - Churn Predictor–specific: metric cards, risk color classes (low/medium/high/critical), sidebar gradient, button style (e.g. JetBrains Mono, gradient buttons).

Pages that need the same look call `inject_sidebar_style()` and optionally `inject_background_style()`.

#### 5.2.2 — `frontend/data_loader.py`

**Purpose:**  
Load the two main **CSV datasets** used by the dashboard and cache them so repeated use doesn’t re-read from disk.

**What it does:**

- **`load_data()`**  
  - Reads `frontend/data/riders_trips.csv`.  
  - Parses `pickup_time` to datetime (UTC).  
  - Adds `pickup_year`, `pickup_month_num`, `pickup_month_name`.  
  - Returns the DataFrame.  
  - Cached with `@st.cache_data(show_spinner="Loading data...")`.

- **`load_data_segments()`**  
  - Reads `frontend/data/rfm_data.csv`.  
  - Drops column `rfm_score` if present.  
  - Returns the DataFrame (rider-level with segments, recency, monetary, etc.).

**Data location:**  
`DATA_DIR = Path(__file__).resolve().parent / "data"` → `output/webapp/frontend/data/`.

You must place (or copy) `riders_trips.csv` and `rfm_data.csv` there; they are not auto-generated by the app. Typically they are copies or derivatives of `data/processed_data/riders_trips.csv` and an RFMS/segment summary (e.g. from the segmentation notebooks).

---

#### 5.2.3 — `frontend/widgets/metric_card.py`

**Purpose:**  
Display a single **metric card** (title + value + optional delta) with consistent styling.

**What it does:**

- **`metric_card(title, value, delta=None, prefix="", suffix="")`**
  - Formats `value` (e.g. integers/floats with commas).
  - If `delta` is set, shows an up/down arrow and percentage in green/red.
  - Renders an HTML card (dark background, rounded border) and injects it with `st.markdown(..., unsafe_allow_html=True)`.

Used on Overview, Demand & Revenue, and Exposure Analysis for KPIs.

#### 5.2.4 — `frontend/widgets/date_card.py`

**Purpose:**  
Display a **date range** in the same card style as the metric cards.

**What it does:**

- **`date_card(value_min, value_max)`**
  - Renders a single card labeled “Date Range” with `value_max - value_min` (order as in code).
  - Used on Exposure Analysis to show the date range of “last activity” for at-risk customers.

---

### 5.3 Page-by-Page Behavior

#### 5.3.1 — Home — `pages/0_Dashboard.py`

**Purpose:**  
Landing page: short intro, project credit, and a **list of what each page does**.

**What it does:**

1. Applies sidebar and background styles.
2. Title: “Rideshare Executive Dashboard.”
3. Short text: project demonstrates end-to-end data science (analytics, modeling, explainability, deployment); developed by Godfrey Alexander Abban.
4. Lists the five areas: Overview, Demand Analysis, Revenue Analysis, Exposure Analysis, Churn Predictor, with one-line descriptions.
5. Info box: “Use the navigation bar above to move between pages.”
6. Calls `load_data()` so the dataset is loaded (and cached) when the user first lands; other pages then use the cache.

**Connection:**  
Entry point after opening the app; no filters or charts, only navigation and context.

---

#### 5.3.2 — Overview — `pages/1_Overview.py`

**Purpose:**  
Show **high-level KPIs** and **distributions** by loyalty tier and city.

**What it does:**

1. Loads trip-level data via `load_data()`.
2. **Sidebar filters:** City (All or one), Loyalty Tier (All or one). Filters the DataFrame for the rest of the page.
3. **Metrics row:** Three metric cards:
   - Total Users (hardcoded 10000 in current code; could be `df.user_id.nunique()`).
   - Total Trips (`trip_id.nunique()`).
   - Revenue (`total_fare_with_tip.sum()`).
4. **Charts:**
   - **Customer Segmentation** — Pie chart: share of users per `loyalty_status`.
   - **City Distribution** — Horizontal bar chart: user count per `city`.

**Data flow:**  
`load_data()` → filter by sidebar → aggregate for metrics and charts. Same `df` is used for both charts.

---

#### 5.3.3 — Demand & Revenue — `pages/2_Demand_Revenue.py`

**Purpose:**  
One page with **two tabs**: when rides happen (**Demand**) and when revenue is earned (**Revenue**), with shared filters and KPIs.

**What it does:**

1. Loads trip-level data via `load_data()`.
2. **Sidebar filters:** Year, Month, City (each “All” or single value). Builds `filtered_df` from `df`.
3. **Shared KPIs (above tabs):** Four metric cards — Total Users, Total Trips, Revenue (sum of `total_fare_with_tip`), Avg Fare.
4. **Tab “Demand Analysis”:**
   - Bar chart: trips by `pickup_hour` (hourly demand).
   - Line chart: daily trip count over time (by `pickup_time` date).
5. **Tab “Revenue Analysis”:**
   - Bar chart: revenue by `pickup_hour`.
   - Line chart: daily revenue over time.

**Data flow:**  
`load_data()` → `filtered_df` by year/month/city → same `filtered_df` for both tabs. Demand uses `trip_id` counts and dates; Revenue uses `total_fare` (and/or total_fare_with_tip depending on code).

---

#### 5.3.4 — Exposure Analysis — `pages/4_Exposure_Analysis.py`

**Purpose:**  
Answer: “How much **revenue is at risk** if we don’t re-engage customers who have been inactive for X days?” and “Which **segments** hold that revenue?”

**What it does:**

1. Loads **segment/rider-level** data via `load_data_segments()` (e.g. `rfm_data.csv`: user_id, recency, segments, monetary, last_trip_time, etc.).
2. **Sidebar:** Slider “Days since last activity” (e.g. 7–90, step 7). Defines “at risk” as `recency <= inactivity_threshold` (customers whose last activity was within that many days — interpretation may depend on how “recency” is defined in the CSV; often “days since last trip,” so lower recency = more recent = “at risk” if we consider them about to churn, or the logic may be inverted; the code uses `at_risk_customers = rfm[rfm['recency'] <= inactivity_threshold]`).
3. **Metrics:** Revenue at risk (sum of `monetary` for at-risk customers), Customer count exposed.
4. **Date card:** Min and max of `last_trip_time` among at-risk customers.
5. **Treemap:** Segments (e.g. `segments` column) with “Revenue Exposure” (sum of `monetary` per segment), with proportion. Color by revenue.
6. **Table:** DataFrame of at-risk customers (columns except `last_trip_time`) so users can see who to re-engage.

**Data flow:**  
`load_data_segments()` → filter by recency threshold → aggregate by segment for treemap and totals; same filtered list for the table.

---

#### 5.3.5 — Churn Predictor — `pages/5_Churn_Predictor.py`

**Purpose:**  
Let users get **churn probability**, **risk level**, and **recommendations** for **one rider** (form) or **many riders** (CSV upload), using the FastAPI backend.

**What it does:**

1. **API URL:** Uses `API_URL = os.getenv("API_URL", "http://localhost:8000")`.
2. **Sidebar:** Calls `check_api_health()` (GET `{API_URL}/health`). Shows “API ready” or an error (e.g. “Cannot reach API”, “Model not loaded”).
3. **Tabs:**
   - **Single Predict:**  
     Form with 11 inputs matching backend schema: recency, total_trips, avg_spend, total_tip, avg_tip, avg_rating_given, loyalty_status, city, avg_distance, avg_duration, RFMS_segment. On “Predict Churn Risk” submit, POSTs to `/predict`, gets back probability, label, threshold, risk_level, recommendation. Opens a **dialog** (`show_result_dialog`) with metrics and recommendation.
   - **Batch Predict:**  
     File upload (CSV). Checks for required columns (same 11). POSTs rows to `/predict/batch`, displays result table and a download button for predictions CSV.
   - **About:**  
     Short explanation of inputs (11 features), outputs (probability, risk level, label, recommendation), and that the backend runs the preprocessor + model.

**Data flow:**  
User input → POST to FastAPI → backend runs preprocessor + model → response → frontend shows result in dialog or table and allows download.

---

## 6. Backend API (Churn Prediction)

**Path:** `output/webapp/backend/`

The backend is a **FastAPI** app that loads the **preprocessor** and **churn model** saved by the **03_SHAP Explainability** notebook and exposes REST endpoints for health, info, single predict, and batch predict.

---

### 6.1 — `main.py`

**Purpose:**  
Define the API app, CORS, and routes.

**Endpoints:**

- **GET `/health`**  
  Returns `{ "status": "ok", "model_loaded": true/false }`. Used by the frontend to show “API ready” or not.

- **GET `/info`**  
  Returns version, threshold, feature count. Responds 503 if model is not loaded.

- **POST `/predict`**  
  Body: JSON object matching **ChurnFeatures** (see schema below). Returns **ChurnPredictionResponse**: churn_probability, churn_label, threshold, risk_level, recommendation.  
  - Calls `model_service.predict_label(features_dict)` → (label, proba).  
  - Calls `model_service.risk_level(proba, threshold, thr_mid)` → "Low Risk" / "Medium Risk" / "High Risk".  
  - Calls `model_service.recommendation(rfms_segment, risk_level)` → string.  
  - Returns all in the response. On error, 500 with detail.

- **POST `/predict/batch`**  
  Body: list of ChurnFeatures. For each item, runs predict_label and risk_level; returns `{ "predictions": [...], "count": N }`. No recommendation in the current batch response (only probability, label, threshold, risk_level).

---

### 6.2 — `schema.py`

**Purpose:**  
Define **request/response** shapes so the API and frontend agree on fields and types.

- **ChurnFeatures** (request):  
  recency, total_trips, avg_spend, total_tip, avg_tip, avg_rating_given (0–5), avg_distance, avg_duration (all numeric), plus loyalty_status, RFMS_segment, city (strings). Matches the 11 features used in 03_SHAP and the form on the Churn Predictor page.

- **ChurnPredictionResponse**:  
  churn_probability, churn_label, threshold, risk_level, recommendation (optional string).

---

### 6.3 — `model_loader.py`

**Purpose:**  
Load the **preprocessor**, **model**, and **metadata** at startup and expose a **ChurnModelService** that performs preprocessing and prediction.

**Paths (relative to backend):**  
`BASE_DIR = Path(__file__).resolve().parent.parent.parent` (i.e. `output/webapp/`). Then:

- `model/preprocessor.joblib`
- `model/lg_churn_model.joblib` (overrides earlier `rf_` paths in the same file)
- `model/lg_churn_model_metadata.joblib`

**ChurnModelService:**

- **Load:**  
  Loads preprocessor, model, metadata; applies a small **sklearn compatibility patch** for tree models (`_patch_tree_monotonic_cst`). Reads `business_threshold` and optional `thr_mid` from metadata; sets `feature_columns`.

- **predict_proba(features_dict):**  
  Builds a single-row DataFrame with columns in **RAW_FEATURE_ORDER** (recency, total_trips, avg_spend, total_tip, avg_tip, avg_rating_given, avg_distance, avg_duration, loyalty_status, RFMS_segment, city). Runs `preprocessor.transform`, then `model.predict_proba` on the transformed features; returns probability of class 1 (churn).

- **predict_label(features_dict):**  
  Returns `(label, proba)` where label = 1 if proba >= threshold else 0.

- **risk_level(proba, threshold, thr_mid):**  
  Returns "Low Risk" (< threshold), "Medium Risk" (threshold ≤ proba < thr_mid), "High Risk" (≥ thr_mid). (Code may also mention “Critical” in comments; the exact buckets are in the file.)

- **recommendation(rfms_segment, risk_level):**  
  **Business rules** (no ML): map segment + risk to a suggested action (e.g. “churn-prevention package for At Risk + High Risk”, “VIP win-back for Core Loyal + High Risk”, “engagement nudges for Occasional Riders + Low Risk”). Returns a string.

If model or preprocessor files are missing or loading fails, `model_service` is set to `None` and the API returns 503 on `/predict` and `/info`.

---

## 7. How the Pieces Connect

- **Notebooks** produce:
  - **Processed CSVs** in `data/processed_data/` (and optionally used/copied to `output/webapp/frontend/data/` for the app).
  - **Model artifacts** in `output/webapp/model/` from **03_SHAP Explainability** (preprocessor + model + metadata).

- **Frontend** uses:
  - **CSVs** in `frontend/data/` for Overview, Demand & Revenue, and Exposure (trip-level and segment-level).
  - **Backend** for Churn Predictor only (single and batch).

- **Backend** uses:
  - Only **model/** (preprocessor, model, metadata); no direct access to CSVs.

- **Page flow:**  
  User opens app → **Home** (0_Dashboard) → can go to **Overview** (1), **Demand & Revenue** (2), **Exposure** (4), or **Churn Predictor** (5). Overview and Demand & Revenue share the same trip-level data and filters (per page). Exposure uses segment-level data. Churn Predictor is the only page that talks to the API.

- **Recommendations:**  
  Generated in the **backend** from segment + risk level (business rules in `model_loader.recommendation`), not from the model itself. The model only outputs probability and label; the backend adds risk level and recommendation.

---

## 8. Running the Project

1. **Environment**  
   Python 3.x; install dependencies (e.g. from a `requirements.txt` in the repo or in `output/webapp/`).

2. **Data**  
   Run the notebooks in order (00 → 01 EDA → 02 Segmentation → 03 Churn) so that:
   - `data/processed_data/` contains the CSVs.
   - `output/webapp/model/` contains `preprocessor.joblib`, `lg_churn_model.joblib`, `lg_churn_model_metadata.joblib` (saved from 03_SHAP).
   - Copy or symlink (as needed) `riders_trips.csv` and `rfm_data.csv` into `output/webapp/frontend/data/` with the expected columns (see data_loader and Exposure page).

3. **Backend**  
   From `output/webapp/backend/`:  
   `uvicorn main:app --reload`  
   (or `backend.main:app` if running from project root.) Default port 8000.

4. **Frontend**  
   From `output/webapp/frontend/`:  
   `streamlit run Home.py`  
   Use the top navigation to open each page. Set `API_URL` if the backend is not at `http://localhost:8000`.

5. **Churn Predictor**  
   Ensure the backend is running and model files are present; otherwise the Churn Predictor page will show “Model not loaded” or “Cannot reach API.”

---

## 9. File and Folder Reference

| Path | Role |
|------|------|
| `data/` | Raw input CSVs (riders, trips, sessions, promotions, drivers). |
| `data/processed_data/` | All intermediate and final CSVs produced by notebooks. |
| `notebooks/00_Dataset_Exploration.ipynb` | Data audit; produces riders_trips (and optionally riders_trips_sessions). |
| `notebooks/01_EDA of Business/01_Feature_Engineering_for_EDA.ipynb` | Trip-level features → data_EDA.csv. |
| `notebooks/01_EDA of Business/02_EDA_for_Business_Context.ipynb` | Business EDA (no file output). |
| `notebooks/02_Customer Segmentation/01_Feature Engineering & EDA.ipynb` | Rider-level aggregates → user_agg_df.csv. |
| `notebooks/02_Customer Segmentation/02_Data Processing for Clustering Modelling.ipynb` | Preprocessing for clustering → data_preprocessed.csv. |
| `notebooks/02_Customer Segmentation/03_Clustering Model Development.ipynb` | Clustering (e.g. K-Means). |
| `notebooks/02_Customer Segmentation/04_RFM_Analysis.ipynb` | RFMS segments → riders_trips_rfms.csv. |
| `notebooks/03_Customer Churn Prediction/01_Churn_Definition_&_Churn_EDA.ipynb` | Churn label → riders_trips_rfms_churned.csv. |
| `notebooks/03_Customer Churn Prediction/02_Data Processing & Classification Model Development.ipynb` | Train/evaluate churn classifiers. |
| `notebooks/03_Customer Churn Prediction/03_SHAP Explainability.ipynb` | SHAP + save preprocessor & model to model/. |
| `output/webapp/frontend/Home.py` | Streamlit entry; defines navigation. |
| `output/webapp/frontend/style.py` | Global CSS and styling. |
| `output/webapp/frontend/data_loader.py` | Load riders_trips.csv and rfm_data.csv from frontend/data/. |
| `output/webapp/frontend/widgets/metric_card.py` | KPI card component. |
| `output/webapp/frontend/widgets/date_card.py` | Date range card component. |
| `output/webapp/frontend/pages/0_Dashboard.py` | Home page. |
| `output/webapp/frontend/pages/1_Overview.py` | Overview KPIs and loyalty/city charts. |
| `output/webapp/frontend/pages/2_Demand_Revenue.py` | Demand and Revenue tabs. |
| `output/webapp/frontend/pages/4_Exposure_Analysis.py` | Revenue at risk and segments. |
| `output/webapp/frontend/pages/5_Churn_Predictor.py` | Single/batch churn prediction UI. |
| `output/webapp/frontend/data/` | riders_trips.csv, rfm_data.csv for the app. |
| `output/webapp/backend/main.py` | FastAPI app and routes. |
| `output/webapp/backend/schema.py` | ChurnFeatures and ChurnPredictionResponse. |
| `output/webapp/backend/model_loader.py` | Load model/preprocessor; predict and recommend. |
| `output/webapp/model/` | preprocessor.joblib, lg_churn_model.joblib, lg_churn_model_metadata.joblib. |

---

*This documentation reflects the project structure and behavior as implemented. For step-by-step user instructions on the dashboard only, see `output/webapp/frontend/Read Me.md`.*
