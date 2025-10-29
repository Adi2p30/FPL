"""
Enhanced FPL Metrics Module
============================

Comprehensive metrics for player decision making including:
- Expected points (xP) calculations
- Form trends and momentum
- Fixture difficulty analysis
- Value metrics (PPM, ROI, etc.)
- Underlying stats (xG, xA, shots, key passes)
- Differential scores
- Consistency metrics
- Upcoming gameweek predictions
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime


class EnhancedMetrics:
    """Enhanced metrics for comprehensive player analysis"""

    def __init__(self, players_df: pd.DataFrame, fixtures_df: Optional[pd.DataFrame] = None):
        self.players_df = players_df.copy()
        self.fixtures_df = fixtures_df
        self._prepare_data()

    def _prepare_data(self):
        """Prepare numeric columns"""
        numeric_cols = [
            'minutes', 'goals_scored', 'assists', 'total_points', 'form',
            'points_per_game', 'now_cost', 'selected_by_percent', 'bonus',
            'bps', 'influence', 'creativity', 'threat', 'ict_index',
            'clean_sheets', 'goals_conceded', 'saves'
        ]

        for col in numeric_cols:
            if col in self.players_df.columns:
                self.players_df[col] = pd.to_numeric(self.players_df[col], errors='coerce').fillna(0)

    def calculate_all_metrics(self) -> pd.DataFrame:
        """Calculate all enhanced metrics"""
        df = self.players_df.copy()

        # Basic metrics
        df['cost'] = df['now_cost'] / 10
        df['ppm'] = self._calculate_ppm()
        df['value_score'] = self._calculate_value_score()

        # Form metrics
        df['form_rating'] = self._calculate_form_rating()
        df['momentum'] = self._calculate_momentum()
        df['consistency'] = self._calculate_consistency()

        # Performance metrics
        df['xgi_per_90'] = self._calculate_xgi_per_90()
        df['expected_points'] = self._calculate_expected_points()
        df['overperformance'] = self._calculate_overperformance()

        # Efficiency metrics
        df['minutes_per_point'] = self._calculate_minutes_per_point()
        df['goal_involvement'] = self._calculate_goal_involvement()
        df['bonus_frequency'] = self._calculate_bonus_frequency()

        # Decision metrics
        df['transfer_priority'] = self._calculate_transfer_priority()
        df['captain_score'] = self._calculate_captain_score()
        df['differential_score'] = self._calculate_differential_score()

        # Advanced stats
        df['threat_rating'] = self._calculate_threat_rating()
        df['creativity_rating'] = self._calculate_creativity_rating()
        df['influence_rating'] = self._calculate_influence_rating()

        # Value metrics
        df['roi'] = self._calculate_roi()
        df['value_rank'] = self._calculate_value_rank()

        # Fixture adjusted
        if self.fixtures_df is not None:
            df['fdr_next_5'] = self._calculate_fdr_next_5()
            df['fixture_adjusted_score'] = self._calculate_fixture_adjusted_score()

        # Composite scores
        df['overall_score'] = self._calculate_overall_score(df)
        df['buy_score'] = self._calculate_buy_score(df)
        df['hold_score'] = self._calculate_hold_score(df)
        df['sell_score'] = self._calculate_sell_score(df)

        return df

    # Value Metrics
    def _calculate_ppm(self) -> pd.Series:
        """Points per million"""
        cost = self.players_df['now_cost'] / 10
        return self.players_df['total_points'] / cost.replace(0, np.nan)

    def _calculate_value_score(self) -> pd.Series:
        """Composite value score"""
        ppm = self._calculate_ppm()
        form = pd.to_numeric(self.players_df.get('form', 0), errors='coerce')
        ppg = self.players_df.get('points_per_game', 0)

        return (ppm * 0.4 + form * 5 * 0.3 + ppg * 0.3)

    def _calculate_roi(self) -> pd.Series:
        """Return on investment considering ownership"""
        ppm = self._calculate_ppm()
        ownership = pd.to_numeric(
            self.players_df.get('selected_by_percent', 1),
            errors='coerce'
        ).replace(0, 1)

        return ppm * (100 / ownership)

    def _calculate_value_rank(self) -> pd.Series:
        """Value ranking within position"""
        value_score = self._calculate_value_score()
        # Rank within element_type
        return self.players_df.groupby('element_type')['total_points'].rank(
            method='dense', ascending=False
        )

    # Form Metrics
    def _calculate_form_rating(self) -> pd.Series:
        """Enhanced form rating (0-10 scale)"""
        form = pd.to_numeric(self.players_df.get('form', 0), errors='coerce')
        # Normalize to 0-10
        max_form = form.max() if form.max() > 0 else 1
        return (form / max_form) * 10

    def _calculate_momentum(self) -> pd.Series:
        """Momentum score (improving/declining form)"""
        # Proxy: Compare form to points_per_game
        form = pd.to_numeric(self.players_df.get('form', 0), errors='coerce')
        ppg = self.players_df.get('points_per_game', 0)

        momentum = form - ppg
        # Normalize to -5 to +5
        return momentum.clip(-5, 5)

    def _calculate_consistency(self) -> pd.Series:
        """Consistency score (lower variance = higher consistency)"""
        # Proxy using total_points / games played
        minutes = self.players_df['minutes'].replace(0, 1)
        games_played = minutes / 90

        ppg = self.players_df['points_per_game']
        total_pts = self.players_df['total_points']

        # If consistent, total/games should be close to ppg
        variance_proxy = abs(total_pts / games_played.replace(0, 1) - ppg)

        # Invert and normalize (lower variance = higher score)
        max_var = variance_proxy.max() if variance_proxy.max() > 0 else 1
        return 10 - (variance_proxy / max_var * 10)

    # Performance Metrics
    def _calculate_xgi_per_90(self) -> pd.Series:
        """Expected goal involvements per 90"""
        xg = pd.to_numeric(
            self.players_df.get('expected_goals_per_90', 0),
            errors='coerce'
        ).fillna(0)

        xa = pd.to_numeric(
            self.players_df.get('expected_assists_per_90', 0),
            errors='coerce'
        ).fillna(0)

        return xg + xa

    def _calculate_expected_points(self) -> pd.Series:
        """Expected points next game"""
        form = pd.to_numeric(self.players_df.get('form', 0), errors='coerce')
        ppg = self.players_df.get('points_per_game', 0)
        xgi = self._calculate_xgi_per_90()

        # Weighted formula
        return (form * 0.4 + ppg * 0.3 + xgi * 2 * 0.3)

    def _calculate_overperformance(self) -> pd.Series:
        """How much player is over/underperforming xG+xA"""
        xgi = self._calculate_xgi_per_90()

        minutes = self.players_df['minutes'].replace(0, 1)
        actual_gi = (
            self.players_df['goals_scored'] + self.players_df['assists']
        ) / minutes * 90

        return actual_gi - xgi

    # Efficiency Metrics
    def _calculate_minutes_per_point(self) -> pd.Series:
        """Minutes needed per point (lower = better)"""
        minutes = self.players_df['minutes'].replace(0, 1)
        points = self.players_df['total_points'].replace(0, 1)

        return minutes / points

    def _calculate_goal_involvement(self) -> pd.Series:
        """% of team's goals involved in"""
        # Simplified: goals + assists
        return self.players_df['goals_scored'] + self.players_df['assists']

    def _calculate_bonus_frequency(self) -> pd.Series:
        """Bonus points per game"""
        minutes = self.players_df['minutes'].replace(0, 1)
        games = minutes / 90

        return self.players_df['bonus'] / games.replace(0, 1)

    # Decision Metrics
    def _calculate_transfer_priority(self) -> pd.Series:
        """Priority score for transferring IN"""
        form = pd.to_numeric(self.players_df.get('form', 0), errors='coerce')
        xgi = self._calculate_xgi_per_90()
        ppm = self._calculate_ppm()
        minutes = self.players_df['minutes']

        # Filter: must play regularly
        minutes_weight = (minutes / minutes.max()).fillna(0)

        return (
            form * 3 +
            xgi * 5 +
            ppm +
            minutes_weight * 2
        )

    def _calculate_captain_score(self) -> pd.Series:
        """Captain selection score"""
        form = pd.to_numeric(self.players_df.get('form', 0), errors='coerce')
        xgi = self._calculate_xgi_per_90()
        consistency = self._calculate_consistency()
        minutes = self.players_df['minutes']

        # Nailed on bonus
        nailed = (minutes > 1000).astype(int) * 2

        return (
            form * 4 +
            xgi * 8 +
            consistency +
            nailed
        )

    def _calculate_differential_score(self) -> pd.Series:
        """Differential player score (low ownership + high value)"""
        ownership = pd.to_numeric(
            self.players_df.get('selected_by_percent', 0),
            errors='coerce'
        )

        ppm = self._calculate_ppm()
        form = pd.to_numeric(self.players_df.get('form', 0), errors='coerce')

        # Inverse ownership weighting
        ownership_factor = 100 - ownership

        return (ownership_factor * 0.3 + ppm * 0.4 + form * 2 * 0.3)

    # Advanced Stats
    def _calculate_threat_rating(self) -> pd.Series:
        """Threat rating (0-10)"""
        threat = pd.to_numeric(
            self.players_df.get('threat', 0),
            errors='coerce'
        )

        max_threat = threat.max() if threat.max() > 0 else 1
        return (threat / max_threat) * 10

    def _calculate_creativity_rating(self) -> pd.Series:
        """Creativity rating (0-10)"""
        creativity = pd.to_numeric(
            self.players_df.get('creativity', 0),
            errors='coerce'
        )

        max_creativity = creativity.max() if creativity.max() > 0 else 1
        return (creativity / max_creativity) * 10

    def _calculate_influence_rating(self) -> pd.Series:
        """Influence rating (0-10)"""
        influence = pd.to_numeric(
            self.players_df.get('influence', 0),
            errors='coerce'
        )

        max_influence = influence.max() if influence.max() > 0 else 1
        return (influence / max_influence) * 10

    # Fixture Metrics
    def _calculate_fdr_next_5(self) -> pd.Series:
        """Fixture difficulty rating for next 5 games"""
        # Placeholder - would need fixture data
        return pd.Series(3.0, index=self.players_df.index)

    def _calculate_fixture_adjusted_score(self) -> pd.Series:
        """Score adjusted for fixture difficulty"""
        form = pd.to_numeric(self.players_df.get('form', 0), errors='coerce')
        fdr = self._calculate_fdr_next_5()

        # Lower FDR = easier fixtures = higher score
        fixture_bonus = (6 - fdr) / 5

        return form * fixture_bonus

    # Composite Scores
    def _calculate_overall_score(self, df: pd.DataFrame) -> pd.Series:
        """Overall player score (0-100)"""
        # Normalize and combine key metrics
        form_norm = df['form_rating'] / 10
        value_norm = df['value_score'] / df['value_score'].max() if df['value_score'].max() > 0 else 0
        xgi_norm = df['xgi_per_90'] / df['xgi_per_90'].max() if df['xgi_per_90'].max() > 0 else 0

        return (form_norm * 30 + value_norm * 40 + xgi_norm * 30) * 100

    def _calculate_buy_score(self, df: pd.DataFrame) -> pd.Series:
        """Score for buying/transferring IN"""
        return (
            df['transfer_priority'] * 0.4 +
            df['value_score'] * 0.3 +
            df['expected_points'] * 0.3
        )

    def _calculate_hold_score(self, df: pd.DataFrame) -> pd.Series:
        """Score for holding current player"""
        return (
            df['consistency'] * 0.4 +
            df['form_rating'] * 0.3 +
            df['momentum'] * 0.3
        )

    def _calculate_sell_score(self, df: pd.DataFrame) -> pd.Series:
        """Score for selling/transferring OUT (lower = sell)"""
        # Inverse of buy score
        return 100 - df['buy_score']

    def get_top_picks(self, position: Optional[int] = None, n: int = 20) -> pd.DataFrame:
        """Get top picks by overall score"""
        df = self.calculate_all_metrics()

        if position:
            df = df[df['element_type'] == position]

        return df.nlargest(n, 'overall_score')

    def get_transfers_in(self, max_cost: float = 15.0, position: Optional[int] = None, n: int = 20) -> pd.DataFrame:
        """Get best transfer IN targets"""
        df = self.calculate_all_metrics()

        df = df[df['cost'] <= max_cost]

        if position:
            df = df[df['element_type'] == position]

        return df.nlargest(n, 'buy_score')

    def get_differentials(self, max_ownership: float = 10.0, min_points: int = 30, n: int = 20) -> pd.DataFrame:
        """Get differential players"""
        df = self.calculate_all_metrics()

        ownership = pd.to_numeric(df.get('selected_by_percent', 0), errors='coerce')

        df = df[
            (ownership < max_ownership) &
            (df['total_points'] >= min_points)
        ]

        return df.nlargest(n, 'differential_score')

    def compare_players(self, player_ids: List[int]) -> pd.DataFrame:
        """Compare multiple players with all metrics"""
        df = self.calculate_all_metrics()

        comparison = df[df['id'].isin(player_ids)]

        # Select key metrics for comparison
        metrics_cols = [
            'web_name', 'cost', 'total_points', 'form', 'ppm',
            'form_rating', 'momentum', 'consistency',
            'xgi_per_90', 'expected_points', 'overperformance',
            'goal_involvement', 'bonus_frequency',
            'threat_rating', 'creativity_rating', 'influence_rating',
            'captain_score', 'differential_score',
            'overall_score', 'buy_score', 'hold_score'
        ]

        available_cols = [col for col in metrics_cols if col in comparison.columns]

        return comparison[available_cols]


# Metric descriptions for frontend
METRIC_DESCRIPTIONS = {
    'ppm': 'Points per million - value efficiency',
    'value_score': 'Composite value metric (PPM + Form + PPG)',
    'form_rating': 'Current form on 0-10 scale',
    'momentum': 'Form trend (improving vs declining)',
    'consistency': 'Score variance - higher = more consistent',
    'xgi_per_90': 'Expected goal involvements per 90 minutes',
    'expected_points': 'Predicted points next gameweek',
    'overperformance': 'Actual vs expected goal involvements',
    'minutes_per_point': 'Minutes needed per point (lower = better)',
    'goal_involvement': 'Total goals + assists',
    'bonus_frequency': 'Bonus points per game',
    'transfer_priority': 'Priority score for transferring IN',
    'captain_score': 'Captaincy selection score',
    'differential_score': 'Low-owned high-value score',
    'threat_rating': 'Goal-scoring threat (0-10)',
    'creativity_rating': 'Playmaking ability (0-10)',
    'influence_rating': 'Overall game influence (0-10)',
    'roi': 'Return on investment vs ownership',
    'overall_score': 'Composite score (0-100)',
    'buy_score': 'Transfer IN recommendation score',
    'hold_score': 'Keep player recommendation score',
    'sell_score': 'Transfer OUT score (higher = sell)',
}
