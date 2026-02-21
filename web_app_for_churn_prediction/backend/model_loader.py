"""Load and serve the churn prediction model with graceful fallback."""
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "churn_model_pipeline.joblib"
METADATA_PATH = BASE_DIR / "model" / "churn_model_metadata.joblib"


class ChurnModelService:
    def __init__(self):
        self._loaded = False
        self.pipeline = None
        self.metadata = None
        self.threshold = 0.5
        self.feature_columns = []

        if MODEL_PATH.exists() and METADATA_PATH.exists():
            try:
                self.pipeline = joblib.load(MODEL_PATH)
                self.metadata = joblib.load(METADATA_PATH)
                self.threshold = self.metadata.get("business_threshold", 0.5)
                self.feature_columns = self.metadata.get("feature_columns", [])
            except Exception as e:
                raise RuntimeError(f"Failed to load model: {e}")
            self._loaded = True
        else:
            raise FileNotFoundError(
                f"Model files not found. Run notebooks/05_Model_Building.ipynb to train and save the model. "
                f"Expected: {MODEL_PATH} and {METADATA_PATH}"
            )

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def predict_proba(self, features_dict: dict) -> float:
        import pandas as pd
        X = pd.DataFrame([features_dict], columns=self.feature_columns)
        proba = self.pipeline.predict_proba(X)[0, 1]
        return float(proba)

    def predict_label(self, features_dict: dict) -> tuple[int, float]:
        proba = self.predict_proba(features_dict)
        label = int(proba >= self.threshold)
        return label, proba

    def risk_level(self, proba: float) -> str:
        if proba < 0.25:
            return "Low"
        if proba < 0.5:
            return "Medium"
        if proba < 0.75:
            return "High"
        return "Critical"


try:
    model_service = ChurnModelService()
except (FileNotFoundError, RuntimeError):
    model_service = None
