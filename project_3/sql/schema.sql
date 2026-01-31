-- Database Schema for Real-Time Sports Analytics System
-- SQLite Database

-- Matches Table: Store match-level data
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    utc_date TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,
    matchday INTEGER,
    stage VARCHAR(50),
    competition_id INTEGER,
    competition_name VARCHAR(100),
    season_start_year INTEGER,
    home_team_id INTEGER NOT NULL,
    home_team_name VARCHAR(100) NOT NULL,
    away_team_id INTEGER NOT NULL,
    away_team_name VARCHAR(100) NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    winner VARCHAR(20),
    duration VARCHAR(20),
    venue VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Player Stats Table: Store player-level performance data
CREATE TABLE IF NOT EXISTS player_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER,
    player_name VARCHAR(100) NOT NULL,
    team_id INTEGER NOT NULL,
    team_name VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    minutes_played INTEGER DEFAULT 0,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    shots INTEGER DEFAULT 0,
    shots_on_target INTEGER DEFAULT 0,
    passes INTEGER DEFAULT 0,
    passes_completed INTEGER DEFAULT 0,
    tackles INTEGER DEFAULT 0,
    interceptions INTEGER DEFAULT 0,
    fouls_committed INTEGER DEFAULT 0,
    fouls_drawn INTEGER DEFAULT 0,
    yellow_cards INTEGER DEFAULT 0,
    red_cards INTEGER DEFAULT 0,
    -- Derived Metrics
    efficiency REAL DEFAULT 0.0,
    involvement_rate REAL DEFAULT 0.0,
    form_score REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE
);

-- Teams Table: Store team information
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    short_name VARCHAR(50),
    tla VARCHAR(10),
    crest_url TEXT,
    founded INTEGER,
    venue VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(utc_date);
CREATE INDEX IF NOT EXISTS idx_matches_teams ON matches(home_team_id, away_team_id);
CREATE INDEX IF NOT EXISTS idx_matches_competition ON matches(competition_id);
CREATE INDEX IF NOT EXISTS idx_player_stats_match ON player_stats(match_id);
CREATE INDEX IF NOT EXISTS idx_player_stats_player ON player_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_player_stats_team ON player_stats(team_id);
CREATE INDEX IF NOT EXISTS idx_player_stats_created ON player_stats(created_at);

-- View: Player Performance Summary
CREATE VIEW IF NOT EXISTS player_performance_summary AS
SELECT 
    ps.player_id,
    ps.player_name,
    ps.team_name,
    ps.position,
    COUNT(DISTINCT ps.match_id) as matches_played,
    SUM(ps.minutes_played) as total_minutes,
    SUM(ps.goals) as total_goals,
    SUM(ps.assists) as total_assists,
    SUM(ps.shots) as total_shots,
    SUM(ps.passes) as total_passes,
    ROUND(AVG(ps.efficiency), 4) as avg_efficiency,
    ROUND(AVG(ps.involvement_rate), 4) as avg_involvement_rate,
    ROUND(AVG(ps.form_score), 4) as avg_form_score,
    MAX(ps.created_at) as last_updated
FROM player_stats ps
GROUP BY ps.player_id, ps.player_name, ps.team_name, ps.position;

-- View: Team Performance Summary
CREATE VIEW IF NOT EXISTS team_performance_summary AS
SELECT 
    ps.team_id,
    ps.team_name,
    COUNT(DISTINCT ps.match_id) as matches_played,
    SUM(ps.goals) as total_goals,
    SUM(ps.assists) as total_assists,
    ROUND(AVG(ps.efficiency), 4) as avg_efficiency,
    COUNT(DISTINCT ps.player_id) as squad_size
FROM player_stats ps
GROUP BY ps.team_id, ps.team_name;

-- View: Recent Matches
CREATE VIEW IF NOT EXISTS recent_matches AS
SELECT 
    m.match_id,
    m.utc_date,
    m.home_team_name,
    m.away_team_name,
    m.home_score,
    m.away_score,
    m.status,
    m.competition_name
FROM matches m
ORDER BY m.utc_date DESC
LIMIT 100;
