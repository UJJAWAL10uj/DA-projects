from __future__ import annotations

import re

import pandas as pd


def _norm_text(x: str) -> str:
    x = x.strip()
    x = re.sub(r"\s+", " ", x)
    return x


def standardize_categories(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # PreferredPaymentMode normalizations
    if "PreferredPaymentMode" in df.columns:
        pm = df["PreferredPaymentMode"].astype("string")
        pm = pm.fillna(pd.NA)

        mapping = {
            "CC": "Credit Card",
            "COD": "Cash on Delivery",
            "Cash on Delivery": "Cash on Delivery",
            "Debit Card": "Debit Card",
            "Credit Card": "Credit Card",
            "UPI": "UPI",
            "E wallet": "E wallet",
        }

        pm = pm.apply(lambda v: _norm_text(str(v)) if pd.notna(v) else v)
        pm = pm.replace(mapping)
        df["PreferredPaymentMode"] = pm

    # PreferredLoginDevice normalizations
    if "PreferredLoginDevice" in df.columns:
        dev = df["PreferredLoginDevice"].astype("string")
        dev = dev.apply(lambda v: _norm_text(str(v)) if pd.notna(v) else v)
        dev = dev.replace({"Phone": "Mobile Phone"})
        df["PreferredLoginDevice"] = dev

    return df


def clean_ecomm_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Column name sanity
    df.columns = [c.strip() for c in df.columns]

    # Convert churn to 0/1 int
    if "Churn" in df.columns:
        df["Churn"] = pd.to_numeric(df["Churn"], errors="coerce").fillna(0).astype(int)

    # Standardize categories
    df = standardize_categories(df)

    # Numeric columns (coerce)
    numeric_cols = [
        "Tenure",
        "CityTier",
        "WarehouseToHome",
        "HourSpendOnApp",
        "NumberOfDeviceRegistered",
        "SatisfactionScore",
        "NumberOfAddress",
        "Complain",
        "OrderAmountHikeFromlastYear",
        "CouponUsed",
        "OrderCount",
        "DaySinceLastOrder",
        "CashbackAmount",
    ]

    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Impute numeric missing with median
    for c in numeric_cols:
        if c in df.columns:
            med = df[c].median()
            df[c] = df[c].fillna(med)

    # Impute categorical missing with mode
    cat_cols = [
        "PreferredLoginDevice",
        "PreferredPaymentMode",
        "Gender",
        "PreferedOrderCat",
        "MaritalStatus",
    ]
    for c in cat_cols:
        if c in df.columns:
            mode = df[c].mode(dropna=True)
            fill = mode.iloc[0] if len(mode) else "Unknown"
            df[c] = df[c].fillna(fill)

    return df
