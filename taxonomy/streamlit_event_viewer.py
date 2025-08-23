import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Event Classes", layout="wide")
st.title("Event Classes — interactive viewer")

DATA_FILE = Path(__file__).parent / "event_classes.csv"

@st.cache_data(show_spinner=False)
def load():
    # All fields as string to avoid unintended type inference issues
    return pd.read_csv(DATA_FILE, dtype=str)

try:
    df = load()
except Exception as e:
    st.error(f"Failed to load CSV: {e}")
    st.stop()

with st.sidebar:
    st.header("Filters")
    categories = sorted(df['category'].unique())
    sel_cats = st.multiselect("Category (A..U)", categories, default=categories)
    routes = sorted(df['default_route'].unique())
    sel_routes = st.multiselect("Route", routes, default=routes)
    q = st.text_input("Search (any field)")

f = df[df['category'].isin(sel_cats) & df['default_route'].isin(sel_routes)].copy()
if q:
    qlow = q.lower()
    f = f[f.apply(lambda r: qlow in " ".join(r.astype(str)).lower(), axis=1)]

st.caption(f"Showing {len(f)} of {len(df)} rows")
st.dataframe(f, use_container_width=True, height=700)

csv_dl = f.to_csv(index=False).encode()
st.download_button("Download filtered CSV", data=csv_dl, file_name="event_classes_filtered.csv", mime="text/csv")

st.markdown("---")
st.subheader("Summary")
st.write(f.groupby(['category','default_route']).size().rename('count'))