"""Load and serve the churn prediction model using preprocessor + model from 03_SHAP Explainability."""
import joblib
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent


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

MODEL_PATH = BASE_DIR / "model" / "rfm_churn_model.joblib"
METADATA_PATH = BASE_DIR / "model" / "rfm_churn_model_metadata.joblib"
PREPROCESSOR_PATH = BASE_DIR / "model" / "preprocessor.joblib"

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
        print(f"transformed_X: \n{transformed_data}")
        try:
            proba = self.model.predict_proba(transformed_data)[:, 1]
            # the result of this is showing a probability of 2.2488945 where as the notebook is showing [0.08]
            # this is causing the prediction to be 224% which is not correct
            # we need to fix this by ensuring the probability is in the range of 0-1
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
