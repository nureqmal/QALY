import json, os
from datetime import datetime

DATA_DIR = "data"

def load(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def save(filename, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, filename), "w") as f:
        json.dump(data, f, indent=2)

def load_dict(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

def save_dict(filename, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, filename), "w") as f:
        json.dump(data, f, indent=2)

def log_visit(user):
    visits = load("visits.json")
    visits.append({
        "user": user,
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
    })
    save("visits.json", visits)

def get_theme_colors():
    import streamlit as st
    DM = st.session_state.get("dark_mode", True)
    if DM:
        return {
            "BG": "#0d0d14", "SURFACE": "#13131f", "SURFACE2": "#1a1a2e",
            "BORDER": "#2a2a3e", "TEXT": "#e8e6f5", "TEXT2": "#8b88a8",
            "TEXT3": "#55527a", "ACCENT": "#7c6fea", "ACCENT2": "#a99eff",
            "CARD_BG": "#16162a", "SUCCESS": "#1a3a2a", "SUCCESS_T": "#4ade80",
            "WARN_BG": "#2a2010", "WARN_T": "#fbbf24",
        }
    else:
        return {
            "BG": "#f5f5fb", "SURFACE": "#ffffff", "SURFACE2": "#f0eeff",
            "BORDER": "#e2e0f0", "TEXT": "#1a1440", "TEXT2": "#6b68a0",
            "TEXT3": "#a09bcc", "ACCENT": "#534AB7", "ACCENT2": "#7c6fea",
            "CARD_BG": "#ffffff", "SUCCESS": "#e8faf2", "SUCCESS_T": "#0d7a4e",
            "WARN_BG": "#fffbeb", "WARN_T": "#92400e",
        }

PRODUCTS = {
    "Qaly 100ml": 30.00,
    "Syed 100ml": 35.00,
    "Syeda 100ml": 35.00,
    "Kimya 100ml": 35.00,
    "Couple Set (Syed + Syeda)": 65.00,
}

CHANNELS = ["Campus Pickup (IIUM)", "Shopee", "Instagram DM", "WhatsApp", "Walk-in", "Other"]
MEMBERS  = ["Dr. Shirwan", "Eqmal", "Syafa", "Nureen"]
STATUSES = ["Pending", "Completed", "Cancelled"]
