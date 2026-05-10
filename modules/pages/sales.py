import streamlit as st
import json, os
from datetime import datetime

DATA_FILE = "data/sales.json"

def load_sales():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_sales(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

PRODUCTS = {
    "Qaly Base (30ml)": 25.00,
    "Qaly Base (60ml)": 45.00,
    "Syed (30ml)": 28.00,
    "Syed (60ml)": 48.00,
    "Syeda (30ml)": 28.00,
    "Syeda (60ml)": 48.00,
    "Couple Set (Syed + Syeda)": 85.00,
}

def show():
    st.title("📦 Sales Tracker")
    st.caption("Log orders, track revenue, monitor stock")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["➕ New Order", "📋 All Orders", "📈 Revenue Summary"])

    # ── Tab 1: New Order ──────────────────────────────
    with tab1:
        st.subheader("Log a new order")
        with st.form("new_order", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Customer name")
                product = st.selectbox("Product", list(PRODUCTS.keys()))
                qty = st.number_input("Quantity", min_value=1, max_value=100, value=1)
            with col2:
                channel = st.selectbox("Channel", ["Campus pickup", "Shopee", "Instagram DM", "WhatsApp", "Other"])
                status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
                date = st.date_input("Order date", value=datetime.today())

            price = PRODUCTS[product]
            total = price * qty
            st.info(f"Unit price: RM {price:.2f} × {qty} = **RM {total:.2f}**")

            notes = st.text_area("Notes (optional)", placeholder="e.g. pickup at IIUM gate, paid via TNG")
            submitted = st.form_submit_button("Save order", use_container_width=True)

            if submitted:
                if not name:
                    st.error("Please enter customer name.")
                else:
                    sales = load_sales()
                    sales.append({
                        "id": f"ORD{len(sales)+1:04d}",
                        "name": name,
                        "product": product,
                        "qty": qty,
                        "unit_price": price,
                        "total": total,
                        "channel": channel,
                        "status": status,
                        "date": str(date),
                        "notes": notes,
                    })
                    save_sales(sales)
                    st.success(f"Order saved! RM {total:.2f} from {name} ✓")

    # ── Tab 2: All Orders ─────────────────────────────
    with tab2:
        sales = load_sales()
        if not sales:
            st.info("No orders yet. Add your first order above.")
        else:
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed", "Cancelled"])
            with col2:
                filter_channel = st.selectbox("Filter by channel", ["All", "Campus pickup", "Shopee", "Instagram DM", "WhatsApp", "Other"])
            with col3:
                filter_product = st.selectbox("Filter by product", ["All"] + list(PRODUCTS.keys()))

            filtered = sales
            if filter_status != "All":
                filtered = [o for o in filtered if o.get("status") == filter_status]
            if filter_channel != "All":
                filtered = [o for o in filtered if o.get("channel") == filter_channel]
            if filter_product != "All":
                filtered = [o for o in filtered if o.get("product") == filter_product]

            filtered = sorted(filtered, key=lambda x: x.get("date", ""), reverse=True)

            st.caption(f"Showing {len(filtered)} of {len(sales)} orders")

            for o in filtered:
                status_icon = {"Completed": "🟢", "Pending": "🟡", "Cancelled": "🔴"}.get(o.get("status"), "⚪")
                with st.expander(f"{status_icon} {o.get('id')} · {o.get('name')} · RM {o.get('total', 0):.2f} · {o.get('date')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Product:** {o.get('product')}")
                        st.write(f"**Qty:** {o.get('qty')} × RM {o.get('unit_price', 0):.2f}")
                        st.write(f"**Channel:** {o.get('channel')}")
                    with col2:
                        st.write(f"**Status:** {o.get('status')}")
                        st.write(f"**Total:** RM {o.get('total', 0):.2f}")
                        if o.get("notes"):
                            st.write(f"**Notes:** {o.get('notes')}")

                    new_status = st.selectbox("Update status", ["Pending", "Completed", "Cancelled"],
                                              index=["Pending", "Completed", "Cancelled"].index(o.get("status", "Pending")),
                                              key=f"status_{o.get('id')}")
                    if st.button("Update", key=f"update_{o.get('id')}"):
                        all_sales = load_sales()
                        for order in all_sales:
                            if order.get("id") == o.get("id"):
                                order["status"] = new_status
                        save_sales(all_sales)
                        st.success("Updated!")
                        st.rerun()

    # ── Tab 3: Revenue Summary ────────────────────────
    with tab3:
        sales = load_sales()
        if not sales:
            st.info("No data yet.")
        else:
            completed = [o for o in sales if o.get("status") == "Completed"]
            total_rev = sum(o.get("total", 0) for o in completed)
            total_orders = len(completed)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total revenue (completed)", f"RM {total_rev:.2f}")
            col2.metric("Completed orders", total_orders)
            col3.metric("Avg order value", f"RM {(total_rev/max(total_orders,1)):.2f}")

            st.divider()
            st.subheader("Revenue by product")
            product_rev = {}
            for o in completed:
                p = o.get("product", "Unknown")
                product_rev[p] = product_rev.get(p, 0) + o.get("total", 0)

            for product, rev in sorted(product_rev.items(), key=lambda x: x[1], reverse=True):
                pct = rev / max(total_rev, 1)
                st.write(f"**{product}** — RM {rev:.2f}")
                st.progress(pct)

            st.divider()
            st.subheader("Revenue by channel")
            channel_rev = {}
            for o in completed:
                ch = o.get("channel", "Unknown")
                channel_rev[ch] = channel_rev.get(ch, 0) + o.get("total", 0)

            for ch, rev in sorted(channel_rev.items(), key=lambda x: x[1], reverse=True):
                pct = rev / max(total_rev, 1)
                st.write(f"**{ch}** — RM {rev:.2f} ({pct*100:.1f}%)")
                st.progress(pct)
