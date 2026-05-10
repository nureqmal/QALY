# 🧪 Qaly OS v2 — Business Suite

Zero AI dependency. Zero cost. Full power.

## Modules

| Module | Features |
|--------|----------|
| 🏠 Dashboard | KPIs, recent orders, product mix, pending alerts |
| 📦 Sales Tracker | Log orders, filter, update status, revenue summary |
| 📊 Analytics | Revenue trend, product performance, channel analysis |
| 📅 Content Planner | Weekly calendar, content bank with ready captions |
| 📌 Market Intel | Competitor map, comparison table, opportunities |
| 👥 Team Hub | Task board, meeting notes, goals tracker |

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud (free, shared team access)

1. Push this folder to GitHub
2. Go to https://share.streamlit.io
3. New app → select your repo → set `app.py` as main file
4. Deploy — share URL with team

## File structure

```
qaly_v2/
├── app.py
├── requirements.txt
├── modules/
│   ├── dashboard.py
│   ├── sales.py
│   ├── analytics.py
│   ├── content.py
│   ├── market.py
│   ├── team.py
│   └── utils.py
└── data/          ← auto-created on first run
    ├── sales.json
    ├── content.json
    ├── tasks.json
    ├── notes.json
    └── goals.json
```

---
"Your scent. Our science." 🧪
