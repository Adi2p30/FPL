"""
Visualization Utilities
=======================

Interactive charts and plots for FPL analysis
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict
import numpy as np


def create_comparison_radar(players_data: List[Dict], metrics: List[str]) -> go.Figure:
    """
    Create radar chart for player comparison

    Args:
        players_data: List of player dictionaries
        metrics: List of metrics to compare

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    for player in players_data:
        values = [player.get(metric, 0) for metric in metrics]

        # Normalize values to 0-100 scale for radar chart
        max_vals = [max([p.get(m, 0) for p in players_data]) for m in metrics]
        normalized = [v / max_v * 100 if max_v > 0 else 0 for v, max_v in zip(values, max_vals)]

        fig.add_trace(go.Scatterpolar(
            r=normalized,
            theta=metrics,
            fill='toself',
            name=player.get('web_name', 'Unknown')
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Player Comparison Radar",
        height=500
    )

    return fig


def create_comparison_bar(players_data: List[Dict], metric: str) -> go.Figure:
    """
    Create bar chart for single metric comparison

    Args:
        players_data: List of player dictionaries
        metric: Metric to compare

    Returns:
        Plotly figure
    """
    names = [p.get('web_name', 'Unknown') for p in players_data]
    values = [p.get(metric, 0) for p in players_data]

    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=values,
            marker_color='rgb(55, 83, 109)',
            text=values,
            textposition='auto'
        )
    ])

    fig.update_layout(
        title=f"Player Comparison: {metric}",
        xaxis_title="Player",
        yaxis_title=metric,
        height=400
    )

    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str = 'position',
    size_col: str = None,
    hover_data: List[str] = None
) -> go.Figure:
    """
    Create scatter plot with optional sizing and hover data

    Args:
        df: DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        color_col: Column for color coding
        size_col: Column for bubble size
        hover_data: Additional hover information

    Returns:
        Plotly figure
    """
    if hover_data is None:
        hover_data = ['web_name', 'team_name', 'cost']

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        hover_data=hover_data,
        title=f"{y_col} vs {x_col}"
    )

    fig.update_layout(
        height=600,
        hovermode='closest'
    )

    return fig


def create_team_formation_visual(team_players: pd.DataFrame, formation: str) -> go.Figure:
    """
    Create visual representation of team formation

    Args:
        team_players: DataFrame of team players
        formation: Formation string (e.g., "3-4-3")

    Returns:
        Plotly figure
    """
    # Parse formation
    parts = formation.split('-')
    if len(parts) != 3:
        parts = [3, 4, 3]
    else:
        parts = [int(x) for x in parts]

    gkp_count = 1
    def_count = parts[0]
    mid_count = parts[1]
    fwd_count = parts[2]

    # Separate players by position
    gkp = team_players[team_players['position'] == 'GKP'].head(gkp_count)
    defenders = team_players[team_players['position'] == 'DEF'].head(def_count)
    midfielders = team_players[team_players['position'] == 'MID'].head(mid_count)
    forwards = team_players[team_players['position'] == 'FWD'].head(fwd_count)

    # Create positions on field
    fig = go.Figure()

    # Y positions (0-100 scale, 0 = defensive, 100 = attacking)
    y_positions = {
        'GKP': 5,
        'DEF': 25,
        'MID': 55,
        'FWD': 85
    }

    def add_players_line(players_df, y_pos, count, position_name, color):
        if players_df.empty:
            return

        x_positions = np.linspace(10, 90, count)

        for i, (_, player) in enumerate(players_df.iterrows()):
            if i >= count:
                break

            fig.add_trace(go.Scatter(
                x=[x_positions[i]],
                y=[y_pos],
                mode='markers+text',
                marker=dict(size=40, color=color, line=dict(width=2, color='white')),
                text=player['web_name'],
                textposition='bottom center',
                textfont=dict(size=10, color='white'),
                name=position_name,
                hovertemplate=f"<b>{player['web_name']}</b><br>" +
                             f"Position: {position_name}<br>" +
                             f"Cost: £{player['cost']:.1f}m<br>" +
                             f"Points: {player['total_points']}<br>" +
                             f"Form: {player.get('form', 0):.1f}<extra></extra>",
                showlegend=False
            ))

    # Add players by position
    add_players_line(gkp, y_positions['GKP'], gkp_count, 'GKP', '#FFD700')
    add_players_line(defenders, y_positions['DEF'], def_count, 'DEF', '#4169E1')
    add_players_line(midfielders, y_positions['MID'], mid_count, 'MID', '#32CD32')
    add_players_line(forwards, y_positions['FWD'], fwd_count, 'FWD', '#DC143C')

    # Style as football pitch
    fig.update_layout(
        title=f"Team Formation: {formation}",
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0, 100],
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0, 100],
            zeroline=False
        ),
        plot_bgcolor='#2d5016',  # Grass green
        height=700,
        hovermode='closest',
        showlegend=False
    )

    # Add pitch lines
    fig.add_shape(
        type="rect",
        x0=0, x1=100, y0=0, y1=100,
        line=dict(color="white", width=3)
    )

    # Add halfway line
    fig.add_shape(
        type="line",
        x0=0, x1=100, y0=50, y1=50,
        line=dict(color="white", width=2)
    )

    return fig


def create_budget_gauge(spent: float, total: float = 100.0) -> go.Figure:
    """
    Create gauge chart for budget tracking

    Args:
        spent: Amount spent
        total: Total budget

    Returns:
        Plotly figure
    """
    remaining = total - spent

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=spent,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Budget Used: £{spent:.1f}m / £{total:.1f}m"},
        delta={'reference': total, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, total], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, total * 0.7], 'color': 'lightgreen'},
                {'range': [total * 0.7, total * 0.9], 'color': 'yellow'},
                {'range': [total * 0.9, total], 'color': 'lightcoral'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': total
            }
        }
    ))

    fig.update_layout(height=300)

    return fig


def create_position_distribution(team_players: pd.DataFrame) -> go.Figure:
    """
    Create pie chart of position distribution

    Args:
        team_players: DataFrame of team players

    Returns:
        Plotly figure
    """
    if team_players.empty:
        return go.Figure()

    position_counts = team_players['position'].value_counts()

    colors = {
        'GKP': '#FFD700',
        'DEF': '#4169E1',
        'MID': '#32CD32',
        'FWD': '#DC143C'
    }

    fig = go.Figure(data=[go.Pie(
        labels=position_counts.index,
        values=position_counts.values,
        marker=dict(colors=[colors.get(pos, '#808080') for pos in position_counts.index]),
        hole=0.3
    )])

    fig.update_layout(
        title="Team Position Distribution",
        height=400
    )

    return fig


def create_points_timeline(players_df: pd.DataFrame, player_names: List[str]) -> go.Figure:
    """
    Create timeline of points scored (if historical data available)

    Args:
        players_df: Players DataFrame
        player_names: List of player names

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    for name in player_names:
        player = players_df[players_df['web_name'] == name]
        if not player.empty:
            player = player.iloc[0]

            # Since we don't have gameweek data, show form as a simple bar
            fig.add_trace(go.Bar(
                x=[name],
                y=[player.get('form', 0)],
                name=name,
                text=f"Form: {player.get('form', 0):.1f}"
            ))

    fig.update_layout(
        title="Player Form Comparison",
        xaxis_title="Player",
        yaxis_title="Form",
        height=400
    )

    return fig


def create_cost_vs_points(df: pd.DataFrame, highlight_players: List[str] = None) -> go.Figure:
    """
    Create cost vs points scatter with highlighted players

    Args:
        df: Players DataFrame
        highlight_players: List of player names to highlight

    Returns:
        Plotly figure
    """
    fig = px.scatter(
        df,
        x='cost',
        y='total_points',
        color='position',
        size='selected_by_percent',
        hover_data=['web_name', 'team_name', 'form'],
        title="Cost vs Points (Size = Ownership %)"
    )

    # Highlight selected players
    if highlight_players:
        highlight_df = df[df['web_name'].isin(highlight_players)]

        fig.add_trace(go.Scatter(
            x=highlight_df['cost'],
            y=highlight_df['total_points'],
            mode='markers+text',
            marker=dict(size=15, color='red', symbol='star'),
            text=highlight_df['web_name'],
            textposition='top center',
            name='Selected Players',
            showlegend=True
        ))

    fig.update_layout(height=600)

    return fig


def create_stat_comparison_table(players_data: List[Dict], stats: List[str]) -> pd.DataFrame:
    """
    Create comparison table for multiple players

    Args:
        players_data: List of player dictionaries
        stats: List of stats to compare

    Returns:
        Comparison DataFrame
    """
    comparison_data = []

    for player in players_data:
        row = {'Player': player.get('web_name', 'Unknown')}
        for stat in stats:
            row[stat] = player.get(stat, 0)
        comparison_data.append(row)

    return pd.DataFrame(comparison_data)
