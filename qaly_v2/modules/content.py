import streamlit as st
from datetime import datetime, timedelta, date
from modules.utils import load, save

PILLARS = ["Educate 🧪", "Personalise ✨", "Local Pride 🇲🇾", "Social Proof 💬", "Promo 🔥", "Behind the Scenes 📸"]
POST_TYPES = ["Reel", "Carousel", "Single Post", "Story", "TikTok"]
PLATFORMS = ["Instagram", "TikTok", "Both"]
STATUS_OPTS = ["Idea", "In Progress", "Ready to Post", "Posted"]


def render_post_card(p):
    status = p.get("status", "")
    badge = "badge-green" if status == "Posted" else "badge-yellow" if status in ["In Progress", "Ready to Post"] else "badge-purple"
    return (
        f'<div style="background:#f5f4ff;border-radius:10px;padding:8px 12px;margin-bottom:6px;font-size:13px;">'
        f'<span style="color:#534AB7;font-weight:500;">{p.get("type","")} · {p.get("pillar","")}</span><br>'
        f'<span style="color:#1a1440;">{p.get("title","")}</span>'
        f'<span class="badge {badge}" style="margin-left:8px;">{status}</span>'
        f'</div>'
    )


def show():
    st.markdown("<div class='section-title'>Content Planner</div><div class='section-sub'>Plan, schedule, and track your social media content</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📅  Content Calendar", "➕  Add Content", "💡  Caption Bank"])

    with tab1:
        posts = load("content.json")
        col1, col2 = st.columns([3, 1])
        with col1:
            week_start = st.date_input("Week starting", value=date.today() - timedelta(days=date.today().weekday()))
        with col2:
            pillar_filter = st.selectbox("Filter pillar", ["All"] + PILLARS)

        week_end = week_start + timedelta(days=6)
        week_posts = [p for p in posts if week_start.isoformat() <= p.get("date", "") <= week_end.isoformat()]
        if pillar_filter != "All":
            week_posts = [p for p in week_posts if p.get("pillar") == pillar_filter]

        st.markdown(
            f"<div style='font-size:13px;color:#9591b8;margin:0.5rem 0 1rem;'>"
            f"Week of {week_start.strftime('%d %b')} – {week_end.strftime('%d %b %Y')} · {len(week_posts)} posts planned</div>",
            unsafe_allow_html=True
        )

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days):
            day_date = week_start + timedelta(days=i)
            day_posts = [p for p in week_posts if p.get("date") == day_date.isoformat()]
            is_today = day_date == date.today()

            border = "border:2px solid #534AB7;" if is_today else "border:1px solid #f0eeff;"
            bg = "background:linear-gradient(135deg,#f8f7ff,white);" if is_today else "background:white;"
            title_color = "#534AB7" if is_today else "#1a1440"
            today_label = " · Today" if is_today else ""

            badge_html = ""
            if day_posts:
                count = len(day_posts)
                plural = "s" if count > 1 else ""
                badge_html = f'<span class="badge badge-purple">{count} post{plural}</span>'

            posts_html = "".join([render_post_card(p) for p in day_posts]) if day_posts else '<div style="font-size:12px;color:#c8c2e8;">No posts planned</div>'

            st.markdown(
                f'<div style="{bg}{border}border-radius:14px;padding:14px 18px;margin-bottom:10px;">'
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:{"10px" if day_posts else "0"};">'
                f'<div style="font-size:13px;font-weight:600;color:{title_color};">{day}{today_label}</div>'
                f'<div style="font-size:12px;color:#b0aad0;">{day_date.strftime("%d %b")}</div>'
                f'{badge_html}</div>'
                f'{posts_html}</div>',
                unsafe_allow_html=True
            )

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("content_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Post Title / Idea *", placeholder="e.g. Why we use magnesium chloride")
                pillar = st.selectbox("Content Pillar", PILLARS)
                post_type = st.selectbox("Post Type", POST_TYPES)
                platform = st.selectbox("Platform", PLATFORMS)
            with col2:
                post_date = st.date_input("Planned Date", value=date.today())
                post_status = st.selectbox("Status", STATUS_OPTS)
                assigned = st.selectbox("Assigned to", ["Founder", "SV", "Master 1", "Master 2", "Whole Team"])
                caption = st.text_area("Caption / Notes", placeholder="Write caption here or add notes...", height=110)

            if st.form_submit_button("📌  Add to Calendar", use_container_width=True):
                if not title.strip():
                    st.error("Post title is required.")
                else:
                    all_posts = load("content.json")
                    all_posts.append({
                        "id": f"P{len(all_posts)+1:03d}",
                        "title": title.strip(),
                        "pillar": pillar,
                        "type": post_type,
                        "platform": platform,
                        "date": post_date.isoformat(),
                        "status": post_status,
                        "assigned": assigned,
                        "caption": caption.strip(),
                        "created": datetime.now().isoformat(),
                    })
                    save("content.json", all_posts)
                    st.success(f"'{title}' added to {post_date.strftime('%d %b %Y')}!")

        st.markdown("<div class='qdivider'></div>", unsafe_allow_html=True)
        st.markdown("**All planned content**")
        all_posts = load("content.json")
        if all_posts:
            for p in sorted(all_posts, key=lambda x: x.get("date", ""), reverse=True):
                sc = {"Posted": "badge-green", "Ready to Post": "badge-green", "In Progress": "badge-yellow", "Idea": "badge-purple"}.get(p.get("status", ""), "badge-purple")
                with st.expander(f"**{p.get('title')}** · {p.get('date')} · {p.get('type')}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Pillar:** {p.get('pillar')}")
                        st.write(f"**Platform:** {p.get('platform')}")
                        st.write(f"**Assigned:** {p.get('assigned')}")
                    with c2:
                        st.write(f"**Status:** {p.get('status')}")
                        st.write(f"**Date:** {p.get('date')}")
                    if p.get("caption"):
                        st.text_area("Caption", value=p.get("caption"), height=100, key=f"cap_{p['id']}", disabled=True)

                    new_status = st.selectbox("Update status", STATUS_OPTS,
                                              index=STATUS_OPTS.index(p.get("status", "Idea")),
                                              key=f"pstatus_{p['id']}")
                    if st.button("Update", key=f"pbtn_{p['id']}"):
                        updated = load("content.json")
                        for post in updated:
                            if post["id"] == p["id"]:
                                post["status"] = new_status
                        save("content.json", updated)
                        st.success("Updated!")
                        st.rerun()
        else:
            st.info("No content planned yet.")

    with tab3:
        st.markdown("**Ready-to-use captions for Qaly**")
        st.caption("Copy any caption directly into Instagram or TikTok.")

        captions = [
            {
                "title": "The Aluminium Truth",
                "pillar": "Educate 🧪",
                "text": "Your deodorant might be working against you.\n\nMost conventional deodorants use aluminium to block your sweat glands — literally plugging them shut.\n\nThe problem? Sweat is how your body regulates temperature and flushes toxins. Blocking it completely isn't freshness. It's interference.\n\nQaly works differently. Our magnesium chloride formula neutralises odour-causing bacteria — without touching your sweat glands. You sweat naturally. You just don't smell.\n\nNo aluminium. No paraben. No interference.\n\n#naturaldeodorant #aluminiumfree #halalbeauty #cleanbeauty #malaysiamade #qaly",
            },
            {
                "title": "Your Scent, Not Ours",
                "pillar": "Personalise ✨",
                "text": "Every other deodorant tells you what to smell like.\n\nQaly doesn't.\n\nOur base is fragrance-free — spray your own perfume in, and your deodorant finally smells like you. Not like a brand. Not like everyone else.\n\nYour identity. Your rules. Your scent.\n\nQaly — Your Signature Scent. 🧪\n\n#signaturescent #personalised #halaldeodorant #qaly #cleanbeauty #malaysiamade",
            },
            {
                "title": "Made By Researchers",
                "pillar": "Local Pride 🇲🇾",
                "text": "Most deodorants are made in a factory. Ours was made in a lab — by actual researchers.\n\nQaly was formulated by chemistry PhD & Master's researchers right here in Malaysia. Every ingredient was chosen based on evidence, not trend.\n\n✓ Magnesium chloride — proven antibacterial\n✓ Aloe vera — soothing skin-safe carrier\n✓ No aluminium. No paraben.\n\nWe didn't guess. We researched it.\n\n#malaysiamade #halalbeauty #localmalaysia #phdresearch #qaly #cleanformula",
            },
            {
                "title": "Still Smelling Bad?",
                "pillar": "Educate 🧪",
                "text": "Still smelling bad even with deodorant on? Here's why.\n\nMost deodorants mask odour with fragrance. When the scent fades — the smell comes back. Because they never solved the actual problem.\n\nBody odour isn't from sweat — it's from bacteria breaking sweat down. No bacteria = no smell.\n\nQaly's magnesium chloride targets exactly that. One spray keeps you fresh through everything.\n\nScience first. Fragrance — yours.\n\n#bodyodour #naturaldeodorant #halalcosmetics #qaly #cleanbeauty",
            },
            {
                "title": "Couple Set",
                "pillar": "Promo 🔥",
                "text": "Him. Her. Both sorted. 💜\n\nIntroducing our Couple Set — Syed for him, Syeda for her. Both aluminium-free, paraben-free, and halal.\n\nPerfect as a gift. Even better as a daily duo.\n\nGrab yours at the link in bio 👆\n\n#qaly #couplegoals #halalbeauty #giftidea #malaysiamade #naturaldeodorant",
            },
        ]

        for cap in captions:
            with st.expander(f"**{cap['title']}** · {cap['pillar']}"):
                st.text_area("Caption", value=cap["text"], height=200, key=f"bank_{cap['title']}")
                st.caption("Select all text above → Ctrl+A → Ctrl+C to copy")
