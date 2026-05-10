import streamlit as st

st.set_page_config(
    page_title="Qaly OS",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f0c29, #1a1440, #0f0c29);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * { color: #c8c2e8 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Main background */
.main .block-container { padding: 2rem 2.5rem; max-width: 1200px; }

/* Metric cards */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    border: 1px solid #f0eeff;
    box-shadow: 0 2px 12px rgba(83,74,183,0.07);
}
.kpi-label { font-size: 12px; font-weight: 500; color: #9591b8; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
.kpi-value { font-size: 28px; font-weight: 700; color: #1a1440; line-height: 1; }
.kpi-sub { font-size: 12px; color: #b0aad0; margin-top: 4px; }

/* Nav buttons in sidebar */
.nav-btn {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-radius: 10px;
    font-size: 14px; font-weight: 500;
    cursor: pointer; margin-bottom: 4px;
    transition: all 0.15s;
    color: #a09bc4 !important;
}
.nav-btn:hover { background: rgba(255,255,255,0.07); color: white !important; }
.nav-btn.active { background: rgba(139,92,246,0.25); color: white !important; border: 1px solid rgba(139,92,246,0.3); }

/* Buttons */
.stButton > button {
    background: #534AB7 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.4rem !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { background: #3C3489 !important; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(83,74,183,0.3) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #f5f4ff; border-radius: 12px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 9px; font-size: 13px; font-weight: 500; color: #7b75b0; }
.stTabs [aria-selected="true"] { background: white !important; color: #534AB7 !important; box-shadow: 0 1px 6px rgba(83,74,183,0.15); }

/* Forms */
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div {
    border-radius: 10px !important;
    border-color: #e8e6f9 !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #534AB7 !important;
    box-shadow: 0 0 0 3px rgba(83,74,183,0.1) !important;
}

/* Tables */
.stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid #f0eeff; }

/* Status badges */
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 99px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.03em;
}
.badge-green { background: #e8faf2; color: #0d7a4e; }
.badge-yellow { background: #fef9e7; color: #926b00; }
.badge-red { background: #fef0f0; color: #b91c1c; }
.badge-purple { background: #f0eeff; color: #534AB7; }

/* Section headers */
.section-title { font-size: 20px; font-weight: 700; color: #1a1440; margin-bottom: 4px; }
.section-sub { font-size: 13px; color: #9591b8; margin-bottom: 1.5rem; }

/* Divider */
.qdivider { height: 1px; background: linear-gradient(to right, #f0eeff, transparent); margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.8rem 0 1.2rem; text-align:center;">
        <div style="font-size:2.2rem; margin-bottom:6px;">🧪</div>
        <div style="font-size:1.25rem; font-weight:700; color:white; letter-spacing:-0.02em;">Qaly OS</div>
        <div style="font-size:11px; color:#6b648a; margin-top:2px; letter-spacing:0.05em; text-transform:uppercase;">Business Suite</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    pages = [
        ("🏠", "Dashboard"),
        ("📦", "Sales Tracker"),
        ("📊", "Analytics"),
        ("📅", "Content Planner"),
        ("📌", "Market Intel"),
        ("👥", "Team Hub"),
    ]

    for icon, name in pages:
        is_active = st.session_state.page == name
        style = "background:rgba(139,92,246,0.2);color:white;border:1px solid rgba(139,92,246,0.3);" if is_active else ""
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()

    st.divider()
    st.markdown("<div style='font-size:11px;color:#4e4870;padding:0 4px;'>LOGGED IN AS</div>", unsafe_allow_html=True)
    user = st.selectbox("", ["Founder", "SV", "Master 1", "Master 2"], label_visibility="collapsed")
    st.session_state.current_user = user

    st.markdown("""
    <div style="position:fixed;bottom:1.5rem;left:0;width:240px;text-align:center;">
        <div style="font-size:11px;color:#3a3560;">"Your scent. Our science." 🧪</div>
    </div>
    """, unsafe_allow_html=True)

# ── Page routing ──────────────────────────────────────
page = st.session_state.page

if page == "Dashboard":
    from modules import dashboard; dashboard.show()
elif page == "Sales Tracker":
    from modules import sales; sales.show()
elif page == "Analytics":
    from modules import analytics; analytics.show()
elif page == "Content Planner":
    from modules import content; content.show()
elif page == "Market Intel":
    from modules import market; market.show()
elif page == "Team Hub":
    from modules import team; team.show()
