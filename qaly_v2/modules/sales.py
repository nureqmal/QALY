import streamlit as st
from datetime import datetime
from modules.utils import load, save, PRODUCTS, CHANNELS, STATUSES

def show():
    st.markdown("<div class='section-title'>Sales Tracker</div><div class='section-sub'>Log and manage every order</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["➕  New Order", "📋  All Orders"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("order_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Customer Name *")
                phone = st.text_input("Phone / Contact", placeholder="01X-XXXXXXX")
                product = st.selectbox("Product *", list(PRODUCTS.keys()))
                qty = st.number_input("Quantity", min_value=1, max_value=50, value=1)
            with col2:
                channel = st.selectbox("Sales Channel", CHANNELS)
                status = st.selectbox("Order Status", STATUSES)
                date = st.date_input("Order Date", value=datetime.today())
                notes = st.text_area("Notes", placeholder="Pickup time, payment method, special requests...", height=108)

            unit_price = PRODUCTS[product]
            total = unit_price * qty
            st.markdown(f"""
            <div style="background:#f0eeff;border-radius:12px;padding:1rem 1.2rem;margin:0.5rem 0;">
                <div style="font-size:13px;color:#7b75b0;">Order Summary</div>
                <div style="font-size:22px;font-weight:700;color:#534AB7;margin-top:4px;">RM {total:.2f}</div>
                <div style="font-size:12px;color:#9591b8;">RM {unit_price:.2f} × {qty} unit{'s' if qty>1 else ''}</div>
            </div>
            """, unsafe_allow_html=True)

            submitted = st.form_submit_button("💾  Save Order", use_container_width=True)
            if submitted:
                if not name.strip():
                    st.error("Customer name is required.")
                else:
                    sales = load("sales.json")
                    new_order = {
                        "id": f"ORD{len(sales)+1:04d}",
                        "name": name.strip(),
                        "phone": phone.strip(),
                        "product": product,
                        "qty": qty,
                        "unit_price": unit_price,
                        "total": total,
                        "channel": channel,
                        "status": status,
                        "date": str(date),
                        "notes": notes.strip(),
                        "created_by": st.session_state.get("current_user", "?"),
                        "created_at": datetime.now().isoformat(),
                    }
                    sales.append(new_order)
                    save("sales.json", sales)
                    st.success(f"✅ Order {new_order['id']} saved! RM {total:.2f} from {name}")

    with tab2:
        sales = load("sales.json")
        if not sales:
            st.info("No orders yet. Add your first order above.")
            return

        # Filters row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            f_status = st.selectbox("Status", ["All"] + STATUSES, key="f_status")
        with col2:
            f_channel = st.selectbox("Channel", ["All"] + CHANNELS, key="f_channel")
        with col3:
            f_product = st.selectbox("Product", ["All"] + list(PRODUCTS.keys()), key="f_product")
        with col4:
            f_search = st.text_input("Search customer", placeholder="Name...", key="f_search")

        filtered = sales
        if f_status != "All": filtered = [o for o in filtered if o.get("status") == f_status]
        if f_channel != "All": filtered = [o for o in filtered if o.get("channel") == f_channel]
        if f_product != "All": filtered = [o for o in filtered if o.get("product") == f_product]
        if f_search: filtered = [o for o in filtered if f_search.lower() in o.get("name","").lower()]
        filtered = sorted(filtered, key=lambda x: x.get("date",""), reverse=True)

        # Summary strip
        filt_rev = sum(o.get("total",0) for o in filtered if o.get("status")=="Completed")
        st.markdown(f"""
        <div style="display:flex;gap:16px;margin:0.75rem 0 1rem;flex-wrap:wrap;">
            <div style="background:#f0eeff;border-radius:10px;padding:8px 16px;font-size:13px;color:#534AB7;font-weight:500;">
                {len(filtered)} orders shown
            </div>
            <div style="background:#e8faf2;border-radius:10px;padding:8px 16px;font-size:13px;color:#0d7a4e;font-weight:500;">
                RM {filt_rev:,.2f} completed revenue
            </div>
        </div>
        """, unsafe_allow_html=True)

        for o in filtered:
            badge_class = {"Completed":"badge-green","Pending":"badge-yellow","Cancelled":"badge-red"}.get(o.get("status",""),"badge-purple")
            with st.expander(f"**{o.get('id')}** · {o.get('name')} · {o.get('product')} · RM {o.get('total',0):.2f}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"**Customer:** {o.get('name')}")
                    st.markdown(f"**Phone:** {o.get('phone') or '—'}")
                    st.markdown(f"**Product:** {o.get('product')}")
                with c2:
                    st.markdown(f"**Qty:** {o.get('qty')} × RM {o.get('unit_price',0):.2f}")
                    st.markdown(f"**Channel:** {o.get('channel')}")
                    st.markdown(f"**Date:** {o.get('date')}")
                with c3:
                    st.markdown(f"**Total:** RM {o.get('total',0):.2f}")
                    st.markdown(f"**Created by:** {o.get('created_by','?')}")
                    if o.get("notes"):
                        st.markdown(f"**Notes:** {o.get('notes')}")

                new_status = st.selectbox(
                    "Update status",
                    STATUSES,
                    index=STATUSES.index(o.get("status", "Pending")),
                    key=f"upd_{o['id']}"
                )
                if st.button("Update Status", key=f"btn_{o['id']}"):
                    all_sales = load("sales.json")
                    for order in all_sales:
                        if order["id"] == o["id"]:
                            order["status"] = new_status
                    save("sales.json", all_sales)
                    st.success("Updated!")
                    st.rerun()
