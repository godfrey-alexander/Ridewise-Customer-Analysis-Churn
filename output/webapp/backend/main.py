"""RideWise Churn Prediction API - FastAPI backend."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schema import ChurnFeatures, ChurnPredictionResponse
from .model_loader import model_service

app = FastAPI(
    title="RideWise Churn Prediction API",
    description="ML-powered customer churn prediction for RideWise ride-sharing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health check for load balancers and monitoring."""
    return {
        "status": "ok",
        "model_loaded": model_service is not None,
    }


@app.get("/info")
def info():
    """API and model info."""
    if model_service is None:
        raise HTTPException(503, "Model not loaded. Train and save the model first.")
    return {
        "version": "1.0.0",
        "threshold": model_service.threshold,
        "feature_count": len(model_service.feature_columns),
    }


@app.post("/predict", response_model=ChurnPredictionResponse)
def predict_churn(features: ChurnFeatures):
    """Predict churn probability and label for a single rider."""
    if model_service is None:
        raise HTTPException(503, "Model not loaded. Train and save the model first.")
    try:
        features_dict = features.model_dump()
        label, proba = model_service.predict_label(features_dict)
        risk = model_service.risk_level(proba)
        print(f"Churn probability: {proba}, \n Churn label: {label}, \n Risk level: {risk}")
        return ChurnPredictionResponse(
            churn_probability=proba,
            churn_label=label,
            threshold=model_service.threshold,
            risk_level=risk,
        )
    except Exception as e:
        raise HTTPException(500, detail=f"Prediction failed: {type(e).__name__}: {e}")


@app.post("/predict/batch")
def predict_batch(features_list: list[ChurnFeatures]):
    """Batch predict churn for multiple riders."""
    if model_service is None:
        raise HTTPException(503, "Model not loaded. Train and save the model first.")
    results = []
    for f in features_list:
        d = f.model_dump()
        label, proba = model_service.predict_label(d)
        risk = model_service.risk_level(proba)
        results.append({
            "churn_probability": proba,
            "churn_label": label,
            "threshold": model_service.threshold,
            "risk_level": risk,
        })
    return {"predictions": results, "count": len(results)}
