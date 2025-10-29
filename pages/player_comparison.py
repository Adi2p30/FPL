"""
Player Comparison Dashboard
============================

Compare multiple players side-by-side with advanced metrics and visualizations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.visualizations import (
    create_comparison_radar,
    create_comparison_bar,
    create_stat_comparison_table
)
from advanced_metrics import AdvancedMetrics


def show_player_comparison(players_df: pd.DataFrame, teams_df: pd.DataFrame):
    """
    Player comparison page

    Args:
        players_df: Players DataFrame with metrics
        teams_df: Teams DataFrame
    """
    st.title("🔍 Player Comparison Dashboard")

    st.markdown("""
    Compare up to **4 players** side-by-side with advanced metrics, visualizations, and stats from the FPL API.
    """)

    # Filters
    st.sidebar.markdown("## 🎯 Filters")

    position_filter = st.sidebar.selectbox(
        "Filter by Position",
        ['All', 'GKP', 'DEF', 'MID', 'FWD']
    )

    team_filter = st.sidebar.selectbox(
        "Filter by Team",
        ['All'] + sorted(players_df['team_name'].unique().tolist())
    )

    min_minutes = st.sidebar.slider(
        "Minimum Minutes Played",
        0, int(players_df['minutes'].max()),
        300
    )

    # Apply filters
    filtered_df = players_df[players_df['minutes'] >= min_minutes].copy()

    if position_filter != 'All':
        filtered_df = filtered_df[filtered_df['position'] == position_filter]

    if team_filter != 'All':
        filtered_df = filtered_df[filtered_df['team_name'] == team_filter]

    # Sort options
    sort_by = st.sidebar.selectbox(
        "Sort Players By",
        ['total_points', 'cost', 'form', 'selected_by_percent', 'goals_scored', 'assists']
    )

    filtered_df = filtered_df.sort_values(sort_by, ascending=False)

    # Player selection
    st.markdown("---")
    st.subheader("👥 Select Players to Compare")

    col1, col2, col3, col4 = st.columns(4)

    available_players = filtered_df['web_name'].tolist()

    with col1:
        player1 = st.selectbox("Player 1", available_players, key='p1')

    with col2:
        player2 = st.selectbox("Player 2", available_players, key='p2', index=min(1, len(available_players)-1))

    with col3:
        player3 = st.selectbox("Player 3 (Optional)", ['None'] + available_players, key='p3')

    with col4:
        player4 = st.selectbox("Player 4 (Optional)", ['None'] + available_players, key='p4')

    # Get selected players
    selected_players = [player1, player2]
    if player3 != 'None':
        selected_players.append(player3)
    if player4 != 'None':
        selected_players.append(player4)

    selected_data = filtered_df[filtered_df['web_name'].isin(selected_players)]

    if selected_data.empty:
        st.warning("Please select at least 2 players to compare.")
        return

    # Player cards
    st.markdown("---")
    st.subheader("📋 Player Overview")

    cols = st.columns(len(selected_players))

    for i, (col, player_name) in enumerate(zip(cols, selected_players)):
        player = selected_data[selected_data['web_name'] == player_name].iloc[0]

        with col:
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 10px; border-left: 5px solid #37003c;">
                <h3 style="margin: 0;">{player['web_name']}</h3>
                <p style="margin: 5px 0;"><strong>Team:</strong> {player['team_name']}</p>
                <p style="margin: 5px 0;"><strong>Position:</strong> {player['position']}</p>
                <p style="margin: 5px 0;"><strong>Cost:</strong> £{player['cost']:.1f}m</p>
                <p style="margin: 5px 0;"><strong>Points:</strong> {player['total_points']:.0f}</p>
                <p style="margin: 5px 0;"><strong>Form:</strong> {player.get('form', 0):.1f}</p>
                <p style="margin: 5px 0;"><strong>Ownership:</strong> {player['selected_by_percent']:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)

    # Comparison metrics
    st.markdown("---")
    st.subheader("📊 Statistical Comparison")

    # Core stats table
    core_stats = [
        'total_points', 'cost', 'form', 'points_per_game',
        'minutes', 'goals_scored', 'assists', 'clean_sheets',
        'bonus', 'bps', 'selected_by_percent'
    ]

    comparison_stats = []
    for player_name in selected_players:
        player = selected_data[selected_data['web_name'] == player_name].iloc[0]
        comparison_stats.append(player[core_stats].to_dict())

    comparison_df = pd.DataFrame(comparison_stats)
    comparison_df.insert(0, 'Player', selected_players)

    # Format the dataframe
    st.dataframe(
        comparison_df.style.background_gradient(cmap='Greens', subset=comparison_df.columns[1:]),
        use_container_width=True
    )

    # Advanced metrics
    st.markdown("---")
    st.subheader("🔬 Advanced Metrics")

    # Check for advanced metrics
    advanced_metrics = []
    for col in ['xgi_per_90', 'ppm', 'bps_per_90', 'threat_index', 'roi_metric']:
        if col in selected_data.columns:
            advanced_metrics.append(col)

    if advanced_metrics:
        adv_comparison = []
        for player_name in selected_players:
            player = selected_data[selected_data['web_name'] == player_name].iloc[0]
            adv_comparison.append({k: player.get(k, 0) for k in advanced_metrics})

        adv_df = pd.DataFrame(adv_comparison)
        adv_df.insert(0, 'Player', selected_players)

        st.dataframe(
            adv_df.style.background_gradient(cmap='Blues', subset=adv_df.columns[1:]),
            use_container_width=True
        )

    # Visualizations
    st.markdown("---")
    st.subheader("📈 Visual Comparisons")

    tab1, tab2, tab3 = st.tabs(["📡 Radar Chart", "📊 Bar Charts", "🎯 Key Metrics"])

    with tab1:
        # Radar chart
        radar_metrics = st.multiselect(
            "Select metrics for radar chart (max 8)",
            ['total_points', 'form', 'goals_scored', 'assists', 'clean_sheets', 'bonus', 'bps', 'minutes'],
            default=['total_points', 'form', 'goals_scored', 'assists', 'bonus']
        )

        if len(radar_metrics) >= 3:
            players_data = []
            for player_name in selected_players:
                player = selected_data[selected_data['web_name'] == player_name].iloc[0]
                players_data.append(player.to_dict())

            fig = create_comparison_radar(players_data, radar_metrics)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select at least 3 metrics for radar chart")

    with tab2:
        # Bar charts for individual metrics
        metric_to_compare = st.selectbox(
            "Select metric for bar chart",
            ['total_points', 'goals_scored', 'assists', 'clean_sheets', 'bonus', 'form', 'cost', 'bps']
        )

        players_data = []
        for player_name in selected_players:
            player = selected_data[selected_data['web_name'] == player_name].iloc[0]
            players_data.append(player.to_dict())

        fig = create_comparison_bar(players_data, metric_to_compare)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Key metrics comparison
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### ⚽ Attacking Stats")

            attack_stats = ['goals_scored', 'assists', 'total_points']
            attack_comparison = []

            for player_name in selected_players:
                player = selected_data[selected_data['web_name'] == player_name].iloc[0]
                attack_comparison.append([player['web_name']] + [player.get(stat, 0) for stat in attack_stats])

            attack_df = pd.DataFrame(attack_comparison, columns=['Player'] + attack_stats)
            st.dataframe(attack_df, hide_index=True, use_container_width=True)

        with col2:
            st.markdown("#### 💰 Value Metrics")

            value_stats = ['cost', 'points_per_game', 'selected_by_percent']
            value_comparison = []

            for player_name in selected_players:
                player = selected_data[selected_data['web_name'] == player_name].iloc[0]
                value_comparison.append([player['web_name']] + [player.get(stat, 0) for stat in value_stats])

            value_df = pd.DataFrame(value_comparison, columns=['Player'] + value_stats)
            st.dataframe(value_df, hide_index=True, use_container_width=True)

    # Position-specific analysis
    st.markdown("---")
    st.subheader("🎯 Position-Specific Analysis")

    # Get position-specific metrics
    if position_filter in ['DEF', 'GKP']:
        st.markdown("#### 🛡️ Defensive Metrics")

        def_metrics = ['clean_sheets', 'goals_conceded', 'saves']
        def_data = []

        for player_name in selected_players:
            player = selected_data[selected_data['web_name'] == player_name].iloc[0]
            def_data.append([player['web_name']] + [player.get(m, 0) for m in def_metrics])

        def_df = pd.DataFrame(def_data, columns=['Player'] + def_metrics)
        st.dataframe(def_df, hide_index=True, use_container_width=True)

    elif position_filter in ['MID', 'FWD']:
        st.markdown("#### ⚡ Attacking Metrics")

        # Check for xG/xA data
        if 'expected_goals' in selected_data.columns or 'expected_assists' in selected_data.columns:
            attack_metrics = ['goals_scored', 'expected_goals', 'assists', 'expected_assists']
        else:
            attack_metrics = ['goals_scored', 'assists', 'bonus', 'bps']

        attack_data = []
        for player_name in selected_players:
            player = selected_data[selected_data['web_name'] == player_name].iloc[0]
            attack_data.append([player['web_name']] + [player.get(m, 0) for m in attack_metrics])

        attack_df = pd.DataFrame(attack_data, columns=['Player'] + attack_metrics)
        st.dataframe(attack_df, hide_index=True, use_container_width=True)

    # Insights and recommendations
    st.markdown("---")
    st.subheader("💡 AI Insights")

    # Generate simple insights
    best_points = selected_data.nlargest(1, 'total_points').iloc[0]
    best_value = selected_data.nlargest(1, 'points_per_game').iloc[0] if 'points_per_game' in selected_data.columns else best_points
    best_form = selected_data.nlargest(1, 'form').iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"""
        **🏆 Highest Points**

        **{best_points['web_name']}** leads with **{best_points['total_points']:.0f} points**
        """)

    with col2:
        st.info(f"""
        **💰 Best Value**

        **{best_value['web_name']}** offers **{best_value.get('points_per_game', 0):.1f} pts/game**
        """)

    with col3:
        st.warning(f"""
        **📈 Best Form**

        **{best_form['web_name']}** is in form with **{best_form.get('form', 0):.1f}**
        """)

    # Recommendation
    st.markdown("---")

    # Simple recommendation logic
    if best_points['web_name'] == best_form['web_name']:
        recommendation = best_points['web_name']
        reason = "highest points AND best current form"
    elif best_form.get('form', 0) > best_points.get('form', 0) * 1.5:
        recommendation = best_form['web_name']
        reason = "excellent current form (momentum)"
    else:
        recommendation = best_points['web_name']
        reason = "most consistent performer"

    st.success(f"""
    ### ⭐ Recommendation

    Based on the comparison, **{recommendation}** appears to be the best pick due to {reason}.

    **Consider:**
    - Current form and fixture difficulty
    - Your budget constraints
    - Team balance and structure
    - Ownership % for differential strategy
    """)

    # Export comparison
    st.markdown("---")

    if st.button("📥 Export Comparison Data"):
        csv = comparison_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"player_comparison_{'_'.join(selected_players)}.csv",
            mime="text/csv"
        )
