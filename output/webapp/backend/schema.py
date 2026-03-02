"""Pydantic schemas for churn prediction.

When the preprocessor from 03_SHAP Explainability is loaded, the API accepts raw features
(identical to notebook X columns): numerics plus loyalty_status, city, RFMS_segment as strings.
"""
from pydantic import BaseModel, Field


class ChurnFeatures(BaseModel):
    """Raw features matching 02 model training data."""
    recency: float = Field(ge=0, description="Recency (e.g. days since last trip)")
    total_trips: float = Field(ge=0, description="Total number of trips")
    avg_spend: float = Field(ge=0, description="Average spend per trip")
    total_tip: float = Field(ge=0, description="Total tips given")
    avg_tip: float = Field(ge=0, description="Average tip per trip")
    avg_rating_given: float = Field(ge=0, le=5, description="Average rating given (0-5)")
    avg_distance: float = Field(ge=0, description="Average trip distance")
    avg_duration: float = Field(ge=0, description="Average trip duration")
    loyalty_status: str = Field(description="Bronze | Silver | Gold | Platinum")
    RFMS_segment: str = Field(description="At Risk | Occasional Riders | Core Loyal Riders | High-Value Surge-Tolerant")
    city: str = Field(description="Cairo | Lagos | Nairobi")



class ChurnPredictionResponse(BaseModel):
    churn_probability: float
    churn_label: int
    threshold: float
    risk_level: str  # Low, Medium, High, Critical
    recommendation: str = ""  # Suggested action based on segment and risk
