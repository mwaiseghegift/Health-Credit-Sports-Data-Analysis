# ⚡ Quick Start Guide

Get up and running with Real-Time Sports Analytics in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Internet connection
- Football-Data.org API key ([Get free key](https://www.football-data.org/client/register))

---

## Automated Setup (Recommended)

### Linux/macOS:
```bash
chmod +x setup.sh
./setup.sh
```

### Windows:
```cmd
setup.bat
```

The setup script will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create .env file
- ✅ Initialize database
- ✅ Run system tests

---

## Manual Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
FOOTBALL_API_KEY=your_actual_api_key_here
```

### Step 3: Initialize Database
```bash
python -c "from src.db_utils import get_database_manager; db = get_database_manager(); db.close()"
```

### Step 4: Test Installation
```bash
python test_system.py
```

---

## Running the Application

### Option 1: Quick Demo (No API Key Needed)
```bash
streamlit run src/app.py
```
The dashboard will open with an empty database. Use the "Fetch Latest Data" button after adding your API key.

### Option 2: Fetch Data First
```bash
# Fetch some data
python src/fetch_data.py

# Launch dashboard
streamlit run src/app.py
```

### Option 3: Automated Updates
```bash
# Terminal 1: Start scheduler (fetches every 10 minutes)
python src/scheduler.py

# Terminal 2: Launch dashboard
streamlit run src/app.py
```

---

## Verify Setup

Run the system test:
```bash
python test_system.py
```

Expected output:
```
✅ All tests passed! System is ready to use.
```

---

## Common Issues

### "API key not configured"
**Solution:** Edit `.env` file and add your API key from Football-Data.org

### "No data in dashboard"
**Solution:** Click "Fetch Latest Data" button in the dashboard sidebar, or run:
```bash
python src/fetch_data.py
```

### "Module not found"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### "Database locked"
**Solution:** Close all connections to the database and restart

---

## What to Expect

After setup, you should see:

1. **Dashboard** at `http://localhost:8501`
2. **KPI Cards** showing metrics (initially zero if no data)
3. **Visualizations** that populate after fetching data
4. **Sidebar Controls** for filtering and data management

---

## Getting Data

The system works with the **free tier** of Football-Data.org API which provides:
- ✅ Match results and schedules
- ✅ Team information
- ✅ Competition standings
- ✅ Top scorers
- ❌ Detailed player-level stats (requires premium)

### Fetching Strategy

**For testing:**
```bash
python src/scheduler.py --once
```

**For continuous monitoring:**
```bash
python src/scheduler.py  # Updates every 10 minutes
```

---

## Next Steps

Once running, explore:

1. **Dashboard Features**
   - Use filters to focus on specific teams or players
   - Click refresh to update visualizations
   - Hover over charts for detailed info

2. **Jupyter Notebooks**
   ```bash
   jupyter notebook notebooks/01_explore_api.ipynb
   ```

3. **Documentation**
   - [README.md](README.md) - Overview and usage
   - [README_DETAILED.md](README_DETAILED.md) - Complete documentation
   - [insights_summary.md](reports/insights_summary.md) - Analytics findings

4. **Customization**
   - Edit `.env` to change competitions (DEFAULT_COMPETITIONS)
   - Adjust fetch interval (FETCH_INTERVAL_MINUTES)
   - Modify dashboard visualizations in `src/app.py`

---

## Support

Need help? Check:
1. [README.md](README.md) - Main documentation
2. [football_api_docs.md](football_api_docs.md) - API reference
3. Run `python test_system.py` to verify setup

---

## Tips for Best Experience

- 🔑 **Get your API key first** - It's free and takes 1 minute
- ⏰ **Be patient** - First data fetch may take 1-2 minutes
- 📊 **Explore filters** - The dashboard is most powerful with filters
- 🔄 **Use scheduler** - For continuous monitoring
- 📓 **Try notebooks** - For deeper data exploration

---

**Ready to go?** Run `streamlit run src/app.py` and enjoy! 🎉
