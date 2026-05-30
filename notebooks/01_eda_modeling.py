import os

import matplotlib.pyplot as plt
import pandas as pd

from src.cleaning import clean_ecomm_df
from src.modeling import train_and_score

RAW_PATH = "data/raw/E Commerce Dataset tab2.csv"


def main() -> None:
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    df_raw = pd.read_csv(RAW_PATH)
    df = clean_ecomm_df(df_raw)

    print(f"Total customers: {len(df):,}")
    print(f"Overall churn rate: {df['Churn'].mean():.1%}")
    print(f"Average tenure (months): {df['Tenure'].mean():.1f}")

    # Simple churn by complaint plot
    churn_by_complain = df.groupby("Complain")["Churn"].mean().reset_index()

    plt.figure(figsize=(6, 4))
    plt.bar(churn_by_complain["Complain"].astype(str), churn_by_complain["Churn"], color=["#2ca02c", "#d62728"])
    plt.title("Churn Rate by Complaint Flag")
    plt.xlabel("Complain (0=No, 1=Yes)")
    plt.ylabel("Churn Rate")
    plt.tight_layout()
    plt.savefig("reports/churn_by_complain.png", dpi=150)

    # Model + scoring
    scored_df, metrics = train_and_score(df)

    df.to_csv("data/processed/ecomm_clean.csv", index=False)
    scored_df.to_csv("data/processed/churn_risk_scored.csv", index=False)

    (pd.Series(metrics).to_json(indent=2))
    with open("data/processed/model_metrics.json", "w", encoding="utf-8") as f:
        f.write(pd.Series(metrics).to_json(indent=2))

    print("Best model:", metrics["best_model"])
    print("LogReg ROC-AUC:", metrics["logistic_regression"]["roc_auc"])
    print("RF ROC-AUC:", metrics["random_forest"]["roc_auc"])


if __name__ == "__main__":
    main()
