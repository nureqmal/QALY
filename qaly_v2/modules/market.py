import streamlit as st
import pandas as pd

def show():
    st.markdown("<div class='section-title'>Market Intel</div><div class='section-sub'>Know your competitors. Own your position.</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏆  Competitor Map", "📊  Comparison Table", "🎯  Opportunities"])

    with tab1:
        competitors = {
            "HYGR": {
                "tagline": "Natural deodorant that actually works",
                "price": "RM 25–45", "founded": "~2019",
                "usp": "12-hour protection, no baking soda, eco packaging",
                "channels": "Website, Shopee, Instagram",
                "ig_followers": "~15K",
                "weakness": "No personalisation, higher price point",
                "color": "#0d7a4e", "bg": "#e8faf2",
            },
            "Hello Natural Co": {
                "tagline": "High-performance all-natural deodorant",
                "price": "RM 40–70", "founded": "~2018",
                "usp": "Targets athletes, pregnant women, sensitive skin",
                "channels": "Website, Shopee, select pharmacies",
                "ig_followers": "~8K",
                "weakness": "Balm format limits audience, premium price",
                "color": "#1d4ed8", "bg": "#eff6ff",
            },
            "Smelly No More": {
                "tagline": "Mineral salt, halal, no synthetic fragrance",
                "price": "RM 20–35", "founded": "~2015",
                "usp": "Halal certified, mineral salt, available in stores",
                "channels": "Total Image stores, Shopee",
                "ig_followers": "~5K",
                "weakness": "Older brand image, generic scents",
                "color": "#92400e", "bg": "#fffbeb",
            },
            "GoSmell": {
                "tagline": "Personalised scent deodorant",
                "price": "RM 30–55", "founded": "~2020",
                "usp": "Strong lifestyle branding, variety of scents",
                "channels": "Instagram, Shopee",
                "ig_followers": "~25K",
                "weakness": "Not science-led, halal not prominent",
                "color": "#7c3aed", "bg": "#f5f3ff",
            },
        }

        col1, col2 = st.columns(2)
        for i, (brand, data) in enumerate(competitors.items()):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                <div style="background:{data['bg']};border:1px solid {data['color']}30;border-radius:16px;padding:1.2rem 1.4rem;margin-bottom:1rem;">
                    <div style="font-size:16px;font-weight:700;color:{data['color']};margin-bottom:4px;">{brand}</div>
                    <div style="font-size:12px;color:#6b7280;font-style:italic;margin-bottom:12px;">"{data['tagline']}"</div>
                    <div style="font-size:13px;line-height:1.8;color:#374151;">
                        <b>Price:</b> {data['price']}<br>
                        <b>USP:</b> {data['usp']}<br>
                        <b>Channels:</b> {data['channels']}<br>
                        <b>IG Followers:</b> {data['ig_followers']}<br>
                        <b>Weakness:</b> <span style="color:#dc2626;">{data['weakness']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#f0eeff,#e8e4ff);border:2px solid #534AB7;border-radius:16px;padding:1.2rem 1.4rem;margin-top:0.5rem;">
            <div style="font-size:16px;font-weight:700;color:#534AB7;margin-bottom:4px;">✦ QALY — Our Position</div>
            <div style="font-size:12px;color:#7b75b0;font-style:italic;margin-bottom:12px;">"Your scent. Our science."</div>
            <div style="font-size:13px;line-height:1.8;color:#374151;">
                <b>Price:</b> RM 25–48<br>
                <b>USP:</b> Blank base (customisable scent) + PhD-formulated + halal<br>
                <b>Channels:</b> IIUM Campus, Shopee, Instagram DM<br>
                <b>IG Followers:</b> Growing 🌱<br>
                <b>Advantage:</b> <span style="color:#0d7a4e;">Only brand letting customers personalise scent + local researcher credibility</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        data = {
            "Feature": ["Aluminium-free","Paraben-free","Halal certified","Malaysian brand","Customisable scent","PhD-formulated","Liquid format","Budget-friendly"],
            "Qaly": ["✅","✅","✅","✅","✅","✅","✅","✅"],
            "HYGR": ["✅","✅","✅","✅","❌","❌","✅","⚠️"],
            "Hello Natural": ["✅","✅","✅","✅","❌","❌","❌ (balm)","❌"],
            "Smelly No More": ["✅","✅","✅","❌","❌","❌","❌ (crystal)","✅"],
            "GoSmell": ["✅","⚠️","⚠️","✅","⚠️","❌","✅","✅"],
        }
        df = pd.DataFrame(data).set_index("Feature")
        st.dataframe(df, use_container_width=True)
        st.caption("✅ Yes  ⚠️ Partial/Unclear  ❌ No")

    with tab3:
        opps = [
            {
                "priority": "🔴 High",
                "title": "The PhD story is completely untapped",
                "insight": "No Malaysian deodorant brand is led by PhD researchers. This is massive credibility — especially for health-conscious Muslims who want to trust what they put on their body.",
                "action": "Post a 'Meet the founders' Reel. Show the lab. Humanize the science. Make this your pinned post.",
                "impact": "Trust + differentiation",
            },
            {
                "priority": "🔴 High",
                "title": "Blank base concept = viral potential",
                "insight": "The concept of 'add your own perfume to your deodorant' is genuinely novel in Malaysia. It's visual, interactive, and gives people a reason to share.",
                "action": "Create a TikTok/Reel showing the process. Ask followers what perfume they'd put in theirs. Make it a challenge.",
                "impact": "Organic reach + engagement",
            },
            {
                "priority": "🟡 Medium",
                "title": "IIUM campus is an underserved goldmine",
                "insight": "IIUM has thousands of health-conscious Muslim students who actively check ingredient labels. Qaly is literally made by their own community.",
                "action": "Set up a proper booth during events. Partner with student clubs (Pharmacy, Chemistry, Health). Offer student discount.",
                "impact": "Direct sales + word of mouth",
            },
            {
                "priority": "🟡 Medium",
                "title": "Couple Set gift positioning",
                "insight": "Syed + Syeda as a couple set is a natural gift product for Eid, Valentine's, anniversaries. Nobody else in this space is doing couple marketing well.",
                "action": "Design premium gift packaging. Market specifically as 'the gift that's actually useful'.",
                "impact": "Higher AOV + new audience",
            },
            {
                "priority": "🟢 Long-term",
                "title": "Pharmacy & organic store distribution",
                "insight": "Stores like BMS Organics, Village Grocer, and independent organic stores carry similar products. Being on their shelves means instant credibility.",
                "action": "Prepare a brand deck with your research credentials. Start outreach to smaller organic stores first.",
                "impact": "Mass distribution + brand legitimacy",
            },
            {
                "priority": "🟢 Long-term",
                "title": "Halal certification = export potential",
                "insight": "The global halal personal care market is growing fast. A certified halal, science-backed deodorant from Malaysia has real export potential to Indonesia, Brunei, Middle East.",
                "action": "Get official halal certification from JAKIM. Document the certification for marketing.",
                "impact": "Market expansion",
            },
        ]

        for opp in opps:
            with st.expander(f"{opp['priority']} · **{opp['title']}**"):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.markdown(f"**Insight:** {opp['insight']}")
                    st.markdown(f"**Action:** {opp['action']}")
                with col2:
                    st.markdown(f"""
                    <div style="background:#f0eeff;border-radius:10px;padding:10px;text-align:center;">
                        <div style="font-size:11px;color:#9591b8;margin-bottom:4px;">IMPACT</div>
                        <div style="font-size:13px;font-weight:600;color:#534AB7;">{opp['impact']}</div>
                    </div>
                    """, unsafe_allow_html=True)
