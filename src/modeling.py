from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .features import FeatureSpec, build_preprocessor


def _evaluate(y_true: np.ndarray, y_prob: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "classification_report": classification_report(y_true, y_pred, zero_division=0),
    }


def train_and_score(df: pd.DataFrame, random_state: int = 42) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    spec = FeatureSpec()
    assert spec.target in df.columns, "Target column Churn not found"

    y = df[spec.target].astype(int).values

    drop_cols = [c for c in ["CustomerID", spec.target] if c in df.columns]
    X = df.drop(columns=drop_cols)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )

    preprocessor = build_preprocessor(df)

    # Baseline model: Logistic Regression
    lr = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", LogisticRegression(max_iter=2000)),
        ]
    )

    lr.fit(X_train, y_train)
    lr_prob = lr.predict_proba(X_test)[:, 1]
    lr_pred = (lr_prob >= 0.5).astype(int)
    lr_metrics = _evaluate(y_test, lr_prob, lr_pred)

    # Stronger model: Random Forest
    rf = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", RandomForestClassifier(n_estimators=300, random_state=random_state)),
        ]
    )
    rf.fit(X_train, y_train)
    rf_prob = rf.predict_proba(X_test)[:, 1]
    rf_pred = (rf_prob >= 0.5).astype(int)
    rf_metrics = _evaluate(y_test, rf_prob, rf_pred)

    # Choose best by ROC-AUC
    best_name, best_pipe = (
        ("random_forest", rf) if rf_metrics["roc_auc"] >= lr_metrics["roc_auc"] else ("logistic_regression", lr)
    )

    # Score full dataset for dashboard export
    full_prob = best_pipe.predict_proba(X)[:, 1]

    scored = df.copy()
    scored["churn_probability"] = full_prob
    scored["risk_band"] = pd.cut(
        scored["churn_probability"],
        bins=[-0.01, 0.33, 0.66, 1.01],
        labels=["Green", "Amber", "Red"],
    )

    metrics = {
        "best_model": best_name,
        "logistic_regression": lr_metrics,
        "random_forest": rf_metrics,
    }

    return scored, metrics
