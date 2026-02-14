"""Optional Streamlit UI for the POA&M tracker.

This is not required for reviewing the repo. It's here as an easy demo UI if you want one.

Run:
  pip install streamlit pandas
  streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
from pathlib import Path
import datetime as dt

st.set_page_config(page_title="POA&M Tracker (Demo)", layout="wide")

st.title("POA&M + Continuous Monitoring Tracker (Demo)")
st.caption("Public-safe demo UI using fictional data.")

default_csv = Path(__file__).resolve().parents[1] / "sample-data" / "findings.sample.csv"
csv_path = st.text_input("Findings CSV path", value=str(default_csv))

try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"Could not read CSV: {e}")
    st.stop()

# Basic filters
col1, col2, col3, col4 = st.columns(4)
with col1:
    status = st.multiselect("Status", sorted(df["status"].unique().tolist()), default=sorted(df["status"].unique().tolist()))
with col2:
    severity = st.multiselect("Severity", sorted(df["severity"].unique().tolist()), default=sorted(df["severity"].unique().tolist()))
with col3:
    owner = st.multiselect("Owner", sorted(df["owner"].unique().tolist()), default=sorted(df["owner"].unique().tolist()))
with col4:
    system = st.multiselect("System", sorted(df["system"].unique().tolist()), default=sorted(df["system"].unique().tolist()))

f = df[
    df["status"].isin(status) &
    df["severity"].isin(severity) &
    df["owner"].isin(owner) &
    df["system"].isin(system)
].copy()

st.subheader("Findings")
st.dataframe(f, use_container_width=True, hide_index=True)

st.subheader("Exports")
st.write("Use the CLI to generate exports:")
st.code("python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports", language="bash")
