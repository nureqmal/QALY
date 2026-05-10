import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from modules.utils import load, PRODUCTS, CHANNELS

def show():
    st.markdown("<div class='section-title'>Analytics</div><div class='section-sub'>Revenue trends, product performance, channel breakdown</div>", unsafe_allow_html=True)

    sales = load("sales.json")
    completed = [o for o in sales if o.get("status") == "Completed"]

    if not completed:
        st.info("No completed orders yet. Complete some orders in Sales Tracker to see analytics.")
        return

    df = pd.DataFrame(completed)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["week"] = df["date"].dt.to_period("W").astype(str)

    # Top KPIs
    total_rev = df["total"].sum()
    total_qty = df["qty"].sum()
    best_product = df.groupby("product")["total"].sum().idxmax()
    best_channel = df.groupby("channel")["total"].sum().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    for col, (icon, label, val) in zip(
        [col1,col2,col3,col4],
        [
            ("💰","Total Revenue", f"RM {total_rev:,.2f}"),
            ("📦","Units Sold", str(int(total_qty))),
            ("🏆","Best Product", best_product.split(" ")[0]),
            ("📡","Top Channel", best_channel),
        ]
    ):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size:18px;margin-bottom:6px;">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div style="font-size:20px;font-weight:700;color:#1a1440;line-height:1.2;">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='qdivider'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📈  Revenue Trend", "🛒  Product Performance", "📡  Channel Analysis"])

    with tab1:
        period = st.radio("Group by", ["Monthly", "Weekly"], horizontal=True)
        group_col = "month" if period == "Monthly" else "week"
        trend = df.groupby(group_col)["total"].sum().reset_index()
        trend.columns = ["Period", "Revenue"]

        # Manual bar chart using st.bar_chart
        chart_df = trend.set_index("Period")
        st.bar_chart(chart_df, color="#534AB7", height=300)

        # Revenue table
        st.markdown("**Detailed breakdown**")
        trend["Revenue"] = trend["Revenue"].apply(lambda x: f"RM {x:,.2f}")
        st.dataframe(trend, use_container_width=True, hide_index=True)

    with tab2:
        prod_rev = df.groupby("product").agg(
            Revenue=("total","sum"),
            Orders=("id","count"),
            Units=("qty","sum")
        ).reset_index().sort_values("Revenue", ascending=False)

        prod_rev["Revenue (RM)"] = prod_rev["Revenue"].apply(lambda x: f"RM {x:,.2f}")
        prod_rev["% of Sales"] = (prod_rev["Revenue"] / prod_rev["Revenue"].sum() * 100).apply(lambda x: f"{x:.1f}%")

        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("**Revenue by product**")
            display_df = prod_rev[["product","Revenue (RM)","Orders","Units","% of Sales"]].rename(columns={"product":"Product"})
            st.dataframe(display_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Visual share**")
            total = prod_rev["Revenue"].sum()
            for _, row in prod_rev.iterrows():
                pct = row["Revenue"] / total
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;font-size:12px;color:#534AB7;margin-bottom:3px;">
                        <span>{row['product'].split(' ')[0]}</span><span>{pct*100:.0f}%</span>
                    </div>
                    <div style="background:#f0eeff;border-radius:99px;height:8px;">
                        <div style="background:#534AB7;width:{pct*100}%;height:8px;border-radius:99px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        ch_data = df.groupby("channel").agg(
            Revenue=("total","sum"),
            Orders=("id","count"),
        ).reset_index().sort_values("Revenue", ascending=False)

        ch_data["Revenue (RM)"] = ch_data["Revenue"].apply(lambda x: f"RM {x:,.2f}")
        ch_data["% Share"] = (ch_data["Revenue"] / ch_data["Revenue"].sum() * 100).apply(lambda x: f"{x:.1f}%")

        display = ch_data[["channel","Revenue (RM)","Orders","% Share"]].rename(columns={"channel":"Channel"})
        st.dataframe(display, use_container_width=True, hide_index=True)

        st.markdown("<br>**Channel performance bars**", unsafe_allow_html=True)
        total_ch = ch_data["Revenue"].sum()
        colors_ch = ["#534AB7","#7C6FD4","#A99EE8","#C8C2F0","#E2DEFF","#6B5CCC"]
        for i, (_, row) in enumerate(ch_data.iterrows()):
            pct = row["Revenue"] / total_ch
            color = colors_ch[i % len(colors_ch)]
            st.markdown(f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                    <span style="color:#1a1440;font-weight:500;">{row['channel']}</span>
                    <span style="color:#9591b8;">RM {row['Revenue']:,.2f} · {row['Orders']} orders</span>
                </div>
                <div style="background:#f5f4ff;border-radius:99px;height:10px;">
                    <div style="background:{color};width:{pct*100}%;height:10px;border-radius:99px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
