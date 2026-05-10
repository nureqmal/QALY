import streamlit as st
import anthropic

SYSTEM_PROMPT = """You are a market intelligence analyst specializing in the Malaysian personal care and halal beauty market. 
You help Qaly, a local halal deodorant startup, understand their competitive landscape and market opportunities.
Give specific, actionable insights — not generic marketing advice."""

def call_claude(prompt, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

COMPETITORS = {
    "HYGR": {
        "tagline": "Natural deodorant that actually works",
        "price": "RM 25–45",
        "usp": "12-hour protection, no baking soda, eco packaging",
        "platform": "Website, Shopee, Instagram",
        "weakness": "Higher price, no personalisation",
    },
    "Hello Natural Co": {
        "tagline": "High-performance all-natural deodorant",
        "price": "RM 40–70",
        "usp": "For athletes, pregnant women, kids",
        "platform": "Website, Shopee",
        "weakness": "Balm format not for everyone, premium price",
    },
    "Smelly No More": {
        "tagline": "Mineral salt, alcohol-free, halal",
        "price": "RM 20–35",
        "usp": "Halal certified, mineral salt, no synthetic fragrance",
        "platform": "Total Image stores, Shopee",
        "weakness": "Generic scents, older brand image",
    },
    "GoSmell": {
        "tagline": "Personalised scent deodorant",
        "price": "RM 30–55",
        "usp": "Strong lifestyle branding, scent variety",
        "platform": "Instagram, Shopee",
        "weakness": "Not science-led, not halal certified prominently",
    },
}

def show():
    st.title("📊 Market Intel")
    st.caption("Understand your competitors and spot opportunities")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["🏆 Competitor Map", "🔍 AI Analysis", "📌 Opportunities"])

    # ── Tab 1: Competitor Map ─────────────────────────
    with tab1:
        st.subheader("Competitor snapshot")

        for brand, data in COMPETITORS.items():
            with st.expander(f"**{brand}** — {data['tagline']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Price range:** {data['price']}")
                    st.write(f"**USP:** {data['usp']}")
                    st.write(f"**Platforms:** {data['platform']}")
                with col2:
                    st.write(f"**Weakness:** {data['weakness']}")
                    st.markdown("""
                    <div style='background:#f0fdf4;border-left:3px solid #22c55e;padding:8px 12px;border-radius:4px;font-size:13px;color:#166534;'>
                    💡 Qaly advantage: local PhD credibility + blank base personalisation
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()
        st.subheader("Qaly vs competitors — key differentiators")

        comparison_data = {
            "Feature": ["Aluminium-free", "Paraben-free", "Halal", "Local Malaysian brand", "Customisable scent", "PhD-formulated", "Budget-friendly"],
            "Qaly": ["✅", "✅", "✅", "✅", "✅", "✅", "✅"],
            "HYGR": ["✅", "✅", "✅", "✅", "❌", "❌", "⚠️"],
            "Hello Natural": ["✅", "✅", "✅", "✅", "❌", "❌", "❌"],
            "Smelly No More": ["✅", "✅", "✅", "❌", "❌", "❌", "✅"],
            "GoSmell": ["✅", "⚠️", "⚠️", "✅", "⚠️", "❌", "✅"],
        }

        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df.set_index("Feature"), use_container_width=True)

    # ── Tab 2: AI Analysis ────────────────────────────
    with tab2:
        st.subheader("AI-powered competitive analysis")

        if "api_key" not in st.session_state:
            st.warning("Add API key in Settings to use AI analysis.")
            st.stop()

        analysis_type = st.selectbox("What do you want to analyze?", [
            "Where is Qaly's biggest gap vs competitors?",
            "How should Qaly price its products?",
            "What marketing angle are competitors NOT using?",
            "How to position Qaly on Shopee to rank higher?",
            "What type of content is working for natural deodorant brands?",
            "Custom question...",
        ])

        custom_q = ""
        if analysis_type == "Custom question...":
            custom_q = st.text_area("Your question", placeholder="e.g. Should Qaly expand to pharmacies?")

        question = custom_q if custom_q else analysis_type

        if st.button("Analyse ✨", use_container_width=True):
            context = f"""
Qaly competitors: {', '.join(COMPETITORS.keys())}
Qaly products: Qaly Base (blank, customisable), Syed (men's), Syeda (women's)
Qaly price: ~RM 25–48
Qaly channels: Campus pickup IIUM, Shopee, Instagram
Qaly followers: 20 Instagram followers, just starting out

Question: {question}"""
            with st.spinner("Analysing market..."):
                try:
                    result = call_claude(context, st.session_state["api_key"])
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── Tab 3: Opportunities ──────────────────────────
    with tab3:
        st.subheader("Identified opportunities for Qaly")

        opportunities = [
            {
                "title": "The PhD story is untapped",
                "detail": "No Malaysian deodorant brand is led by PhD researchers. This is a massive credibility differentiator — especially for health-conscious Muslims who want to trust what they put on their body.",
                "action": "Post a 'Meet the founders' Reel. Show the lab. Humanize the science.",
                "priority": "🔴 High",
            },
            {
                "title": "Blank base = viral concept",
                "detail": "The concept of 'add your own perfume to your deodorant' is genuinely novel. It's visual, interactive, and gives people a reason to share.",
                "action": "Create a TikTok/Reel showing the process. Ask followers 'what perfume would you put in yours?'",
                "priority": "🔴 High",
            },
            {
                "title": "IIUM campus market is underserved",
                "detail": "IIUM has thousands of health-conscious Muslim students who actively avoid haram/doubtful ingredients. Qaly is literally made by their own community.",
                "action": "Set up a proper booth during events. Partner with student clubs. Offer student discount.",
                "priority": "🟡 Medium",
            },
            {
                "title": "Couple set for Eid/Valentine's",
                "detail": "Syed + Syeda as a couple set is a natural gift product. This is an underpriced marketing angle.",
                "action": "Bundle and market specifically as a gift set with nice packaging.",
                "priority": "🟡 Medium",
            },
            {
                "title": "Pharmacy / organic store distribution",
                "detail": "Natural health stores like BMS Organics and Village Grocer carry similar products. Getting on their shelves gives Qaly massive credibility.",
                "action": "Prepare a brand deck and reach out to buyers. Start with smaller organic stores.",
                "priority": "🟢 Long-term",
            },
        ]

        for opp in opportunities:
            with st.expander(f"{opp['priority']} {opp['title']}"):
                st.write(opp["detail"])
                st.markdown(f"**Action:** {opp['action']}")
