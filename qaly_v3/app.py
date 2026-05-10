import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="QALY One Centre",
    page_icon="assets/logo.png" if False else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme init ────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "current_user" not in st.session_state:
    st.session_state.current_user = "Dr. Shirwan"

DM = st.session_state.dark_mode

# ── CSS ───────────────────────────────────────────────
if DM:
    BG       = "#0d0d14"
    SURFACE  = "#13131f"
    SURFACE2 = "#1a1a2e"
    BORDER   = "#2a2a3e"
    TEXT     = "#e8e6f5"
    TEXT2    = "#8b88a8"
    TEXT3    = "#55527a"
    ACCENT   = "#7c6fea"
    ACCENT2  = "#a99eff"
    CARD_BG  = "#16162a"
    SIDEBAR  = "#0a0a14"
    SUCCESS  = "#1a3a2a"
    SUCCESS_T = "#4ade80"
    WARN_BG  = "#2a2010"
    WARN_T   = "#fbbf24"
else:
    BG       = "#f5f5fb"
    SURFACE  = "#ffffff"
    SURFACE2 = "#f0eeff"
    BORDER   = "#e2e0f0"
    TEXT     = "#1a1440"
    TEXT2    = "#6b68a0"
    TEXT3    = "#a09bcc"
    ACCENT   = "#534AB7"
    ACCENT2  = "#7c6fea"
    CARD_BG  = "#ffffff"
    SIDEBAR  = "#1a1440"
    SUCCESS  = "#e8faf2"
    SUCCESS_T = "#0d7a4e"
    WARN_BG  = "#fffbeb"
    WARN_T   = "#92400e"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

.main {{ background: {BG}; }}
.main .block-container {{ padding: 2rem 2.5rem 3rem; max-width: 1280px; }}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}

[data-testid="stSidebar"] {{ background: {SIDEBAR}; border-right: 1px solid {BORDER}; min-width: 240px !important; max-width: 240px !important; }}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
[data-testid="stSidebar"] hr {{ border-color: {BORDER} !important; }}

.stButton > button {{
    background: {ACCENT} !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    padding: 0.45rem 1.2rem !important; font-weight: 500 !important;
    font-size: 13px !important; transition: all 0.15s !important;
    width: 100%;
}}
.stButton > button:hover {{
    background: {ACCENT2} !important;
    box-shadow: 0 4px 14px {ACCENT}55 !important;
    transform: translateY(-1px) !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 2px; background: {SURFACE2};
    border-radius: 10px; padding: 3px; border: 1px solid {BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px; font-size: 13px; font-weight: 500;
    color: {TEXT2}; padding: 6px 16px;
}}
.stTabs [aria-selected="true"] {{
    background: {ACCENT} !important; color: white !important;
}}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {{
    background: {SURFACE2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {TEXT} !important;
    font-size: 13px !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px {ACCENT}25 !important;
}}

label, .stSelectbox label, .stDateInput label, .stNumberInput label {{
    color: {TEXT2} !important; font-size: 12px !important; font-weight: 500 !important;
}}

.stDataFrame {{ border-radius: 10px; overflow: hidden; border: 1px solid {BORDER}; }}
.stDataFrame td, .stDataFrame th {{ background: {SURFACE} !important; color: {TEXT} !important; }}

.stExpander {{ border: 1px solid {BORDER} !important; border-radius: 10px !important; background: {SURFACE} !important; }}
.stExpander summary {{ color: {TEXT} !important; }}

.stProgress > div > div {{ background: {SURFACE2} !important; border-radius: 99px; }}
.stProgress > div > div > div {{ background: {ACCENT} !important; border-radius: 99px; }}

.stAlert {{ background: {SURFACE2} !important; border: 1px solid {BORDER} !important; color: {TEXT} !important; border-radius: 10px !important; }}

/* Custom components */
.qcard {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 1.25rem 1.5rem; margin-bottom: 0.75rem;
}}
.qcard-accent {{
    background: linear-gradient(135deg, {ACCENT}18, {ACCENT}08);
    border: 1px solid {ACCENT}30;
}}
.page-title {{ font-size: 22px; font-weight: 700; color: {TEXT}; margin-bottom: 2px; letter-spacing: -0.02em; }}
.page-sub {{ font-size: 13px; color: {TEXT2}; margin-bottom: 1.5rem; }}
.kpi-label {{ font-size: 11px; font-weight: 600; color: {TEXT3}; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 6px; }}
.kpi-value {{ font-size: 26px; font-weight: 800; color: {TEXT}; letter-spacing: -0.03em; line-height: 1; }}
.kpi-sub {{ font-size: 12px; color: {TEXT2}; margin-top: 5px; }}
.badge {{ display: inline-block; padding: 3px 9px; border-radius: 99px; font-size: 11px; font-weight: 600; letter-spacing: 0.02em; }}
.badge-green {{ background: {SUCCESS}; color: {SUCCESS_T}; }}
.badge-yellow {{ background: {WARN_BG}; color: {WARN_T}; }}
.badge-red {{ background: #3a1010; color: #f87171; }}
.badge-blue {{ background: #0f1f3a; color: #60a5fa; }}
.badge-purple {{ background: {ACCENT}20; color: {ACCENT2}; }}
.divider {{ height: 1px; background: {BORDER}; margin: 1.5rem 0; }}
.nav-item {{ padding: 8px 12px; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 500; margin-bottom: 2px; color: {TEXT2}; }}
.nav-item:hover {{ background: {SURFACE2}; }}
.nav-active {{ background: {ACCENT}20 !important; color: {ACCENT2} !important; border-left: 2px solid {ACCENT}; }}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:1.6rem 0 1rem;text-align:center;border-bottom:1px solid {BORDER};margin-bottom:1rem;">
        <div style="width:44px;height:44px;background:linear-gradient(135deg,{ACCENT},{ACCENT2});border-radius:12px;margin:0 auto 10px;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:white;letter-spacing:-1px;">Q</div>
        <div style="font-size:14px;font-weight:700;color:{TEXT};letter-spacing:-0.01em;">QALY One Centre</div>
        <div style="font-size:10px;color:{TEXT3};margin-top:2px;letter-spacing:0.06em;text-transform:uppercase;">Business Suite v3</div>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        ("Dashboard", "Dashboard"),
        ("Sales Tracker", "Sales"),
        ("Analytics", "Analytics"),
        ("Inventory & Costing", "Inventory"),
        ("Upcoming Events", "Events"),
        ("Team Hub", "Team"),
    ]

    for page_key, page_label in pages:
        active = st.session_state.page == page_key
        if st.button(page_label, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.page = page_key
            # Log visit
            from modules.utils import log_visit
            log_visit(st.session_state.current_user)
            st.rerun()

    st.markdown(f"<div style='height:1px;background:{BORDER};margin:1rem 0;'></div>", unsafe_allow_html=True)

    MEMBERS = ["Dr. Shirwan", "Eqmal", "Syafa", "Nureen"]
    prev_user = st.session_state.current_user
    new_user = st.selectbox("Logged in as", MEMBERS,
                             index=MEMBERS.index(st.session_state.current_user),
                             label_visibility="visible")
    if new_user != prev_user:
        st.session_state.current_user = new_user
        from modules.utils import log_visit
        log_visit(new_user)
        st.rerun()

    st.markdown(f"<div style='height:1px;background:{BORDER};margin:1rem 0;'></div>", unsafe_allow_html=True)

    mode_label = "Switch to Light Mode" if DM else "Switch to Dark Mode"
    if st.button(mode_label, key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown(f"""
    <div style="position:fixed;bottom:1.2rem;left:0;width:240px;text-align:center;">
        <div style="font-size:10px;color:{TEXT3};letter-spacing:0.04em;">YOUR SCENT. OUR SCIENCE.</div>
    </div>
    """, unsafe_allow_html=True)

# ── Route ─────────────────────────────────────────────
page = st.session_state.page
if page == "Dashboard":
    from modules import dashboard; dashboard.show()
elif page == "Sales Tracker":
    from modules import sales; sales.show()
elif page == "Analytics":
    from modules import analytics; analytics.show()
elif page == "Inventory & Costing":
    from modules import inventory; inventory.show()
elif page == "Upcoming Events":
    from modules import events; events.show()
elif page == "Team Hub":
    from modules import team; team.show()
