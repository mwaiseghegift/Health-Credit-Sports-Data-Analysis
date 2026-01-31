#!/bin/bash
# Setup script for Real-Time Sports Analytics
# This script automates the initial setup process

set -e  # Exit on error

echo "======================================================"
echo "⚽ Real-Time Sports Analytics - Setup Script"
echo "======================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 detected: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your Football-Data.org API key"
    echo "   Get your free API key: https://www.football-data.org/client/register"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Initialize database
echo "💾 Initializing database..."
python -c "from src.db_utils import get_database_manager; db = get_database_manager(); db.close()"
echo "✅ Database initialized"
echo ""

# Run system tests
echo "🧪 Running system tests..."
python test_system.py
echo ""

echo "======================================================"
echo "🎉 Setup Complete!"
echo "======================================================"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env file and add your API key"
echo "   2. Run: python src/fetch_data.py (to fetch data)"
echo "   3. Run: streamlit run src/app.py (to launch dashboard)"
echo ""
echo "Or run with scheduler:"
echo "   python src/scheduler.py"
echo ""
echo "======================================================"
