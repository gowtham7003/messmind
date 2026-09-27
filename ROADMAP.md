## The 14-day build

| Day | Deliverable | Acceptance check | Status |
|---|---|---|---|
| 1 | Meal ledger, local storage, overview and synthetic demo | Save valid meals; reject duplicates and impossible values; keep demo isolated; test weighted metrics | Complete |
| 2 | Correct and delete meal records | Explicit edit/delete flow; cancel leaves data unchanged; validation still applies; database backup before destructive edits | Planned |
| 3 | CSV import and export | Download a template; preview and validate every row before writing; report duplicates; escape spreadsheet formulas on export | Planned |
| 4 | First demand forecast | Use past records only; rolling-mean and weekday baselines; report sample counts and an honest cold-start state | Planned |
| 5 | Menu insights | Show menu-level demand and surplus with sample counts; flag small samples; compare within meal service | Planned |
| 6 | Calendar and known attendance | Store optional holiday/event/expected-attendance inputs with explicit forecast-time availability | Planned |
| 7 | First learned forecasting model | Train a small scikit-learn model; deterministic seed; demand target includes shortages; fit preprocessing on training data only | Planned |
| 8 | Time-based model evaluation | Compare against Day 4 baselines on chronological held-out dates; report MAE and sample sizes; never claim real accuracy from synthetic data | Planned |
| 9 | Portion recommendation policy | Let users set surplus and shortage priorities; backtest decisions; label uncertainty and avoid unsupported guarantees | Planned |
| 10 | What-if planning | Show how attendance and service priorities alter recommendations; cap outputs at sensible values; no silent changes to real records | Planned |
| 11 | Forecast explanations | Explain baseline evidence and model drivers; distinguish associations from causes; show model version and data period | Planned |
| 12 | Data-quality and forecast monitoring | Surface missing services, sparse data and unusually large errors with transparent thresholds | Planned |
| 13 | Regression checks and GitHub CI | Run meaningful tests on push; handle empty, sparse and invalid datasets; keep dependency and model setup documented | Planned |
| 14 | Portfolio release | Add screenshots, a short walkthrough, model limitations, reproducible evaluation and final setup instructions | Planned |

The order is intentional: collect reliable data, establish a baseline, evaluate a model, then support decisions. A milestone is complete only when its acceptance check passes. If a daily run is blocked, report the blocker and leave it planned. Do not advance the day counter for a no-op commit.
