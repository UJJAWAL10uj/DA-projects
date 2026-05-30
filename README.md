# Revenue & Retention Growth Strategy Dashboard (E-Commerce Churn)

This repo contains an end-to-end, resume-ready analytics project aligned to:

> Built Excel & SQL dashboards modelling revenue drivers, retention cohorts & churn risk for a fintech platform; identified 3 growth levers.

**Dataset note:** the public dataset used here is an *e-commerce* churn dataset (Kaggle). The analytics framework (cohorting, churn-risk scoring, growth lever simulation) is directly transferable to fintech subscription / payments products.

## What’s included

### Data
- Raw CSVs (Kaggle export)
  - `data/raw/E Commerce Dataset tab2.csv` (customer-level dataset)
  - `data/raw/E Commerce Dataset tab1.csv` (data dictionary)
- Processed outputs (generated)
  - `data/processed/ecomm_clean.csv`
  - `data/processed/churn_risk_scored.csv`
  - `data/processed/model_metrics.json`

### SQL (dashboard queries)
- `sql/01_schema.sql` (SQLite-friendly table schema + import notes)
- `sql/02_dashboard_queries.sql`
  - KPI summary
  - Driver cuts (complaints, payment mode, device)
  - Cohort-style retention matrix (Tenure band × Recency band)
  - Churn risk list (RAG)

### Python
- `src/` — modular pipeline (clean → model → score)
- `notebooks/01_eda_modeling.py` — one-command EDA + modeling script that also exports charts and scored customers.

### Power BI
- `powerbi/dashboard_spec.md` — exact visuals + DAX + field mapping.

## Quickstart (Windows)

```bat
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m src.run_pipeline --input "data/raw/E Commerce Dataset tab2.csv" --outdir data/processed
```

## Run EDA + charts

```bat
python notebooks\01_eda_modeling.py
```

Outputs:
- `reports/retention_analysis.png`
- `data/processed/churn_risk_scored.csv`


