"""
Database utilities for the Real-Time Sports Analytics System.
Handles database connections, table creation, and data operations.
"""

import os
import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            db_path = os.getenv('DATABASE_PATH', 'data/sports.db')
        
        self.db_path = db_path
        self._ensure_data_directory()
        self.engine = self._create_engine()
        self._initialize_schema()
        logger.info(f"Database initialized at: {self.db_path}")
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _create_engine(self):
        """Create SQLAlchemy engine."""
        return create_engine(
            f'sqlite:///{self.db_path}',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
            echo=False
        )
    
    def _initialize_schema(self):
        """Initialize database schema from schema.sql."""
        schema_path = Path(__file__).parent.parent / 'sql' / 'schema.sql'
        
        if not schema_path.exists():
            logger.warning(f"Schema file not found at {schema_path}")
            return
        
        try:
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            # Split into individual statements
            statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
            
            with self.engine.connect() as conn:
                for statement in statements:
                    if statement:
                        conn.execute(text(statement))
                conn.commit()
            
            logger.info("Database schema initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing schema: {e}")
            raise
    
    def execute_query(self, query: str, params: Dict = None) -> pd.DataFrame:
        """
        Execute a SELECT query and return results as DataFrame.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            DataFrame with query results
        """
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql_query(query, conn, params=params)
            return df
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    def insert_match(self, match_data: Dict[str, Any]) -> int:
        """
        Insert or update match data.
        
        Args:
            match_data: Dictionary with match information
            
        Returns:
            Match ID
        """
        try:
            with self.engine.connect() as conn:
                # Check if match exists
                existing = conn.execute(
                    text("SELECT match_id FROM matches WHERE match_id = :match_id"),
                    {"match_id": match_data['match_id']}
                ).fetchone()
                
                if existing:
                    # Update existing match
                    update_query = text("""
                        UPDATE matches 
                        SET status = :status,
                            home_score = :home_score,
                            away_score = :away_score,
                            winner = :winner,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE match_id = :match_id
                    """)
                    conn.execute(update_query, match_data)
                    logger.info(f"Updated match {match_data['match_id']}")
                else:
                    # Insert new match
                    insert_query = text("""
                        INSERT INTO matches (
                            match_id, utc_date, status, matchday, stage,
                            competition_id, competition_name, season_start_year,
                            home_team_id, home_team_name, away_team_id, away_team_name,
                            home_score, away_score, winner, duration, venue
                        ) VALUES (
                            :match_id, :utc_date, :status, :matchday, :stage,
                            :competition_id, :competition_name, :season_start_year,
                            :home_team_id, :home_team_name, :away_team_id, :away_team_name,
                            :home_score, :away_score, :winner, :duration, :venue
                        )
                    """)
                    conn.execute(insert_query, match_data)
                    logger.info(f"Inserted new match {match_data['match_id']}")
                
                conn.commit()
                return match_data['match_id']
        except Exception as e:
            logger.error(f"Error inserting match: {e}")
            raise
    
    def insert_player_stats(self, player_stats: List[Dict[str, Any]]) -> int:
        """
        Insert player statistics.
        
        Args:
            player_stats: List of player stat dictionaries
            
        Returns:
            Number of records inserted
        """
        if not player_stats:
            return 0
        
        try:
            df = pd.DataFrame(player_stats)
            records_inserted = df.to_sql(
                'player_stats',
                self.engine,
                if_exists='append',
                index=False
            )
            logger.info(f"Inserted {len(player_stats)} player stat records")
            return records_inserted
        except Exception as e:
            logger.error(f"Error inserting player stats: {e}")
            raise
    
    def insert_team(self, team_data: Dict[str, Any]) -> int:
        """
        Insert or update team data.
        
        Args:
            team_data: Dictionary with team information
            
        Returns:
            Team ID
        """
        try:
            with self.engine.connect() as conn:
                # Check if team exists
                existing = conn.execute(
                    text("SELECT team_id FROM teams WHERE team_id = :team_id"),
                    {"team_id": team_data['team_id']}
                ).fetchone()
                
                if existing:
                    # Update existing team
                    update_query = text("""
                        UPDATE teams 
                        SET team_name = :team_name,
                            short_name = :short_name,
                            tla = :tla,
                            crest_url = :crest_url,
                            founded = :founded,
                            venue = :venue,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE team_id = :team_id
                    """)
                    conn.execute(update_query, team_data)
                else:
                    # Insert new team
                    insert_query = text("""
                        INSERT INTO teams (
                            team_id, team_name, short_name, tla, 
                            crest_url, founded, venue
                        ) VALUES (
                            :team_id, :team_name, :short_name, :tla,
                            :crest_url, :founded, :venue
                        )
                    """)
                    conn.execute(insert_query, team_data)
                
                conn.commit()
                return team_data['team_id']
        except Exception as e:
            logger.error(f"Error inserting team: {e}")
            raise
    
    def get_recent_matches(self, limit: int = 100) -> pd.DataFrame:
        """Get recent matches."""
        query = "SELECT * FROM recent_matches LIMIT :limit"
        return self.execute_query(query, {"limit": limit})
    
    def get_player_performance(self, player_id: int = None) -> pd.DataFrame:
        """Get player performance summary."""
        if player_id:
            query = """
                SELECT * FROM player_performance_summary 
                WHERE player_id = :player_id
            """
            return self.execute_query(query, {"player_id": player_id})
        else:
            query = "SELECT * FROM player_performance_summary"
            return self.execute_query(query)
    
    def get_team_performance(self, team_id: int = None) -> pd.DataFrame:
        """Get team performance summary."""
        if team_id:
            query = """
                SELECT * FROM team_performance_summary 
                WHERE team_id = :team_id
            """
            return self.execute_query(query, {"team_id": team_id})
        else:
            query = "SELECT * FROM team_performance_summary"
            return self.execute_query(query)
    
    def close(self):
        """Close database connection."""
        if hasattr(self, 'engine'):
            self.engine.dispose()
            logger.info("Database connection closed")


def get_database_manager() -> DatabaseManager:
    """
    Factory function to get database manager instance.
    
    Returns:
        DatabaseManager instance
    """
    return DatabaseManager()
