import streamlit as st
from datetime import datetime, date, timedelta
from modules.utils import load, save, get_theme_colors, PRODUCTS, MEMBERS

PROD_STATUSES = ["Active", "Completed", "On Hold"]

def show():
    C = get_theme_colors()
    st.markdown(f"<div class='page-title'>Production</div><div class='page-sub'>Track batches, volumes, and finished stock</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["All Batches", "New Batch"])

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("prod_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                product      = st.selectbox("Product", list(PRODUCTS.keys()))
                batch_no     = st.text_input("Batch No.", placeholder="e.g. B001 or 2025-05-001")
                prod_date    = st.date_input("Production Date", value=date.today())
                volume_L     = st.number_input("Volume produced (Litres)", min_value=0.0, step=0.1)
                units        = st.number_input("Units produced (bottles)", min_value=0, step=1)
            with col2:
                duration_hrs = st.number_input("Duration (hours)", min_value=0.0, step=0.5)
                pic          = st.multiselect("Person-in-Charge", MEMBERS)
                status       = st.selectbox("Batch Status", PROD_STATUSES)
                expiry_date  = st.date_input("Expiry / Best Before", value=date.today() + timedelta(days=365))
                notes        = st.text_area("Notes / Observations", height=90, placeholder="Any issues, adjustments, QC notes...")

            st.markdown(f"""
            <div class="qcard" style="padding:10px 14px;margin-top:.5rem;">
                <span style="font-size:12px;color:{C['TEXT2']};">Est. yield per litre: </span>
                <span style="font-weight:700;color:{C['TEXT']};">{(units/volume_L if volume_L>0 else 0):.1f} bottles/L</span>
            </div>
            """, unsafe_allow_html=True)

            if st.form_submit_button("Record Batch", use_container_width=True):
                if not batch_no.strip():
                    st.error("Batch number is required.")
                else:
                    batches = load("production.json")
                    batches.append({
                        "id":            f"PROD{len(batches)+1:04d}",
                        "batch_no":      batch_no.strip(),
                        "product":       product,
                        "date":          str(prod_date),
                        "volume_L":      volume_L,
                        "units_produced":units,
                        "units_remaining":units,
                        "duration_hrs":  duration_hrs,
                        "pic":           pic,
                        "status":        status,
                        "expiry_date":   str(expiry_date),
                        "notes":         notes.strip(),
                        "recorded_by":   st.session_state.get("current_user","?"),
                        "created_at":    datetime.now().isoformat(),
                    })
                    save("production.json", batches)
                    st.success(f"Batch {batch_no} recorded — {units} units / {volume_L}L")

    with tab1:
        batches = load("production.json")

        if not batches:
            st.info("No production batches yet. Add your first batch.")
            return

        # Summary KPIs
        active    = [b for b in batches if b.get("status")=="Active"]
        completed = [b for b in batches if b.get("status")=="Completed"]
        total_L   = sum(b.get("volume_L",0) for b in batches)
        total_units = sum(b.get("units_produced",0) for b in batches)
        remaining   = sum(b.get("units_remaining",0) for b in batches if b.get("status")=="Active")

        col1,col2,col3,col4 = st.columns(4)
        for col,(label,val) in zip([col1,col2,col3,col4],[
            ("TOTAL BATCHES",   str(len(batches))),
            ("ACTIVE BATCHES",  str(len(active))),
            ("TOTAL VOLUME",    f"{total_L:.1f} L"),
            ("UNITS IN STOCK",  str(remaining)),
        ]):
            with col:
                st.markdown(f'<div class="qcard"><div class="kpi-label">{label}</div><div class="kpi-value" style="font-size:22px;">{val}</div></div>', unsafe_allow_html=True)

        st.markdown(f"<div class='divider'></div>", unsafe_allow_html=True)

        # Filter
        col1,col2 = st.columns(2)
        with col1: f_product = st.selectbox("Filter product", ["All"]+list(PRODUCTS.keys()), key="fprod")
        with col2: f_status  = st.selectbox("Filter status",  ["All"]+PROD_STATUSES,         key="fstat")

        filtered = batches
        if f_product!="All": filtered=[b for b in filtered if b.get("product")==f_product]
        if f_status !="All": filtered=[b for b in filtered if b.get("status") ==f_status]
        filtered = sorted(filtered, key=lambda x: x.get("date",""), reverse=True)

        for b in filtered:
            bc = {"Active":"badge-green","Completed":"badge-purple","On Hold":"badge-yellow"}.get(b.get("status",""),"badge-blue")
            remaining_b = b.get("units_remaining", b.get("units_produced",0))
            produced    = b.get("units_produced",0)
            sold_pct    = (1 - remaining_b/max(produced,1))*100

            with st.expander(f"Batch {b.get('batch_no','?')}  ·  {b.get('product','?')}  ·  {b.get('date','?')}"):
                col1,col2,col3 = st.columns(3)
                with col1:
                    st.write(f"**Product:** {b.get('product')}")
                    st.write(f"**Volume:** {b.get('volume_L',0)} L")
                    st.write(f"**Units produced:** {produced}")
                    st.write(f"**Units remaining:** {remaining_b}")
                with col2:
                    st.write(f"**Duration:** {b.get('duration_hrs',0)} hrs")
                    st.write(f"**PIC:** {', '.join(b.get('pic',[])) or '—'}")
                    st.write(f"**Expiry:** {b.get('expiry_date','—')}")
                    st.write(f"**Recorded by:** {b.get('recorded_by','?')}")
                with col3:
                    st.markdown(f'<span class="badge {bc}">{b.get("status")}</span>', unsafe_allow_html=True)
                    st.write(f"**Sold:** {sold_pct:.0f}%")
                    if b.get("notes"):
                        st.write(f"**Notes:** {b.get('notes')}")

                # Stock depletion bar
                st.markdown(f"""
                <div style="margin:8px 0 4px;">
                    <div style="font-size:11px;color:{C['TEXT2']};margin-bottom:4px;">Stock remaining: {remaining_b}/{produced} units</div>
                    <div style="background:{C['BORDER']};border-radius:99px;height:8px;">
                        <div style="background:{C['ACCENT']};width:{(remaining_b/max(produced,1))*100:.0f}%;height:8px;border-radius:99px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    new_remaining = st.number_input("Update units remaining", min_value=0, max_value=produced,
                                                    value=remaining_b, key=f"rem_{b['id']}")
                with col_b:
                    new_status = st.selectbox("Update status", PROD_STATUSES,
                                              index=PROD_STATUSES.index(b.get("status","Active")),
                                              key=f"pst_{b['id']}")
                with col_c:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Update", key=f"pbtn_{b['id']}", use_container_width=True):
                        all_b = load("production.json")
                        for batch in all_b:
                            if batch["id"]==b["id"]:
                                batch["units_remaining"] = new_remaining
                                batch["status"]          = new_status
                                if new_remaining==0: batch["status"] = "Completed"
                        save("production.json", all_b)
                        st.success("Updated!")
                        st.rerun()
