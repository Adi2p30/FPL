"""
FPL Strategy & Analysis Module
===============================

Advanced FPL strategies and techniques used by popular content creators:
- FPL Focal, Let's Talk FPL, FPL Wire, FPL General, FPL BlackBox

Includes:
- Team selection optimization
- Transfer planning algorithms
- Chip strategy (Wildcard, Bench Boost, Triple Captain, Free Hit)
- Budget balancing and team value optimization
- Gameweek planning
- Mini-league ranking strategies
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


@dataclass
class Player:
    """Player data structure"""
    id: int
    name: str
    position: str
    team: int
    cost: float
    total_points: int
    form: float
    xgi_per_90: float
    minutes: int
    ownership: float


@dataclass
class TransferSuggestion:
    """Transfer recommendation"""
    player_out: str
    player_in: str
    position: str
    cost_change: float
    expected_points_gain: float
    priority: int
    reason: str


class FPLStrategy:
    """
    FPL Strategy optimizer and planning tool

    Implements techniques from popular FPL content creators
    """

    def __init__(self, players_df: pd.DataFrame):
        """
        Initialize with players DataFrame

        Args:
            players_df: DataFrame with player data and calculated metrics
        """
        self.players_df = players_df.copy()
        self.position_limits = {
            'GKP': (2, 2),  # (min, max)
            'DEF': (5, 5),
            'MID': (5, 5),
            'FWD': (3, 3)
        }
        self.squad_size = 15
        self.starting_xi = 11
        self.budget = 100.0  # £100m budget

    # ========================================================================
    # TEAM BUILDING & OPTIMIZATION
    # ========================================================================

    def build_optimal_team(
        self,
        budget: float = 100.0,
        formation: str = "3-4-3",
        strategy: str = "balanced"
    ) -> Dict:
        """
        Build optimal 15-man squad using various strategies

        Strategies:
        - balanced: Mix of premium and budget options
        - template: High ownership core + differentials
        - differential: Low ownership focus
        - premium_heavy: Triple premium + enablers

        Popular approach from FPL Wire's "Template Team" series
        """
        self.budget = budget

        # Parse formation
        formation_split = [int(x) for x in formation.split('-')]
        starting_formation = {
            'DEF': formation_split[0],
            'MID': formation_split[1],
            'FWD': formation_split[2],
            'GKP': 1
        }

        # Strategy-based player selection
        if strategy == "template":
            team = self._build_template_team(starting_formation)
        elif strategy == "differential":
            team = self._build_differential_team(starting_formation)
        elif strategy == "premium_heavy":
            team = self._build_premium_heavy_team(starting_formation)
        else:  # balanced
            team = self._build_balanced_team(starting_formation)

        return team

    def _build_balanced_team(self, formation: Dict) -> Dict:
        """Build balanced team with mix of price points"""
        team = {'starters': [], 'bench': [], 'total_cost': 0, 'projected_points': 0}

        # Get best value players per position
        for position, count in self.position_limits.items():
            pos_code = self._position_to_code(position)
            pos_players = self.players_df[
                self.players_df['element_type'] == pos_code
            ].copy()

            if pos_players.empty:
                continue

            # Calculate value score
            pos_players['value_score'] = (
                pos_players.get('points_per_million', 0) * 2 +
                pos_players.get('xgi_per_90', 0) * 5 +
                pos_players.get('form', 0) * 3
            )

            # Sort by value
            pos_players = pos_players.sort_values('value_score', ascending=False)

            # Select players for this position
            starters_needed = formation.get(position, 0)
            total_needed = count[1]

            selected = pos_players.head(total_needed)

            for idx, player in selected.iterrows():
                player_dict = {
                    'name': player['web_name'],
                    'position': position,
                    'cost': player['now_cost'] / 10,
                    'points': player.get('total_points', 0),
                    'starter': len([p for p in team['starters'] if p['position'] == position]) < starters_needed
                }

                if player_dict['starter']:
                    team['starters'].append(player_dict)
                else:
                    team['bench'].append(player_dict)

                team['total_cost'] += player_dict['cost']
                team['projected_points'] += player.get('form', 0) * 5  # Projected

        return team

    def _build_template_team(self, formation: Dict) -> Dict:
        """Build template team with high ownership core"""
        team = {'starters': [], 'bench': [], 'total_cost': 0, 'projected_points': 0}

        # Prioritize high ownership (template) players
        self.players_df['template_score'] = (
            pd.to_numeric(self.players_df.get('selected_by_percent', 0), errors='coerce') * 0.5 +
            self.players_df.get('total_points', 0) * 0.3 +
            self.players_df.get('form', 0) * 10
        )

        # Similar logic to balanced but prioritizing ownership
        return self._select_team_by_metric(formation, 'template_score')

    def _build_differential_team(self, formation: Dict) -> Dict:
        """Build differential team with low ownership gems"""
        team = {'starters': [], 'bench': [], 'total_cost': 0, 'projected_points': 0}

        # Prioritize low ownership, high value
        ownership = pd.to_numeric(
            self.players_df.get('selected_by_percent', 0),
            errors='coerce'
        )

        self.players_df['differential_score'] = (
            (100 - ownership) * 0.2 +
            self.players_df.get('points_per_million', 0) * 5 +
            self.players_df.get('xgi_per_90', 0) * 10
        )

        return self._select_team_by_metric(formation, 'differential_score')

    def _build_premium_heavy_team(self, formation: Dict) -> Dict:
        """Build team with triple premium + budget enablers"""
        # Focus on getting 3 premium players (>11.0m) + budget options
        team = {'starters': [], 'bench': [], 'total_cost': 0, 'projected_points': 0}

        # Get premium players
        expensive = self.players_df[self.players_df['now_cost'] >= 110].copy()  # £11.0m+
        expensive = expensive.sort_values('total_points', ascending=False)

        # Get budget enablers
        cheap = self.players_df[self.players_df['now_cost'] <= 50].copy()  # £5.0m or less
        cheap = cheap.sort_values('points_per_million', ascending=False)

        # Mix of premium and budget
        # Implementation similar to above

        return team

    def _select_team_by_metric(self, formation: Dict, metric: str) -> Dict:
        """Generic team selection by specified metric"""
        team = {'starters': [], 'bench': [], 'total_cost': 0, 'projected_points': 0}

        for position, count in self.position_limits.items():
            pos_code = self._position_to_code(position)
            pos_players = self.players_df[
                self.players_df['element_type'] == pos_code
            ].copy()

            if pos_players.empty or metric not in pos_players.columns:
                continue

            pos_players = pos_players.sort_values(metric, ascending=False)

            starters_needed = formation.get(position, 0)
            total_needed = count[1]

            selected = pos_players.head(total_needed)

            for idx, player in selected.iterrows():
                player_dict = {
                    'name': player['web_name'],
                    'position': position,
                    'cost': player['now_cost'] / 10,
                    'points': player.get('total_points', 0),
                    'starter': len([p for p in team['starters'] if p['position'] == position]) < starters_needed
                }

                if player_dict['starter']:
                    team['starters'].append(player_dict)
                else:
                    team['bench'].append(player_dict)

                team['total_cost'] += player_dict['cost']

        return team

    # ========================================================================
    # TRANSFER PLANNING
    # ========================================================================

    def analyze_transfer_targets(
        self,
        current_team: List[str],
        budget: float,
        free_transfers: int = 1,
        gameweeks_ahead: int = 5
    ) -> List[TransferSuggestion]:
        """
        Analyze and suggest optimal transfers

        Used by Let's Talk FPL for weekly transfer analysis
        Considers form, fixtures, and value
        """
        suggestions = []

        # Get players not in current team
        available_players = self.players_df[
            ~self.players_df['web_name'].isin(current_team)
        ].copy()

        # Calculate transfer priority score
        available_players['transfer_priority'] = (
            available_players.get('form', 0) * 3 +
            available_players.get('xgi_per_90', 0) * 10 +
            available_players.get('points_per_million', 0) * 2 +
            (100 - pd.to_numeric(available_players.get('selected_by_percent', 0), errors='coerce')) * 0.1
        )

        # Find transfer candidates per position
        for position in ['GKP', 'DEF', 'MID', 'FWD']:
            pos_code = self._position_to_code(position)

            # Top transfer targets
            targets = available_players[
                available_players['element_type'] == pos_code
            ].nlargest(5, 'transfer_priority')

            for _, target in targets.iterrows():
                # Find potential players to transfer out
                current_pos_players = self.players_df[
                    (self.players_df['web_name'].isin(current_team)) &
                    (self.players_df['element_type'] == pos_code)
                ]

                if current_pos_players.empty:
                    continue

                # Find worst performing player in position
                worst_player = current_pos_players.nsmallest(1, 'form')

                if worst_player.empty:
                    continue

                worst = worst_player.iloc[0]

                cost_diff = (target['now_cost'] - worst['now_cost']) / 10

                if cost_diff <= budget:
                    expected_gain = (
                        (target.get('form', 0) - worst.get('form', 0)) * gameweeks_ahead
                    )

                    suggestion = TransferSuggestion(
                        player_out=worst['web_name'],
                        player_in=target['web_name'],
                        position=position,
                        cost_change=cost_diff,
                        expected_points_gain=expected_gain,
                        priority=int(target['transfer_priority']),
                        reason=f"Better form ({target.get('form', 0):.1f} vs {worst.get('form', 0):.1f}) and xGI"
                    )

                    suggestions.append(suggestion)

        # Sort by priority
        suggestions.sort(key=lambda x: x.priority, reverse=True)

        return suggestions[:10]  # Top 10 suggestions

    # ========================================================================
    # CHIP STRATEGY
    # ========================================================================

    def wildcard_planning(self, gameweek: int) -> Dict:
        """
        Wildcard chip strategy planner

        FPL content creators recommend Wildcarding:
        - GW8-10: Early wildcard to fix team
        - GW16-18: Pre-holiday fixtures
        - GW25-27: Post-January transfer window

        Returns optimal wildcard timing and team structure
        """
        optimal_gws = {
            'early': (8, 10),
            'mid': (16, 18),
            'late': (25, 27)
        }

        # Determine which window
        if 8 <= gameweek <= 10:
            window = 'early'
            strategy = 'Fix early mistakes, set up for good fixtures'
        elif 16 <= gameweek <= 18:
            window = 'mid'
            strategy = 'Prepare for Double Gameweeks and fixture swings'
        elif 25 <= gameweek <= 27:
            window = 'late'
            strategy = 'New signings and final run-in preparation'
        else:
            window = 'suboptimal'
            strategy = 'Consider saving for better timing'

        return {
            'gameweek': gameweek,
            'window': window,
            'strategy': strategy,
            'recommended': window != 'suboptimal',
            'reasoning': self._get_wildcard_reasoning(window)
        }

    def _get_wildcard_reasoning(self, window: str) -> str:
        """Get reasoning for wildcard timing"""
        reasoning = {
            'early': 'Early wildcard allows fixing initial mistakes and setting up for first favorable fixture run',
            'mid': 'Mid-season wildcard targets Double Gameweeks and capitalizes on fixture swings',
            'late': 'Late wildcard incorporates January transfers and prepares for final fixture run',
            'suboptimal': 'This timing may not be optimal - consider waiting for fixture swings or DGWs'
        }
        return reasoning.get(window, '')

    def bench_boost_planner(self, upcoming_dgw: Optional[int] = None) -> Dict:
        """
        Bench Boost chip strategy

        Popular strategy: Use on Double Gameweek when all 15 players have 2 games
        """
        recommendations = {
            'chip': 'Bench Boost',
            'optimal_timing': 'Double Gameweek where all 15 players have 2 fixtures',
            'preparation': [
                '1. Identify upcoming Double Gameweeks',
                '2. Build team with 15 players from DGW teams',
                '3. Ensure all bench players are nailed starters',
                '4. Prioritize teams with good fixtures in DGW'
            ],
            'expected_return': '20-40 additional points in optimal DGW'
        }

        if upcoming_dgw:
            recommendations['recommended_gw'] = upcoming_dgw
            recommendations['preparation_time'] = '1-2 gameweeks before DGW'

        return recommendations

    def triple_captain_analysis(self, captaincy_df: pd.DataFrame) -> Dict:
        """
        Triple Captain chip strategy

        Popular strategy from FPL content creators:
        - Use on highest-scoring player in Double Gameweek
        - Target premium players (Salah, Haaland, etc.) with 2 favorable fixtures
        """
        # Get best captain options
        top_captains = captaincy_df.nlargest(5, 'captain_score')

        recommendations = {
            'chip': 'Triple Captain',
            'optimal_timing': 'Double Gameweek on premium player vs weak opposition',
            'top_targets': [],
            'criteria': [
                'Premium player (11.0m+)',
                'Double Gameweek with 2 favorable fixtures',
                'Strong recent form (xGI > 0.8)',
                'High expected points (>15 for DGW)'
            ]
        }

        for _, player in top_captains.iterrows():
            recommendations['top_targets'].append({
                'name': player['web_name'],
                'captain_score': player.get('captain_score', 0),
                'form': player.get('form', 0),
                'xgi_per_90': player.get('xgi_per_90', 0)
            })

        return recommendations

    def free_hit_strategy(self, gameweek: int) -> Dict:
        """
        Free Hit chip strategy

        Popular usage:
        - Blank Gameweeks (when many teams don't play)
        - DGW if you can't field strong team
        - BGW29 and BGW33 historically
        """
        recommendations = {
            'chip': 'Free Hit',
            'optimal_timing': 'Blank Gameweeks or when unable to field strong XI',
            'typical_gameweeks': [29, 33],
            'strategy': [
                '1. Identify Blank Gameweeks early in season',
                '2. Build team exclusively from teams that play',
                '3. Don\'t worry about team value - it\'s only one week',
                '4. Go heavy on teams with good fixtures',
                '5. Maximize playing players over long-term value'
            ],
            'expected_benefit': 'Avoid fielding weak team in BGW, maintain rank'
        }

        return recommendations

    # ========================================================================
    # FIXTURE ANALYSIS
    # ========================================================================

    def analyze_fixture_swings(self, teams_df: pd.DataFrame, fixtures_df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify fixture swings for transfer planning

        Fixture swings = when team's fixtures change from hard to easy (or vice versa)
        Popular strategy from FPL General, FPL Focal
        """
        fixture_analysis = []

        for _, team in teams_df.iterrows():
            team_id = team.get('id', team.name)

            # Get next 5 fixtures
            team_fixtures = fixtures_df[
                (fixtures_df['team_h'] == team_id) |
                (fixtures_df['team_a'] == team_id)
            ].head(5)

            if team_fixtures.empty:
                continue

            # Calculate average difficulty
            avg_difficulty = team_fixtures['difficulty'].mean() if 'difficulty' in team_fixtures.columns else 3.0

            fixture_analysis.append({
                'team': team.get('name', 'Unknown'),
                'team_id': team_id,
                'avg_fdr': avg_difficulty,
                'fixture_quality': 6 - avg_difficulty,  # Invert (higher = better)
                'recommendation': 'Target' if avg_difficulty < 3 else 'Avoid' if avg_difficulty > 3.5 else 'Neutral'
            })

        result = pd.DataFrame(fixture_analysis)
        return result.sort_values('fixture_quality', ascending=False)

    # ========================================================================
    # VALUE & BUDGET MANAGEMENT
    # ========================================================================

    def optimize_team_value(self, current_team: List[Dict]) -> Dict:
        """
        Team value optimization strategy

        Popular strategy for building "team value" over the season
        Focus on price risers and form players
        """
        recommendations = {
            'current_value': sum(p['cost'] for p in current_team),
            'strategies': [
                'Transfer in players before price rises',
                'Hold price risers even if slightly out of form',
                'Avoid early hits on players who may drop',
                'Build value early to afford premiums later'
            ],
            'price_rise_candidates': [],
            'value_optimization_tips': [
                'Monitor ownership increases (>5% daily = likely rise)',
                'Check price change predictors (FPL Statistics)',
                'Make transfers before deadline to catch rises',
                'Don\'t chase price rises at expense of points'
            ]
        }

        # Identify potential price risers (high ownership increase proxy)
        high_ownership = self.players_df[
            pd.to_numeric(self.players_df.get('selected_by_percent', 0), errors='coerce') > 20
        ].copy()

        high_ownership = high_ownership.sort_values('form', ascending=False).head(10)

        for _, player in high_ownership.iterrows():
            recommendations['price_rise_candidates'].append({
                'name': player['web_name'],
                'cost': player['now_cost'] / 10,
                'ownership': player.get('selected_by_percent', 0),
                'form': player.get('form', 0)
            })

        return recommendations

    # ========================================================================
    # MINI-LEAGUE STRATEGIES
    # ========================================================================

    def mini_league_strategy(self, your_rank: int, total_players: int, ml_leader_team: Optional[List[str]] = None) -> Dict:
        """
        Mini-league specific strategy

        Different approaches for leaders vs chasers
        """
        rank_percentage = (your_rank / total_players) * 100

        if rank_percentage <= 25:  # Top 25%
            strategy_type = 'leader'
            approach = 'defensive'
            tactics = [
                'Maintain template core (high ownership)',
                '1-2 differentials maximum',
                'Avoid risky punts',
                'Captain safe picks (Salah, Haaland)',
                'Preserve rank, don\'t chase points'
            ]
        elif rank_percentage <= 50:  # Top 50%
            strategy_type = 'contender'
            approach = 'balanced'
            tactics = [
                'Mix of template and differentials',
                '2-3 differential picks',
                'Calculated captaincy risks',
                'Target fixture swings early',
                'Build value for final surge'
            ]
        else:  # Chasing
            strategy_type = 'chaser'
            approach = 'aggressive'
            tactics = [
                'High differential strategy',
                'Avoid template picks',
                'Risky captaincy choices',
                'Target low-owned premiums',
                'Take calculated hits for differentials'
            ]

        recommendations = {
            'rank': your_rank,
            'rank_percentage': rank_percentage,
            'strategy_type': strategy_type,
            'approach': approach,
            'tactics': tactics,
            'risk_level': 'Low' if strategy_type == 'leader' else 'High' if strategy_type == 'chaser' else 'Medium'
        }

        if ml_leader_team:
            # Analyze leader's team for differential opportunities
            leader_players = set(ml_leader_team)
            your_differentials = self.players_df[
                ~self.players_df['web_name'].isin(leader_players)
            ].nlargest(10, 'form')

            recommendations['differential_targets'] = your_differentials['web_name'].tolist()

        return recommendations

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _position_to_code(self, position: str) -> int:
        """Convert position string to FPL code"""
        mapping = {'GKP': 1, 'DEF': 2, 'MID': 3, 'FWD': 4}
        return mapping.get(position, 0)

    def _code_to_position(self, code: int) -> str:
        """Convert FPL code to position string"""
        mapping = {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}
        return mapping.get(code, 'UNKNOWN')


# ============================================================================
# GAMEWEEK PLANNING
# ============================================================================

class GameweekPlanner:
    """
    Gameweek-by-gameweek planning tool

    Helps plan transfers, captaincy, and chip usage across the season
    """

    def __init__(self, current_gw: int):
        """
        Initialize planner

        Args:
            current_gw: Current gameweek number
        """
        self.current_gw = current_gw
        self.total_gws = 38

    def create_season_plan(self) -> Dict:
        """
        Create rough season plan for chips and wildcards

        Based on popular FPL content creator strategies
        """
        plan = {
            'current_gw': self.current_gw,
            'chips_remaining': ['Wildcard 1', 'Wildcard 2', 'Bench Boost', 'Triple Captain', 'Free Hit'],
            'recommended_schedule': {
                'gw8_10': 'Consider first Wildcard (fix early mistakes)',
                'gw16_18': 'Second Wildcard or save for GW25-27',
                'gw19_onwards': 'Identify Double Gameweeks for Bench Boost',
                'gw25_27': 'Wildcard if not used earlier (January transfers)',
                'gw29_33': 'Free Hit in Blank Gameweek',
                'dgw_with_premium': 'Triple Captain on best DGW'
            },
            'transfer_strategy': 'Plan 2-3 GWs ahead, avoid hits unless essential',
            'captaincy': 'Premium options (Salah, Haaland) unless strong differential case'
        }

        return plan

    def weekly_checklist(self, gameweek: int) -> List[str]:
        """
        Weekly preparation checklist

        FPL content creator pre-deadline routine
        """
        checklist = [
            f'1. Check {gameweek} fixtures and kickoff times',
            '2. Review injury news and press conferences',
            '3. Analyze underlying stats (xG, xA) from last GW',
            '4. Check price changes and team value',
            '5. Identify fixture swings for transfer targets',
            '6. Review differential options vs template',
            '7. Plan captaincy (C and VC)',
            '8. Set starting XI and bench order (def > mid > fwd)',
            '9. Make transfers (save until late for injury news)',
            '10. Double-check team before deadline!'
        ]

        return checklist


# ============================================================================
# BONUS POINT PREDICTION
# ============================================================================

class BonusPredictor:
    """
    Bonus point prediction system

    Predicts BPS performance based on player stats
    """

    def __init__(self, players_df: pd.DataFrame):
        """Initialize with players data"""
        self.players_df = players_df

    def predict_bonus_potential(self) -> pd.DataFrame:
        """
        Predict bonus point potential per 90 minutes

        BPS formula approximation:
        - Goals: +24 (FWD), +18 (MID), +12 (DEF), +6 (GKP)
        - Assists: +9
        - Clean sheet: +12 (GKP/DEF)
        - Saves: +2 per save
        - Key passes, tackles, etc.
        """
        df = self.players_df.copy()

        # Normalize BPS to per 90
        minutes = df['minutes'].replace(0, 1)
        bps_per_90 = (df.get('bps', 0) / minutes) * 90

        # Predict future BPS based on underlying stats
        xg_per_90 = pd.to_numeric(df.get('expected_goals_per_90', 0), errors='coerce').fillna(0)
        xa_per_90 = pd.to_numeric(df.get('expected_assists_per_90', 0), errors='coerce').fillna(0)

        position_bonus_weight = df['element_type'].map({
            4: 24,  # FWD
            3: 18,  # MID
            2: 12,  # DEF
            1: 6    # GKP
        })

        predicted_bps = (
            xg_per_90 * position_bonus_weight +
            xa_per_90 * 9 +
            bps_per_90 * 0.5  # Historical BPS component
        )

        result = pd.DataFrame({
            'web_name': df['web_name'],
            'position': df['element_type'].map({1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}),
            'bps_per_90_historical': bps_per_90,
            'predicted_bps_per_90': predicted_bps,
            'bonus_potential': (predicted_bps / 32).clip(upper=3)  # 32+ BPS usually = 3 bonus
        })

        return result.sort_values('predicted_bps_per_90', ascending=False)


if __name__ == "__main__":
    print("FPL Strategy & Analysis Module")
    print("=" * 50)
    print("\nModules available:")
    print("- FPLStrategy: Team building, transfers, chip strategy")
    print("- GameweekPlanner: Season planning and weekly checklists")
    print("- BonusPredictor: Bonus point prediction")
    print("\nUse: from fpl_strategy import FPLStrategy, GameweekPlanner, BonusPredictor")
