import streamlit as st
import pandas as pd
from datetime import datetime
from modules.utils import load, save, load_dict, save_dict, get_theme_colors, PRODUCTS, CHANNELS, STATUSES, GFORM_SHEET_ID, GFORM_GID

# Build the published CSV URL from spreadsheet ID + gid
# User must "Publish to web" → Sheet tab → CSV
def build_csv_url(sheet_id, gid):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

@st.cache_data(ttl=30)
def fetch_orders(url):
    try:
        df = pd.read_csv(url)
        return df, None
    except Exception as e:
        return None, str(e)

def show():
    C = get_theme_colors()
    st.markdown(f"<div class='page-title'>Sales Tracker</div><div class='page-sub'>Live Google Form orders + Shopee / manual entries</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Google Form Orders", "Shopee / Manual", "All Manual Orders"])

    # ── Tab 1: Google Form live pull ──────────────────
    with tab1:
        cfg = load_dict("config.json")

        # Try auto-build URL from known IDs
        auto_url = build_csv_url(GFORM_SHEET_ID, GFORM_GID)
        saved_url = cfg.get("gsheet_url", auto_url)

        with st.expander("Connection settings", expanded=(not cfg.get("gsheet_url"))):
            st.markdown(f"""
            <div class="qcard qcard-accent" style="margin-bottom:1rem;">
                <div style="font-size:13px;font-weight:600;color:{C['TEXT']};margin-bottom:6px;">How to enable live sync</div>
                <div style="font-size:12px;color:{C['TEXT2']};line-height:1.9;">
                    1. Open your Google Spreadsheet (form responses)<br>
                    2. File &gt; Share &gt; Publish to web<br>
                    3. Select the correct sheet tab &gt; CSV format &gt; Publish<br>
                    4. Paste the published CSV URL below (or use the auto-detected URL)
                </div>
            </div>
            """, unsafe_allow_html=True)

            csv_url = st.text_input("Published CSV URL", value=saved_url,
                                    placeholder="https://docs.google.com/spreadsheets/d/.../pub?output=csv")
            if st.button("Save & Connect", use_container_width=True, key="save_url"):
                cfg["gsheet_url"] = csv_url
                save_dict("config.json", cfg)
                st.cache_data.clear()
                st.success("Saved!")
                st.rerun()

        active_url = cfg.get("gsheet_url", auto_url)

        col_refresh, col_info = st.columns([1,3])
        with col_refresh:
            if st.button("Refresh Now", use_container_width=True, key="refresh_gsheet"):
                st.cache_data.clear()
                st.rerun()
        with col_info:
            st.markdown(f"<div style='font-size:12px;color:{C['TEXT2']};padding-top:8px;'>Auto-refreshes every 30 seconds</div>", unsafe_allow_html=True)

        with st.spinner("Loading orders from Google Form..."):
            df, err = fetch_orders(active_url)

        if err:
            st.error(f"Could not fetch data: {err}")
            st.markdown(f"""
            <div class="qcard" style="border:1px solid {C['WARN_T']}40;background:{C['WARN_BG']};">
                <div style="font-size:13px;font-weight:600;color:{C['WARN_T']};">Spreadsheet not published yet</div>
                <div style="font-size:12px;color:{C['TEXT2']};margin-top:4px;line-height:1.7;">
                    Go to your Google Spreadsheet → File → Share → Publish to web → choose the response sheet tab → CSV → Publish. Then paste the URL in settings above.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif df is not None and not df.empty:
            st.markdown(f"""
            <div style="display:flex;gap:12px;margin-bottom:1rem;flex-wrap:wrap;">
                <span class="badge badge-green">{len(df)} total responses</span>
                <span class="badge badge-purple">Live from Google Form</span>
            </div>
            """, unsafe_allow_html=True)

            # Column mapping
            cols = df.columns.tolist()
            saved_map = cfg.get("col_map", {})
            with st.expander("Column mapping"):
                c1,c2,c3,c4,c5 = st.columns(5)
                with c1: cn = st.selectbox("Name",      cols, index=cols.index(saved_map.get("name",cols[0]))      if saved_map.get("name") in cols else 0, key="cn")
                with c2: cp = st.selectbox("Product",   cols, index=cols.index(saved_map.get("product",cols[0]))   if saved_map.get("product") in cols else 0, key="cp")
                with c3: cq = st.selectbox("Quantity",  cols, index=cols.index(saved_map.get("qty",cols[0]))       if saved_map.get("qty") in cols else 0, key="cq")
                with c4: cc = st.selectbox("Channel",   cols, index=cols.index(saved_map.get("channel",cols[0]))   if saved_map.get("channel") in cols else 0, key="cc")
                with c5: cd = st.selectbox("Timestamp", cols, index=cols.index(saved_map.get("date",cols[0]))      if saved_map.get("date") in cols else 0, key="cd")
                if st.button("Save mapping"):
                    cfg["col_map"] = {"name":cn,"product":cp,"qty":cq,"channel":cc,"date":cd}
                    save_dict("config.json", cfg)
                    st.success("Mapping saved!")

            # Render clean table
            display_cols = [c for c in [
                cfg.get("col_map",{}).get("date"),
                cfg.get("col_map",{}).get("name"),
                cfg.get("col_map",{}).get("product"),
                cfg.get("col_map",{}).get("qty"),
                cfg.get("col_map",{}).get("channel"),
            ] if c and c in df.columns]

            show_df = df[display_cols] if display_cols else df
            show_df = show_df.sort_values(show_df.columns[0], ascending=False) if len(show_df.columns) > 0 else show_df
            st.dataframe(show_df, use_container_width=True, hide_index=True)
        else:
            st.info("No responses found. Make sure the sheet is published and has data.")

    # ── Tab 2: Shopee / Manual ────────────────────────
    with tab2:
        st.markdown(f"<div style='font-size:14px;font-weight:500;color:{C['TEXT']};margin-bottom:1rem;'>Record Shopee sale or any manual order</div>", unsafe_allow_html=True)

        with st.form("shopee_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                name    = st.text_input("Customer Name")
                product = st.selectbox("Product", list(PRODUCTS.keys()))
                qty     = st.number_input("Qty", min_value=1, value=1)
            with col2:
                channel    = st.selectbox("Channel", CHANNELS)
                status     = st.selectbox("Status", STATUSES)
                order_date = st.date_input("Date", value=datetime.today())
            with col3:
                selling_price = st.number_input("Selling Price (RM)", min_value=0.0,
                                                value=float(PRODUCTS.get(product if product in PRODUCTS else list(PRODUCTS.keys())[0], 30)),
                                                step=0.50)
                profit = st.number_input("Net Profit (RM)", min_value=0.0, value=0.0, step=0.50,
                                         help="Your actual take-home after fees, shipping, discounts")
                notes  = st.text_input("Notes / Order ID", placeholder="Shopee order ID etc.")

            total = selling_price * qty
            st.markdown(f"""
            <div class="qcard" style="padding:10px 14px;">
                <span style="font-size:12px;color:{C['TEXT2']};">Gross: </span><span style="font-weight:700;color:{C['TEXT']};">RM {total:.2f}</span>
                &nbsp;&nbsp;&nbsp;
                <span style="font-size:12px;color:{C['TEXT2']};">Net Profit: </span><span style="font-weight:700;color:{C['ACCENT']};">RM {profit:.2f}</span>
            </div>
            """, unsafe_allow_html=True)

            if st.form_submit_button("Save Order", use_container_width=True):
                orders = load("sales.json")
                orders.append({
                    "id":           f"ORD{len(orders)+1:04d}",
                    "name":         name.strip() or "—",
                    "product":      product,
                    "qty":          qty,
                    "selling_price":selling_price,
                    "total":        total,
                    "net":          profit,
                    "channel":      channel,
                    "status":       status,
                    "date":         str(order_date),
                    "notes":        notes.strip(),
                    "recorded_by":  st.session_state.get("current_user","?"),
                })
                save("sales.json", orders)
                st.success(f"Saved — RM {total:.2f} gross / RM {profit:.2f} net")

    # ── Tab 3: All Manual Orders ──────────────────────
    with tab3:
        orders = load("sales.json")
        if not orders:
            st.info("No manual orders yet.")
            return

        f_status = st.selectbox("Filter status", ["All"]+STATUSES, key="fs3")
        filtered = sorted(
            [o for o in orders if f_status=="All" or o.get("status")==f_status],
            key=lambda x: x.get("date",""), reverse=True
        )

        total_gross = sum(o.get("total",0) for o in filtered if o.get("status")=="Completed")
        total_net   = sum(o.get("net",0)   for o in filtered if o.get("status")=="Completed")
        st.markdown(f"""
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:1rem;">
            <span class="badge badge-purple">{len(filtered)} orders</span>
            <span class="badge badge-green">RM {total_gross:,.2f} gross</span>
            <span class="badge badge-blue">RM {total_net:,.2f} net</span>
        </div>
        """, unsafe_allow_html=True)

        for o in filtered:
            bc = {"Completed":"badge-green","Pending":"badge-yellow","Cancelled":"badge-red"}.get(o.get("status",""),"badge-purple")
            with st.expander(f"{o.get('id')}  ·  {o.get('name')}  ·  {o.get('product')}  ·  RM {o.get('total',0):.2f}"):
                c1,c2 = st.columns(2)
                with c1:
                    st.write(f"**Product:** {o.get('product')} x{o.get('qty')}")
                    st.write(f"**Channel:** {o.get('channel')}")
                    st.write(f"**Date:** {o.get('date')}")
                with c2:
                    st.write(f"**Gross:** RM {o.get('total',0):.2f}")
                    st.write(f"**Net Profit:** RM {o.get('net',0):.2f}")
                    st.write(f"**Recorded by:** {o.get('recorded_by','?')}")
                if o.get("notes"):
                    st.write(f"**Notes:** {o.get('notes')}")

                ns = st.selectbox("Update status", STATUSES,
                                  index=STATUSES.index(o.get("status","Pending")),
                                  key=f"s3_{o['id']}")
                if st.button("Update", key=f"b3_{o['id']}"):
                    all_o = load("sales.json")
                    for order in all_o:
                        if order["id"]==o["id"]: order["status"]=ns
                    save("sales.json", all_o)
                    st.success("Updated!")
                    st.rerun()
