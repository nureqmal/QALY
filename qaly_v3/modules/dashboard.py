import streamlit as st
from datetime import datetime, date
from modules.utils import load, get_theme_colors

def show():
    C = get_theme_colors()
    now = datetime.now()

    # Big date header
    st.markdown(f"""
    <div style="margin-bottom:2rem;">
        <div style="font-size:13px;font-weight:500;color:{C['TEXT3']};letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;">
            {now.strftime('%A').upper()}
        </div>
        <div style="font-size:48px;font-weight:800;color:{C['TEXT']};letter-spacing:-0.04em;line-height:1;">
            {now.strftime('%d %B %Y')}
        </div>
        <div style="font-size:13px;color:{C['TEXT2']};margin-top:6px;">{now.strftime('%I:%M %p')} &nbsp;·&nbsp; QALY One Centre</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ──────────────────────────────────────
    sales = load("sales.json")
    completed = [o for o in sales if o.get("status") == "Completed"]
    pending   = [o for o in sales if o.get("status") == "Pending"]
    total_rev = sum(o.get("total", 0) for o in completed)
    this_month = now.strftime("%Y-%m")
    month_sales = [o for o in completed if o.get("date","").startswith(this_month)]
    month_rev   = sum(o.get("total", 0) for o in month_sales)

    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("TOTAL REVENUE", f"RM {total_rev:,.2f}", f"{len(completed)} completed orders"),
        ("THIS MONTH", f"RM {month_rev:,.2f}", f"{len(month_sales)} orders in {now.strftime('%B')}"),
        ("TOTAL ORDERS", str(len(sales)), f"{len(pending)} pending"),
        ("AVG ORDER VALUE", f"RM {(total_rev/max(len(completed),1)):,.2f}", "per completed order"),
    ]
    for col, (label, val, sub) in zip([col1,col2,col3,col4], kpis):
        with col:
            st.markdown(f"""
            <div class="qcard">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"<div class='divider'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Recent orders
        st.markdown(f"<div style='font-size:15px;font-weight:600;color:{C['TEXT']};margin-bottom:12px;'>Recent Orders</div>", unsafe_allow_html=True)
        recent = sorted(sales, key=lambda x: x.get("date",""), reverse=True)[:5]
        if recent:
            for o in recent:
                badge_class = {"Completed":"badge-green","Pending":"badge-yellow","Cancelled":"badge-red"}.get(o.get("status",""),"badge-purple")
                st.markdown(f"""
                <div class="qcard" style="padding:10px 14px;display:flex;align-items:center;justify-content:space-between;">
                    <div>
                        <div style="font-size:13px;font-weight:600;color:{C['TEXT']};">{o.get('name','?')}</div>
                        <div style="font-size:11px;color:{C['TEXT2']};margin-top:2px;">{o.get('product','?')} &nbsp;·&nbsp; {o.get('channel','?')} &nbsp;·&nbsp; {o.get('date','?')}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:14px;font-weight:700;color:{C['ACCENT']};">RM {o.get('total',0):.2f}</div>
                        <span class="badge {badge_class}" style="margin-top:3px;display:inline-block;">{o.get('status','?')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='qcard'><div style='color:{C['TEXT2']};font-size:13px;'>No orders yet.</div></div>", unsafe_allow_html=True)

    with col_right:
        # Upcoming events
        st.markdown(f"<div style='font-size:15px;font-weight:600;color:{C['TEXT']};margin-bottom:12px;'>Upcoming Events</div>", unsafe_allow_html=True)
        events = load("events.json")
        today = date.today()
        upcoming = sorted(
            [e for e in events if e.get("date","") >= str(today)],
            key=lambda x: x.get("date","")
        )[:4]
        if upcoming:
            for e in upcoming:
                edate = e.get("date","")
                days_left = (date.fromisoformat(edate) - today).days if edate else 0
                urgency = "badge-red" if days_left <= 3 else "badge-yellow" if days_left <= 7 else "badge-blue"
                label = "Today" if days_left == 0 else f"In {days_left}d"
                st.markdown(f"""
                <div class="qcard" style="padding:10px 14px;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <div style="font-size:13px;font-weight:600;color:{C['TEXT']};">{e.get('title','?')}</div>
                            <div style="font-size:11px;color:{C['TEXT2']};margin-top:2px;">{edate} &nbsp;·&nbsp; {e.get('location','')}</div>
                        </div>
                        <span class="badge {urgency}">{label}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='qcard'><div style='color:{C['TEXT2']};font-size:13px;'>No upcoming events. Add one in Upcoming Events.</div></div>", unsafe_allow_html=True)

        # Pending alert
        if pending:
            st.markdown(f"""
            <div class="qcard" style="border:1px solid {C['WARN_T']}40;background:{C['WARN_BG']};">
                <div style="font-size:13px;font-weight:600;color:{C['WARN_T']};">{len(pending)} Pending Order{'s' if len(pending)>1 else ''}</div>
                <div style="font-size:12px;color:{C['TEXT2']};margin-top:3px;">Update status in Sales Tracker.</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"<div class='divider'></div>", unsafe_allow_html=True)

    # ── Visit log ────────────────────────────────────
    st.markdown(f"<div style='font-size:15px;font-weight:600;color:{C['TEXT']};margin-bottom:12px;'>System Activity</div>", unsafe_allow_html=True)
    visits = load("visits.json")

    col_activity, col_stats = st.columns([3, 2])

    with col_activity:
        st.markdown(f"<div style='font-size:12px;color:{C['TEXT2']};margin-bottom:8px;'>Recent logins</div>", unsafe_allow_html=True)
        recent_visits = sorted(visits, key=lambda x: x.get("timestamp",""), reverse=True)[:8]
        if recent_visits:
            for v in recent_visits:
                ts = v.get("timestamp","")
                try:
                    dt = datetime.fromisoformat(ts)
                    time_str = dt.strftime("%d %b %Y &nbsp;·&nbsp; %I:%M %p")
                except:
                    time_str = ts
                initials = "".join([w[0].upper() for w in v.get("user","?").split()])
                colors_map = {"Dr. Shirwan":"#7c6fea","Eqmal":"#4ade80","Syafa":"#f472b6","Nureen":"#60a5fa"}
                uc = colors_map.get(v.get("user",""), C["ACCENT"])
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid {C['BORDER']};">
                    <div style="width:30px;height:30px;border-radius:8px;background:{uc}22;color:{uc};font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{initials}</div>
                    <div>
                        <div style="font-size:13px;font-weight:500;color:{C['TEXT']};">{v.get('user','?')}</div>
                        <div style="font-size:11px;color:{C['TEXT2']};">{time_str}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:{C['TEXT2']};font-size:13px;'>No activity yet.</div>", unsafe_allow_html=True)

    with col_stats:
        st.markdown(f"<div style='font-size:12px;color:{C['TEXT2']};margin-bottom:8px;'>Login count (all time)</div>", unsafe_allow_html=True)
        from modules.utils import MEMBERS
        user_counts = {m: sum(1 for v in visits if v.get("user") == m) for m in MEMBERS}
        total_visits = max(sum(user_counts.values()), 1)
        colors_map = {"Dr. Shirwan":"#7c6fea","Eqmal":"#4ade80","Syafa":"#f472b6","Nureen":"#60a5fa"}

        for member, count in sorted(user_counts.items(), key=lambda x: x[1], reverse=True):
            pct = count / total_visits
            uc = colors_map.get(member, C["ACCENT"])
            st.markdown(f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;">
                    <span style="color:{C['TEXT']};font-weight:500;">{member}</span>
                    <span style="color:{C['TEXT2']};">{count} {'login' if count==1 else 'logins'}</span>
                </div>
                <div style="background:{C['BORDER']};border-radius:99px;height:6px;">
                    <div style="background:{uc};width:{pct*100:.0f}%;height:6px;border-radius:99px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
