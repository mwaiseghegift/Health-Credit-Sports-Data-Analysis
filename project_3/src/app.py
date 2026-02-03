"""
Real-Time Sports Analytics Dashboard
Interactive Streamlit dashboard for player performance tracking.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import logging

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from db_utils import get_database_manager
from fetch_data import FootballDataFetcher
from process_data import DataProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Real-Time Sports Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }
    h2 {
        color: #3b82f6;
        font-weight: 600;
    }
    h3 {
        color: #60a5fa;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_db_connection():
    """Get cached database connection."""
    return get_database_manager()


def load_data():
    """Load data from database."""
    db = get_db_connection()
    
    try:
        # Load matches
        matches_query = """
            SELECT * FROM matches 
            ORDER BY utc_date DESC 
            LIMIT 1000
        """
        matches = db.execute_query(matches_query)
        
        # Load player stats
        stats_query = """
            SELECT * FROM player_stats 
            ORDER BY created_at DESC 
            LIMIT 5000
        """
        player_stats = db.execute_query(stats_query)
        
        # Load team performance
        team_performance = db.get_team_performance()
        
        return matches, player_stats, team_performance
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


def display_header():
    """Display dashboard header."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(" Real-Time Sports Analytics")
        st.markdown("**Player Performance Tracker** | Live football data analysis and insights")
    
    with col2:
        if st.button("Refresh Data", use_container_width=True):
            st.cache_resource.clear()
            st.rerun()


def display_kpis(player_stats, matches):
    """Display key performance indicators."""
    st.subheader(" Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_matches = len(matches) if not matches.empty else 0
        st.metric(
            label="Total Matches",
            value=f"{total_matches:,}",
            delta=None
        )
    
    with col2:
        total_goals = int(player_stats['goals'].sum()) if not player_stats.empty else 0
        st.metric(
            label="Total Goals",
            value=f"{total_goals:,}",
            delta=None
        )
    
    with col3:
        total_assists = int(player_stats['assists'].sum()) if not player_stats.empty else 0
        st.metric(
            label="Total Assists",
            value=f"{total_assists:,}",
            delta=None
        )
    
    with col4:
        avg_efficiency = player_stats['efficiency'].mean() if not player_stats.empty else 0
        st.metric(
            label="Avg Efficiency",
            value=f"{avg_efficiency:.4f}",
            delta=None
        )


def display_top_performers(player_stats):
    """Display top performing players."""
    st.subheader(" Top Performers")
    
    if player_stats.empty:
        st.info("No player data available yet. Fetch some data to see top performers!")
        return
    
    # Filter out team-level aggregates
    individual_stats = player_stats[player_stats['player_id'].notna()].copy()
    
    if individual_stats.empty:
        # Show team-level stats if no individual player data
        st.info("Individual player stats not available. Showing team-level data:")
        team_stats = player_stats.groupby('team_name').agg({
            'goals': 'sum',
            'assists': 'sum',
            'minutes_played': 'sum',
            'efficiency': 'mean'
        }).reset_index()
        
        team_stats = team_stats.sort_values('goals', ascending=False).head(10)
        team_stats.columns = ['Team', 'Goals', 'Assists', 'Minutes', 'Avg Efficiency']
        st.dataframe(
            team_stats,
            use_container_width=True,
            hide_index=True
        )
        return
    
    # Aggregate by player
    top_players = individual_stats.groupby(['player_name', 'team_name']).agg({
        'goals': 'sum',
        'assists': 'sum',
        'minutes_played': 'sum',
        'efficiency': 'mean'
    }).reset_index()
    
    top_players = top_players.sort_values('goals', ascending=False).head(10)
    top_players.columns = ['Player', 'Team', 'Goals', 'Assists', 'Minutes', 'Avg Efficiency']
    
    st.dataframe(
        top_players,
        use_container_width=True,
        hide_index=True
    )


def display_performance_scatter(player_stats):
    """Display goals vs assists scatter plot."""
    st.subheader(" Performance Overview: Goals vs Assists")
    
    if player_stats.empty:
        st.info("No data available for visualization.")
        return
    
    # Aggregate by player
    perf_data = player_stats.groupby(['player_name', 'team_name']).agg({
        'goals': 'sum',
        'assists': 'sum',
        'minutes_played': 'sum'
    }).reset_index()
    
    if perf_data.empty or len(perf_data) < 2:
        st.info("Insufficient data for scatter plot.")
        return
    
    fig = px.scatter(
        perf_data,
        x='goals',
        y='assists',
        size='minutes_played',
        hover_data=['player_name', 'team_name'],
        title='Player Performance: Goals vs Assists',
        labels={'goals': 'Total Goals', 'assists': 'Total Assists'},
        color='team_name',
        size_max=30
    )
    
    fig.update_layout(
        height=500,
        hovermode='closest',
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_team_comparison(team_performance):
    """Display team comparison bar chart."""
    st.subheader(" Team Comparison")
    
    if team_performance.empty:
        st.info("No team data available yet.")
        return
    
    # Sort by total goals
    team_perf = team_performance.sort_values('total_goals', ascending=False).head(15)
    
    fig = px.bar(
        team_perf,
        x='team_name',
        y='total_goals',
        title='Team Performance: Total Goals',
        labels={'team_name': 'Team', 'total_goals': 'Total Goals'},
        color='total_goals',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=500,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_trend_analysis(player_stats):
    """Display performance trend over time."""
    st.subheader(" Trend Analysis: Performance Over Time")
    
    if player_stats.empty or 'created_at' not in player_stats.columns:
        st.info("No temporal data available for trend analysis.")
        return
    
    # Convert created_at to datetime
    trend_data = player_stats.copy()
    trend_data['date'] = pd.to_datetime(trend_data['created_at']).dt.date
    
    # Aggregate by date
    daily_stats = trend_data.groupby('date').agg({
        'goals': 'sum',
        'assists': 'sum',
        'efficiency': 'mean'
    }).reset_index()
    
    if daily_stats.empty or len(daily_stats) < 2:
        st.info("Insufficient temporal data for trend visualization.")
        return
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_stats['date'],
        y=daily_stats['goals'],
        mode='lines+markers',
        name='Goals',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_stats['date'],
        y=daily_stats['assists'],
        mode='lines+markers',
        name='Assists',
        line=dict(color='#10b981', width=3)
    ))
    
    fig.update_layout(
        title='Daily Performance Trends',
        xaxis_title='Date',
        yaxis_title='Count',
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_workload_analysis(player_stats):
    """Display workload vs performance bubble chart."""
    st.subheader(" Workload Analysis: Minutes vs Performance")
    
    if player_stats.empty:
        st.info("No data available for workload analysis.")
        return
    
    # Aggregate by player
    workload_data = player_stats.groupby(['player_name', 'team_name']).agg({
        'minutes_played': 'sum',
        'efficiency': 'mean',
        'goals': 'sum'
    }).reset_index()
    
    if workload_data.empty or len(workload_data) < 2:
        st.info("Insufficient data for workload visualization.")
        return
    
    fig = px.scatter(
        workload_data,
        x='minutes_played',
        y='efficiency',
        size='goals',
        hover_data=['player_name', 'team_name'],
        title='Workload vs Efficiency',
        labels={'minutes_played': 'Total Minutes Played', 'efficiency': 'Average Efficiency'},
        color='team_name',
        size_max=40
    )
    
    fig.update_layout(
        height=500,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_insights(player_stats, matches, team_performance):
    """Display automated insights."""
    st.subheader(" Key Insights")
    
    insights = []
    
    # Generate insights
    if not matches.empty:
        total_matches = len(matches)
        insights.append(f" **{total_matches}** matches tracked in the database")
    
    if not player_stats.empty:
        total_goals = int(player_stats['goals'].sum())
        avg_efficiency = player_stats['efficiency'].mean()
        insights.append(f" **{total_goals}** total goals scored with average efficiency of **{avg_efficiency:.4f}**")
    
    if not team_performance.empty and len(team_performance) > 0:
        top_team = team_performance.sort_values('total_goals', ascending=False).iloc[0]
        insights.append(f" **{top_team['team_name']}** leads with **{int(top_team['total_goals'])}** goals")
    
    # Display insights
    if insights:
        for insight in insights:
            st.markdown(f"- {insight}")
    else:
        st.info("No insights available yet. Fetch some data to generate insights!")
    
    # Additional insights section
    with st.expander(" Detailed Analysis"):
        st.markdown("""
        ### Analysis Notes
        - **Efficiency Metric**: Calculated as (goals + assists) / minutes_played
        - **Involvement Rate**: Calculated as (shots + passes) / minutes_played
        - **Form Score**: Rolling average of last 5 matches per player
        
        ### Data Collection
        - Data is fetched from Football-Data.org API
        - Updates can be scheduled every 10 minutes
        - All responses are saved as timestamped snapshots
        
        ### Recommendations
        1. Monitor players with declining efficiency over time
        2. Watch for workload-related performance drops
        3. Track team momentum through goal patterns
        """)


def display_sidebar_filters(matches, player_stats):
    """Display sidebar filters."""
    st.sidebar.header("Filters")
    
    # Date range filter
    st.sidebar.subheader("Date Range")
    if not matches.empty and 'utc_date' in matches.columns:
        matches['utc_date'] = pd.to_datetime(matches['utc_date'])
        min_date = matches['utc_date'].min().date()
        max_date = matches['utc_date'].max().date()
        
        date_range = st.sidebar.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    else:
        st.sidebar.info("No date data available")
        date_range = None
    
    # Team filter
    st.sidebar.subheader("Team")
    if not player_stats.empty and 'team_name' in player_stats.columns:
        teams = ['All'] + sorted(player_stats['team_name'].unique().tolist())
        selected_team = st.sidebar.selectbox("Select team", teams)
    else:
        selected_team = 'All'
    
    # Player filter
    st.sidebar.subheader("Player")
    if not player_stats.empty and 'player_name' in player_stats.columns:
        players = ['All'] + sorted(player_stats['player_name'].unique().tolist())
        selected_player = st.sidebar.selectbox("Select player", players)
    else:
        selected_player = 'All'
    
    return date_range, selected_team, selected_player


def display_data_fetch_section():
    """Display data fetch controls."""
    st.sidebar.markdown("---")
    st.sidebar.header(" Data Management")
    
    if st.sidebar.button("Fetch Latest Data", use_container_width=True):
        with st.spinner("Fetching data from API..."):
            try:
                fetcher = FootballDataFetcher()
                results = fetcher.fetch_recent_data(days=30)
                
                processor = DataProcessor()
                total_processed = 0
                
                for comp, matches_data in results['matches'].items():
                    count = processor.process_and_store_matches(matches_data)
                    total_processed += count
                
                processor.close()
                
                st.sidebar.success(f" Fetched and processed {total_processed} matches!")
                st.cache_resource.clear()
                st.rerun()
            except Exception as e:
                st.sidebar.error(f" Error fetching data: {str(e)}")


def main():
    """Main dashboard function."""
    # Display header
    display_header()
    
    # Load data
    matches, player_stats, team_performance = load_data()
    
    # Sidebar
    date_range, selected_team, selected_player = display_sidebar_filters(matches, player_stats)
    display_data_fetch_section()
    
    # Apply filters
    filtered_stats = player_stats.copy()
    if selected_team != 'All' and not filtered_stats.empty:
        filtered_stats = filtered_stats[filtered_stats['team_name'] == selected_team]
    if selected_player != 'All' and not filtered_stats.empty:
        filtered_stats = filtered_stats[filtered_stats['player_name'] == selected_player]
    
    # Main content
    st.markdown("---")
    
    # KPIs
    display_kpis(filtered_stats, matches)
    
    st.markdown("---")
    
    # Top performers
    display_top_performers(filtered_stats)
    
    st.markdown("---")
    
    # Visualizations in columns
    col1, col2 = st.columns(2)
    
    with col1:
        display_performance_scatter(filtered_stats)
    
    with col2:
        display_team_comparison(team_performance)
    
    st.markdown("---")
    
    # More visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        display_trend_analysis(filtered_stats)
    
    with col4:
        display_workload_analysis(filtered_stats)
    
    st.markdown("---")
    
    # Insights
    display_insights(filtered_stats, matches, team_performance)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #6b7280; padding: 20px;'>
            <p> Real-Time Sports Analytics Dashboard | Powered by Football-Data.org API</p>
            <p>Built with Streamlit, Plotly, and SQLite</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
