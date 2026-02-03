"""
Data fetcher for the Real-Time Sports Analytics System.
Handles API calls to Football-Data.org and saves responses.
"""

import os
import json
import logging
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_dir = Path('data/logs')
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'data/logs/app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FootballDataFetcher:
    """Fetches data from Football-Data.org API."""
    
    def __init__(self):
        """Initialize the data fetcher."""
        self.api_key = os.getenv('FOOTBALL_API_KEY')
        if not self.api_key or self.api_key == 'your_api_key_here':
            logger.warning("API key not configured. Please set FOOTBALL_API_KEY in .env file")
        
        self.base_url = os.getenv('API_BASE_URL', 'https://api.football-data.org/v4')
        self.headers = {
            'X-Auth-Token': self.api_key
        }
        self.snapshot_dir = Path('data/snapshots')
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting: 10 requests per minute for free tier
        self.request_delay = 6  # seconds
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.request_delay:
            sleep_time = self.request_delay - time_since_last_request
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Make API request with error handling.
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            
        Returns:
            JSON response or None if error
        """
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            latency = time.time() - start_time
            
            if response.status_code == 200:
                logger.info(f"SUCCESS: {endpoint} (latency: {latency:.2f}s)")
                return response.json()
            elif response.status_code == 429:
                logger.warning("Rate limit exceeded. Waiting 60 seconds...")
                time.sleep(60)
                return self._make_request(endpoint, params)
            else:
                logger.error(f"ERROR {response.status_code}: {endpoint} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"REQUEST FAILED: {endpoint} - {str(e)}")
            return None
    
    def _save_snapshot(self, data: Dict, name: str):
        """
        Save API response as timestamped JSON file.
        
        Args:
            data: Response data to save
            name: Base name for the file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.json"
        filepath = self.snapshot_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Snapshot saved: {filepath}")
        except Exception as e:
            logger.error(f"Error saving snapshot: {e}")
    
    def fetch_competitions(self) -> Optional[Dict]:
        """Fetch available competitions."""
        logger.info("Fetching competitions...")
        data = self._make_request('competitions')
        if data:
            self._save_snapshot(data, 'competitions')
        return data
    
    def fetch_matches(self, competition_code: str = None, 
                     date_from: str = None, 
                     date_to: str = None,
                     status: str = None) -> Optional[Dict]:
        """
        Fetch matches for a competition or across competitions.
        
        Args:
            competition_code: Competition code (e.g., 'PL', 'CL')
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            status: Match status (SCHEDULED, LIVE, FINISHED, etc.)
            
        Returns:
            Matches data
        """
        params = {}
        if date_from:
            params['dateFrom'] = date_from
        if date_to:
            params['dateTo'] = date_to
        if status:
            params['status'] = status
        
        if competition_code:
            endpoint = f'competitions/{competition_code}/matches'
            logger.info(f"Fetching matches for {competition_code}...")
        else:
            endpoint = 'matches'
            logger.info("Fetching matches across competitions...")
        
        data = self._make_request(endpoint, params)
        if data:
            snapshot_name = f'matches_{competition_code}' if competition_code else 'matches_all'
            self._save_snapshot(data, snapshot_name)
        return data
    
    def fetch_team(self, team_id: int) -> Optional[Dict]:
        """
        Fetch team information.
        
        Args:
            team_id: Team ID
            
        Returns:
            Team data
        """
        logger.info(f"Fetching team {team_id}...")
        data = self._make_request(f'teams/{team_id}')
        if data:
            self._save_snapshot(data, f'team_{team_id}')
        return data
    
    def fetch_team_matches(self, team_id: int, 
                          date_from: str = None, 
                          date_to: str = None) -> Optional[Dict]:
        """
        Fetch matches for a specific team.
        
        Args:
            team_id: Team ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            
        Returns:
            Team matches data
        """
        params = {}
        if date_from:
            params['dateFrom'] = date_from
        if date_to:
            params['dateTo'] = date_to
        
        logger.info(f"Fetching matches for team {team_id}...")
        data = self._make_request(f'teams/{team_id}/matches', params)
        if data:
            self._save_snapshot(data, f'team_{team_id}_matches')
        return data
    
    def fetch_competition_standings(self, competition_code: str) -> Optional[Dict]:
        """
        Fetch standings for a competition.
        
        Args:
            competition_code: Competition code (e.g., 'PL', 'CL')
            
        Returns:
            Standings data
        """
        logger.info(f"Fetching standings for {competition_code}...")
        data = self._make_request(f'competitions/{competition_code}/standings')
        if data:
            self._save_snapshot(data, f'standings_{competition_code}')
        return data
    
    def fetch_competition_scorers(self, competition_code: str, limit: int = 20) -> Optional[Dict]:
        """
        Fetch top scorers for a competition.
        
        Args:
            competition_code: Competition code (e.g., 'PL', 'CL')
            limit: Number of scorers to return
            
        Returns:
            Top scorers data
        """
        logger.info(f"Fetching top scorers for {competition_code}...")
        params = {'limit': limit}
        data = self._make_request(f'competitions/{competition_code}/scorers', params)
        if data:
            self._save_snapshot(data, f'scorers_{competition_code}')
        return data
    
    def fetch_recent_data(self, competitions: List[str] = None, days: int = 7) -> Dict[str, Any]:
        """
        Fetch recent data for specified competitions.
        
        Args:
            competitions: List of competition codes
            days: Number of days to look back
            
        Returns:
            Dictionary with all fetched data
        """
        if competitions is None:
            competitions_str = os.getenv('DEFAULT_COMPETITIONS', 'PL,CL')
            competitions = [c.strip() for c in competitions_str.split(',')]
        
        date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')
        
        results = {
            'competitions': competitions,
            'date_range': {'from': date_from, 'to': date_to},
            'matches': {},
            'standings': {},
            'scorers': {}
        }
        
        for comp in competitions:
            logger.info(f"\n{'='*50}")
            logger.info(f"Processing competition: {comp}")
            logger.info(f"{'='*50}")
            
            # Fetch matches
            matches_data = self.fetch_matches(comp, date_from, date_to)
            if matches_data:
                results['matches'][comp] = matches_data
            
            # Fetch standings
            standings_data = self.fetch_competition_standings(comp)
            if standings_data:
                results['standings'][comp] = standings_data
            
            # Fetch top scorers
            scorers_data = self.fetch_competition_scorers(comp)
            if scorers_data:
                results['scorers'][comp] = scorers_data
        
        logger.info(f"\n{'='*50}")
        logger.info("Data fetch completed")
        logger.info(f"{'='*50}\n")
        
        return results


def main():
    """Main function to test data fetching."""
    logger.info("Starting data fetch process...")
    
    fetcher = FootballDataFetcher()
    
    # Fetch recent data for default competitions
    results = fetcher.fetch_recent_data()
    
    # Print summary
    logger.info("\n" + "="*50)
    logger.info("FETCH SUMMARY")
    logger.info("="*50)
    for comp in results['competitions']:
        matches_count = len(results['matches'].get(comp, {}).get('matches', []))
        logger.info(f"{comp}: {matches_count} matches fetched")
    logger.info("="*50 + "\n")


if __name__ == '__main__':
    main()
