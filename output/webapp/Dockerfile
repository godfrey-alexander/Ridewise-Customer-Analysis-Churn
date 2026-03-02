# RideWise webapp: single image for both API and frontend.
# Run API (default): docker run -p 8000:8000 ...
# Run frontend: override CMD, e.g. streamlit run frontend/Home.py --server.port 8501 ...
# Build context must be the webapp directory (contains backend/, frontend/, requirements.txt).
# For API: include model/ with lg_churn_model.joblib, lg_churn_model_metadata.joblib, preprocessor.joblib.
# For frontend: include frontend/data/ with riders_trips.csv and rfm_data.csv for dashboard pages.
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 8000 8501

# Default: run FastAPI (churn prediction). Use PORT=8000 or override.
# For Streamlit frontend, override CMD with: streamlit run frontend/Home.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
