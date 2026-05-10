import streamlit as st
import json, os
from datetime import datetime, timedelta
import random

DATA_FILE = "data/sales.json"

def load_sales():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def show(user="Founder"):
    st.title(f"Good {'morning' if datetime.now().hour < 12 else 'afternoon'}, {user.split('(')[0].strip()} 👋")
    st.caption(f"Qaly Business OS · {datetime.now().strftime('%A, %d %B %Y')}")
    st.divider()

    sales = load_sales()
    total_revenue = sum(o.get("total", 0) for o in sales)
    total_orders = len(sales)
    qaly_orders = sum(1 for o in sales if "Qaly" in o.get("product", ""))
    syed_orders = sum(1 for o in sales if "Syed" in o.get("product", ""))
    syeda_orders = sum(1 for o in sales if "Syeda" in o.get("product", ""))

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"RM {total_revenue:.2f}", help="All time")
    with col2:
        st.metric("Total Orders", total_orders, help="All time")
    with col3:
        st.metric("Qaly (base) sold", qaly_orders)
    with col4:
        pending = sum(1 for o in sales if o.get("status") == "Pending")
        st.metric("Pending orders", pending, delta=f"-{pending} to action" if pending else None, delta_color="inverse")

    st.divider()

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Recent orders")
        if sales:
            recent = sorted(sales, key=lambda x: x.get("date", ""), reverse=True)[:5]
            for o in recent:
                status_color = "🟢" if o.get("status") == "Completed" else "🟡"
                st.markdown(f"{status_color} **{o.get('name', 'Unknown')}** — {o.get('product', '?')} · RM {o.get('total', 0):.2f} · `{o.get('date', '?')}`")
        else:
            st.info("No orders yet. Add your first order in Sales Tracker.")

    with col_right:
        st.subheader("Product breakdown")
        if total_orders > 0:
            st.progress(qaly_orders / max(total_orders, 1), text=f"Qaly Base: {qaly_orders}")
            st.progress(syed_orders / max(total_orders, 1), text=f"Syed: {syed_orders}")
            st.progress(syeda_orders / max(total_orders, 1), text=f"Syeda: {syeda_orders}")
        else:
            st.info("No data yet.")

    st.divider()

    # AI Quick Ask
    st.subheader("✨ Ask Qaly AI")
    st.caption("Ask anything about your business — strategy, content, analysis")

    quick_prompts = [
        "What should we focus on this week?",
        "Write a caption for Syeda product",
        "How can we grow our Instagram faster?",
        "Suggest a promo strategy for this month",
    ]
    cols = st.columns(2)
    for i, prompt in enumerate(quick_prompts):
        with cols[i % 2]:
            if st.button(prompt, key=f"quick_{i}", use_container_width=True):
                st.session_state["quick_prompt"] = prompt
                st.session_state["goto_content"] = True
                st.rerun()

    if "api_key" not in st.session_state:
        st.info("💡 Add your Anthropic API key in Settings (sidebar) to enable AI features.")
