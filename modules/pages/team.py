import streamlit as st
import json, os
from datetime import datetime, date

TASKS_FILE = "data/tasks.json"
NOTES_FILE = "data/notes.json"

def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def save_json(path, data):
    os.makedirs("data", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

MEMBERS = ["Qaly (Founder)", "SV", "Master 1", "Master 2"]

def show():
    st.title("👥 Team Hub")
    st.caption("Tasks, notes, and team goals — all in one place")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["✅ Task Board", "📝 Meeting Notes", "🎯 Weekly Goals"])

    # ── Tab 1: Task Board ─────────────────────────────
    with tab1:
        st.subheader("Task board")

        with st.form("new_task", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                task_title = st.text_input("Task", placeholder="e.g. Post 3 IG captions this week")
            with col2:
                assigned = st.selectbox("Assigned to", MEMBERS)
                priority = st.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"])
            with col3:
                due = st.date_input("Due date", value=datetime.today())
                category = st.selectbox("Category", ["Marketing", "Sales", "Operations", "R&D", "Other"])

            if st.form_submit_button("Add task", use_container_width=True):
                if task_title:
                    tasks = load_json(TASKS_FILE)
                    tasks.append({
                        "id": f"T{len(tasks)+1:03d}",
                        "title": task_title,
                        "assigned": assigned,
                        "priority": priority,
                        "due": str(due),
                        "category": category,
                        "done": False,
                        "created": str(datetime.today().date()),
                    })
                    save_json(TASKS_FILE, tasks)
                    st.success("Task added!")
                    st.rerun()

        st.divider()
        tasks = load_json(TASKS_FILE)
        if not tasks:
            st.info("No tasks yet. Add one above.")
        else:
            filter_member = st.selectbox("Filter by member", ["All"] + MEMBERS)
            filter_done = st.radio("Show", ["Active", "Completed", "All"], horizontal=True)

            filtered = tasks
            if filter_member != "All":
                filtered = [t for t in filtered if t.get("assigned") == filter_member]
            if filter_done == "Active":
                filtered = [t for t in filtered if not t.get("done")]
            elif filter_done == "Completed":
                filtered = [t for t in filtered if t.get("done")]

            filtered = sorted(filtered, key=lambda x: x.get("due", ""))

            for t in filtered:
                col1, col2, col3 = st.columns([0.05, 0.75, 0.2])
                with col1:
                    done = st.checkbox("", value=t.get("done", False), key=f"done_{t['id']}")
                    if done != t.get("done"):
                        all_tasks = load_json(TASKS_FILE)
                        for task in all_tasks:
                            if task["id"] == t["id"]:
                                task["done"] = done
                        save_json(TASKS_FILE, all_tasks)
                        st.rerun()
                with col2:
                    title_style = "~~" if t.get("done") else ""
                    st.markdown(f"{t.get('priority', '')} {title_style}**{t.get('title')}**{title_style}  \n`{t.get('assigned')}` · {t.get('category')} · Due {t.get('due')}")
                with col3:
                    if st.button("🗑️", key=f"del_{t['id']}"):
                        all_tasks = load_json(TASKS_FILE)
                        all_tasks = [task for task in all_tasks if task["id"] != t["id"]]
                        save_json(TASKS_FILE, all_tasks)
                        st.rerun()
                st.divider()

    # ── Tab 2: Meeting Notes ──────────────────────────
    with tab2:
        st.subheader("Meeting notes")

        with st.form("new_note", clear_on_submit=True):
            note_title = st.text_input("Meeting title", placeholder="e.g. Weekly sync 12 May")
            note_content = st.text_area("Notes", placeholder="Key discussion points, decisions, action items...", height=150)
            note_date = st.date_input("Date", value=datetime.today())

            if st.form_submit_button("Save notes", use_container_width=True):
                if note_title and note_content:
                    notes = load_json(NOTES_FILE)
                    notes.append({
                        "id": f"N{len(notes)+1:03d}",
                        "title": note_title,
                        "content": note_content,
                        "date": str(note_date),
                    })
                    save_json(NOTES_FILE, notes)
                    st.success("Notes saved!")
                    st.rerun()

        st.divider()
        notes = load_json(NOTES_FILE)
        if not notes:
            st.info("No notes yet.")
        else:
            for n in sorted(notes, key=lambda x: x.get("date", ""), reverse=True):
                with st.expander(f"📝 {n.get('title')} — {n.get('date')}"):
                    st.write(n.get("content"))
                    if st.button("🗑️ Delete", key=f"delnote_{n['id']}"):
                        all_notes = load_json(NOTES_FILE)
                        all_notes = [note for note in all_notes if note["id"] != n["id"]]
                        save_json(NOTES_FILE, all_notes)
                        st.rerun()

    # ── Tab 3: Weekly Goals ───────────────────────────
    with tab3:
        st.subheader("This week's goals")

        if "weekly_goals" not in st.session_state:
            st.session_state.weekly_goals = [
                {"goal": "Post 3 times on Instagram", "done": False},
                {"goal": "Get 5 new orders", "done": False},
                {"goal": "Reply all customer DMs within 24h", "done": False},
                {"goal": "Update Shopee listing with new photos", "done": False},
            ]

        for i, g in enumerate(st.session_state.weekly_goals):
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                checked = st.checkbox("", value=g["done"], key=f"goal_{i}")
                st.session_state.weekly_goals[i]["done"] = checked
            with col2:
                style = "~~" if g["done"] else ""
                st.markdown(f"{style}{g['goal']}{style}")

        done_count = sum(1 for g in st.session_state.weekly_goals if g["done"])
        total = len(st.session_state.weekly_goals)
        st.progress(done_count / max(total, 1), text=f"{done_count}/{total} goals completed this week")

        st.divider()
        new_goal = st.text_input("Add a goal", placeholder="e.g. Send 10 samples to micro-influencers")
        if st.button("Add goal") and new_goal:
            st.session_state.weekly_goals.append({"goal": new_goal, "done": False})
            st.rerun()
