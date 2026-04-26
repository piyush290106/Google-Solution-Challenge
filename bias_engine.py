from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


@dataclass
class FairnessResult:
    sensitive_attribute: str
    target_column: str
    positive_label: Any
    total_rows: int
    group_metrics: List[Dict[str, Any]]
    demographic_parity_difference: float
    disparate_impact_ratio: Optional[float]
    risk_level: str
    summary: str
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensitive_attribute": self.sensitive_attribute,
            "target_column": self.target_column,
            "positive_label": self.positive_label,
            "total_rows": self.total_rows,
            "group_metrics": self.group_metrics,
            "demographic_parity_difference": round(self.demographic_parity_difference, 4),
            "disparate_impact_ratio": None if self.disparate_impact_ratio is None else round(self.disparate_impact_ratio, 4),
            "risk_level": self.risk_level,
            "summary": self.summary,
            "recommendations": self.recommendations,
        }


def _infer_positive_label(series: pd.Series) -> Any:
    """Infer the favorable/positive decision label from common binary formats."""
    non_null = series.dropna()
    unique_values = list(non_null.unique())

    if len(unique_values) == 0:
        raise ValueError("Target column has no valid values.")

    normalized = {str(v).strip().lower(): v for v in unique_values}
    preferred = [
        "1", "yes", "true", "approved", "approve", "selected", "shortlisted",
        "hired", "pass", "accepted", "eligible", "positive"
    ]
    for key in preferred:
        if key in normalized:
            return normalized[key]

    if pd.api.types.is_numeric_dtype(non_null):
        return non_null.max()

    # fallback: choose the most common class as favorable for prototype use
    return non_null.value_counts().idxmax()


def analyze_fairness(df: pd.DataFrame, sensitive_attribute: str, target_column: str, positive_label: Optional[Any] = None) -> FairnessResult:
    if sensitive_attribute not in df.columns:
        raise ValueError(f"Sensitive attribute '{sensitive_attribute}' not found in dataset.")
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")
    if len(df) == 0:
        raise ValueError("Dataset is empty.")

    working = df[[sensitive_attribute, target_column]].dropna().copy()
    if len(working) == 0:
        raise ValueError("Selected columns do not contain usable rows after removing missing values.")

    if positive_label is None or positive_label == "":
        positive_label = _infer_positive_label(working[target_column])

    working["_positive"] = working[target_column].astype(str) == str(positive_label)

    group_metrics: List[Dict[str, Any]] = []
    for group_name, group_df in working.groupby(sensitive_attribute, dropna=False):
        total = int(len(group_df))
        positives = int(group_df["_positive"].sum())
        rate = float(positives / total) if total else 0.0
        group_metrics.append({
            "group": str(group_name),
            "total": total,
            "positive_count": positives,
            "selection_rate": round(rate, 4),
        })

    rates = [g["selection_rate"] for g in group_metrics]
    max_rate = max(rates)
    min_rate = min(rates)
    demographic_parity_difference = float(max_rate - min_rate)
    disparate_impact_ratio = None if max_rate == 0 else float(min_rate / max_rate)

    if demographic_parity_difference >= 0.25 or (disparate_impact_ratio is not None and disparate_impact_ratio < 0.6):
        risk_level = "High"
    elif demographic_parity_difference >= 0.10 or (disparate_impact_ratio is not None and disparate_impact_ratio < 0.8):
        risk_level = "Medium"
    else:
        risk_level = "Low"

    worst_group = min(group_metrics, key=lambda x: x["selection_rate"])
    best_group = max(group_metrics, key=lambda x: x["selection_rate"])

    summary = (
        f"FairAI found a {risk_level.lower()} fairness risk. "
        f"The highest selection rate is {best_group['selection_rate']:.2%} for {best_group['group']}, "
        f"while the lowest is {worst_group['selection_rate']:.2%} for {worst_group['group']}."
    )

    recommendations = [
        "Review whether the sensitive attribute is directly or indirectly influencing the decision outcome.",
        "Balance under-represented groups in training data before model training.",
        "Use fairness-aware model evaluation before deploying the decision system.",
        "Add human review for high-impact decisions such as hiring, lending, and education selection.",
    ]

    return FairnessResult(
        sensitive_attribute=sensitive_attribute,
        target_column=target_column,
        positive_label=positive_label,
        total_rows=int(len(working)),
        group_metrics=group_metrics,
        demographic_parity_difference=demographic_parity_difference,
        disparate_impact_ratio=disparate_impact_ratio,
        risk_level=risk_level,
        summary=summary,
        recommendations=recommendations,
    )
