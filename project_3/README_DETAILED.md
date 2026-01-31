# ⚽ Real-Time Sports Analytics — Player Performance Tracker

> **Disclaimer:** This project structure and requirements are specific to `project_3`. Other projects like `project_1` and future `project_2` have their own structures and requirements.

![Project Type](https://img.shields.io/badge/Type-End--to--End%20Analytics-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29%2B-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents
- [Overview](#overview)
- [Business Context](#business-context)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Stack](#technical-stack)
- [Dashboard Preview](#dashboard-preview)
- [Key Insights](#key-insights)
- [Contributing](#contributing)
- [Future Enhancements](#future-enhancements)

## 🎯 Overview

**Real-Time Sports Analytics** is an end-to-end data analytics system that fetches live football match and player data via the Football-Data.org API, stores it in a SQLite database, and visualizes real-time performance metrics through an interactive Streamlit dashboard.

### What Does This Project Do?

- 🔄 **Automated Data Collection**: Fetches football data from Football-Data.org API at configurable intervals
- 💾 **Persistent Storage**: Stores match and player statistics in SQLite database with incremental updates
- 📊 **Real-Time Analytics**: Computes performance metrics like efficiency, involvement rate, and form scores
- 🎨 **Interactive Dashboard**: Provides visual insights through Streamlit with filters and dynamic charts
- ⏰ **Scheduled Updates**: Automates data fetching every 10 minutes (configurable)

## 🏆 Business Context

### The Problem

Coaches and analysts need **real-time insights** on player and team performance to make informed game decisions. Traditional methods of analyzing sports data are often:
- ❌ Manual and time-consuming
- ❌ Delayed, with outdated information
- ❌ Fragmented across multiple sources
- ❌ Difficult to visualize and interpret

### Our Solution

This system provides **live tracking** of football statistics (goals, assists, minutes played, team efficiency), enabling:
- ✅ Quick identification of trends and patterns
- ✅ Recognition of standout performers
- ✅ Detection of tactical weaknesses
- ✅ Data-driven decision making

### Business Questions Answered

1. **Which players show declining performance over time?**
   - Track form scores and efficiency trends

2. **How does player workload affect match efficiency?**
   - Analyze minutes played vs. performance metrics

3. **Can we monitor team momentum and performance in real time?**
   - View real-time standings and goal patterns

4. **Who are the top-performing players and which positions need improvement?**
   - Identify leaders and areas for tactical adjustments

## 🏗️ Architecture

```
┌─────────────────┐
│  Football Data  │
│   API (v4)      │
└────────┬────────┘
         │
         │ HTTP Requests (Every 10 min)
         │
         ▼
┌─────────────────┐
│  fetch_data.py  │──────► Snapshots (JSON)
│  (Data Layer)   │        data/snapshots/
└────────┬────────┘
         │
         │ Raw Data
         │
         ▼
┌─────────────────┐
│ process_data.py │
│  (ETL Layer)    │
└────────┬────────┘
         │
         │ Cleaned & Transformed Data
         │
         ▼
┌─────────────────┐
│   SQLite DB     │◄─────► db_utils.py
│  (sports.db)    │        (Data Access)
└────────┬────────┘
         │
         │ Query Results
         │
         ▼
┌─────────────────┐
│    app.py       │
│ (Streamlit UI)  │
└─────────────────┘
```

### Data Flow

1. **Fetch**: `fetch_data.py` calls Football-Data.org API
2. **Store**: Raw responses saved as timestamped JSON snapshots
3. **Process**: `process_data.py` cleans and transforms data
4. **Load**: Processed data inserted into SQLite database via `db_utils.py`
5. **Visualize**: `app.py` queries database and displays interactive dashboard
6. **Automate**: `scheduler.py` orchestrates periodic updates

## ✨ Features

### Data Collection
- ✅ Secure API key management via `.env` file
- ✅ Rate limiting to respect API quotas (10 req/min for free tier)
- ✅ Automatic retry on rate limit errors
- ✅ Timestamped JSON snapshots for data auditing
- ✅ Comprehensive logging with latency tracking

### Data Storage
- ✅ Normalized SQLite database schema
- ✅ Separate tables for matches, player stats, and teams
- ✅ Foreign key relationships for data integrity
- ✅ Indexed columns for query performance
- ✅ Database views for common aggregations

### Data Processing
- ✅ **Efficiency Score**: `(goals + assists) / minutes_played`
- ✅ **Involvement Rate**: `(shots + passes) / minutes_played`
- ✅ **Form Score**: Rolling average of last 5 matches
- ✅ Graceful handling of missing data
- ✅ Incremental updates (no data overwriting)

### Dashboard
- ✅ **KPI Cards**: Top scorers, assists, average efficiency
- ✅ **Performance Scatter**: Goals vs. Assists visualization
- ✅ **Trend Analysis**: Performance over time line charts
- ✅ **Workload Analysis**: Minutes played vs. efficiency
- ✅ **Team Comparison**: Side-by-side team statistics
- ✅ **Interactive Filters**: Team, player, and date range selection
- ✅ **Auto-Refresh**: Manual refresh button for latest data
- ✅ **Responsive Design**: Professional color scheme and layout

### Automation
- ✅ Scheduled data fetching every 10 minutes (configurable)
- ✅ Detailed logging with timestamps and status
- ✅ One-time fetch option for testing
- ✅ Command-line interface for flexible execution

## 🚀 Installation

### Prerequisites

- **Python 3.8+**
- **pip** package manager
- **Football-Data.org API Key** (free tier available)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Health-Credit-Sports-Data-Analysis/project_3
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API key:
```env
FOOTBALL_API_KEY=your_actual_api_key_here
```

**Get your free API key:** [Football-Data.org Registration](https://www.football-data.org/client/register)

### Step 5: Initialize Database

The database will be automatically created on first run. Optionally, you can initialize it manually:

```bash
python -c "from src.db_utils import get_database_manager; get_database_manager()"
```

## 🎬 Quick Start

### Option 1: Fetch Data and Launch Dashboard

```bash
# Fetch initial data
python src/fetch_data.py

# Launch dashboard
streamlit run src/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Option 2: Automated Scheduler

```bash
# Start scheduler (fetches data every 10 minutes)
python src/scheduler.py

# In another terminal, launch dashboard
streamlit run src/app.py
```

### Option 3: One-Time Fetch

```bash
# Fetch data once without scheduling
python src/scheduler.py --once
```

## 📖 Usage

### Fetching Data

**Manual fetch:**
```bash
python src/fetch_data.py
```

**Scheduled fetching:**
```bash
# Use default interval (10 minutes)
python src/scheduler.py

# Custom interval (30 minutes)
python src/scheduler.py --interval 30
```

### Processing Data

Data is automatically processed after fetching. To process existing snapshots:

```bash
python src/process_data.py
```

### Running the Dashboard

```bash
streamlit run src/app.py
```

**Dashboard features:**
- Use sidebar filters to select teams, players, or date ranges
- Click "Refresh Data" to reload from database
- Click "Fetch Latest Data" to pull new data from API
- Hover over charts for detailed information

### Jupyter Notebooks

Explore data interactively:

```bash
jupyter notebook notebooks/01_explore_api.ipynb
```

## 📁 Project Structure

```
project_3/
├── data/
│   ├── snapshots/              # Raw API responses (timestamped JSON)
│   ├── logs/                   # Application and scheduler logs
│   └── sports.db               # SQLite database
├── src/
│   ├── fetch_data.py           # API data fetcher
│   ├── process_data.py         # Data cleaning and transformation
│   ├── db_utils.py             # Database utilities
│   ├── app.py                  # Streamlit dashboard
│   └── scheduler.py            # Automated scheduling
├── notebooks/
│   ├── 01_explore_api.ipynb    # API exploration
│   └── 02_data_prep.ipynb      # Feature engineering
├── sql/
│   └── schema.sql              # Database schema definition
├── reports/
│   └── insights_summary.md     # Key findings
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── football_api_docs.md        # API documentation
└── README.md                   # This file
```

## 🛠️ Technical Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Data Source** | Football-Data.org API (v4) | Live football match and player data |
| **Backend** | Python 3.8+ | Core programming language |
| **Storage** | SQLite | Lightweight embedded database |
| **ORM** | SQLAlchemy | Database abstraction and queries |
| **Data Processing** | Pandas, NumPy | Data manipulation and analysis |
| **Visualization** | Streamlit, Plotly | Interactive web dashboard |
| **Scheduling** | schedule library | Periodic task automation |
| **Environment** | python-dotenv | Secure configuration management |
| **Notebooks** | Jupyter | Interactive data exploration |

## 📸 Dashboard Preview

### Main Dashboard
*[Screenshot will be added after first run]*

**Key Sections:**
- 📊 KPI Cards: Total matches, goals, assists, average efficiency
- 🏆 Top Performers: Leaderboard of best players
- 📈 Performance Overview: Goals vs. Assists scatter plot
- 🏟️ Team Comparison: Total goals by team
- 📉 Trend Analysis: Performance metrics over time
- ⚡ Workload Analysis: Minutes played vs. efficiency
- 💡 Key Insights: Automated findings and recommendations

## 💡 Key Insights

Based on the analytics system, here are example insights:

### Performance Insights
- ⚽ **Top Scorers**: Identify leading goal scorers across competitions
- 🎯 **Efficiency Leaders**: Players with highest goals+assists per minute
- 📈 **Form Trends**: Spot players with improving or declining performance
- 🔄 **Workload Impact**: Correlation between minutes played and efficiency

### Team Insights
- 🏆 **League Leaders**: Teams with most goals and best efficiency
- 📊 **Goal Distribution**: How goals are spread across matches
- ⏰ **Tactical Patterns**: First-half vs. second-half performance
- 🔀 **Substitution Impact**: Effect of fresh players on performance

### Actionable Recommendations
1. **Monitor Fatigue**: Players with 400+ minutes may show efficiency drops
2. **Tactical Adjustments**: Teams scoring mostly in one half may need strategy changes
3. **Squad Rotation**: High-workload players need rest to maintain performance
4. **Rising Stars**: Identify players with consistently improving form scores

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔮 Future Enhancements

### Short-term
- [ ] Add more competitions (La Liga, Serie A, Bundesliga)
- [ ] Implement player comparison tool
- [ ] Add export functionality (CSV, PDF reports)
- [ ] Email notifications for key events

### Medium-term
- [ ] Integrate additional data sources (injuries, transfers)
- [ ] Advanced filtering (by position, nationality)
- [ ] Historical trend analysis (season-over-season)
- [ ] Mobile-responsive improvements

### Long-term
- [ ] **Machine Learning**: Predict player performance
- [ ] **Sentiment Analysis**: Incorporate social media data
- [ ] **Real-time Updates**: WebSocket for live match updates
- [ ] **Cloud Deployment**: AWS/Azure hosting
- [ ] **Multi-user Support**: User authentication and preferences
- [ ] **Premium Features**: Advanced analytics for paid subscriptions

## 📄 License

This project is for educational and analytical purposes. Please respect the [Football-Data.org Terms of Service](https://www.football-data.org/terms).

## 🙏 Acknowledgments

- **Football-Data.org** for providing the free API
- **Streamlit** for the amazing dashboard framework
- **Plotly** for interactive visualizations

## 📞 Support

For issues or questions:
1. Check the [Football-Data.org Documentation](https://www.football-data.org/documentation/quickstart)
2. Review `football_api_docs.md` in this project
3. Open an issue on GitHub

---

**Built with ❤️ for sports analytics enthusiasts**
