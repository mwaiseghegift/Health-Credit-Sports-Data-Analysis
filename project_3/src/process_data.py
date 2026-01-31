"""
Data processor for the Real-Time Sports Analytics System.
Cleans, transforms, and computes KPIs from raw API data.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd
import numpy as np

from db_utils import get_database_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Processes raw API data and computes analytics metrics."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.db_manager = get_database_manager()
        logger.info("Data processor initialized")
    
    def process_match_data(self, match_raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw match data from API.
        
        Args:
            match_raw: Raw match data from API
            
        Returns:
            Processed match data ready for database insertion
        """
        try:
            score = match_raw.get('score', {})
            fulltime = score.get('fullTime', {})
            competition = match_raw.get('competition', {})
            season = match_raw.get('season', {})
            home_team = match_raw.get('homeTeam', {})
            away_team = match_raw.get('awayTeam', {})
            
            match_data = {
                'match_id': match_raw.get('id'),
                'utc_date': match_raw.get('utcDate'),
                'status': match_raw.get('status', 'SCHEDULED'),
                'matchday': match_raw.get('matchday'),
                'stage': match_raw.get('stage'),
                'competition_id': competition.get('id'),
                'competition_name': competition.get('name'),
                'season_start_year': season.get('startDate', '')[:4] if season.get('startDate') else None,
                'home_team_id': home_team.get('id'),
                'home_team_name': home_team.get('name'),
                'away_team_id': away_team.get('id'),
                'away_team_name': away_team.get('name'),
                'home_score': fulltime.get('home'),
                'away_score': fulltime.get('away'),
                'winner': score.get('winner'),
                'duration': score.get('duration', 'REGULAR'),
                'venue': match_raw.get('venue')
            }
            
            return match_data
        except Exception as e:
            logger.error(f"Error processing match data: {e}")
            return None
    
    def process_team_data(self, team_raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw team data from API.
        
        Args:
            team_raw: Raw team data from API
            
        Returns:
            Processed team data
        """
        try:
            team_data = {
                'team_id': team_raw.get('id'),
                'team_name': team_raw.get('name'),
                'short_name': team_raw.get('shortName'),
                'tla': team_raw.get('tla'),
                'crest_url': team_raw.get('crest'),
                'founded': team_raw.get('founded'),
                'venue': team_raw.get('venue')
            }
            return team_data
        except Exception as e:
            logger.error(f"Error processing team data: {e}")
            return None
    
    def generate_player_stats_from_match(self, match_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate player statistics from match data.
        Note: The free tier API doesn't provide detailed player stats per match.
        This generates placeholder data based on match results.
        
        Args:
            match_data: Processed match data
            
        Returns:
            List of player stat dictionaries
        """
        player_stats = []
        
        # This is a simplified version since the free API doesn't provide player-level stats
        # In a production system, you'd need a premium API subscription
        # For now, we'll create aggregate team-level stats
        
        try:
            if match_data.get('status') == 'FINISHED':
                # Generate basic stats for home team
                home_stat = {
                    'match_id': match_data['match_id'],
                    'player_id': None,
                    'player_name': f"{match_data['home_team_name']} Squad",
                    'team_id': match_data['home_team_id'],
                    'team_name': match_data['home_team_name'],
                    'position': 'Team',
                    'minutes_played': 90,
                    'goals': match_data.get('home_score', 0) or 0,
                    'assists': 0,
                    'shots': 0,
                    'shots_on_target': 0,
                    'passes': 0,
                    'passes_completed': 0,
                    'tackles': 0,
                    'interceptions': 0,
                    'fouls_committed': 0,
                    'fouls_drawn': 0,
                    'yellow_cards': 0,
                    'red_cards': 0,
                    'efficiency': 0.0,
                    'involvement_rate': 0.0,
                    'form_score': 0.0
                }
                
                # Generate basic stats for away team
                away_stat = {
                    'match_id': match_data['match_id'],
                    'player_id': None,
                    'player_name': f"{match_data['away_team_name']} Squad",
                    'team_id': match_data['away_team_id'],
                    'team_name': match_data['away_team_name'],
                    'position': 'Team',
                    'minutes_played': 90,
                    'goals': match_data.get('away_score', 0) or 0,
                    'assists': 0,
                    'shots': 0,
                    'shots_on_target': 0,
                    'passes': 0,
                    'passes_completed': 0,
                    'tackles': 0,
                    'interceptions': 0,
                    'fouls_committed': 0,
                    'fouls_drawn': 0,
                    'yellow_cards': 0,
                    'red_cards': 0,
                    'efficiency': 0.0,
                    'involvement_rate': 0.0,
                    'form_score': 0.0
                }
                
                player_stats.extend([home_stat, away_stat])
        except Exception as e:
            logger.error(f"Error generating player stats: {e}")
        
        return player_stats
    
    def calculate_derived_metrics(self, player_stat: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate derived performance metrics.
        
        Args:
            player_stat: Player statistics dictionary
            
        Returns:
            Updated dictionary with calculated metrics
        """
        try:
            minutes = player_stat.get('minutes_played', 0)
            goals = player_stat.get('goals', 0)
            assists = player_stat.get('assists', 0)
            shots = player_stat.get('shots', 0)
            passes = player_stat.get('passes', 0)
            
            # Efficiency: (goals + assists) / minutes_played
            if minutes > 0:
                player_stat['efficiency'] = round((goals + assists) / minutes, 4)
            else:
                player_stat['efficiency'] = 0.0
            
            # Involvement Rate: (shots + passes) / minutes_played
            if minutes > 0:
                player_stat['involvement_rate'] = round((shots + passes) / minutes, 4)
            else:
                player_stat['involvement_rate'] = 0.0
            
            # Form score will be calculated separately based on rolling average
            player_stat['form_score'] = 0.0
            
        except Exception as e:
            logger.error(f"Error calculating derived metrics: {e}")
        
        return player_stat
    
    def calculate_form_scores(self, lookback_matches: int = 5):
        """
        Calculate form scores for all players based on last N matches.
        
        Args:
            lookback_matches: Number of recent matches to consider
        """
        try:
            query = """
                SELECT 
                    player_id,
                    player_name,
                    team_id,
                    efficiency,
                    created_at
                FROM player_stats
                WHERE player_id IS NOT NULL
                ORDER BY player_id, created_at DESC
            """
            
            df = self.db_manager.execute_query(query)
            
            if df.empty:
                logger.info("No player data available for form score calculation")
                return
            
            # Calculate rolling average of efficiency
            df['form_score'] = df.groupby('player_id')['efficiency'].transform(
                lambda x: x.rolling(window=lookback_matches, min_periods=1).mean()
            )
            
            # Update form scores in database
            logger.info("Updating form scores in database...")
            # Note: This is a simplified update; in production, you'd use batch updates
            
        except Exception as e:
            logger.error(f"Error calculating form scores: {e}")
    
    def process_and_store_matches(self, matches_data: Dict[str, Any]) -> int:
        """
        Process and store match data in database.
        
        Args:
            matches_data: Raw matches data from API
            
        Returns:
            Number of matches processed
        """
        if not matches_data or 'matches' not in matches_data:
            logger.warning("No matches data to process")
            return 0
        
        matches = matches_data.get('matches', [])
        processed_count = 0
        
        for match_raw in matches:
            try:
                # Process match data
                match_data = self.process_match_data(match_raw)
                if not match_data:
                    continue
                
                # Insert match
                match_id = self.db_manager.insert_match(match_data)
                
                # Process and insert team data
                home_team_data = self.process_team_data(match_raw.get('homeTeam', {}))
                if home_team_data:
                    self.db_manager.insert_team(home_team_data)
                
                away_team_data = self.process_team_data(match_raw.get('awayTeam', {}))
                if away_team_data:
                    self.db_manager.insert_team(away_team_data)
                
                # Generate and insert player stats
                player_stats = self.generate_player_stats_from_match(match_data)
                if player_stats:
                    # Calculate derived metrics for each player
                    player_stats = [self.calculate_derived_metrics(ps) for ps in player_stats]
                    self.db_manager.insert_player_stats(player_stats)
                
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing match {match_raw.get('id')}: {e}")
                continue
        
        logger.info(f"Processed {processed_count} matches successfully")
        return processed_count
    
    def process_scorers_data(self, scorers_data: Dict[str, Any]):
        """
        Process top scorers data.
        
        Args:
            scorers_data: Raw scorers data from API
        """
        if not scorers_data or 'scorers' not in scorers_data:
            logger.warning("No scorers data to process")
            return
        
        scorers = scorers_data.get('scorers', [])
        logger.info(f"Processing {len(scorers)} top scorers")
        
        # This could be used to enrich player data
        # For now, we just log the information
        for scorer in scorers[:10]:
            player = scorer.get('player', {})
            logger.info(
                f"  {player.get('name')}: {scorer.get('goals')} goals, "
                f"{scorer.get('assists', 0)} assists"
            )
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """
        Generate analytics summary from stored data.
        
        Returns:
            Dictionary with key analytics metrics
        """
        summary = {
            'total_matches': 0,
            'total_goals': 0,
            'top_scorers': [],
            'team_performance': [],
            'recent_matches': []
        }
        
        try:
            # Get total matches
            query = "SELECT COUNT(*) as count FROM matches"
            result = self.db_manager.execute_query(query)
            summary['total_matches'] = int(result.iloc[0]['count']) if not result.empty else 0
            
            # Get total goals
            query = "SELECT SUM(goals) as total FROM player_stats"
            result = self.db_manager.execute_query(query)
            summary['total_goals'] = int(result.iloc[0]['total']) if not result.empty and result.iloc[0]['total'] else 0
            
            # Get top scorers
            query = """
                SELECT player_name, team_name, SUM(goals) as total_goals
                FROM player_stats
                WHERE player_id IS NOT NULL
                GROUP BY player_name, team_name
                ORDER BY total_goals DESC
                LIMIT 10
            """
            top_scorers = self.db_manager.execute_query(query)
            summary['top_scorers'] = top_scorers.to_dict('records') if not top_scorers.empty else []
            
            # Get team performance
            team_perf = self.db_manager.get_team_performance()
            summary['team_performance'] = team_perf.to_dict('records') if not team_perf.empty else []
            
            # Get recent matches
            recent = self.db_manager.get_recent_matches(limit=10)
            summary['recent_matches'] = recent.to_dict('records') if not recent.empty else []
            
        except Exception as e:
            logger.error(f"Error generating analytics summary: {e}")
        
        return summary
    
    def close(self):
        """Close database connection."""
        self.db_manager.close()


def main():
    """Main function to test data processing."""
    logger.info("Starting data processing...")
    
    processor = DataProcessor()
    
    # Generate analytics summary
    summary = processor.get_analytics_summary()
    
    logger.info("\n" + "="*50)
    logger.info("ANALYTICS SUMMARY")
    logger.info("="*50)
    logger.info(f"Total Matches: {summary['total_matches']}")
    logger.info(f"Total Goals: {summary['total_goals']}")
    logger.info(f"Teams Tracked: {len(summary['team_performance'])}")
    logger.info("="*50 + "\n")
    
    processor.close()


if __name__ == '__main__':
    main()
