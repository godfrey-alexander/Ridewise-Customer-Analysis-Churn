"""Load and serve the churn prediction model using preprocessor + model from 03_SHAP Explainability."""
import joblib
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "model" / "rf_churn_model.joblib"
METADATA_PATH = BASE_DIR / "model" / "rf_churn_model_metadata.joblib"
PREPROCESSOR_PATH = BASE_DIR / "model" / "preprocessor.joblib"

MODEL_PATH = BASE_DIR / "model" / "lg_churn_model.joblib"
METADATA_PATH = BASE_DIR / "model" / "lg_churn_model_metadata.joblib"


def _patch_tree_monotonic_cst(estimator):
    """Add monotonic_cst if missing (sklearn version compatibility: model saved with older sklearn)."""
    if hasattr(estimator, "estimators_"):
        for est in estimator.estimators_:
            _patch_tree_monotonic_cst(est)
    if not hasattr(estimator, "monotonic_cst"):
        try:
            estimator.monotonic_cst = None
        except (AttributeError, TypeError):
            pass



# Column order for raw features (must match 03_SHAP X before transform)
RAW_FEATURE_ORDER = [
    "recency",
    "total_trips",
    "avg_spend",
    "total_tip",
    "avg_tip",
    "avg_rating_given",
    "avg_distance",
    "avg_duration",
    "loyalty_status",
    "RFMS_segment",
    "city",
]

# NUMERIC_RAW = {
#     "recency", "total_trips", "avg_spend", "total_tip", "avg_tip",
#     "avg_rating_given", "avg_distance", "avg_duration",
# }


class ChurnModelService:
    def __init__(self):
        self._loaded = False
        self.model = None
        self.preprocessor = None
        self.metadata = None
        self.threshold = 0.5
        self.feature_columns = []
        self.thr_mid = 0.65

        if not MODEL_PATH.exists() or not METADATA_PATH.exists():
            raise FileNotFoundError(
                f"Model files not found. Expected: {MODEL_PATH}, {METADATA_PATH}"
            )
        if not PREPROCESSOR_PATH.exists():
            raise FileNotFoundError(
                f"Preprocessor not found. Save it from 03_SHAP Explainability to {PREPROCESSOR_PATH}"
            )
        try:
            self.model = joblib.load(MODEL_PATH)
            _patch_tree_monotonic_cst(self.model)
            # Patch for sklearn DecisionTree/RandomForest models missing monotonic_cst
            self.metadata = joblib.load(METADATA_PATH)
            self.preprocessor = joblib.load(PREPROCESSOR_PATH)
            self.threshold = self.metadata.get("business_threshold", 0.35)
            self.feature_columns = self.metadata.get("feature_columns", [])
        except Exception as e:
            raise RuntimeError(f"Failed to load model or preprocessor: {e}")
        self._loaded = True

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def predict_proba(self, features_dict: dict) -> float:
        row = [features_dict[k] for k in RAW_FEATURE_ORDER]
        X = pd.DataFrame([row], columns=RAW_FEATURE_ORDER)
        # Ensure numeric columns are float (preprocessor/scaler expect numeric dtypes)
        # for c in NUMERIC_RAW:
        #     X[c] = pd.to_numeric(X[c], errors="coerce").astype(float)
        X_t = self.preprocessor.transform(X)

        # Retrieve the new column names
        column_names = self.preprocessor.get_feature_names_out()

        # Reconstruct the DataFrame
        transformed_data = pd.DataFrame(X_t, columns=column_names)
        try:
            proba = self.model.predict_proba(transformed_data)[:, 1]

            print(f'probability: {proba}')
        except ValueError as e:
            if "features" in str(e).lower() or "shape" in str(e).lower():
                n_out = X_t.shape[1] if hasattr(X_t, "shape") else "?"
                n_exp = len(self.feature_columns)
                raise ValueError(
                    f"Preprocessor output has {n_out} features but model expects {n_exp}. "
                    "In 03_SHAP Explainability, uncomment the numeric branch in the ColumnTransformer "
                    '("num", numeric_transformer, numeric_features), then re-fit and save the preprocessor.'
                ) from e
            raise
        return float(proba)

    def predict_label(self, features_dict: dict) -> tuple[int, float]:
        proba = self.predict_proba(features_dict)
        label = int(proba >= self.threshold)
        return label, proba

    def risk_level(self, proba: float, threshold: float, thr_mid: float = 0.65) -> str:
        if proba < threshold:
            return "Low Risk"
        if proba < thr_mid:
            return "Medium Risk"
        else:
            return "High Risk"


    def recommendation(self, rfms_segment: str, risk_level: str) -> str:
        """
        Business rule mapping: RFMS segment × churn risk → recommended action.
        This is NOT machine learning; it's decision logic based on your project strategy.
        """

        if risk_level == "High Risk":
            if rfms_segment == "At Risk":
                return "Highest priority: churn-prevention package (credits + surge relief + service recovery)"
            if rfms_segment == "Core Loyal Riders":
                return "VIP win-back: targeted credit + service recovery + feedback request"
            if rfms_segment == "Occasional Riders":
                return "Reactivation: limited-time discount + convenience messaging"
            if rfms_segment == "High-Value Surge-Tolerant":
                return "White-glove retention: personalized outreach + priority support"

        if risk_level == "Medium Risk":
            if rfms_segment == "At Risk":
                return "Targeted off-peak discount + education on saving/avoiding surge"
            if rfms_segment == "Core Loyal Riders":
                return "Reinforce loyalty: bonus points + gentle reminder"
            if rfms_segment == "Occasional Riders":
                return "Activation: time-limited offer for next ride"
            if rfms_segment == "High-Value Surge-Tolerant":
                return "Recognition: perks (no discounts) + premium experience"

        # Low Risk
        if rfms_segment == "High-Value Surge-Tolerant":
            return "Reward/recognition (no discounts): perks, priority support, surprise upgrades"
        if rfms_segment == "Core Loyal Riders":
            return "Maintain loyalty: points boosts, referrals, cross-sell bundles"
        if rfms_segment == "Occasional Riders":
            return "Engagement nudges: seasonal campaigns, feature prompts"
        if rfms_segment == "At Risk":
            return "Monitor: low-cost reminders + reduce friction (payments/app UX)"

        return "No action rule defined"

try:
    model_service = ChurnModelService()
except (FileNotFoundError, RuntimeError):
    model_service = None
