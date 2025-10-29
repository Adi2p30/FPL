"""
Team Builder Dashboard
======================

Build your FPL team with budget tracking, formation management, and constraints
"""

import streamlit as st
import pandas as pd
from typing import Dict, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.visualizations import (
    create_team_formation_visual,
    create_budget_gauge,
    create_position_distribution
)
from utils.data_loader import calculate_team_stats


# Initialize session state for team
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = {
        'GKP': [],
        'DEF': [],
        'MID': [],
        'FWD': []
    }

if 'formation' not in st.session_state:
    st.session_state.formation = '3-4-3'

if 'budget' not in st.session_state:
    st.session_state.budget = 100.0


# Position limits (min, max)
POSITION_LIMITS = {
    'GKP': (2, 2),
    'DEF': (5, 5),
    'MID': (5, 5),
    'FWD': (3, 3)
}

TEAM_SIZE = 15


def show_team_builder(players_df: pd.DataFrame, teams_df: pd.DataFrame):
    """
    Team builder page

    Args:
        players_df: Players DataFrame with metrics
        teams_df: Teams DataFrame
    """
    st.title("⚽ FPL Team Builder")

    st.markdown("""
    Build your Fantasy Premier League team with **budget tracking**, **formation management**,
    and **real-time constraints**. Data from FPL API.
    """)

    # Sidebar - Team controls
    st.sidebar.markdown("## ⚙️ Team Settings")

    # Formation selector
    formation = st.sidebar.selectbox(
        "Select Formation",
        ['3-4-3', '3-5-2', '4-3-3', '4-4-2', '4-5-1', '5-3-2', '5-4-1'],
        index=0
    )

    st.session_state.formation = formation

    # Budget reset
    if st.sidebar.button("🔄 Reset Team"):
        st.session_state.selected_team = {
            'GKP': [],
            'DEF': [],
            'MID': [],
            'FWD': []
        }
        st.session_state.budget = 100.0
        st.rerun()

    # Export/Import team
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📤 Export/Import")

    if st.sidebar.button("📥 Export Team"):
        team_data = []
        for pos, players in st.session_state.selected_team.items():
            for player_name in players:
                team_data.append(player_name)

        if team_data:
            export_str = ','.join(team_data)
            st.sidebar.download_button(
                "Download Team",
                export_str,
                file_name="fpl_team.txt",
                mime="text/plain"
            )
        else:
            st.sidebar.warning("No players selected yet")

    # Main layout
    col1, col2 = st.columns([2, 1])

    with col2:
        # Budget tracker
        st.markdown("### 💰 Budget Tracker")

        total_players = sum(len(players) for players in st.session_state.selected_team.values())
        selected_players_list = []

        for pos, player_names in st.session_state.selected_team.items():
            for name in player_names:
                player = players_df[players_df['web_name'] == name]
                if not player.empty:
                    selected_players_list.append(player.iloc[0])

        if selected_players_list:
            selected_df = pd.DataFrame(selected_players_list)
            total_cost = selected_df['cost'].sum()
        else:
            selected_df = pd.DataFrame()
            total_cost = 0

        remaining_budget = st.session_state.budget - total_cost

        # Budget gauge
        fig = create_budget_gauge(total_cost, st.session_state.budget)
        st.plotly_chart(fig, use_container_width=True)

        # Budget metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Spent", f"£{total_cost:.1f}m")
            st.metric("Players", f"{total_players}/15")

        with col_b:
            st.metric("Remaining", f"£{remaining_budget:.1f}m")
            st.metric("Avg Cost", f"£{total_cost/max(total_players, 1):.1f}m")

        # Position breakdown
        st.markdown("---")
        st.markdown("### 📊 Squad Composition")

        for pos, (min_req, max_req) in POSITION_LIMITS.items():
            current = len(st.session_state.selected_team[pos])
            progress = current / max_req

            color = "green" if current == max_req else "orange" if current >= min_req else "red"

            st.progress(progress, text=f"{pos}: {current}/{max_req}")

            if current < min_req:
                st.error(f"⚠️ Need {min_req - current} more {pos}")
            elif current == max_req:
                st.success(f"✅ {pos} complete")

        # Team validation
        st.markdown("---")
        st.markdown("### ✅ Team Validation")

        is_valid = True
        validation_messages = []

        # Check squad size
        if total_players < TEAM_SIZE:
            is_valid = False
            validation_messages.append(f"❌ Need {TEAM_SIZE - total_players} more players")
        elif total_players == TEAM_SIZE:
            validation_messages.append("✅ Squad size: 15/15")

        # Check positions
        for pos, (min_req, max_req) in POSITION_LIMITS.items():
            current = len(st.session_state.selected_team[pos])
            if current < min_req:
                is_valid = False
                validation_messages.append(f"❌ {pos}: Need {min_req - current} more")
            elif current > max_req:
                is_valid = False
                validation_messages.append(f"❌ {pos}: {current - max_req} too many")
            else:
                validation_messages.append(f"✅ {pos}: {current}/{max_req}")

        # Check budget
        if total_cost > st.session_state.budget:
            is_valid = False
            validation_messages.append(f"❌ Over budget by £{total_cost - st.session_state.budget:.1f}m")
        else:
            validation_messages.append(f"✅ Budget: £{total_cost:.1f}m/£{st.session_state.budget:.1f}m")

        # Check max players per team (3)
        if not selected_df.empty:
            team_counts = selected_df['team_name'].value_counts()
            max_per_team = team_counts.max()
            if max_per_team > 3:
                is_valid = False
                overloaded_teams = team_counts[team_counts > 3]
                for team, count in overloaded_teams.items():
                    validation_messages.append(f"❌ {team}: {count} players (max 3)")
            else:
                validation_messages.append("✅ Max 3 per team rule")

        for msg in validation_messages:
            if "❌" in msg:
                st.error(msg)
            elif "✅" in msg:
                st.success(msg)
            else:
                st.info(msg)

        if is_valid:
            st.balloons()
            st.success("🎉 Your team is valid and ready!")

    with col1:
        # Player selection
        st.markdown("### 👥 Select Players")

        # Position tabs
        tabs = st.tabs(["🧤 Goalkeepers", "🛡️ Defenders", "⚽ Midfielders", "⚡ Forwards"])

        positions = ['GKP', 'DEF', 'MID', 'FWD']

        for tab, position in zip(tabs, positions):
            with tab:
                st.markdown(f"#### Select {position} ({len(st.session_state.selected_team[position])}/{POSITION_LIMITS[position][1]})")

                # Filter controls
                col_filter1, col_filter2, col_filter3 = st.columns(3)

                with col_filter1:
                    team_filter = st.selectbox(
                        "Filter by Team",
                        ['All'] + sorted(teams_df['name'].unique().tolist()),
                        key=f"team_{position}"
                    )

                with col_filter2:
                    max_cost = st.number_input(
                        "Max Cost (£m)",
                        min_value=4.0,
                        max_value=15.0,
                        value=remaining_budget if remaining_budget > 4.0 else 15.0,
                        step=0.5,
                        key=f"cost_{position}"
                    )

                with col_filter3:
                    sort_by = st.selectbox(
                        "Sort By",
                        ['total_points', 'cost', 'form', 'points_per_game'],
                        key=f"sort_{position}"
                    )

                # Filter players
                pos_players = players_df[players_df['position'] == position].copy()

                if team_filter != 'All':
                    pos_players = pos_players[pos_players['team_name'] == team_filter]

                pos_players = pos_players[pos_players['cost'] <= max_cost]
                pos_players = pos_players.sort_values(sort_by, ascending=False)

                # Display available players
                st.markdown("##### Available Players")

                for _, player in pos_players.head(20).iterrows():
                    player_name = player['web_name']

                    # Check if already selected
                    is_selected = player_name in st.session_state.selected_team[position]

                    # Check team constraint (max 3 per team)
                    if not selected_df.empty:
                        team_count = len(selected_df[selected_df['team_name'] == player['team_name']])
                        team_limit_reached = team_count >= 3 and not is_selected
                    else:
                        team_limit_reached = False

                    # Check position limit
                    position_limit_reached = len(st.session_state.selected_team[position]) >= POSITION_LIMITS[position][1]

                    # Player card
                    with st.container():
                        col_a, col_b, col_c = st.columns([3, 1, 1])

                        with col_a:
                            emoji = "✅" if is_selected else ""
                            st.markdown(f"""
                            **{emoji} {player_name}** ({player['team_name']})

                            💰 £{player['cost']:.1f}m | 📊 {player['total_points']:.0f} pts |
                            📈 Form: {player.get('form', 0):.1f} | 👥 {player['selected_by_percent']:.1f}%
                            """)

                        with col_b:
                            # Stats display
                            if position == 'GKP':
                                st.caption(f"CS: {player.get('clean_sheets', 0)}")
                                st.caption(f"Saves: {player.get('saves', 0)}")
                            elif position == 'DEF':
                                st.caption(f"CS: {player.get('clean_sheets', 0)}")
                                st.caption(f"G+A: {player.get('goals_scored', 0) + player.get('assists', 0)}")
                            else:
                                st.caption(f"Goals: {player.get('goals_scored', 0)}")
                                st.caption(f"Assists: {player.get('assists', 0)}")

                        with col_c:
                            if is_selected:
                                if st.button("❌ Remove", key=f"remove_{player_name}"):
                                    st.session_state.selected_team[position].remove(player_name)
                                    st.rerun()
                            else:
                                disabled = position_limit_reached or team_limit_reached or (player['cost'] > remaining_budget)

                                tooltip = ""
                                if position_limit_reached:
                                    tooltip = f"Max {position} reached"
                                elif team_limit_reached:
                                    tooltip = "Max 3 from team"
                                elif player['cost'] > remaining_budget:
                                    tooltip = "Insufficient budget"

                                if st.button(
                                    "➕ Add",
                                    key=f"add_{player_name}",
                                    disabled=disabled,
                                    help=tooltip if disabled else "Add to team"
                                ):
                                    st.session_state.selected_team[position].append(player_name)
                                    st.rerun()

                        st.markdown("---")

        # Current team display
        st.markdown("---")
        st.markdown("### 🏆 Your Current Team")

        if not selected_df.empty:
            # Team formation visualization
            fig = create_team_formation_visual(selected_df, st.session_state.formation)
            st.plotly_chart(fig, use_container_width=True)

            # Team stats
            st.markdown("#### 📈 Team Statistics")

            team_stats = calculate_team_stats(selected_df)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Points", f"{team_stats['total_points']:.0f}")

            with col2:
                st.metric("Total Goals", f"{team_stats['total_goals']:.0f}")

            with col3:
                st.metric("Total Assists", f"{team_stats['total_assists']:.0f}")

            with col4:
                st.metric("Avg Ownership", f"{team_stats['avg_ownership']:.1f}%")

            # Selected players table
            st.markdown("#### 📋 Selected Players")

            display_df = selected_df[['web_name', 'position', 'team_name', 'cost', 'total_points', 'form']].copy()
            display_df.columns = ['Player', 'Pos', 'Team', 'Cost (£m)', 'Points', 'Form']

            # Sort by position
            pos_order = {'GKP': 1, 'DEF': 2, 'MID': 3, 'FWD': 4}
            display_df['sort'] = display_df['Pos'].map(pos_order)
            display_df = display_df.sort_values('sort').drop('sort', axis=1)

            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True
            )

            # Position distribution chart
            col1, col2 = st.columns(2)

            with col1:
                fig = create_position_distribution(selected_df)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Team distribution
                team_dist = selected_df['team_name'].value_counts()

                import plotly.express as px
                fig = px.bar(
                    x=team_dist.index,
                    y=team_dist.values,
                    labels={'x': 'Team', 'y': 'Players'},
                    title='Players per Team'
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("👆 Start building your team by selecting players from the tabs above!")

    # Tips and strategies
    st.markdown("---")
    st.markdown("### 💡 Team Building Tips")

    tip_col1, tip_col2, tip_col3 = st.columns(3)

    with tip_col1:
        st.info("""
        **💰 Budget Strategy**
        - Leave £0.5-1.5m for transfers
        - Balance premiums with enablers
        - Don't overspend on GKP
        """)

    with tip_col2:
        st.info("""
        **📊 Formation Tips**
        - 3-4-3: Balanced attack
        - 4-4-2: Budget forwards
        - 3-5-2: Mid-heavy
        """)

    with tip_col3:
        st.info("""
        **⚖️ Balance**
        - Max 3 players per team
        - Mix premiums (11m+) with value picks
        - Consider fixtures
        """)
