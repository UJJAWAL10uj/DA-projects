from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .cleaning import clean_ecomm_df
from .modeling import train_and_score


def main() -> None:
    parser = argparse.ArgumentParser(description="Run churn cleaning + modeling pipeline")
    parser.add_argument("--input", required=True, help="Path to raw CSV")
    parser.add_argument("--outdir", required=True, help="Output directory")
    args = parser.parse_args()

    in_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df_raw = pd.read_csv(in_path)
    df_clean = clean_ecomm_df(df_raw)

    clean_path = outdir / "ecomm_clean.csv"
    df_clean.to_csv(clean_path, index=False)

    scored_df, metrics = train_and_score(df_clean)

    scored_path = outdir / "churn_risk_scored.csv"
    scored_df.to_csv(scored_path, index=False)

    metrics_path = outdir / "model_metrics.json"
    metrics_path.write_text(pd.Series(metrics).to_json(indent=2))

    print(f"Wrote cleaned data: {clean_path}")
    print(f"Wrote scored churn risk: {scored_path}")
    print(f"Wrote model metrics: {metrics_path}")


if __name__ == "__main__":
    main()
