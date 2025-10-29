"""
Data Loader Utility
===================

Handles loading and caching FPL data from API
"""

import pandas as pd
import streamlit as st
from typing import Dict, Tuple
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Fpl_api import FPLapi_main_endpoint, players as get_players, teamdata
from advanced_metrics import AdvancedMetrics


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_fpl_data() -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
    """
    Load FPL data from API with caching

    Returns:
        Tuple of (players_df, teams_df, raw_data)
    """
    try:
        # Fetch data from FPL API
        raw_data = FPLapi_main_endpoint()

        # Extract players and teams
        players_df = get_players(raw_data)
        teams_df = teamdata(raw_data)

        # Ensure numeric columns
        numeric_cols = [
            'now_cost', 'total_points', 'points_per_game', 'minutes',
            'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
            'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat',
            'ict_index', 'selected_by_percent', 'form'
        ]

        for col in numeric_cols:
            if col in players_df.columns:
                players_df[col] = pd.to_numeric(players_df[col], errors='coerce')

        # Fill NaN values
        players_df = players_df.fillna(0)

        # Add position names
        position_map = {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}
        players_df['position'] = players_df['element_type'].map(position_map)

        # Add team names
        team_name_map = dict(zip(teams_df['id'], teams_df['name']))
        players_df['team_name'] = players_df['team'].map(team_name_map)

        # Convert cost to millions
        players_df['cost'] = players_df['now_cost'] / 10

        return players_df, teams_df, raw_data

    except Exception as e:
        st.error(f"Error loading FPL data: {e}")
        return pd.DataFrame(), pd.DataFrame(), {}


@st.cache_data(ttl=3600)
def load_advanced_metrics(_players_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate advanced metrics with caching

    Args:
        _players_df: Players DataFrame

    Returns:
        DataFrame with all advanced metrics
    """
    try:
        metrics = AdvancedMetrics(_players_df)
        analysis_df = metrics.get_comprehensive_analysis()

        # Add all calculated metrics
        analysis_df['ppm'] = metrics.calculate_points_per_million()
        analysis_df['captain_score'] = metrics.calculate_captain_score()['captain_score'].values

        return analysis_df

    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
        return _players_df


def get_player_by_name(players_df: pd.DataFrame, name: str) -> pd.Series:
    """
    Get player data by name

    Args:
        players_df: Players DataFrame
        name: Player name

    Returns:
        Player data as Series
    """
    player = players_df[players_df['web_name'] == name]
    if not player.empty:
        return player.iloc[0]
    return pd.Series()


def get_players_by_position(players_df: pd.DataFrame, position: str) -> pd.DataFrame:
    """
    Filter players by position

    Args:
        players_df: Players DataFrame
        position: Position (GKP, DEF, MID, FWD)

    Returns:
        Filtered DataFrame
    """
    return players_df[players_df['position'] == position]


def get_players_by_team(players_df: pd.DataFrame, team_name: str) -> pd.DataFrame:
    """
    Filter players by team

    Args:
        players_df: Players DataFrame
        team_name: Team name

    Returns:
        Filtered DataFrame
    """
    return players_df[players_df['team_name'] == team_name]


def filter_players(
    players_df: pd.DataFrame,
    position: str = None,
    team: str = None,
    min_cost: float = 0,
    max_cost: float = 20,
    min_points: int = 0,
    min_minutes: int = 0
) -> pd.DataFrame:
    """
    Filter players by multiple criteria

    Args:
        players_df: Players DataFrame
        position: Position filter
        team: Team filter
        min_cost: Minimum cost
        max_cost: Maximum cost
        min_points: Minimum total points
        min_minutes: Minimum minutes played

    Returns:
        Filtered DataFrame
    """
    df = players_df.copy()

    if position and position != 'All':
        df = df[df['position'] == position]

    if team and team != 'All':
        df = df[df['team_name'] == team]

    df = df[
        (df['cost'] >= min_cost) &
        (df['cost'] <= max_cost) &
        (df['total_points'] >= min_points) &
        (df['minutes'] >= min_minutes)
    ]

    return df


def get_top_players(
    players_df: pd.DataFrame,
    metric: str = 'total_points',
    n: int = 10,
    position: str = None
) -> pd.DataFrame:
    """
    Get top N players by metric

    Args:
        players_df: Players DataFrame
        metric: Metric to sort by
        n: Number of players
        position: Position filter

    Returns:
        Top N players
    """
    df = players_df.copy()

    if position and position != 'All':
        df = df[df['position'] == position]

    if metric in df.columns:
        return df.nlargest(n, metric)

    return df.head(n)


def calculate_team_stats(team_players: pd.DataFrame) -> Dict:
    """
    Calculate team statistics

    Args:
        team_players: DataFrame of selected team players

    Returns:
        Dictionary of team stats
    """
    if team_players.empty:
        return {
            'total_cost': 0,
            'total_points': 0,
            'avg_points': 0,
            'total_goals': 0,
            'total_assists': 0,
            'total_clean_sheets': 0,
            'avg_ownership': 0
        }

    return {
        'total_cost': team_players['cost'].sum(),
        'total_points': team_players['total_points'].sum(),
        'avg_points': team_players['total_points'].mean(),
        'total_goals': team_players['goals_scored'].sum(),
        'total_assists': team_players['assists'].sum(),
        'total_clean_sheets': team_players['clean_sheets'].sum(),
        'avg_ownership': team_players['selected_by_percent'].mean()
    }
