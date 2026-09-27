# Day 1 validation

Validated on 2026-09-26 with Python 3.12.14, Streamlit 1.64.0 and pandas 2.2.3.

Command: `python -m unittest discover -s tests -v`

Result: **10 tests passed**.

The suite exercises weighted metrics, decimal cost aggregation, empty data, shortages, invalid input, persistence across database reopen, duplicate protection, meal ordering, reproducible demo data and the complete Streamlit save/duplicate/error/data-source flow.

The Streamlit server also started successfully on the local test port. A browser screenshot was not captured because a local Chromium executable was unavailable. UI interactions were checked with Streamlit AppTest.

Forecast accuracy is not measured: Day 1 has no forecasting model. Demo values are synthetic.
