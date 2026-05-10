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

PRODUCTS = {
    "Qaly Base 30ml": 25.00,
    "Qaly Base 60ml": 45.00,
    "Syed 30ml": 28.00,
    "Syed 60ml": 48.00,
    "Syeda 30ml": 28.00,
    "Syeda 60ml": 48.00,
    "Couple Set (Syed + Syeda)": 85.00,
}

CHANNELS = ["Campus Pickup (IIUM)", "Shopee", "Instagram DM", "WhatsApp", "Walk-in", "Other"]
MEMBERS = ["Founder", "SV", "Master 1", "Master 2"]
STATUSES = ["Pending", "Completed", "Cancelled"]
