import streamlit as st
import pandas as pd
import urllib.request, json
from datetime import datetime
from modules.utils import load, save, get_theme_colors, PRODUCTS, CHANNELS, STATUSES, MEMBERS

# Google Form responses sheet — publish as CSV to use
# Instructions: File > Share > Publish to web > CSV format
GSHEET_CSV_URL = ""  # User pastes their published CSV URL here

def fetch_gsheet(url):
    try:
        df = pd.read_csv(url)
        return df, None
    except Exception as e:
        return None, str(e)

def show():
    C = get_theme_colors()
    st.markdown(f"<div class='page-title'>Sales Tracker</div><div class='page-sub'>Google Form orders + Shopee sales</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Google Form Orders", "Shopee / Manual", "All Orders"])

    # ── Tab 1: Google Form ────────────────────────────
    with tab1:
        st.markdown(f"""
        <div class="qcard qcard-accent" style="margin-bottom:1rem;">
            <div style="font-size:13px;font-weight:600;color:{C['TEXT']};margin-bottom:4px;">Setup: Connect your Google Form responses</div>
            <div style="font-size:12px;color:{C['TEXT2']};line-height:1.7;">
                1. Open your Google Spreadsheet (order responses)<br>
                2. File &gt; Share &gt; Publish to web<br>
                3. Select the correct sheet tab &gt; CSV format &gt; Publish<br>
                4. Paste the CSV link below
            </div>
        </div>
        """, unsafe_allow_html=True)

        saved_cfg = load("config.json")
        if isinstance(saved_cfg, list):
            saved_cfg = {}
        default_url = saved_cfg.get("gsheet_url", "")

        csv_url = st.text_input(
            "Published CSV URL",
            value=default_url,
            placeholder="https://docs.google.com/spreadsheets/d/.../pub?output=csv"
        )
        col1, col2 = st.columns([1,3])
        with col1:
            if st.button("Connect & Save", use_container_width=True):
                if csv_url:
                    saved_cfg["gsheet_url"] = csv_url
                    from modules.utils import save_dict
                    save_dict("config.json", saved_cfg)
                    st.success("URL saved!")
                    st.rerun()
        with col2:
            if st.button("Refresh Data", use_container_width=True):
                st.cache_data.clear()
                st.rerun()

        active_url = csv_url or default_url
        if active_url:
            with st.spinner("Fetching orders from Google Sheets..."):
                df, err = fetch_gsheet(active_url)
            if err:
                st.error(f"Could not connect: {err}")
                st.info("Make sure the sheet is published as CSV and the link is correct.")
            elif df is not None and not df.empty:
                st.success(f"{len(df)} responses loaded from Google Form")

                # Show column mapping
                with st.expander("Column mapping (verify your column names)"):
                    st.write("Detected columns:", list(df.columns))
                    st.caption("Map your form columns below if needed.")

                    col_name     = st.selectbox("Customer Name column",     df.columns.tolist(), key="cn")
                    col_product  = st.selectbox("Product column",           df.columns.tolist(), key="cp")
                    col_qty      = st.selectbox("Quantity column",          df.columns.tolist(), key="cq")
                    col_channel  = st.selectbox("Channel column",           df.columns.tolist(), key="cc")
                    col_date     = st.selectbox("Date/Timestamp column",    df.columns.tolist(), key="cd")

                    if st.button("Save column mapping"):
                        saved_cfg["col_name"]    = col_name
                        saved_cfg["col_product"] = col_product
                        saved_cfg["col_qty"]     = col_qty
                        saved_cfg["col_channel"] = col_channel
                        saved_cfg["col_date"]    = col_date
                        from modules.utils import save_dict
                        save_dict("config.json", saved_cfg)
                        st.success("Mapping saved!")

                # Use saved or default mapping
                col_name    = saved_cfg.get("col_name",    df.columns[0])
                col_product = saved_cfg.get("col_product", df.columns[1] if len(df.columns)>1 else df.columns[0])
                col_qty     = saved_cfg.get("col_qty",     df.columns[2] if len(df.columns)>2 else df.columns[0])
                col_channel = saved_cfg.get("col_channel", df.columns[3] if len(df.columns)>3 else df.columns[0])
                col_date    = saved_cfg.get("col_date",    df.columns[0])

                # Render orders
                st.markdown(f"<div style='font-size:13px;color:{C['TEXT2']};margin:1rem 0 0.5rem;'>Live orders</div>", unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True)
        else:
            st.info("Paste your Google Sheet CSV URL above to load live orders.")

    # ── Tab 2: Shopee / Manual ────────────────────────
    with tab2:
        st.markdown(f"<div style='font-size:14px;font-weight:500;color:{C['TEXT']};margin-bottom:1rem;'>Record Shopee sales or manual orders</div>", unsafe_allow_html=True)

        with st.form("manual_order", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name     = st.text_input("Customer Name *")
                product  = st.selectbox("Product", list(PRODUCTS.keys()))
                qty      = st.number_input("Quantity", min_value=1, max_value=50, value=1)
                channel  = st.selectbox("Channel", CHANNELS)
            with col2:
                status   = st.selectbox("Status", STATUSES)
                order_date = st.date_input("Order Date", value=datetime.today())
                selling_price = st.number_input(
                    "Selling Price (RM)",
                    min_value=0.0,
                    value=float(PRODUCTS[product if product in PRODUCTS else list(PRODUCTS.keys())[0]]),
                    step=0.50
                )
                platform_fee = st.number_input("Platform Fee / Discount (RM)", min_value=0.0, value=0.0, step=0.50,
                                               help="Shopee commission, vouchers, shipping subsidy etc.")
                notes    = st.text_area("Notes", height=72, placeholder="Shopee order ID, notes...")

            total     = selling_price * qty
            net       = total - platform_fee

            st.markdown(f"""
            <div class="qcard" style="padding:10px 14px;margin-top:0.5rem;">
                <div style="display:flex;gap:2rem;flex-wrap:wrap;">
                    <div><div class="kpi-label">Gross</div><div style="font-size:18px;font-weight:700;color:{C['TEXT']};">RM {total:.2f}</div></div>
                    <div><div class="kpi-label">Net Profit</div><div style="font-size:18px;font-weight:700;color:{C['ACCENT']};">RM {net:.2f}</div></div>
                    <div><div class="kpi-label">Fees/Discount</div><div style="font-size:18px;font-weight:700;color:{C['WARN_T']};">- RM {platform_fee:.2f}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.form_submit_button("Save Order", use_container_width=True):
                if not name.strip():
                    st.error("Customer name is required.")
                else:
                    orders = load("sales.json")
                    orders.append({
                        "id": f"ORD{len(orders)+1:04d}",
                        "name": name.strip(),
                        "product": product,
                        "qty": qty,
                        "selling_price": selling_price,
                        "total": total,
                        "platform_fee": platform_fee,
                        "net": net,
                        "channel": channel,
                        "status": status,
                        "date": str(order_date),
                        "notes": notes.strip(),
                        "recorded_by": st.session_state.get("current_user","?"),
                    })
                    save("sales.json", orders)
                    st.success(f"Order saved — RM {total:.2f} gross / RM {net:.2f} net")

    # ── Tab 3: All Orders ─────────────────────────────
    with tab3:
        orders = load("sales.json")
        if not orders:
            st.info("No orders recorded yet.")
            return

        col1, col2, col3 = st.columns(3)
        with col1: f_status  = st.selectbox("Status",  ["All"] + STATUSES, key="fs2")
        with col2: f_channel = st.selectbox("Channel", ["All"] + CHANNELS, key="fc2")
        with col3: f_search  = st.text_input("Search customer", key="fsearch2", label_visibility="visible")

        filtered = orders
        if f_status  != "All": filtered = [o for o in filtered if o.get("status") == f_status]
        if f_channel != "All": filtered = [o for o in filtered if o.get("channel") == f_channel]
        if f_search:            filtered = [o for o in filtered if f_search.lower() in o.get("name","").lower()]
        filtered = sorted(filtered, key=lambda x: x.get("date",""), reverse=True)

        # Summary strip
        frev = sum(o.get("total",0) for o in filtered if o.get("status")=="Completed")
        fnet = sum(o.get("net",   o.get("total",0)) for o in filtered if o.get("status")=="Completed")
        st.markdown(f"""
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin:0.75rem 0 1rem;">
            <div class="badge badge-purple">{len(filtered)} orders</div>
            <div class="badge badge-green">RM {frev:,.2f} gross</div>
            <div class="badge badge-blue">RM {fnet:,.2f} net</div>
        </div>
        """, unsafe_allow_html=True)

        for o in filtered:
            bc = {"Completed":"badge-green","Pending":"badge-yellow","Cancelled":"badge-red"}.get(o.get("status",""),"badge-purple")
            with st.expander(f"{o.get('id')}  ·  {o.get('name')}  ·  {o.get('product')}  ·  RM {o.get('total',0):.2f}"):
                c1,c2 = st.columns(2)
                with c1:
                    st.write(f"**Product:** {o.get('product')}  x {o.get('qty')}")
                    st.write(f"**Channel:** {o.get('channel')}")
                    st.write(f"**Date:** {o.get('date')}")
                with c2:
                    st.write(f"**Gross:** RM {o.get('total',0):.2f}")
                    st.write(f"**Net:** RM {o.get('net', o.get('total',0)):.2f}")
                    st.write(f"**Recorded by:** {o.get('recorded_by','?')}")
                if o.get("notes"):
                    st.write(f"**Notes:** {o.get('notes')}")

                new_status = st.selectbox("Update status", STATUSES,
                                           index=STATUSES.index(o.get("status","Pending")),
                                           key=f"upd3_{o['id']}")
                if st.button("Update", key=f"ubtn3_{o['id']}"):
                    all_o = load("sales.json")
                    for order in all_o:
                        if order["id"] == o["id"]:
                            order["status"] = new_status
                    save("sales.json", all_o)
                    st.success("Updated!")
                    st.rerun()
