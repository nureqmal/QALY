import streamlit as st
from datetime import datetime, date, timedelta
from modules.utils import load, save, MEMBERS

PRIORITIES = ["🔴 High", "🟡 Medium", "🟢 Low"]
CATEGORIES = ["Marketing", "Sales", "Operations", "R&D", "Finance", "Other"]
TASK_STATUSES = ["To Do", "In Progress", "Done"]

def show():
    st.markdown("<div class='section-title'>Team Hub</div><div class='section-sub'>Tasks, notes, and goals — your team in sync</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["✅  Task Board", "📝  Meeting Notes", "🎯  Goals Tracker"])

    # ── TASK BOARD ────────────────────────────────────
    with tab1:
        col_form, col_board = st.columns([1, 2])

        with col_form:
            st.markdown("**Add new task**")
            with st.form("task_form", clear_on_submit=True):
                title = st.text_input("Task *", placeholder="e.g. Post 3 captions this week")
                assigned = st.selectbox("Assign to", MEMBERS)
                priority = st.selectbox("Priority", PRIORITIES)
                category = st.selectbox("Category", CATEGORIES)
                due = st.date_input("Due date", value=date.today() + timedelta(days=3))

                if st.form_submit_button("Add Task", use_container_width=True):
                    if title.strip():
                        tasks = load("tasks.json")
                        tasks.append({
                            "id": f"T{len(tasks)+1:03d}",
                            "title": title.strip(),
                            "assigned": assigned,
                            "priority": priority,
                            "category": category,
                            "due": str(due),
                            "status": "To Do",
                            "created": datetime.now().isoformat(),
                        })
                        save("tasks.json", tasks)
                        st.success("Task added!")
                        st.rerun()
                    else:
                        st.error("Task title required.")

        with col_board:
            tasks = load("tasks.json")
            active = [t for t in tasks if t.get("status") != "Done"]
            done_tasks = [t for t in tasks if t.get("status") == "Done"]

            # Filter
            member_filter = st.selectbox("Filter by member", ["All"] + MEMBERS, key="tmember")
            if member_filter != "All":
                active = [t for t in active if t.get("assigned") == member_filter]
                done_tasks = [t for t in done_tasks if t.get("assigned") == member_filter]

            # Stats
            st.markdown(f"""
            <div style="display:flex;gap:10px;margin-bottom:1rem;flex-wrap:wrap;">
                <div style="background:#fef9e7;border-radius:10px;padding:6px 14px;font-size:13px;color:#926b00;font-weight:500;">{len([t for t in active if t.get('status')=='To Do'])} To Do</div>
                <div style="background:#eff6ff;border-radius:10px;padding:6px 14px;font-size:13px;color:#1d4ed8;font-weight:500;">{len([t for t in active if t.get('status')=='In Progress'])} In Progress</div>
                <div style="background:#e8faf2;border-radius:10px;padding:6px 14px;font-size:13px;color:#0d7a4e;font-weight:500;">{len(done_tasks)} Done</div>
            </div>
            """, unsafe_allow_html=True)

            for t in sorted(active, key=lambda x: x.get("due", "")):
                overdue = t.get("due","") < str(date.today()) and t.get("status") != "Done"
                border_color = "#dc2626" if overdue else "#f0eeff"
                with st.container():
                    st.markdown(f"""
                    <div style="background:white;border:1px solid {border_color};border-radius:12px;padding:12px 16px;margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                            <div style="flex:1;">
                                <div style="font-size:14px;font-weight:600;color:#1a1440;margin-bottom:4px;">{t.get('title')}</div>
                                <div style="font-size:12px;color:#9591b8;">{t.get('priority')} · {t.get('category')} · {t.get('assigned')} · Due {t.get('due')}{'  ⚠️ OVERDUE' if overdue else ''}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2, c3 = st.columns([2,1,1])
                    with c1:
                        new_status = st.selectbox("", TASK_STATUSES,
                                                  index=TASK_STATUSES.index(t.get("status","To Do")),
                                                  key=f"ts_{t['id']}", label_visibility="collapsed")
                    with c2:
                        if st.button("Update", key=f"tu_{t['id']}", use_container_width=True):
                            all_tasks = load("tasks.json")
                            for task in all_tasks:
                                if task["id"] == t["id"]:
                                    task["status"] = new_status
                            save("tasks.json", all_tasks)
                            st.rerun()
                    with c3:
                        if st.button("🗑️", key=f"td_{t['id']}", use_container_width=True):
                            all_tasks = load("tasks.json")
                            all_tasks = [task for task in all_tasks if task["id"] != t["id"]]
                            save("tasks.json", all_tasks)
                            st.rerun()

            if done_tasks:
                with st.expander(f"✅ Completed tasks ({len(done_tasks)})"):
                    for t in done_tasks[-10:]:
                        st.markdown(f"~~{t.get('title')}~~ · {t.get('assigned')} · {t.get('due')}")

    # ── MEETING NOTES ─────────────────────────────────
    with tab2:
        col1, col2 = st.columns([1, 1.5])

        with col1:
            st.markdown("**New meeting note**")
            with st.form("note_form", clear_on_submit=True):
                note_title = st.text_input("Meeting title *", placeholder="e.g. Weekly sync")
                note_date = st.date_input("Date", value=date.today())
                attendees = st.multiselect("Attendees", MEMBERS, default=MEMBERS)
                agenda = st.text_area("Agenda / Discussion", height=100)
                decisions = st.text_area("Decisions made", height=80)
                action_items = st.text_area("Action items", placeholder="1. [Name] will do X by [date]", height=80)

                if st.form_submit_button("Save Notes", use_container_width=True):
                    if note_title.strip():
                        notes = load("notes.json")
                        notes.append({
                            "id": f"N{len(notes)+1:03d}",
                            "title": note_title.strip(),
                            "date": str(note_date),
                            "attendees": attendees,
                            "agenda": agenda,
                            "decisions": decisions,
                            "action_items": action_items,
                        })
                        save("notes.json", notes)
                        st.success("Notes saved!")
                        st.rerun()
                    else:
                        st.error("Title required.")

        with col2:
            st.markdown("**Previous meetings**")
            notes = load("notes.json")
            if notes:
                for n in sorted(notes, key=lambda x: x.get("date",""), reverse=True):
                    with st.expander(f"📝 **{n.get('title')}** · {n.get('date')}"):
                        st.markdown(f"**Attendees:** {', '.join(n.get('attendees',[]))}")
                        if n.get("agenda"): st.markdown(f"**Discussion:**\n{n.get('agenda')}")
                        if n.get("decisions"): st.markdown(f"**Decisions:**\n{n.get('decisions')}")
                        if n.get("action_items"): st.markdown(f"**Action items:**\n{n.get('action_items')}")
            else:
                st.info("No notes yet.")

    # ── GOALS TRACKER ─────────────────────────────────
    with tab3:
        st.markdown("**Weekly Goals**")
        goals = load("goals.json")

        # Add goal
        with st.form("goal_form", clear_on_submit=True):
            col1, col2, col3 = st.columns([3,1,1])
            with col1:
                new_goal = st.text_input("New goal", placeholder="e.g. Get 10 new orders this week", label_visibility="collapsed")
            with col2:
                goal_owner = st.selectbox("Owner", MEMBERS, label_visibility="collapsed")
            with col3:
                if st.form_submit_button("Add", use_container_width=True):
                    if new_goal.strip():
                        goals.append({"id": f"G{len(goals)+1:03d}", "goal": new_goal.strip(), "owner": goal_owner, "done": False, "week": str(date.today())})
                        save("goals.json", goals)
                        st.rerun()

        if goals:
            done_count = sum(1 for g in goals if g.get("done"))
            total_g = len(goals)
            pct = done_count / max(total_g, 1)

            st.markdown(f"""
            <div style="background:white;border:1px solid #f0eeff;border-radius:14px;padding:1rem 1.4rem;margin:0.5rem 0 1rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div style="font-size:14px;font-weight:600;color:#1a1440;">Overall Progress</div>
                    <div style="font-size:14px;font-weight:700;color:#534AB7;">{done_count}/{total_g} done</div>
                </div>
                <div style="background:#f0eeff;border-radius:99px;height:10px;">
                    <div style="background:linear-gradient(to right,#534AB7,#8B5CF6);width:{pct*100}%;height:10px;border-radius:99px;transition:width 0.5s;"></div>
                </div>
                <div style="font-size:12px;color:#9591b8;margin-top:6px;">{pct*100:.0f}% complete</div>
            </div>
            """, unsafe_allow_html=True)

            for g in goals:
                col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
                with col1:
                    checked = st.checkbox("", value=g.get("done", False), key=f"g_{g['id']}")
                    if checked != g.get("done"):
                        all_goals = load("goals.json")
                        for goal in all_goals:
                            if goal["id"] == g["id"]:
                                goal["done"] = checked
                        save("goals.json", all_goals)
                        st.rerun()
                with col2:
                    style_text = f"~~{g['goal']}~~" if g.get("done") else g["goal"]
                    color = "#9591b8" if g.get("done") else "#1a1440"
                    st.markdown(f"<span style='color:{color};font-size:14px;'>{style_text}</span>  <span style='color:#b0aad0;font-size:12px;'>· {g.get('owner','?')}</span>", unsafe_allow_html=True)
                with col3:
                    if st.button("✕", key=f"gd_{g['id']}"):
                        all_goals = load("goals.json")
                        all_goals = [goal for goal in all_goals if goal["id"] != g["id"]]
                        save("goals.json", all_goals)
                        st.rerun()
        else:
            st.info("No goals set yet. Add your first team goal above.")
