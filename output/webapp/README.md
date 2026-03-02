# RideWise Churn Prediction Web App

Professional ML-powered customer churn prediction for RideWise ride-sharing., built from the `05_Model_Building` notebook.

## Architecture

- **Backend**: FastAPI (REST API)
- **Frontend**: Streamlit (dashboard UI)
- **Model**: Logistic Regression pipeline with RobustScaler + OneHotEncoder (from notebook)

## Setup

### 1. Train the Model

Run the notebook to train and save the model:

```bash
# From project root
jupyter notebook notebooks/05_Model_Building.ipynb
```

Execute all cells. The notebook saves to `web_app_for_churn_prediction/model/`:
- `churn_model_pipeline.joblib`
- `churn_model_metadata.joblib`

### 2. Install Dependencies

```bash
cd web_app_for_churn_prediction
pip install -r requirements.txt
```

### 3. Run Locally

**Terminal 1 – API:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 – Frontend:**
```bash
streamlit run frontend/app.py --server.port 8501
```

Then open http://localhost:8501

### 4. Docker (Optional)

```bash
# API
docker build -t ridewise-api . && docker run -p 8000:8000 ridewise-api

# Frontend (set API_URL to your API host)
docker run -p 8501:8501 -e API_URL=http://host.docker.internal:8000 ridewise-frontend
```

## Deployment (Render)

1. Connect the repo to Render.
2. `render.yaml` defines two services: `ridewise-churn-api` and `ridewise-churn-frontend`.
3. After first deploy, set `API_URL` on the frontend service to the API URL (e.g. `https://ridewise-churn-api.onrender.com`).

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /info | Model info |
| POST | /predict | Single prediction |
| POST | /predict/batch | Batch predictions |

## Features (19 total)

- **Numeric**: total_trips, total_spent, avg_fare, total_tip, avg_tip, avg_surge, weekend_trip_ratio, peak_hour_trip_ratio, total_sessions, total_time_on_app, avg_time_on_app, total_pages_visited, avg_pages_visited, conversion_rate, RFMS_weighted_score, age
- **Categorical**: RFMS_segment, city, loyalty_status
