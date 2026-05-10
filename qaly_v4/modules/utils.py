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
            "BG":"#0d0d14","SURFACE":"#13131f","SURFACE2":"#1a1a2e",
            "BORDER":"#2a2a3e","TEXT":"#e8e6f5","TEXT2":"#8b88a8",
            "TEXT3":"#55527a","ACCENT":"#7c6fea","ACCENT2":"#a99eff",
            "CARD_BG":"#16162a","SUCCESS":"#1a3a2a","SUCCESS_T":"#4ade80",
            "WARN_BG":"#2a2010","WARN_T":"#fbbf24","ERR_BG":"#3a1010","ERR_T":"#f87171",
        }
    else:
        return {
            "BG":"#f5f5fb","SURFACE":"#ffffff","SURFACE2":"#f0eeff",
            "BORDER":"#e2e0f0","TEXT":"#1a1440","TEXT2":"#6b68a0",
            "TEXT3":"#a09bcc","ACCENT":"#534AB7","ACCENT2":"#7c6fea",
            "CARD_BG":"#ffffff","SUCCESS":"#e8faf2","SUCCESS_T":"#0d7a4e",
            "WARN_BG":"#fffbeb","WARN_T":"#92400e","ERR_BG":"#fef2f2","ERR_T":"#b91c1c",
        }

PASSCODES = {
    "Dr. Shirwan": "0000",
    "Eqmal":       "1234",
    "Syafa":       "5555",
    "Nureen":      "5678",
}

PRODUCTS = {
    "Qaly 100ml":               30.00,
    "Syed 100ml":               35.00,
    "Syeda 100ml":              35.00,
    "Kimya 100ml":              35.00,
    "Couple Set (Syed+Syeda)":  65.00,
}

CHANNELS = ["Campus Pickup (IIUM)", "Shopee", "Instagram DM", "WhatsApp", "Walk-in", "Other"]
MEMBERS  = ["Dr. Shirwan", "Eqmal", "Syafa", "Nureen"]
STATUSES = ["Pending", "Completed", "Cancelled"]

# Google Sheets IDs
GFORM_SHEET_ID  = "14EvKoF1dFyQeu5ishr6UBgsWniordtn6Ka3SYWl6k_8"
GFORM_GID       = "743510311"

DEFAULT_INVENTORY = [
    {"id":"MAT001","name":"Magnesium Chloride","supplier":"","unit":"g",  "stock":1000,"reorder":200,"unit_cost":0.020,"last_bought":"","notes":"Antibacterial active ingredient"},
    {"id":"MAT002","name":"Aloe Vera Extract", "supplier":"","unit":"ml", "stock":500, "reorder":100,"unit_cost":0.050,"last_bought":"","notes":"Skin soothing carrier"},
    {"id":"MAT003","name":"Dipropylene Glycol","supplier":"","unit":"ml", "stock":500, "reorder":100,"unit_cost":0.030,"last_bought":"","notes":"Solvent / carrier"},
    {"id":"MAT004","name":"Potassium Sorbate", "supplier":"","unit":"g",  "stock":200, "reorder":50, "unit_cost":0.080,"last_bought":"","notes":"Natural preservative"},
    {"id":"MAT005","name":"Distilled Water",   "supplier":"","unit":"ml", "stock":5000,"reorder":1000,"unit_cost":0.001,"last_bought":"","notes":"Aqueous base"},
    {"id":"MAT006","name":"Bottle 100ml",      "supplier":"","unit":"pcs","stock":200, "reorder":50, "unit_cost":1.200,"last_bought":"","notes":"Primary packaging"},
    {"id":"MAT007","name":"Label / Sticker",   "supplier":"","unit":"pcs","stock":200, "reorder":50, "unit_cost":0.300,"last_bought":"","notes":"Product label"},
    {"id":"MAT008","name":"Fragrance Oil",     "supplier":"","unit":"ml", "stock":300, "reorder":80, "unit_cost":0.120,"last_bought":"","notes":"For Syed, Syeda, Kimya"},
    {"id":"MAT009","name":"Box / Outer Pack",  "supplier":"","unit":"pcs","stock":100, "reorder":30, "unit_cost":0.500,"last_bought":"","notes":"Optional outer packaging"},
]

DEFAULT_COSTING = [
    {"product":"Qaly 100ml","overhead":2.00,"selling_price":30.00,"ingredients":[
        {"name":"Magnesium Chloride","qty":5.0,  "unit":"g",  "cost_per_unit":0.020,"line_cost":0.1000},
        {"name":"Aloe Vera Extract", "qty":20.0, "unit":"ml", "cost_per_unit":0.050,"line_cost":1.0000},
        {"name":"Dipropylene Glycol","qty":10.0, "unit":"ml", "cost_per_unit":0.030,"line_cost":0.3000},
        {"name":"Potassium Sorbate", "qty":0.5,  "unit":"g",  "cost_per_unit":0.080,"line_cost":0.0400},
        {"name":"Distilled Water",   "qty":64.5, "unit":"ml", "cost_per_unit":0.001,"line_cost":0.0645},
        {"name":"Bottle 100ml",      "qty":1,    "unit":"pcs","cost_per_unit":1.200,"line_cost":1.2000},
        {"name":"Label / Sticker",   "qty":1,    "unit":"pcs","cost_per_unit":0.300,"line_cost":0.3000},
    ]},
    {"product":"Syed 100ml","overhead":2.00,"selling_price":35.00,"ingredients":[
        {"name":"Magnesium Chloride","qty":5.0,  "unit":"g",  "cost_per_unit":0.020,"line_cost":0.1000},
        {"name":"Aloe Vera Extract", "qty":20.0, "unit":"ml", "cost_per_unit":0.050,"line_cost":1.0000},
        {"name":"Dipropylene Glycol","qty":10.0, "unit":"ml", "cost_per_unit":0.030,"line_cost":0.3000},
        {"name":"Potassium Sorbate", "qty":0.5,  "unit":"g",  "cost_per_unit":0.080,"line_cost":0.0400},
        {"name":"Fragrance Oil",     "qty":3.0,  "unit":"ml", "cost_per_unit":0.120,"line_cost":0.3600},
        {"name":"Distilled Water",   "qty":61.5, "unit":"ml", "cost_per_unit":0.001,"line_cost":0.0615},
        {"name":"Bottle 100ml",      "qty":1,    "unit":"pcs","cost_per_unit":1.200,"line_cost":1.2000},
        {"name":"Label / Sticker",   "qty":1,    "unit":"pcs","cost_per_unit":0.300,"line_cost":0.3000},
    ]},
    {"product":"Syeda 100ml","overhead":2.00,"selling_price":35.00,"ingredients":[
        {"name":"Magnesium Chloride","qty":5.0,  "unit":"g",  "cost_per_unit":0.020,"line_cost":0.1000},
        {"name":"Aloe Vera Extract", "qty":20.0, "unit":"ml", "cost_per_unit":0.050,"line_cost":1.0000},
        {"name":"Dipropylene Glycol","qty":10.0, "unit":"ml", "cost_per_unit":0.030,"line_cost":0.3000},
        {"name":"Potassium Sorbate", "qty":0.5,  "unit":"g",  "cost_per_unit":0.080,"line_cost":0.0400},
        {"name":"Fragrance Oil",     "qty":3.0,  "unit":"ml", "cost_per_unit":0.120,"line_cost":0.3600},
        {"name":"Distilled Water",   "qty":61.5, "unit":"ml", "cost_per_unit":0.001,"line_cost":0.0615},
        {"name":"Bottle 100ml",      "qty":1,    "unit":"pcs","cost_per_unit":1.200,"line_cost":1.2000},
        {"name":"Label / Sticker",   "qty":1,    "unit":"pcs","cost_per_unit":0.300,"line_cost":0.3000},
    ]},
    {"product":"Kimya 100ml","overhead":2.00,"selling_price":35.00,"ingredients":[
        {"name":"Magnesium Chloride","qty":5.0,  "unit":"g",  "cost_per_unit":0.020,"line_cost":0.1000},
        {"name":"Aloe Vera Extract", "qty":20.0, "unit":"ml", "cost_per_unit":0.050,"line_cost":1.0000},
        {"name":"Dipropylene Glycol","qty":10.0, "unit":"ml", "cost_per_unit":0.030,"line_cost":0.3000},
        {"name":"Potassium Sorbate", "qty":0.5,  "unit":"g",  "cost_per_unit":0.080,"line_cost":0.0400},
        {"name":"Fragrance Oil",     "qty":3.0,  "unit":"ml", "cost_per_unit":0.120,"line_cost":0.3600},
        {"name":"Distilled Water",   "qty":61.5, "unit":"ml", "cost_per_unit":0.001,"line_cost":0.0615},
        {"name":"Bottle 100ml",      "qty":1,    "unit":"pcs","cost_per_unit":1.200,"line_cost":1.2000},
        {"name":"Label / Sticker",   "qty":1,    "unit":"pcs","cost_per_unit":0.300,"line_cost":0.3000},
    ]},
    {"product":"Couple Set (Syed+Syeda)","overhead":3.00,"selling_price":65.00,"ingredients":[
        {"name":"Magnesium Chloride","qty":10.0, "unit":"g",  "cost_per_unit":0.020,"line_cost":0.2000},
        {"name":"Aloe Vera Extract", "qty":40.0, "unit":"ml", "cost_per_unit":0.050,"line_cost":2.0000},
        {"name":"Dipropylene Glycol","qty":20.0, "unit":"ml", "cost_per_unit":0.030,"line_cost":0.6000},
        {"name":"Potassium Sorbate", "qty":1.0,  "unit":"g",  "cost_per_unit":0.080,"line_cost":0.0800},
        {"name":"Fragrance Oil",     "qty":6.0,  "unit":"ml", "cost_per_unit":0.120,"line_cost":0.7200},
        {"name":"Distilled Water",   "qty":123.0,"unit":"ml", "cost_per_unit":0.001,"line_cost":0.1230},
        {"name":"Bottle 100ml",      "qty":2,    "unit":"pcs","cost_per_unit":1.200,"line_cost":2.4000},
        {"name":"Label / Sticker",   "qty":2,    "unit":"pcs","cost_per_unit":0.300,"line_cost":0.6000},
        {"name":"Box / Outer Pack",  "qty":1,    "unit":"pcs","cost_per_unit":0.500,"line_cost":0.5000},
    ]},
]

def ensure_defaults():
    if not os.path.exists(os.path.join(DATA_DIR, "inventory.json")):
        save("inventory.json", DEFAULT_INVENTORY)
    if not os.path.exists(os.path.join(DATA_DIR, "costing.json")):
        save("costing.json", DEFAULT_COSTING)

USER_COLORS = {
    "Dr. Shirwan": "#7c6fea",
    "Eqmal":       "#4ade80",
    "Syafa":       "#f472b6",
    "Nureen":      "#60a5fa",
}
