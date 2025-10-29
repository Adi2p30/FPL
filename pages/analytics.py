"""
Advanced Analytics Dashboard
============================

Deep dive into advanced metrics, xG, xA, and position-specific analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from advanced_metrics import AdvancedMetrics
from utils.visualizations import create_scatter_plot


def show_analytics(players_df: pd.DataFrame, teams_df: pd.DataFrame):
    """
    Advanced analytics page

    Args:
        players_df: Players DataFrame with metrics
        teams_df: Teams DataFrame
    """
    st.title("📊 Advanced Analytics Dashboard")

    st.markdown("""
    Dive deep into **20+ advanced metrics** including xG, xA, BPS, and position-specific analysis.
    Data fetched live from the **FPL API**.
    """)

    # Initialize metrics calculator
    metrics = AdvancedMetrics(players_df)

    # Sidebar - Analysis options
    st.sidebar.markdown("## 🎯 Analysis Options")

    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        [
            "Overview",
            "Expected Goals (xG)",
            "Position-Specific",
            "Captain Analysis",
            "Differentials",
            "Value Analysis",
            "Bonus Points"
        ]
    )

    # Main content based on selection
    if analysis_type == "Overview":
        show_overview(players_df, metrics)

    elif analysis_type == "Expected Goals (xG)":
        show_xg_analysis(players_df, metrics)

    elif analysis_type == "Position-Specific":
        show_position_analysis(players_df, metrics)

    elif analysis_type == "Captain Analysis":
        show_captain_analysis(players_df, metrics)

    elif analysis_type == "Differentials":
        show_differentials_analysis(players_df, metrics)

    elif analysis_type == "Value Analysis":
        show_value_analysis(players_df, metrics)

    elif analysis_type == "Bonus Points":
        show_bonus_analysis(players_df, metrics)


def show_overview(players_df: pd.DataFrame, metrics: AdvancedMetrics):
    """Show overview analytics"""
    st.subheader("📈 Analytics Overview")

    # Get comprehensive analysis
    analysis_df = metrics.get_comprehensive_analysis()

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_xgi = analysis_df['xgi_per_90'].mean()
        st.metric("Avg xGI per 90", f"{avg_xgi:.3f}")

    with col2:
        if 'ppm' in analysis_df.columns:
            avg_ppm = analysis_df['ppm'].mean()
            st.metric("Avg PPM", f"{avg_ppm:.2f}")

    with col3:
        avg_bps = analysis_df['bps_per_90'].mean()
        st.metric("Avg BPS/90", f"{avg_bps:.1f}")

    with col4:
        if 'threat_index' in analysis_df.columns:
            avg_threat = analysis_df['threat_index'].mean()
            st.metric("Avg Threat", f"{avg_threat:.3f}")

    st.markdown("---")

    # Top performers by different metrics
    st.subheader("🏆 Top Performers by Metric")

    metric_choice = st.selectbox(
        "Select Metric",
        ['xgi_per_90', 'ppm', 'bps_per_90', 'threat_index', 'total_points', 'form']
    )

    top_players = analysis_df[analysis_df['minutes'] >= 300].nlargest(15, metric_choice)

    st.dataframe(
        top_players[['web_name', 'position', 'team_name', 'cost', metric_choice, 'total_points']],
        hide_index=True,
        use_container_width=True
    )

    # Scatter plot
    st.markdown("---")
    st.subheader("📊 Metric Relationships")

    col1, col2 = st.columns(2)

    with col1:
        x_metric = st.selectbox("X-axis", ['cost', 'minutes', 'xgi_per_90', 'form'], index=0)

    with col2:
        y_metric = st.selectbox("Y-axis", ['total_points', 'xgi_per_90', 'ppm', 'bps_per_90'], index=0)

    filtered_df = analysis_df[analysis_df['minutes'] >= 300]

    fig = create_scatter_plot(
        filtered_df,
        x_metric,
        y_metric,
        'position',
        'selected_by_percent',
        ['web_name', 'team_name', 'cost', 'form']
    )

    st.plotly_chart(fig, use_container_width=True)


def show_xg_analysis(players_df: pd.DataFrame, metrics: AdvancedMetrics):
    """Show xG and xA analysis"""
    st.subheader("⚽ Expected Goals (xG) Analysis")

    st.markdown("""
    **Expected Goals (xG)** measures the quality of chances a player gets.
    **Expected Assists (xA)** measures the quality of chances a player creates.
    """)

    # Filter attacking players
    attacking_players = players_df[
        (players_df['position'].isin(['MID', 'FWD'])) &
        (players_df['minutes'] >= 500)
    ].copy()

    # Calculate xGI
    attacking_players['xgi_per_90'] = metrics.calculate_xgi_per_90()

    # Top xGI players
    st.markdown("#### 🎯 Top Expected Goal Involvement (xGI) per 90")

    top_xgi = attacking_players.nlargest(20, 'xgi_per_90')

    fig = px.bar(
        top_xgi,
        x='web_name',
        y='xgi_per_90',
        color='position',
        hover_data=['team_name', 'cost', 'total_points'],
        title="Top 20 Players by xGI per 90 minutes"
    )

    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # xG vs Actual Goals
    if 'expected_goals' in attacking_players.columns:
        st.markdown("---")
        st.markdown("#### 📊 Expected vs Actual Goals")

        # Calculate per 90 stats
        attacking_players['goals_per_90'] = (
            attacking_players['goals_scored'] / attacking_players['minutes'] * 90
        )

        attacking_players['xg_per_90'] = pd.to_numeric(
            attacking_players.get('expected_goals_per_90', 0),
            errors='coerce'
        ).fillna(0)

        fig = px.scatter(
            attacking_players,
            x='xg_per_90',
            y='goals_per_90',
            size='minutes',
            color='position',
            hover_data=['web_name', 'team_name', 'cost'],
            title="Expected Goals vs Actual Goals per 90"
        )

        # Add diagonal line (perfect expectation)
        max_val = max(attacking_players['xg_per_90'].max(), attacking_players['goals_per_90'].max())
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            line=dict(dash='dash', color='red'),
            name='Expected Line',
            showlegend=True
        ))

        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        **Interpretation:**
        - Players **above the line**: Outperforming xG (good finishers)
        - Players **on the line**: Performing as expected
        - Players **below the line**: Underperforming xG (unlucky or poor finishing)
        """)

    # Detailed table
    st.markdown("---")
    st.markdown("#### 📋 Detailed xG/xA Stats")

    xg_cols = ['web_name', 'position', 'team_name', 'cost', 'minutes', 'goals_scored', 'assists']

    if 'expected_goals' in attacking_players.columns:
        xg_cols.append('expected_goals')
    if 'expected_assists' in attacking_players.columns:
        xg_cols.append('expected_assists')

    xg_cols.extend(['xgi_per_90', 'total_points'])

    available_cols = [col for col in xg_cols if col in attacking_players.columns]

    st.dataframe(
        attacking_players.nlargest(30, 'xgi_per_90')[available_cols],
        hide_index=True,
        use_container_width=True
    )


def show_position_analysis(players_df: pd.DataFrame, metrics: AdvancedMetrics):
    """Show position-specific analysis"""
    st.subheader("🎯 Position-Specific Analysis")

    position = st.selectbox(
        "Select Position",
        ['GKP', 'DEF', 'MID', 'FWD']
    )

    if position == 'GKP':
        gk_metrics = metrics.calculate_goalkeeper_metrics()

        if not gk_metrics.empty:
            st.markdown("#### 🧤 Goalkeeper Metrics")

            st.dataframe(
                gk_metrics.nlargest(10, 'goalkeeper_score'),
                hide_index=True,
                use_container_width=True
            )

            # Visualize
            fig = px.bar(
                gk_metrics.nlargest(15, 'goalkeeper_score'),
                x='web_name',
                y='goalkeeper_score',
                color='cs_percentage',
                hover_data=['team', 'now_cost', 'saves_per_90'],
                title="Top Goalkeepers by Overall Score"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    elif position == 'DEF':
        def_metrics = metrics.calculate_defender_metrics()

        if not def_metrics.empty:
            st.markdown("#### 🛡️ Defender Metrics")

            st.dataframe(
                def_metrics.nlargest(15, 'defender_score'),
                hide_index=True,
                use_container_width=True
            )

            # Attacking defenders
            st.markdown("##### ⚡ Most Attacking Defenders")

            attacking_defs = def_metrics.nlargest(10, 'attacking_threat')

            fig = px.bar(
                attacking_defs,
                x='web_name',
                y='attacking_threat',
                color='clean_sheet_prob',
                hover_data=['team', 'now_cost', 'defensive_quality'],
                title="Defenders with Highest Attacking Threat"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    elif position == 'MID':
        mid_metrics = metrics.calculate_midfielder_metrics()

        if not mid_metrics.empty:
            st.markdown("#### ⚽ Midfielder Metrics")

            st.dataframe(
                mid_metrics.nlargest(15, 'midfielder_score'),
                hide_index=True,
                use_container_width=True
            )

            # Creativity vs Goal threat
            fig = px.scatter(
                mid_metrics,
                x='creativity_index',
                y='xgi_per_90',
                size='midfielder_score',
                color='now_cost',
                hover_data=['web_name', 'team'],
                title="Midfielder Creativity vs Goal Involvement",
                labels={
                    'creativity_index': 'Creativity (Assists)',
                    'xgi_per_90': 'Goal Involvement (xGI)'
                }
            )
            st.plotly_chart(fig, use_container_width=True)

    elif position == 'FWD':
        fwd_metrics = metrics.calculate_forward_metrics()

        if not fwd_metrics.empty:
            st.markdown("#### ⚡ Forward Metrics")

            st.dataframe(
                fwd_metrics.nlargest(15, 'forward_score'),
                hide_index=True,
                use_container_width=True
            )

            # Shot quality analysis
            fig = px.scatter(
                fwd_metrics,
                x='shot_quality',
                y='conversion_rate',
                size='forward_score',
                color='now_cost',
                hover_data=['web_name', 'team'],
                title="Forward Shot Quality vs Conversion Rate",
                labels={
                    'shot_quality': 'Shot Quality (xG per 90)',
                    'conversion_rate': 'Conversion Rate'
                }
            )
            st.plotly_chart(fig, use_container_width=True)


def show_captain_analysis(players_df: pd.DataFrame, metrics: AdvancedMetrics):
    """Show captain pick analysis"""
    st.subheader("👑 Captain Analysis")

    st.markdown("""
    Captain picks are crucial for FPL success! This analysis combines form, xGI,
    and minutes reliability to identify the best captaincy options.
    """)

    captain_df = metrics.calculate_captain_score()

    # Top captains
    st.markdown("#### 🏆 Top Captain Picks")

    top_captains = captain_df.head(20)

    st.dataframe(
        top_captains,
        hide_index=True,
        use_container_width=True
    )

    # Visualize captain scores
    fig = px.bar(
        top_captains.head(15),
        x='web_name',
        y='captain_score',
        color='position',
        hover_data=['team', 'form', 'xgi_per_90'],
        title="Top 15 Captain Options"
    )
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Captain score components
    st.markdown("---")
    st.markdown("#### 📊 Captain Score Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        # Form leaders
        st.markdown("##### 📈 Best Form")
        form_leaders = captain_df.nlargest(10, 'form')[['web_name', 'team', 'form', 'captain_score']]
        st.dataframe(form_leaders, hide_index=True, use_container_width=True)

    with col2:
        # xGI leaders
        st.markdown("##### ⚽ Best xGI")
        xgi_leaders = captain_df.nlargest(10, 'xgi_per_90')[['web_name', 'team', 'xgi_per_90', 'captain_score']]
        st.dataframe(xgi_leaders, hide_index=True, use_container_width=True)


def show_differentials_analysis(players_df: pd.DataFrame, metrics: AdvancedMetrics):
    """Show differential players analysis"""
    st.subheader("💎 Differential Players")

    st.markdown("""
    **Differentials** are low-owned players who can help you climb rankings.
    Perfect for chasing in mini-leagues!
    """)

    # Ownership threshold
    max_ownership = st.slider(
        "Maximum Ownership %",
        0.0, 20.0, 10.0, 0.5
    )

    min_points = st.slider(
        "Minimum Total Points",
        0, 100, 30, 5
    )

    # Find differentials
    differentials = metrics.find_differentials(
        max_ownership=max_ownership,
        min_points=min_points
    )

    if differentials.empty:
        st.warning("No differentials found with these criteria. Try adjusting the filters.")
        return

    st.markdown(f"#### 🔍 Found {len(differentials)} Differential Options")

    st.dataframe(
        differentials.head(25),
        hide_index=True,
        use_container_width=True
    )

    # Visualize differentials
    fig = px.scatter(
        differentials.head(30),
        x='ownership',
        y='ppm',
        size='differential_score',
        color='element_type',
        hover_data=['web_name', 'team', 'now_cost', 'total_points'],
        title="Differential Players: Ownership vs Value",
        labels={'ppm': 'Points per Million', 'ownership': 'Ownership %'}
    )

    st.plotly_chart(fig, use_container_width=True)

    # Differential by position
    st.markdown("---")
    st.markdown("#### 📊 Differentials by Position")

    position_filter = st.selectbox(
        "Filter by Position",
        ['All'] + differentials['element_type'].unique().tolist()
    )

    if position_filter != 'All':
        position_diffs = differentials[differentials['element_type'] == position_filter]
    else:
        position_diffs = differentials

    st.dataframe(
        position_diffs.head(15),
        hide_index=True,
        use_container_width=True
    )


def show_value_analysis(players_df: pd.DataFrame, metrics: AdvancedMetrics):
    """Show value analysis"""
    st.subheader("💰 Value Analysis")

    st.markdown("""
    **Points per Million (PPM)** is the key value metric in FPL.
    Find the most efficient players for your budget!
    """)

    # Calculate PPM
    players_df['ppm'] = metrics.calculate_points_per_million()

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        position_filter = st.selectbox("Position", ['All', 'GKP', 'DEF', 'MID', 'FWD'])

    with col2:
        min_cost = st.number_input("Min Cost (£m)", 4.0, 15.0, 4.0, 0.5)

    with col3:
        max_cost = st.number_input("Max Cost (£m)", 4.0, 15.0, 15.0, 0.5)

    # Filter data
    value_df = players_df[
        (players_df['minutes'] >= 500) &
        (players_df['cost'] >= min_cost) &
        (players_df['cost'] <= max_cost)
    ].copy()

    if position_filter != 'All':
        value_df = value_df[value_df['position'] == position_filter]

    # Top value players
    st.markdown("#### 🏆 Best Value Players")

    top_value = value_df.nlargest(20, 'ppm')

    st.dataframe(
        top_value[['web_name', 'position', 'team_name', 'cost', 'total_points', 'ppm', 'form']],
        hide_index=True,
        use_container_width=True
    )

    # Value visualization
    fig = px.bar(
        top_value.head(15),
        x='web_name',
        y='ppm',
        color='position',
        hover_data=['team_name', 'cost', 'total_points'],
        title="Top 15 Players by Points per Million"
    )
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Cost brackets
    st.markdown("---")
    st.markdown("#### 💵 Value by Price Bracket")

    value_df['price_bracket'] = pd.cut(
        value_df['cost'],
        bins=[0, 5, 7, 9, 11, 20],
        labels=['Budget (<£5m)', 'Mid (£5-7m)', 'Premium (£7-9m)', 'Elite (£9-11m)', 'Super Elite (>£11m)']
    )

    bracket_analysis = value_df.groupby('price_bracket').agg({
        'ppm': 'mean',
        'total_points': 'mean',
        'web_name': 'count'
    }).round(2)

    bracket_analysis.columns = ['Avg PPM', 'Avg Points', 'Player Count']

    st.dataframe(bracket_analysis, use_container_width=True)


def show_bonus_analysis(players_df: pd.DataFrame, metrics: AdvancedMetrics):
    """Show bonus point analysis"""
    st.subheader("🎁 Bonus Point Analysis")

    st.markdown("""
    **Bonus Points** can make a huge difference! BPS (Bonus Point System) determines
    who gets the 3, 2, and 1 bonus points in each match.
    """)

    # Calculate BPS per 90
    players_df['bps_per_90'] = metrics.calculate_bonus_point_potential()

    # Top BPS players
    bps_df = players_df[players_df['minutes'] >= 500].copy()

    st.markdown("#### 🏆 Top Bonus Point Magnets")

    top_bps = bps_df.nlargest(20, 'bps_per_90')

    st.dataframe(
        top_bps[['web_name', 'position', 'team_name', 'cost', 'bonus', 'bps', 'bps_per_90', 'total_points']],
        hide_index=True,
        use_container_width=True
    )

    # BPS visualization
    fig = px.bar(
        top_bps.head(15),
        x='web_name',
        y='bps_per_90',
        color='position',
        hover_data=['team_name', 'cost', 'bonus'],
        title="Top 15 Players by BPS per 90 minutes"
    )
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Bonus frequency
    st.markdown("---")
    st.markdown("#### 📊 Bonus Point Frequency")

    col1, col2 = st.columns(2)

    with col1:
        # Most bonus points
        most_bonus = bps_df.nlargest(10, 'bonus')[['web_name', 'position', 'team_name', 'bonus', 'bps_per_90']]
        st.dataframe(most_bonus, hide_index=True, use_container_width=True)

    with col2:
        # Bonus by position
        bonus_by_pos = bps_df.groupby('position').agg({
            'bonus': 'mean',
            'bps_per_90': 'mean'
        }).round(2)

        fig = px.bar(
            bonus_by_pos,
            y=['bonus', 'bps_per_90'],
            title="Average Bonus Stats by Position",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
