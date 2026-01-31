"""
Test script to verify the Real-Time Sports Analytics system.
Runs basic tests on all components.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test all imports work correctly."""
    print("\n🔍 Testing imports...")
    try:
        from db_utils import get_database_manager
        from fetch_data import FootballDataFetcher
        from process_data import DataProcessor
        print("   ✅ All imports successful")
        return True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False


def test_database():
    """Test database initialization."""
    print("\n🔍 Testing database...")
    try:
        from db_utils import get_database_manager
        db = get_database_manager()
        
        # Test basic query
        result = db.execute_query("SELECT COUNT(*) as count FROM matches")
        count = result.iloc[0]['count']
        print(f"   ✅ Database working - {count} matches in database")
        
        db.close()
        return True
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        return False


def test_data_processor():
    """Test data processor."""
    print("\n🔍 Testing data processor...")
    try:
        from process_data import DataProcessor
        processor = DataProcessor()
        
        # Test analytics summary
        summary = processor.get_analytics_summary()
        print(f"   ✅ Data processor working")
        print(f"      - Total matches: {summary['total_matches']}")
        print(f"      - Total goals: {summary['total_goals']}")
        
        processor.close()
        return True
    except Exception as e:
        print(f"   ❌ Data processor test failed: {e}")
        return False


def test_fetcher_init():
    """Test fetcher initialization."""
    print("\n🔍 Testing data fetcher...")
    try:
        from fetch_data import FootballDataFetcher
        fetcher = FootballDataFetcher()
        
        print(f"   ✅ Data fetcher initialized")
        print(f"      - API base URL: {fetcher.base_url}")
        print(f"      - API key configured: {'Yes' if fetcher.api_key and fetcher.api_key != 'your_api_key_here' else 'No (use .env file)'}")
        return True
    except Exception as e:
        print(f"   ❌ Data fetcher test failed: {e}")
        return False


def test_scheduler():
    """Test scheduler initialization."""
    print("\n🔍 Testing scheduler...")
    try:
        from scheduler import DataScheduler
        scheduler = DataScheduler(interval_minutes=10)
        
        print(f"   ✅ Scheduler initialized")
        print(f"      - Interval: {scheduler.interval_minutes} minutes")
        return True
    except Exception as e:
        print(f"   ❌ Scheduler test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("🚀 Real-Time Sports Analytics - System Tests")
    print("="*60)
    
    results = {
        'Imports': test_imports(),
        'Database': test_database(),
        'Data Processor': test_data_processor(),
        'Data Fetcher': test_fetcher_init(),
        'Scheduler': test_scheduler()
    }
    
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:.<30} {status}")
    
    print("="*60)
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Add your API key to .env file")
        print("   2. Run: python src/fetch_data.py (to get data)")
        print("   3. Run: streamlit run src/app.py (to launch dashboard)")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("")
    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
