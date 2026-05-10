import streamlit as st

st.set_page_config(
    page_title="Qaly OS",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0f0f1a; }
    [data-testid="stSidebar"] * { color: #e8e6f0 !important; }
    [data-testid="stSidebar"] .stSelectbox label { color: #9f9bb8 !important; }
    .sidebar-logo { text-align: center; padding: 1.5rem 0 1rem; }
    .metric-card {
        background: #f8f7ff;
        border: 1px solid #e2e0f9;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d2a5e;
        margin-bottom: 0.5rem;
    }
    .stButton > button {
        background: #534AB7;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
    }
    .stButton > button:hover { background: #3C3489; color: white; }
    div[data-testid="stChatMessage"] { border-radius: 12px; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:2rem;">🧪</div>
        <div style="font-size:1.3rem; font-weight:700; color:#a89ee8;">Qaly OS</div>
        <div style="font-size:0.75rem; color:#6b6494; margin-top:2px;">Business Intelligence Suite</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("**Navigate**")
    page = st.selectbox(
        "Module",
        ["🏠 Dashboard", "📦 Sales Tracker", "✍️ AI Content Studio", "📊 Market Intel", "👥 Team Hub"],
        label_visibility="collapsed"
    )
    st.divider()

    st.markdown("**Team**")
    user = st.selectbox("Logged in as", ["Qaly (Founder)", "SV", "Master 1", "Master 2"], label_visibility="collapsed")
    st.divider()

    with st.expander("⚙️ Settings"):
        api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
        if api_key:
            st.session_state["api_key"] = api_key
            st.success("Key saved!")
        elif "api_key" in st.session_state:
            st.success("Key loaded ✓")
        else:
            st.info("Add API key to unlock AI features")

# Page routing
if page == "🏠 Dashboard":
    from module import dashboard
    dashboard.show(user)
elif page == "📦 Sales Tracker":
    from module import sales
    sales.show()
elif page == "✍️ AI Content Studio":
    from module import content
    content.show()
elif page == "📊 Market Intel":
    from module import market
    market.show()
elif page == "👥 Team Hub":
    from module import team
    team.show()
