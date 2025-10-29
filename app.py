"""
FPL Advanced Analytics Dashboard
=================================

Comprehensive Fantasy Premier League analysis tool with:
- Player Comparison
- Team Builder
- Advanced Analytics
- Live Data from FPL API
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_fpl_data, load_advanced_metrics, get_top_players
from utils.visualizations import create_scatter_plot, create_cost_vs_points

# Page config
st.set_page_config(
    page_title="FPL Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #37003c;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #00ff87 0%, #37003c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #37003c;
    }

    .stButton>button {
        background-color: #37003c;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 2rem;
    }

    .stButton>button:hover {
        background-color: #00ff87;
        color: #37003c;
    }

    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }

    h1, h2, h3 {
        color: #37003c;
    }

    .dataframe {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application"""

    # Header
    st.markdown('<h1 class="main-header">⚽ FPL Advanced Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["🏠 Home", "🔍 Player Comparison", "⚽ Team Builder", "📊 Advanced Analytics"],
        label_visibility="collapsed"
    )

    # Load data
    with st.spinner("Loading FPL data..."):
        players_df, teams_df, raw_data = load_fpl_data()

        if players_df.empty:
            st.error("Failed to load FPL data. Please check your connection and try again.")
            return

        # Load advanced metrics
        analysis_df = load_advanced_metrics(players_df)

    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.info(f"""
    **Data Info**

    🎮 Players: {len(players_df)}

    🏆 Teams: {len(teams_df)}

    📊 Metrics: 20+

    🔄 Last Updated: Now
    """)

    # Route to pages
    if page == "🏠 Home":
        show_home(analysis_df, teams_df)
    elif page == "🔍 Player Comparison":
        from pages.player_comparison import show_player_comparison
        show_player_comparison(analysis_df, teams_df)
    elif page == "⚽ Team Builder":
        from pages.team_builder import show_team_builder
        show_team_builder(analysis_df, teams_df)
    elif page == "📊 Advanced Analytics":
        from pages.analytics import show_analytics
        show_analytics(analysis_df, teams_df)


def show_home(players_df: pd.DataFrame, teams_df: pd.DataFrame):
    """
    Home page with overview and top players

    Args:
        players_df: Players DataFrame
        teams_df: Teams DataFrame
    """
    st.title("🏠 Welcome to FPL Analytics Dashboard")

    st.markdown("""
    ### 🚀 Features

    - **🔍 Player Comparison**: Compare players side-by-side with advanced metrics
    - **⚽ Team Builder**: Build your FPL team with budget tracking and formation visualization
    - **📊 Advanced Analytics**: Deep dive into xG, xA, BPS, and 20+ metrics
    - **💡 Smart Insights**: AI-powered recommendations based on form and fixtures

    ---
    """)

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Players",
            len(players_df),
            delta="Active"
        )

    with col2:
        avg_points = players_df['total_points'].mean()
        st.metric(
            "Avg Points",
            f"{avg_points:.1f}",
            delta=f"{players_df['total_points'].max()} max"
        )

    with col3:
        avg_cost = players_df['cost'].mean()
        st.metric(
            "Avg Cost",
            f"£{avg_cost:.1f}m",
            delta=f"£{players_df['cost'].max():.1f}m max"
        )

    with col4:
        avg_ownership = players_df['selected_by_percent'].mean()
        st.metric(
            "Avg Ownership",
            f"{avg_ownership:.1f}%",
            delta=f"{players_df['selected_by_percent'].max():.1f}% max"
        )

    st.markdown("---")

    # Top performers section
    st.subheader("🏆 Top Performers")

    tab1, tab2, tab3, tab4 = st.tabs(["⚽ Top Scorers", "🎯 Best Value", "📈 Form", "👥 Most Owned"])

    with tab1:
        top_scorers = get_top_players(players_df, 'total_points', 10)
        st.dataframe(
            top_scorers[['web_name', 'position', 'team_name', 'cost', 'total_points', 'goals_scored', 'assists']],
            hide_index=True,
            use_container_width=True
        )

    with tab2:
        if 'ppm' in players_df.columns:
            top_value = get_top_players(players_df[players_df['minutes'] >= 500], 'ppm', 10)
            st.dataframe(
                top_value[['web_name', 'position', 'team_name', 'cost', 'total_points', 'ppm']],
                hide_index=True,
                use_container_width=True
            )

    with tab3:
        top_form = get_top_players(players_df[players_df['minutes'] >= 300], 'form', 10)
        st.dataframe(
            top_form[['web_name', 'position', 'team_name', 'cost', 'form', 'total_points']],
            hide_index=True,
            use_container_width=True
        )

    with tab4:
        top_owned = get_top_players(players_df, 'selected_by_percent', 10)
        st.dataframe(
            top_owned[['web_name', 'position', 'team_name', 'cost', 'selected_by_percent', 'total_points']],
            hide_index=True,
            use_container_width=True
        )

    st.markdown("---")

    # Visualizations
    st.subheader("📊 Quick Insights")

    col1, col2 = st.columns(2)

    with col1:
        # Cost vs Points scatter
        fig = create_cost_vs_points(players_df[players_df['minutes'] >= 500])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Position distribution
        pos_counts = players_df['position'].value_counts()
        fig = px.pie(
            values=pos_counts.values,
            names=pos_counts.index,
            title="Players by Position",
            color_discrete_map={
                'GKP': '#FFD700',
                'DEF': '#4169E1',
                'MID': '#32CD32',
                'FWD': '#DC143C'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    # Team overview
    st.markdown("---")
    st.subheader("🏟️ Teams Overview")

    team_stats = players_df.groupby('team_name').agg({
        'total_points': 'sum',
        'goals_scored': 'sum',
        'assists': 'sum',
        'clean_sheets': 'sum',
        'cost': 'mean'
    }).round(2)

    team_stats = team_stats.sort_values('total_points', ascending=False).head(10)
    team_stats.columns = ['Total Points', 'Goals', 'Assists', 'Clean Sheets', 'Avg Cost']

    st.dataframe(team_stats, use_container_width=True)

    # Footer
    st.markdown("---")
    st.info("""
    💡 **Pro Tip**: Use the sidebar to navigate between different features.
    Start with Player Comparison to find the best picks, then build your team in Team Builder!
    """)


if __name__ == "__main__":
    main()
