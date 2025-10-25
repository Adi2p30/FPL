"""
FPL Advanced Metrics Module
============================

This module provides advanced football metrics and position-specific analysis
techniques inspired by popular FPL content creators and analysts.

Includes:
- xG (Expected Goals) calculations and variations
- Position-specific metrics (GKP, DEF, MID, FWD)
- Form analysis and fixture difficulty
- Value metrics and captain picks
- Underlying stats analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class AdvancedMetrics:
    """
    Advanced FPL metrics calculator with position-specific analysis
    """

    def __init__(self, players_df: pd.DataFrame):
        """
        Initialize with players DataFrame from FPL API

        Args:
            players_df: DataFrame containing player data from FPL API
        """
        self.players_df = players_df.copy()
        self._prepare_data()

    def _prepare_data(self):
        """Prepare and clean data for calculations"""
        # Ensure numeric columns
        numeric_cols = [
            'minutes', 'goals_scored', 'assists', 'clean_sheets',
            'goals_conceded', 'saves', 'bonus', 'bps', 'influence',
            'creativity', 'threat', 'ict_index', 'total_points',
            'points_per_game', 'now_cost', 'selected_by_percent'
        ]

        for col in numeric_cols:
            if col in self.players_df.columns:
                self.players_df[col] = pd.to_numeric(self.players_df[col], errors='coerce')

        # Fill NaN values with 0 for per_90 columns
        per_90_cols = [col for col in self.players_df.columns if 'per_90' in col]
        for col in per_90_cols:
            self.players_df[col] = self.players_df[col].fillna(0)

    # ========================================================================
    # GENERAL METRICS (All Positions)
    # ========================================================================

    def calculate_points_per_million(self) -> pd.Series:
        """
        Metric 1: Points per million (Value metric)

        Popular metric used by FPL Wire, Let's Talk FPL
        Shows efficiency of points generation relative to price
        """
        cost = self.players_df['now_cost'] / 10  # Convert to millions
        return self.players_df['total_points'] / cost.replace(0, np.nan)

    def calculate_form_index(self, recent_games: int = 5) -> pd.Series:
        """
        Metric 2: Form Index

        Weighted recent form metric
        Higher weight on more recent performances
        """
        if 'form' in self.players_df.columns:
            form = pd.to_numeric(self.players_df['form'], errors='coerce')
            return form * 2  # Weighted form score
        return pd.Series(0, index=self.players_df.index)

    def calculate_xgi_per_90(self) -> pd.Series:
        """
        Metric 3: xGI per 90 (Expected Goal Involvements)

        Key metric used by FPL Focal, FPL BlackBox
        Combines xG and xA to show attacking threat
        """
        xg = self.players_df.get('expected_goals_per_90', 0)
        xa = self.players_df.get('expected_assists_per_90', 0)
        return pd.to_numeric(xg, errors='coerce').fillna(0) + \
               pd.to_numeric(xa, errors='coerce').fillna(0)

    def calculate_bonus_point_potential(self) -> pd.Series:
        """
        Metric 4: Bonus Point System (BPS) per 90

        Used by FPL General, FPL Raptor
        Predicts bonus point potential
        """
        minutes = self.players_df['minutes'].replace(0, 1)
        bps = pd.to_numeric(self.players_df.get('bps', 0), errors='coerce')
        return (bps / minutes) * 90

    def calculate_threat_index(self) -> pd.Series:
        """
        Metric 5: Advanced Threat Index

        FPL's official threat metric normalized
        Shows goal-scoring potential
        """
        threat = pd.to_numeric(self.players_df.get('threat', 0), errors='coerce')
        return threat / 100  # Normalize

    def calculate_roi_metric(self) -> pd.Series:
        """
        Metric 6: Return on Investment (ROI)

        Points per million adjusted for ownership
        Finds differential picks
        """
        ppm = self.calculate_points_per_million()
        ownership = pd.to_numeric(
            self.players_df.get('selected_by_percent', 1),
            errors='coerce'
        ).replace(0, 1)

        # Higher ROI for low ownership + high points
        return ppm * (100 / ownership)

    # ========================================================================
    # FORWARD-SPECIFIC METRICS
    # ========================================================================

    def calculate_forward_metrics(self) -> pd.DataFrame:
        """
        Metrics 7-9: Forward-specific calculations

        Used by FPL content creators for striker analysis
        """
        forwards = self.players_df[self.players_df['element_type'] == 4].copy()

        if forwards.empty:
            return pd.DataFrame()

        # Metric 7: Shot Quality Score
        xg_per_90 = pd.to_numeric(
            forwards.get('expected_goals_per_90', 0),
            errors='coerce'
        ).fillna(0)

        # Metric 8: Big Chance Conversion (proxy using xG vs actual goals)
        minutes = forwards['minutes'].replace(0, 1)
        actual_goals_per_90 = (forwards['goals_scored'] / minutes) * 90
        conversion_rate = actual_goals_per_90 / xg_per_90.replace(0, np.nan)

        # Metric 9: Penalty Box Threat (using threat metric)
        penalty_box_threat = pd.to_numeric(
            forwards.get('threat', 0),
            errors='coerce'
        ) / forwards['minutes'].replace(0, 1) * 90

        forwards['shot_quality'] = xg_per_90
        forwards['conversion_rate'] = conversion_rate.fillna(0)
        forwards['penalty_box_threat'] = penalty_box_threat
        forwards['forward_score'] = (
            xg_per_90 * 3 +
            conversion_rate.fillna(1) * 2 +
            penalty_box_threat / 100
        )

        return forwards[[
            'web_name', 'team', 'now_cost',
            'shot_quality', 'conversion_rate',
            'penalty_box_threat', 'forward_score'
        ]]

    # ========================================================================
    # MIDFIELDER-SPECIFIC METRICS
    # ========================================================================

    def calculate_midfielder_metrics(self) -> pd.DataFrame:
        """
        Metrics 10-12: Midfielder-specific calculations

        Combines attacking and creative metrics
        """
        midfielders = self.players_df[self.players_df['element_type'] == 3].copy()

        if midfielders.empty:
            return pd.DataFrame()

        # Metric 10: Creativity Index (official FPL metric enhanced)
        creativity = pd.to_numeric(
            midfielders.get('creativity', 0),
            errors='coerce'
        )

        # Metric 11: Expected Assists per 90
        xa_per_90 = pd.to_numeric(
            midfielders.get('expected_assists_per_90', 0),
            errors='coerce'
        ).fillna(0)

        # Metric 12: Goal Involvement Index (combines xG and xA)
        xg_per_90 = pd.to_numeric(
            midfielders.get('expected_goals_per_90', 0),
            errors='coerce'
        ).fillna(0)

        xgi = xg_per_90 + xa_per_90

        # Balanced midfielder score
        midfielders['creativity_index'] = creativity / 100
        midfielders['xa_per_90'] = xa_per_90
        midfielders['xgi_per_90'] = xgi
        midfielders['midfielder_score'] = (
            xgi * 5 +
            creativity / 100 * 3 +
            midfielders['bonus'] / midfielders['minutes'].replace(0, 1) * 90 * 2
        )

        return midfielders[[
            'web_name', 'team', 'now_cost',
            'creativity_index', 'xa_per_90',
            'xgi_per_90', 'midfielder_score'
        ]]

    # ========================================================================
    # DEFENDER-SPECIFIC METRICS
    # ========================================================================

    def calculate_defender_metrics(self) -> pd.DataFrame:
        """
        Metrics 13-15: Defender-specific calculations

        Clean sheet probability and attacking potential
        """
        defenders = self.players_df[self.players_df['element_type'] == 2].copy()

        if defenders.empty:
            return pd.DataFrame()

        # Metric 13: Clean Sheet Probability
        matches_played = defenders['minutes'] / 90
        cs_rate = defenders['clean_sheets'] / matches_played.replace(0, np.nan)

        # Metric 14: Expected Goals Conceded per 90
        xgc_per_90 = pd.to_numeric(
            defenders.get('expected_goals_conceded_per_90', 0),
            errors='coerce'
        ).fillna(0)

        # Lower xGC is better - invert for scoring
        defensive_quality = 2 - xgc_per_90.clip(upper=2)

        # Metric 15: Attacking Defender Score (xGI for defenders)
        xgi = pd.to_numeric(
            defenders.get('expected_goal_involvements_per_90', 0),
            errors='coerce'
        ).fillna(0)

        defenders['clean_sheet_prob'] = cs_rate.fillna(0) * 100
        defenders['defensive_quality'] = defensive_quality
        defenders['attacking_threat'] = xgi
        defenders['defender_score'] = (
            cs_rate.fillna(0) * 6 +  # CS worth 4 points, weighted
            defensive_quality * 3 +
            xgi * 4 +  # Attacking returns valuable for defenders
            defenders['bonus'] / defenders['minutes'].replace(0, 1) * 90
        )

        return defenders[[
            'web_name', 'team', 'now_cost',
            'clean_sheet_prob', 'defensive_quality',
            'attacking_threat', 'defender_score'
        ]]

    # ========================================================================
    # GOALKEEPER-SPECIFIC METRICS
    # ========================================================================

    def calculate_goalkeeper_metrics(self) -> pd.DataFrame:
        """
        Metrics 16-18: Goalkeeper-specific calculations

        Save percentage, clean sheets, and bonus potential
        """
        goalkeepers = self.players_df[self.players_df['element_type'] == 1].copy()

        if goalkeepers.empty:
            return pd.DataFrame()

        # Metric 16: Save Percentage & Saves per 90
        saves_per_90 = pd.to_numeric(
            goalkeepers.get('saves_per_90', 0),
            errors='coerce'
        ).fillna(0)

        # Metric 17: Expected Goals Prevented (xG - actual goals conceded)
        xgc_per_90 = pd.to_numeric(
            goalkeepers.get('expected_goals_conceded_per_90', 0),
            errors='coerce'
        ).fillna(0)

        minutes = goalkeepers['minutes'].replace(0, 1)
        actual_gc_per_90 = (goalkeepers['goals_conceded'] / minutes) * 90
        xg_prevented = xgc_per_90 - actual_gc_per_90

        # Metric 18: Clean Sheet Percentage
        matches = minutes / 90
        cs_percentage = (goalkeepers['clean_sheets'] / matches.replace(0, np.nan)) * 100

        goalkeepers['saves_per_90'] = saves_per_90
        goalkeepers['xg_prevented'] = xg_prevented
        goalkeepers['cs_percentage'] = cs_percentage.fillna(0)
        goalkeepers['goalkeeper_score'] = (
            cs_percentage.fillna(0) / 10 * 4 +  # CS worth 4 points
            xg_prevented * 5 +  # Reward overperformance
            saves_per_90 * 0.5 +  # Saves contribute to BPS
            goalkeepers['bonus'] / minutes * 90
        )

        return goalkeepers[[
            'web_name', 'team', 'now_cost',
            'saves_per_90', 'xg_prevented',
            'cs_percentage', 'goalkeeper_score'
        ]]

    # ========================================================================
    # CAPTAIN ANALYSIS
    # ========================================================================

    def calculate_captain_score(self, upcoming_fixtures: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Metric 19: Captain Score

        Identifies best captaincy options based on form, fixtures, and consistency
        Used by Let's Talk FPL, FPL Focal for weekly captain picks
        """
        df = self.players_df.copy()

        # Base captain score on multiple factors
        form = pd.to_numeric(df.get('form', 0), errors='coerce').fillna(0)
        xgi = self.calculate_xgi_per_90()
        ppm = self.calculate_points_per_million()
        minutes_reliability = (df['minutes'] / df['minutes'].max()).fillna(0)

        # Weighted captain score
        captain_score = (
            form * 3 +                    # Recent form heavily weighted
            xgi * 10 +                    # Underlying stats important
            ppm / 10 +                    # Value consideration
            minutes_reliability * 2       # Nailedness important
        )

        result = pd.DataFrame({
            'web_name': df['web_name'],
            'team': df['team'],
            'position': df['element_type'].map({1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}),
            'form': form,
            'xgi_per_90': xgi,
            'minutes_reliability': minutes_reliability * 100,
            'captain_score': captain_score
        })

        return result.sort_values('captain_score', ascending=False)

    # ========================================================================
    # DIFFERENTIAL FINDER
    # ========================================================================

    def find_differentials(self, max_ownership: float = 10.0, min_points: int = 20) -> pd.DataFrame:
        """
        Metric 20: Differential Players

        Finds low-owned players with strong metrics
        Popular strategy from FPL Wire, FPL BlackBox
        """
        ownership = pd.to_numeric(
            self.players_df.get('selected_by_percent', 0),
            errors='coerce'
        ).fillna(0)

        points = self.players_df['total_points']

        # Filter low ownership, decent points
        mask = (ownership < max_ownership) & (points >= min_points)
        differentials = self.players_df[mask].copy()

        if differentials.empty:
            return pd.DataFrame()

        # Calculate differential score
        xgi = self.calculate_xgi_per_90()[mask]
        ppm = self.calculate_points_per_million()[mask]

        differentials['ownership'] = ownership[mask]
        differentials['xgi_per_90'] = xgi
        differentials['ppm'] = ppm
        differentials['differential_score'] = (
            ppm * 2 +
            xgi * 5 +
            (max_ownership - ownership[mask]) * 0.5  # Reward lower ownership
        )

        return differentials[[
            'web_name', 'team', 'element_type', 'now_cost',
            'total_points', 'ownership', 'xgi_per_90',
            'ppm', 'differential_score'
        ]].sort_values('differential_score', ascending=False)

    # ========================================================================
    # FIXTURE DIFFICULTY & FORM
    # ========================================================================

    def calculate_form_vs_fixture(self, fixture_difficulty: Optional[Dict] = None) -> pd.DataFrame:
        """
        Metric 21: Form vs Fixture Analysis

        Combines current form with upcoming fixture difficulty
        Technique used by FPL General, FPL Raptor
        """
        df = self.players_df.copy()

        form = pd.to_numeric(df.get('form', 0), errors='coerce').fillna(0)

        # If fixture difficulty provided, factor it in
        if fixture_difficulty:
            # This would integrate with fixture data
            # Placeholder for demonstration
            df['fixture_ease'] = 3  # Neutral difficulty
        else:
            df['fixture_ease'] = 3

        # Form-Fixture score (higher = better pick)
        df['form_fixture_score'] = form * df['fixture_ease']

        return df[[
            'web_name', 'team', 'element_type',
            'form', 'fixture_ease', 'form_fixture_score'
        ]].sort_values('form_fixture_score', ascending=False)

    # ========================================================================
    # COMPREHENSIVE PLAYER ANALYSIS
    # ========================================================================

    def get_comprehensive_analysis(self) -> pd.DataFrame:
        """
        Generate comprehensive analysis with all key metrics

        Returns a DataFrame with all calculated metrics for easy comparison
        """
        df = self.players_df.copy()

        # Add all general metrics
        df['points_per_million'] = self.calculate_points_per_million()
        df['xgi_per_90'] = self.calculate_xgi_per_90()
        df['bps_per_90'] = self.calculate_bonus_point_potential()
        df['threat_index'] = self.calculate_threat_index()
        df['roi_metric'] = self.calculate_roi_metric()

        # Add position label
        df['position'] = df['element_type'].map({
            1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'
        })

        # Select key columns for display
        analysis_cols = [
            'web_name', 'team', 'position', 'now_cost',
            'total_points', 'points_per_million', 'form',
            'xgi_per_90', 'bps_per_90', 'threat_index',
            'roi_metric', 'selected_by_percent', 'minutes'
        ]

        return df[[col for col in analysis_cols if col in df.columns]]

    # ========================================================================
    # EXPORT FUNCTIONS
    # ========================================================================

    def export_all_metrics(self, output_dir: str = './Data/') -> Dict[str, pd.DataFrame]:
        """
        Export all calculated metrics to separate DataFrames

        Returns dictionary with all metric DataFrames
        """
        metrics = {
            'comprehensive': self.get_comprehensive_analysis(),
            'forwards': self.calculate_forward_metrics(),
            'midfielders': self.calculate_midfielder_metrics(),
            'defenders': self.calculate_defender_metrics(),
            'goalkeepers': self.calculate_goalkeeper_metrics(),
            'captains': self.calculate_captain_score(),
            'differentials': self.find_differentials(),
            'form_fixture': self.calculate_form_vs_fixture()
        }

        return metrics


# ============================================================================
# FIXTURE ANALYSIS CLASS
# ============================================================================

class FixtureAnalysis:
    """
    Fixture difficulty and schedule analysis

    Techniques from FPL content creators for fixture planning
    """

    def __init__(self, fixtures_df: pd.DataFrame, teams_df: pd.DataFrame):
        """
        Initialize with fixtures and teams data

        Args:
            fixtures_df: Fixtures data from FPL API
            teams_df: Teams data from FPL API
        """
        self.fixtures_df = fixtures_df.copy()
        self.teams_df = teams_df.copy()

    def calculate_fixture_difficulty_rating(self, team_id: int, next_n_games: int = 5) -> float:
        """
        Calculate FDR (Fixture Difficulty Rating) for upcoming games

        Used by FPL community for transfer planning
        """
        team_fixtures = self.fixtures_df[
            (self.fixtures_df['team_h'] == team_id) |
            (self.fixtures_df['team_a'] == team_id)
        ].head(next_n_games)

        if team_fixtures.empty:
            return 0.0

        avg_difficulty = team_fixtures['difficulty'].mean() if 'difficulty' in team_fixtures.columns else 3.0
        return avg_difficulty

    def find_best_fixture_runs(self, games: int = 5, top_n: int = 10) -> pd.DataFrame:
        """
        Find teams with the best upcoming fixture runs

        Popular for planning transfers and building teams
        """
        fixture_ratings = []

        for _, team in self.teams_df.iterrows():
            team_id = team.get('id', team.name)
            fdr = self.calculate_fixture_difficulty_rating(team_id, games)

            fixture_ratings.append({
                'team_id': team_id,
                'team_name': team.get('name', 'Unknown'),
                'avg_fdr': fdr,
                'fixture_quality': 6 - fdr  # Invert so higher is better
            })

        result = pd.DataFrame(fixture_ratings)
        return result.sort_values('fixture_quality', ascending=False).head(top_n)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_fpl_data(json_path: str = './Data/players_2025-01-22.json') -> pd.DataFrame:
    """
    Load FPL player data from JSON

    Args:
        json_path: Path to player data JSON file

    Returns:
        DataFrame with player data
    """
    import json

    with open(json_path, 'r') as f:
        data = json.load(f)

    if isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict) and 'elements' in data:
        return pd.DataFrame(data['elements'])
    else:
        raise ValueError("Unexpected JSON format")


def generate_metric_summary() -> str:
    """
    Generate a summary of all available metrics

    Returns description of all 21+ metrics
    """
    summary = """
    FPL Advanced Metrics Summary
    ============================

    GENERAL METRICS (All Positions):
    1. Points per Million (PPM) - Value efficiency metric
    2. Form Index - Weighted recent performance
    3. xGI per 90 - Expected Goal Involvements
    4. Bonus Point Potential - BPS per 90
    5. Threat Index - Goal-scoring potential
    6. ROI Metric - Return on Investment (differential finder)

    FORWARD METRICS (FWD):
    7. Shot Quality Score - xG per 90
    8. Conversion Rate - Actual vs expected goals
    9. Penalty Box Threat - Positional threat

    MIDFIELDER METRICS (MID):
    10. Creativity Index - Chance creation
    11. xA per 90 - Expected assists
    12. Goal Involvement - Combined xG + xA

    DEFENDER METRICS (DEF):
    13. Clean Sheet Probability - CS likelihood
    14. Defensive Quality - xGC based rating
    15. Attacking Threat - xGI for defenders

    GOALKEEPER METRICS (GKP):
    16. Saves per 90 - Save frequency
    17. xG Prevented - Performance vs expected
    18. Clean Sheet Percentage - CS rate

    STRATEGIC METRICS:
    19. Captain Score - Best captaincy options
    20. Differential Score - Low-owned gems
    21. Form vs Fixture - Combined analysis

    Plus comprehensive analysis, fixture difficulty ratings, and more!
    """

    return summary


if __name__ == "__main__":
    # Example usage
    print("FPL Advanced Metrics Module")
    print("=" * 50)
    print(generate_metric_summary())
    print("\nUse: from advanced_metrics import AdvancedMetrics")
    print("Then: metrics = AdvancedMetrics(players_df)")
