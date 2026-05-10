# 🧪 Qaly OS — Business Intelligence Suite

Your all-in-one business platform for Qaly deodorant startup.

## Features

| Module | What it does |
|--------|-------------|
| 🏠 Dashboard | KPIs, recent orders, quick AI prompts |
| 📦 Sales Tracker | Log orders, track revenue by product & channel |
| ✍️ AI Content Studio | Generate Instagram captions, content plans, AI chat |
| 📊 Market Intel | Competitor analysis, opportunities, AI market insights |
| 👥 Team Hub | Task board, meeting notes, weekly goals |

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
cd qaly_os
streamlit run app.py
```

### 3. Add your Anthropic API key
- Open the app in browser
- Click ⚙️ Settings in the sidebar
- Paste your API key (get one at console.anthropic.com)
- AI features will unlock immediately

## File structure
```
qaly_os/
├── app.py              # Main app + navigation
├── requirements.txt
├── pages/
│   ├── dashboard.py    # Home dashboard
│   ├── sales.py        # Sales tracker
│   ├── content.py      # AI content studio
│   ├── market.py       # Market intelligence
│   └── team.py         # Team hub
└── data/               # Auto-created on first use
    ├── sales.json
    ├── tasks.json
    └── notes.json
```

## Team access
All 4 team members can run the app locally, or deploy to Streamlit Cloud (free) for shared access.

### Deploy to Streamlit Cloud (recommended for team)
1. Push this folder to a GitHub repo
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Add `ANTHROPIC_API_KEY` in Streamlit secrets
6. Share the URL with your team

## Built by Claude for Qaly
"Your scent. Our science." 🧪
