"""Pydantic schemas aligned with model feature columns from 05_Model_Building.ipynb."""
from pydantic import BaseModel, Field
from typing import Optional


# Model expects these 19 features (16 numeric + 3 categorical) in this order:
# total_trips, total_spent, avg_fare, total_tip, avg_tip, avg_surge,
# weekend_trip_ratio, peak_hour_trip_ratio, total_sessions, total_time_on_app,
# avg_time_on_app, total_pages_visited, avg_pages_visited, conversion_rate,
# RFMS_weighted_score, RFMS_segment, city, loyalty_status, age
class ChurnFeatures(BaseModel):
    total_trips: int = Field(ge=0, description="Total number of trips")
    total_spent: float = Field(ge=0, description="Total amount spent")
    avg_fare: float = Field(ge=0, description="Average fare per trip")
    total_tip: float = Field(ge=0, description="Total tips given")
    avg_tip: float = Field(ge=0, description="Average tip per trip")
    avg_surge: float = Field(ge=0, description="Average surge multiplier")
    weekend_trip_ratio: float = Field(ge=0, le=1, description="Ratio of trips on weekends")
    peak_hour_trip_ratio: float = Field(ge=0, le=1, description="Ratio of trips in peak hours")
    total_sessions: float = Field(ge=0, description="Total app sessions")
    total_time_on_app: float = Field(ge=0, description="Total time on app (minutes)")
    avg_time_on_app: float = Field(ge=0, description="Average time per session (minutes)")
    total_pages_visited: float = Field(ge=0, description="Total pages visited in app")
    avg_pages_visited: float = Field(ge=0, description="Average pages per session")
    conversion_rate: float = Field(ge=0, le=1, description="Session to trip conversion rate")
    RFMS_weighted_score: float = Field(ge=0, description="RFMS weighted engagement score")
    RFMS_segment: str = Field(description="RFMS customer segment")
    city: str = Field(description="Primary city")
    loyalty_status: str = Field(description="Loyalty tier")
    age: float = Field(ge=18, le=100, description="Rider age")


class ChurnPredictionResponse(BaseModel):
    churn_probability: float
    churn_label: int
    threshold: float
    risk_level: str  # Low, Medium, High, Critical
