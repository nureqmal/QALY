import streamlit as st
from datetime import datetime, date, timedelta
from modules.utils import load, save, get_theme_colors, PRODUCTS, MEMBERS

PROD_STATUSES = ["Active", "Completed", "On Hold"]

# ── Default formulas per 1L base ─────────────────────
DEFAULT_FORMULAS = {
    "Qaly (Base)": [
        {"ingredient": "Magnesium Chloride",  "amount": 20.0,  "unit": "g"},
        {"ingredient": "Aloe Vera Extract",   "amount": 25.0,  "unit": "g"},
        {"ingredient": "Dipropylene Glycol",  "amount": 25.0,  "unit": "g"},
        {"ingredient": "Potassium Sorbate",   "amount": 2.0,   "unit": "g"},
        {"ingredient": "Distilled Water",     "amount": 928.0, "unit": "ml", "note": "top up to 1000ml"},
    ],
    "Syed / Syeda / Kimya": [
        {"ingredient": "Magnesium Chloride",  "amount": 20.0,  "unit": "g"},
        {"ingredient": "Aloe Vera Extract",   "amount": 25.0,  "unit": "g"},
        {"ingredient": "Dipropylene Glycol",  "amount": 25.0,  "unit": "g"},
        {"ingredient": "Potassium Sorbate",   "amount": 2.0,   "unit": "g"},
        {"ingredient": "Fragrance Oil",       "amount": 10.0,  "unit": "ml"},
        {"ingredient": "Distilled Water",     "amount": 918.0, "unit": "ml", "note": "top up to 1000ml"},
    ],
}


def show():
    C = get_theme_colors()
    st.markdown("<div class='page-title'>Production</div><div class='page-sub'>Track batches, volumes, and finished stock</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["All Batches", "New Batch", "Formula Calculator"])

    # ══════════════════════════════════════════════════
    # TAB: NEW BATCH
    # ══════════════════════════════════════════════════
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
                        "id":             f"PROD{len(batches)+1:04d}",
                        "batch_no":       batch_no.strip(),
                        "product":        product,
                        "date":           str(prod_date),
                        "volume_L":       volume_L,
                        "units_produced": units,
                        "units_remaining":units,
                        "duration_hrs":   duration_hrs,
                        "pic":            pic,
                        "status":         status,
                        "expiry_date":    str(expiry_date),
                        "notes":          notes.strip(),
                        "recorded_by":    st.session_state.get("current_user", "?"),
                        "created_at":     datetime.now().isoformat(),
                    })
                    save("production.json", batches)
                    st.success(f"Batch {batch_no} recorded — {units} units / {volume_L}L")

    # ══════════════════════════════════════════════════
    # TAB: FORMULA CALCULATOR
    # ══════════════════════════════════════════════════
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)

        # Load saved custom formulas, fallback to defaults
        saved_formulas = load("formulas.json")
        if not saved_formulas:
            saved_formulas = DEFAULT_FORMULAS
            save("formulas.json", saved_formulas)

        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.markdown(f"<div style='font-size:14px;font-weight:600;color:{C['TEXT']};margin-bottom:12px;'>Calculator</div>", unsafe_allow_html=True)

            formula_names = list(saved_formulas.keys())
            selected_formula = st.selectbox("Select formula", formula_names, key="calc_formula")
            target_volume    = st.number_input("Target volume (Litres)", min_value=0.1, value=1.0, step=0.5, key="calc_vol")

            st.markdown(f"""
            <div class="qcard qcard-accent" style="padding:10px 14px;margin-top:.5rem;">
                <div style="font-size:12px;color:{C['TEXT2']};margin-bottom:4px;">Scaling factor</div>
                <div style="font-size:22px;font-weight:800;color:{C['ACCENT']};letter-spacing:-.02em;">{target_volume:.1f}x</div>
                <div style="font-size:11px;color:{C['TEXT3']};margin-top:2px;">Base formula is per 1L</div>
            </div>
            """, unsafe_allow_html=True)

            # Bottles estimate
            bottles_estimate = int(target_volume * 1000 / 100)
            st.markdown(f"""
            <div class="qcard" style="padding:10px 14px;margin-top:8px;">
                <div style="font-size:12px;color:{C['TEXT2']};margin-bottom:4px;">Est. bottles (100ml each)</div>
                <div style="font-size:22px;font-weight:800;color:{C['TEXT']};letter-spacing:-.02em;">{bottles_estimate} units</div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown(f"<div style='font-size:14px;font-weight:600;color:{C['TEXT']};margin-bottom:12px;'>Ingredients needed for {target_volume:.1f}L</div>", unsafe_allow_html=True)

            formula = saved_formulas.get(selected_formula, [])
            if formula:
                colors = ["#7c6fea", "#4ade80", "#f472b6", "#60a5fa", "#fbbf24", "#a99eff", "#34d399"]
                total_weight = sum(
                    ing["amount"] * target_volume
                    for ing in formula
                    if ing["unit"] in ["g", "ml"]
                )

                for i, ing in enumerate(formula):
                    scaled = ing["amount"] * target_volume
                    color  = colors[i % len(colors)]
                    note   = f" — {ing.get('note','')}" if ing.get("note") else ""
                    pct    = (ing["amount"] / max(sum(x["amount"] for x in formula), 1)) * 100

                    st.markdown(f"""
                    <div class="qcard" style="padding:10px 16px;margin-bottom:6px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                            <div>
                                <span style="font-size:13px;font-weight:600;color:{C['TEXT']};">{ing['ingredient']}</span>
                                <span style="font-size:11px;color:{C['TEXT3']};margin-left:8px;">{pct:.1f}% of formula{note}</span>
                            </div>
                            <span style="font-size:16px;font-weight:800;color:{color};">{scaled:.1f} {ing['unit']}</span>
                        </div>
                        <div style="background:{C['BORDER']};border-radius:99px;height:5px;">
                            <div style="background:{color};width:{pct:.0f}%;height:5px;border-radius:99px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="qcard qcard-accent" style="padding:10px 16px;margin-top:4px;">
                    <div style="font-size:12px;color:{C['TEXT2']};">Total measured (excl. top-up water)</div>
                    <div style="font-size:16px;font-weight:700;color:{C['ACCENT']};">{sum(ing['amount'] * target_volume for ing in formula if ing['ingredient'] != 'Distilled Water'):.1f} g/ml</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No ingredients in this formula.")

        # ── Edit / Add formula ────────────────────────
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:14px;font-weight:600;color:{C['TEXT']};margin-bottom:8px;'>Manage Formulas</div>", unsafe_allow_html=True)

        

        with st.expander("Edit existing formula", expanded=True):
            edit_formula_name = st.selectbox("Formula to edit", list(saved_formulas.keys()), key="edit_fname")
            edit_formula      = saved_formulas.get(edit_formula_name, [])

            # Show current ingredients with remove option
            if edit_formula:
                st.markdown(f"<div style='font-size:12px;color:{C['TEXT2']};margin-bottom:8px;'>Current ingredients (per 1L)</div>", unsafe_allow_html=True)
                for idx, ing in enumerate(edit_formula):
                    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                    with c1: st.markdown(f"<div style='padding:8px 0;font-size:13px;color:{C['TEXT']};'>{ing['ingredient']}</div>", unsafe_allow_html=True)
                    with c2: st.markdown(f"<div style='padding:8px 0;font-size:13px;color:{C['ACCENT']};font-weight:600;'>{ing['amount']} {ing['unit']}</div>", unsafe_allow_html=True)
                    with c3: st.markdown(f"<div style='padding:8px 0;font-size:11px;color:{C['TEXT3']};'>{ing.get('note','')}</div>", unsafe_allow_html=True)
                    with c4:
                        if st.button("Remove", key=f"rem_ing_{edit_formula_name}_{idx}_{ing['ingredient'][:4]}", use_container_width=True):
                            saved_formulas[edit_formula_name] = [x for j, x in enumerate(edit_formula) if j != idx]
                            save("formulas.json", saved_formulas)
                            st.success(f"Removed {ing['ingredient']}")
                            st.rerun()

            # Add ingredient to existing formula
            st.markdown(f"<div style='font-size:12px;color:{C['TEXT2']};margin:12px 0 8px;'>Add ingredient to this formula</div>", unsafe_allow_html=True)
            with st.form(f"add_ing_{edit_formula_name}", clear_on_submit=True):
                c1, c2, c3, c4 = st.columns([3, 1.5, 1, 2])
                with c1: ing_name   = st.text_input("Ingredient", placeholder="e.g. Vitamin E")
                with c2: ing_amount = st.number_input("Amount (per 1L)", min_value=0.0, step=0.1)
                with c3: ing_unit   = st.selectbox("Unit", ["g", "ml", "drop"])
                with c4: ing_note   = st.text_input("Note (optional)", placeholder="e.g. top up to 1000ml")
                if st.form_submit_button("Add Ingredient", use_container_width=True):
                    if ing_name.strip() and ing_amount > 0:
                        new_ing = {"ingredient": ing_name.strip(), "amount": ing_amount, "unit": ing_unit}
                        if ing_note.strip():
                            new_ing["note"] = ing_note.strip()
                        saved_formulas.setdefault(edit_formula_name, []).append(new_ing)
                        save("formulas.json", saved_formulas)
                        st.success(f"Added {ing_name} to {edit_formula_name}!")
                        st.rerun()
                    else:
                        st.error("Ingredient name and amount required.")

        with st.expander("Add new formula"):
            with st.form("new_formula_form", clear_on_submit=True):
                new_fname = st.text_input("Formula name *", placeholder="e.g. Kimya Special Edition")
                st.markdown(f"<div style='font-size:12px;color:{C['TEXT2']};margin:6px 0;'>You can add ingredients after creating the formula.</div>", unsafe_allow_html=True)
                if st.form_submit_button("Create Formula", use_container_width=True):
                    if new_fname.strip():
                        if new_fname.strip() in saved_formulas:
                            st.error("Formula name already exists.")
                        else:
                            saved_formulas[new_fname.strip()] = []
                            save("formulas.json", saved_formulas)
                            st.success(f"Formula '{new_fname}' created! Go to Edit tab to add ingredients.")
                            st.rerun()
                    else:
                        st.error("Formula name required.")

        # Reset to defaults
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        col_rst, _ = st.columns([1, 3])
        with col_rst:
            if st.button("Reset to default formulas", use_container_width=True):
                save("formulas.json", DEFAULT_FORMULAS)
                st.success("Reset to defaults!")
                st.rerun()

    # ══════════════════════════════════════════════════
    # TAB: ALL BATCHES
    # ══════════════════════════════════════════════════
    with tab1:
        batches = load("production.json")
        if not batches:
            st.info("No production batches yet. Add your first batch.")
            return

        active      = [b for b in batches if b.get("status") == "Active"]
        total_L     = sum(b.get("volume_L", 0) for b in batches)
        total_units = sum(b.get("units_produced", 0) for b in batches)
        remaining   = sum(b.get("units_remaining", 0) for b in batches if b.get("status") == "Active")

        col1, col2, col3, col4 = st.columns(4)
        for col, (label, val) in zip([col1, col2, col3, col4], [
            ("TOTAL BATCHES",  str(len(batches))),
            ("ACTIVE BATCHES", str(len(active))),
            ("TOTAL VOLUME",   f"{total_L:.1f} L"),
            ("UNITS IN STOCK", str(remaining)),
        ]):
            with col:
                st.markdown(f'<div class="qcard"><div class="kpi-label">{label}</div><div class="kpi-value" style="font-size:22px;">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1: f_product = st.selectbox("Filter product", ["All"] + list(PRODUCTS.keys()), key="fprod")
        with col2: f_status  = st.selectbox("Filter status",  ["All"] + PROD_STATUSES,         key="fstat")

        filtered = batches
        if f_product != "All": filtered = [b for b in filtered if b.get("product") == f_product]
        if f_status  != "All": filtered = [b for b in filtered if b.get("status")  == f_status]
        filtered = sorted(filtered, key=lambda x: x.get("date", ""), reverse=True)

        for b in filtered:
            bc          = {"Active": "badge-green", "Completed": "badge-purple", "On Hold": "badge-yellow"}.get(b.get("status", ""), "badge-blue")
            remaining_b = b.get("units_remaining", b.get("units_produced", 0))
            produced    = b.get("units_produced", 0)
            sold_pct    = (1 - remaining_b / max(produced, 1)) * 100

            with st.expander(f"Batch {b.get('batch_no','?')}  ·  {b.get('product','?')}  ·  {b.get('date','?')}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Product:** {b.get('product')}")
                    st.write(f"**Volume:** {b.get('volume_L', 0)} L")
                    st.write(f"**Units produced:** {produced}")
                    st.write(f"**Units remaining:** {remaining_b}")
                with col2:
                    st.write(f"**Duration:** {b.get('duration_hrs', 0)} hrs")
                    st.write(f"**PIC:** {', '.join(b.get('pic', [])) or '—'}")
                    st.write(f"**Expiry:** {b.get('expiry_date', '—')}")
                    st.write(f"**Recorded by:** {b.get('recorded_by', '?')}")
                with col3:
                    st.markdown(f'<span class="badge {bc}">{b.get("status")}</span>', unsafe_allow_html=True)
                    st.write(f"**Sold:** {sold_pct:.0f}%")
                    if b.get("notes"):
                        st.write(f"**Notes:** {b.get('notes')}")

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
                                              index=PROD_STATUSES.index(b.get("status", "Active")),
                                              key=f"pst_{b['id']}")
                with col_c:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Update", key=f"pbtn_{b['id']}", use_container_width=True):
                        all_b = load("production.json")
                        for batch in all_b:
                            if batch["id"] == b["id"]:
                                batch["units_remaining"] = new_remaining
                                batch["status"]          = new_status
                                if new_remaining == 0:
                                    batch["status"] = "Completed"
                        save("production.json", all_b)
                        st.success("Updated!")
                        st.rerun()
