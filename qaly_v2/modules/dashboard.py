import streamlit as st
from datetime import datetime, timedelta
from modules.utils import load, PRODUCTS

def show():
    user = st.session_state.get("current_user", "Founder")
    hour = datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"

    st.markdown(f"""
    <div style="margin-bottom:2rem;">
        <div style="font-size:26px;font-weight:700;color:#1a1440;">{greeting}, {user} 👋</div>
        <div style="font-size:14px;color:#9591b8;">{datetime.now().strftime('%A, %d %B %Y')} · Qaly Business OS</div>
    </div>
    """, unsafe_allow_html=True)

    sales = load("sales.json")
    completed = [o for o in sales if o.get("status") == "Completed"]
    pending = [o for o in sales if o.get("status") == "Pending"]
    total_rev = sum(o.get("total", 0) for o in completed)
    total_orders = len(sales)

    # This month
    this_month = datetime.now().strftime("%Y-%m")
    month_sales = [o for o in completed if o.get("date", "").startswith(this_month)]
    month_rev = sum(o.get("total", 0) for o in month_sales)

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)
    cards = [
        ("Total Revenue", f"RM {total_rev:,.2f}", "All time completed orders", "💰"),
        ("This Month", f"RM {month_rev:,.2f}", f"{len(month_sales)} orders in {datetime.now().strftime('%B')}", "📅"),
        ("Total Orders", str(total_orders), f"{len(pending)} pending action", "📦"),
        ("Avg Order Value", f"RM {(total_rev/max(len(completed),1)):,.2f}", "Per completed order", "📈"),
    ]
    for col, (label, value, sub, icon) in zip([col1,col2,col3,col4], cards):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size:20px;margin-bottom:8px;">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='qdivider'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("<div class='section-title'>Recent Orders</div><div class='section-sub'>Latest 6 transactions</div>", unsafe_allow_html=True)
        recent = sorted(sales, key=lambda x: x.get("date",""), reverse=True)[:6]
        if recent:
            for o in recent:
                badge_class = {"Completed":"badge-green","Pending":"badge-yellow","Cancelled":"badge-red"}.get(o.get("status",""),"badge-purple")
                st.markdown(f"""
                <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:white;border-radius:12px;margin-bottom:8px;border:1px solid #f0eeff;">
                    <div>
                        <div style="font-size:14px;font-weight:600;color:#1a1440;">{o.get('name','?')}</div>
                        <div style="font-size:12px;color:#9591b8;">{o.get('product','?')} · {o.get('channel','?')} · {o.get('date','?')}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:15px;font-weight:700;color:#534AB7;">RM {o.get('total',0):.2f}</div>
                        <span class="badge {badge_class}">{o.get('status','?')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No orders yet. Add your first order in Sales Tracker.")

    with col_right:
        st.markdown("<div class='section-title'>Product Mix</div><div class='section-sub'>Sales by product (all time)</div>", unsafe_allow_html=True)

        product_counts = {}
        for o in completed:
            p = o.get("product","?")
            product_counts[p] = product_counts.get(p, 0) + o.get("qty", 1)

        if product_counts:
            total_qty = sum(product_counts.values())
            colors = ["#534AB7","#7C6FD4","#A99EE8","#C8C2F0","#E2DEFF","#6B5CCC","#9085D9"]
            for i, (prod, qty) in enumerate(sorted(product_counts.items(), key=lambda x: x[1], reverse=True)):
                pct = qty / max(total_qty, 1)
                color = colors[i % len(colors)]
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                        <span style="color:#1a1440;font-weight:500;">{prod}</span>
                        <span style="color:#9591b8;">{qty} units · {pct*100:.0f}%</span>
                    </div>
                    <div style="background:#f0eeff;border-radius:99px;height:8px;">
                        <div style="background:{color};width:{pct*100}%;height:8px;border-radius:99px;transition:width 0.5s;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No sales data yet.")

    st.markdown("<div class='qdivider'></div>", unsafe_allow_html=True)

    # Pending orders alert
    if pending:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fff8e7,#fef3cd);border:1px solid #fde68a;border-radius:14px;padding:1.2rem 1.5rem;display:flex;align-items:center;gap:12px;">
            <div style="font-size:24px;">⚠️</div>
            <div>
                <div style="font-weight:600;color:#92610a;font-size:15px;">{len(pending)} Pending Order{'s' if len(pending)>1 else ''}</div>
                <div style="font-size:13px;color:#b07d1a;">Go to Sales Tracker to update their status.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
