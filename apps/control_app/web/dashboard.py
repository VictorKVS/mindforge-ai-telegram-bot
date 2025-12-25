"""
File: apps/control_app/web/dashboard.py

Purpose:
MindForge Web Control Dashboard (DEMO).
"""

import sys
from pathlib import Path

# -------------------------------------------------------------------
# 🔧 FIX FOR STREAMLIT IMPORTS
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# -------------------------------------------------------------------
# Imports (AFTER sys.path fix)
# -------------------------------------------------------------------
import streamlit as st

from apps.control_app.data_sources.audit import load_audit_events
from apps.control_app.metrics.risk import risk_score
from apps.control_app.metrics.decisions import decision_metrics
from apps.control_app.metrics.policies import policy_stats
from apps.control_app.feedback.policy import render_policy_feedback

from src.core.policy_feedback import apply_policy_feedback
from src.core.runtime_state import STATE
from src.bot.config import settings

# -------------------------------------------------------------------
# UI
# -------------------------------------------------------------------
st.set_page_config(
    page_title="MindForge Control Panel",
    layout="wide",
)

st.title("🧠 MindForge Control Panel")

# --- Load data ---
events = load_audit_events(limit=100)
snap = STATE.get_sync_snapshot()

# --- Top status ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Agent", "ENABLED" if snap["agent_enabled"] else "DISABLED")

with col2:
    st.metric("Policy Mode", snap["policy_mode"])

with col3:
    st.metric("Environment", settings.APP_ENV.upper())

with col4:
    st.metric("Audit Events", len(events))

st.divider()

if not events:
    st.info("No audit events yet.")
    st.stop()

# --- Metrics ---
decisions = decision_metrics(events)
risk = risk_score(events)
policies = policy_stats(events)

feedback = apply_policy_feedback(risk)

# --- Layout ---
left, right = st.columns(2)

with left:
    st.subheader("📊 Decisions")
    st.json(decisions)

    st.subheader("🛡 Policies")
    st.json(policies)

with right:
    st.subheader("⚠ Risk")
    st.metric("Risk Score", risk["risk_score"])
    st.metric("Risk Level", risk["level"])

    st.subheader("🔁 Policy Feedback")
    st.code(render_policy_feedback(feedback))

st.divider()
st.caption("MindForge DEMO · Adaptive AI Governance")
