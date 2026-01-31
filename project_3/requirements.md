# Real-Time Sports Analytics — Player Performance Tracker

**Disclaimer:** This project structure and requirements are specific to `project_3`. Other projects like `project_1` and future `project_2` have their own structures and requirements.

**Type:** End-to-End Data Analytics Project  
**Goal:** Build a real-time analytics system and interactive dashboard that fetches football match and player data via an API, stores it in SQL, and visualizes live performance metrics using Streamlit or Plotly Dash.

## 1️⃣ Business Context

Coaches and analysts need real-time insights on player and team performance to make informed game decisions. This system provides live tracking of football statistics (e.g., goals, assists, minutes played, team efficiency), allowing for quick identification of trends, standout performers, and tactical weaknesses.

## 2️⃣ Business Questions

Which players show declining performance over time?

How does player workload affect match efficiency?

Can we monitor team momentum and performance in real time?

Who are the top-performing players and which positions need improvement?

## 3️⃣ Technical Stack

| Layer | Tool/Technology | Purpose |
|-------|-----------------|---------|
| Data Source | Sports API (e.g., Football-Data.org, API-Football) | Fetch live player and match data |
| Backend / Storage | SQLite or PostgreSQL | Store match and player data snapshots |
| Processing / Logic | Python (Requests, Pandas, SQLAlchemy) | Extract, clean, and aggregate data |
| Visualization / UI | Streamlit or Plotly Dash | Interactive real-time dashboard |
| Scheduling | schedule or cron | Automate periodic API updates |
| Version Control | GitHub | Code, documentation, and visuals hosting |

## 4️⃣ Folder Structure

```bash
player-performance-tracker/
├─ data/
│  ├─ snapshots/              # raw API responses (timestamped JSON)
│  ├─ sports.db               # SQLite database
├─ src/
│  ├─ fetch_data.py           # handles API calls and data retrieval
│  ├─ process_data.py         # cleans and normalizes data
│  ├─ db_utils.py             # database connection & insert utilities
│  ├─ app.py                  # Streamlit dashboard
├─ notebooks/
│  ├─ 01_explore_api.ipynb    # test API responses and data structure
│  ├─ 02_data_prep.ipynb      # feature engineering & EDA
├─ sql/
│  ├─ schema.sql              # DB schema definition
├─ reports/
│  ├─ insights_summary.md     # final key findings
├─ requirements.txt
└─ README.md
```

## 5️⃣ Functional Requirements

### 5.1 Data Collection

System should connect to the given sports API using an API key stored securely (e.g., .env file). Refer to the API documentation: [Football-Data.org Quickstart](https://www.football-data.org/documentation/quickstart) or in `project_3/football_api_docs.md`.

API response should include:

Match ID, Date, Home Team, Away Team, Scores

Player statistics (minutes, goals, assists, passes, shots)

The data should be fetched every 10 minutes (or configurable interval).

All fetched responses should be saved in data/snapshots/ with a timestamped filename.

### 5.2 Data Storage

Database: SQLite for local testing (or PostgreSQL in production).

Schema:

matches table → stores match-level data

player_stats table → stores player-level performance data

Foreign keys should link player stats to match IDs.

Old data should not be overwritten — store incremental updates.

### 5.3 Data Processing

Clean and transform raw API data into structured tables.

Derive new metrics:

efficiency = (goals + assists) / minutes_played

involvement_rate = (shots + passes) / minutes_played

form_score = rolling average of last 5 matches per player

Handle missing or incomplete stats gracefully.

Store processed data back to the SQL database.

## 6️⃣ Dashboard Requirements

### 6.1 Framework

Streamlit (preferred) or Plotly Dash for interactivity.

The app should be runnable via:

streamlit run src/app.py

### 6.2 Dashboard Layout

| Section | Description | Visual Type |
|---------|-------------|-------------|
| Header | Project title, logo, filters (team, date range) | Text + Sidebar Filters |
| KPIs | Top scorer, top assist, avg efficiency, team goals | KPI cards |
| Performance Overview | Compare goals vs assists per player | Scatter plot |
| Trend Analysis | Player form score or team momentum over time | Line chart |
| Workload Analysis | Minutes played vs performance | Bubble chart |
| Team Comparison | Team-wise average efficiency | Bar chart |
| Insights Summary | Text block for top 3 findings | Markdown/Text area |

### 6.3 Interactivity

Sidebar filters for Team, Match Date, and Player.

Hover tooltips to show player details.

Auto-refresh or refresh button to fetch latest data.

Responsive layout for both laptop and mobile view.

## 7️⃣ Automation Requirements

Implement scheduled job (via schedule library or cron) that triggers API fetching every 10 minutes.

Maintain log file in /data/logs/ with timestamp, status, and API latency.

Optional: Email or print alert when API call fails.

## 8️⃣ Business Insights & Output

The system should generate insights automatically such as:

⚽ “Player X’s performance dropped 30% in last 3 matches — potential fatigue.”

🧠 “Team Y’s goals are concentrated in the first half — possible strategy bias.”

📊 “Increasing substitutions after 70 minutes improved team performance by 15%.”

Each update (or dashboard refresh) should display:

Summary table of top 5 players (goals, assists, efficiency)

Team comparison insights

Trend charts for performance decay/improvement

## 9️⃣ Deliverables

| Deliverable | Description |
|-------------|-------------|
| ✅ Functional API fetcher | fetch_data.py — pulls, stores, and logs data from live API |
| ✅ Database schema | schema.sql — defines tables and relationships |
| ✅ Processing pipeline | process_data.py — cleans, transforms, and computes KPIs |
| ✅ Dashboard | app.py — Streamlit app with visuals and KPIs |
| ✅ Documentation | README + visual screenshots + insights summary |
| ✅ Automation | Scheduler for periodic updates |

## 🔟 Documentation & Reporting

README.md must include:

Overview: What the project does and why it matters

Business Problem: Explained in plain English

Architecture Diagram: Data flow (API → SQL → Dashboard)

Setup Guide:

```
pip install -r requirements.txt
python src/fetch_data.py
streamlit run src/app.py
```

Screenshots or GIFs: Dashboard visuals

Key Insights: Bullet-point summary for non-technical readers

Next Steps: Future improvements (e.g., ML-based player performance prediction)

## ✅ Non-Functional Requirements

Clean, reusable, and modular Python code.

No hardcoded secrets — use .env for API key.

Consistent naming conventions across scripts.

Responsive dashboard design and professional color scheme.

Runs end-to-end with one command.

No personal or sensitive data committed to GitHub.
