"""Run with: python -m streamlit run app.py"""

from dataclasses import asdict
from datetime import date
from pathlib import Path
import os
import sqlite3

import pandas as pd
import streamlit as st

from messmind.analytics import summarize
from messmind.demo import demo_records
from messmind.models import MAX_PORTIONS, MEALS, MealRecord
from messmind.storage import MealStore

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("MESSMIND_DB_PATH", str(ROOT / "data" / "meals.db")))

st.set_page_config(page_title="MessMind · Meal intelligence", page_icon="🌱", layout="wide")
st.markdown("""
<style>
  .block-container {max-width: 1200px; padding-top: 2.5rem;}
  [data-testid="stMetric"] {background: #eef5ee; border: 1px solid #d8e6da;
    border-radius: 16px; padding: 18px;}
  .eyebrow {font-size: 12px; letter-spacing: .18em; font-weight: 700; color: #317653;}
  h1 {letter-spacing: -.045em;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🌱 MessMind")
    st.caption("LESS SURPLUS. BETTER PLANNING.")
    source = st.radio("Data source", ["Demo kitchen", "My kitchen"], key="source")
    st.divider()
    st.caption("BUILD IN PROGRESS")
    st.markdown("**Day 1 of 14** · Meal ledger")
    st.progress(1 / 14)
    st.caption("A practical Python project, built one feature at a time.")

st.markdown('<div class="eyebrow">HOSTEL MEAL INTELLIGENCE</div>', unsafe_allow_html=True)
st.title("Every portion tells a story.")
st.write("Track what you cook, what gets served, and where tomorrow can improve.")

demo = source == "Demo kitchen"
store = None
if demo:
    records = demo_records()
    st.info("Demo mode · 28 days of synthetic meal records. These are illustrative values, not measured results.")
else:
    try:
        store = MealStore(DB_PATH)
        records = store.list_all()
    except (OSError, sqlite3.Error) as exc:
        st.error(f"Could not open the local meal ledger: {exc}")
        st.stop()
    st.caption("Your records are saved on this computer. Each record describes one date and meal service.")

if st.session_state.pop("meal_saved", False):
    st.success("Meal saved. Your dashboard now includes this record.")

overview, ledger, journey = st.tabs(["Overview", "Meal log", "Build journal"])

with overview:
    meal_filter = st.selectbox("View meal service", ["All meals", *MEALS], key="meal_filter")
    filtered = [r for r in records if meal_filter == "All meals" or r.meal == meal_filter]
    summary = summarize(filtered)
    if not filtered:
        st.info("Your dashboard is ready. Open Meal log and record a completed meal to begin.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Portions prepared", f"{summary.prepared:,}")
    c2.metric("Portions served", f"{summary.served:,}")
    c3.metric("Unused portions", f"{summary.surplus:,}")
    c4.metric("Unused portion value", f"₹{summary.surplus_value:,.2f}")
    st.caption("Unused portion value = unused portions × entered cost per portion. It is a cost estimate, not proven savings or a measurement of discarded food.")

    left, right = st.columns([2, 1], gap="large")
    with left:
        st.subheader("Prepared vs served")
        if filtered:
            frame = pd.DataFrame([asdict(r) for r in filtered])
            trend = frame.groupby("log_date")[["prepared", "served"]].sum()
            trend.index = pd.to_datetime(trend.index)
            st.line_chart(trend.rename(columns={"prepared": "Prepared", "served": "Served"}), color=["#8fa99a", "#257653"])
        else:
            st.write("The trend will appear after you add meal records.")
    with right:
        st.subheader("Keep both sides in view")
        rate = "—" if summary.surplus_rate is None else f"{summary.surplus_rate:.1f}%"
        service = "—" if summary.service_rate is None else f"{summary.service_rate:.1f}%"
        st.metric("Unused share of preparation", rate)
        st.metric("Recorded demand served", service)
        st.write(f"**{summary.unserved:,}** unserved requests across **{summary.meal_count}** meal records.")
        st.caption("Low surplus alone does not mean success. Record people who requested a meal but could not receive one.")

with ledger:
    st.subheader("Record a completed meal")
    if demo:
        st.caption("Choose My kitchen in the sidebar to save your own meal records.")
    else:
        st.caption("Use portions of a consistent size. Record one request per diner; aggregate counts only.")
        with st.form("meal_form"):
            a, b = st.columns(2)
            log_date = a.date_input("Meal date", value=date.today(), max_value=date.today(), key="log_date")
            meal = b.selectbox("Meal", MEALS, key="meal")
            menu = st.text_input("Menu", placeholder="For example: rice, sambar and vegetables", max_chars=120, key="menu")
            a, b, c = st.columns(3)
            prepared = a.number_input("Portions prepared", min_value=0, max_value=MAX_PORTIONS, value=200, step=1, key="prepared")
            served = b.number_input("Portions served", min_value=0, max_value=MAX_PORTIONS, value=180, step=1, key="served")
            unserved = c.number_input("Unserved requests", min_value=0, max_value=MAX_PORTIONS, value=0, step=1, key="unserved")
            cost = st.number_input("Estimated cost per portion (₹)", min_value=0.0, max_value=10_000.0, value=30.0, step=0.5, key="cost")
            st.caption("Unserved requests are diners turned away after portions ran out. If food remained but a different dish was unavailable, log comparable portions separately in a future dish-level feature.")
            submitted = st.form_submit_button("Save meal", type="primary")
        if submitted:
            try:
                record = MealRecord(log_date.isoformat(), meal, menu, prepared, served, unserved, cost)
                store.add(record)
            except ValueError as exc:
                st.error(str(exc))
            except (OSError, sqlite3.Error) as exc:
                st.error(f"The record could not be saved: {exc}")
            else:
                st.session_state["meal_saved"] = True
                st.rerun()
    if records:
        table = pd.DataFrame([
            {"Date": r.log_date, "Meal": r.meal, "Menu": r.menu,
             "Prepared": r.prepared, "Served": r.served, "Unserved": r.unserved,
             "Unused": r.surplus, "Cost / portion (₹)": r.cost_per_portion}
            for r in sorted(records, key=lambda r: (r.log_date, -MEALS.index(r.meal)), reverse=True)
        ])
        st.subheader("Meal ledger")
        st.dataframe(table, hide_index=True, width="stretch")

with journey:
    st.subheader("One useful feature each day")
    st.write("**Day 1 complete:** a validated meal ledger, a local SQLite database, a dashboard and synthetic demo data.")
    st.write("**Next:** correct existing records, then add safe CSV import and a simple forecast baseline.")
    st.write("**The project goal:** explainable meal-demand forecasts that account for both unused food and unmet demand.")
    st.info("Forecasting is planned. This version does not contain a trained ML model or claim prediction accuracy.")
    st.markdown((ROOT / "ROADMAP.md").read_text(encoding="utf-8"))

st.divider()
st.caption("MESSMIND · Python + Streamlit + SQLite · Day 1 foundation · No API key required")
