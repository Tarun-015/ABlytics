"""
Trend-over-time chart — intentionally not implemented yet.

Manual mode is a single point-in-time comparison (two totals per variant),
so there's no time series to chart. This becomes meaningful once Historical
Comparison or True A/B GA4 modes fetch day-by-day GA4 data (ga4/fetcher.py
is currently an empty stub). Left as a documented no-op rather than a fake
chart with placeholder data, so it's obvious this is pending, not broken.
"""

import streamlit as st


def show_trend_chart(*args, **kwargs):
    st.caption("Trend charts require day-by-day data (Historical/True A/B GA4 modes, not yet implemented).")
