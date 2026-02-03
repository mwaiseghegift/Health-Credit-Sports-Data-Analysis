"""
Scheduler for automated data fetching.
Fetches data at specified intervals and processes it.
"""

import os
import time
import logging
from datetime import datetime
from pathlib import Path
import schedule
from dotenv import load_dotenv

from fetch_data import FootballDataFetcher
from process_data import DataProcessor

# Load environment variables
load_dotenv()

# Configure logging
log_dir = Path('data/logs')
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'data/logs/scheduler.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataScheduler:
    """Scheduler for automated data fetching and processing."""
    
    def __init__(self, interval_minutes: int = None):
        """
        Initialize the scheduler.
        
        Args:
            interval_minutes: Fetch interval in minutes (default from env)
        """
        if interval_minutes is None:
            interval_minutes = int(os.getenv('FETCH_INTERVAL_MINUTES', 10))
        
        self.interval_minutes = interval_minutes
        self.fetcher = FootballDataFetcher()
        self.processor = DataProcessor()
        
        logger.info(f"Scheduler initialized with {interval_minutes} minute interval")
    
    def fetch_and_process(self):
        """Fetch data from API and process it."""
        try:
            logger.info("\n" + "="*70)
            logger.info(f"Starting scheduled data fetch at {datetime.now()}")
            logger.info("="*70)
            
            start_time = time.time()
            
            # Fetch recent data
            results = self.fetcher.fetch_recent_data(days=7)
            
            # Process and store matches
            total_processed = 0
            for comp, matches_data in results['matches'].items():
                count = self.processor.process_and_store_matches(matches_data)
                total_processed += count
            
            # Process scorers data
            for comp, scorers_data in results['scorers'].items():
                self.processor.process_scorers_data(scorers_data)
            
            elapsed_time = time.time() - start_time
            
            logger.info("="*70)
            logger.info(f" Fetch completed successfully!")
            logger.info(f"   - Processed: {total_processed} matches")
            logger.info(f"   - Duration: {elapsed_time:.2f} seconds")
            logger.info(f"   - Next fetch: {self.interval_minutes} minutes")
            logger.info("="*70 + "\n")
            
        except Exception as e:
            logger.error(f" Error during scheduled fetch: {e}", exc_info=True)
    
    def run_once(self):
        """Run the fetch job once."""
        logger.info("Running one-time data fetch...")
        self.fetch_and_process()
        logger.info("One-time fetch completed")
    
    def start(self):
        """Start the scheduler."""
        logger.info(f"\n{'='*70}")
        logger.info(" Starting Real-Time Sports Analytics Scheduler")
        logger.info(f"{'='*70}")
        logger.info(f"Fetch interval: Every {self.interval_minutes} minutes")
        logger.info(f"Started at: {datetime.now()}")
        logger.info(f"{'='*70}\n")
        
        # Run immediately on start
        self.fetch_and_process()
        
        # Schedule periodic fetches
        schedule.every(self.interval_minutes).minutes.do(self.fetch_and_process)
        
        # Keep the scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n" + "="*70)
            logger.info("⏸  Scheduler stopped by user")
            logger.info("="*70 + "\n")
        except Exception as e:
            logger.error(f"Scheduler error: {e}", exc_info=True)
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        self.processor.close()
        logger.info("Cleanup completed")


def main():
    """Main function to run the scheduler."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Real-Time Sports Analytics Scheduler')
    parser.add_argument(
        '--interval',
        type=int,
        help='Fetch interval in minutes (default from .env)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (no scheduling)'
    )
    
    args = parser.parse_args()
    
    scheduler = DataScheduler(interval_minutes=args.interval)
    
    if args.once:
        scheduler.run_once()
    else:
        scheduler.start()


if __name__ == '__main__':
    main()
