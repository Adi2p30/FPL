# 🎨 FPL Advanced Analytics Dashboard - UI Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Features](#features)
- [Page-by-Page Guide](#page-by-page-guide)
- [API Integration](#api-integration)
- [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

A comprehensive **web-based dashboard** for Fantasy Premier League analysis built with **Streamlit**. Features:

- 🔍 **Player Comparison** - Compare up to 4 players with advanced metrics
- ⚽ **Team Builder** - Build your FPL team with budget tracking
- 📊 **Advanced Analytics** - 20+ metrics including xG, xA, BPS
- 🎯 **Live Data** - Fetches real-time data from FPL API
- 📈 **Interactive Visualizations** - Plotly charts and graphs
- 💡 **Smart Insights** - AI-powered recommendations

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
# Navigate to the FPL directory
cd /path/to/FPL

# Install required packages
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
# Check Streamlit installation
streamlit version
```

---

## 🎮 Running the App

### Start the Dashboard

```bash
# From the FPL directory
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

### Alternative: Specify Port

```bash
streamlit run app.py --server.port 8080
```

### Run in Background

```bash
nohup streamlit run app.py &
```

---

## ✨ Features

### 🏠 Home Page

**Overview Dashboard**
- Quick stats: Total players, avg points, avg cost
- Top performers by category (scorers, value, form, ownership)
- Visual insights (cost vs points, position distribution)
- Team overview with stats

**Navigation**
- Sidebar navigation to all pages
- Live data refresh indicator
- Player and team counts

---

## 📖 Page-by-Page Guide

### 1. 🔍 Player Comparison

**Purpose**: Compare multiple players side-by-side

**Features**:
- ✅ Compare up to 4 players simultaneously
- 📊 Statistical comparison tables
- 📡 Radar charts for visual comparison
- 📈 Bar charts for individual metrics
- 🎯 Position-specific stats
- 💡 AI-powered recommendations

**How to Use**:

1. **Apply Filters** (Sidebar):
   - Filter by position (GKP, DEF, MID, FWD)
   - Filter by team
   - Set minimum minutes played
   - Choose sort criteria

2. **Select Players**:
   - Choose Player 1 and Player 2 (required)
   - Optionally add Player 3 and Player 4
   - Players must have played minimum minutes

3. **View Comparisons**:
   - **Overview Cards**: Quick player stats
   - **Statistical Table**: Core stats with color coding
   - **Advanced Metrics**: xGI, PPM, BPS, etc.
   - **Radar Chart**: Visual multi-metric comparison
   - **Bar Charts**: Individual metric comparison

4. **Get Insights**:
   - View highest points, best value, best form
   - Read AI recommendation
   - Export comparison data

**Metrics Compared**:
- Total Points
- Cost (£m)
- Form
- Points per Game
- Minutes
- Goals & Assists
- Clean Sheets
- Bonus Points
- Ownership %
- xGI per 90 (if available)
- PPM (Points per Million)

---

### 2. ⚽ Team Builder

**Purpose**: Build your 15-player FPL team with constraints

**Features**:
- 💰 Real-time budget tracking (£100m total)
- 🎯 Position limits enforcement (2 GKP, 5 DEF, 5 MID, 3 FWD)
- ⚖️ Team constraint validation (max 3 per club)
- 🏟️ Formation visualization
- 📊 Team statistics
- 💾 Export/Import team

**How to Use**:

1. **Select Formation** (Sidebar):
   - Choose from: 3-4-3, 3-5-2, 4-3-3, 4-4-2, 4-5-1, 5-3-2, 5-4-1
   - Formation determines starting XI structure

2. **Build Your Squad**:

   **For Each Position** (Tabs):
   - 🧤 Goalkeepers (2 required)
   - 🛡️ Defenders (5 required)
   - ⚽ Midfielders (5 required)
   - ⚡ Forwards (3 required)

   **Player Selection**:
   - Filter by team
   - Set max cost
   - Sort by metric
   - View player stats (goals, assists, form, etc.)
   - Click **➕ Add** to add player
   - Click **❌ Remove** to remove player

3. **Monitor Budget** (Right Panel):
   - **Budget Gauge**: Visual remaining budget
   - **Spent**: Total cost of selected players
   - **Remaining**: Money left in bank
   - **Players**: Count (must be 15)
   - **Avg Cost**: Average player cost

4. **Check Squad Composition**:
   - Progress bars for each position
   - ✅ Green: Position complete
   - ⚠️ Orange: Minimum met
   - ❌ Red: Below minimum

5. **Validate Team**:
   - Squad size: Must be 15
   - Position requirements: Must meet min/max
   - Budget: Must be under £100m
   - Team limit: Max 3 players per club
   - 🎉 Balloons when valid!

6. **View Team**:
   - **Formation Visual**: See your team on a pitch
   - **Team Stats**: Points, goals, assists, ownership
   - **Player Table**: Full squad list
   - **Position Distribution**: Pie chart
   - **Team Distribution**: Players per club

7. **Export/Import**:
   - Export team to text file
   - Share with friends
   - Import previously saved team

**Constraints**:
- ✅ Budget: £100.0m total
- ✅ Squad size: 15 players
- ✅ Positions: 2 GKP, 5 DEF, 5 MID, 3 FWD
- ✅ Max per team: 3 players
- ✅ Formation: 11 starters matching formation

**Tips**:
- Leave £0.5-1.5m for future transfers
- Balance premiums (11m+) with enablers (4.5m)
- Don't overspend on goalkeepers
- Consider player fixtures
- Mix template (high ownership) with differentials

---

### 3. 📊 Advanced Analytics

**Purpose**: Deep dive into 20+ advanced metrics

**Analysis Types**:

#### a) 📈 Overview
- Average metrics across all players
- Top performers by selected metric
- Scatter plots showing metric relationships
- Customizable X and Y axes

#### b) ⚽ Expected Goals (xG)
- **xGI (Expected Goal Involvements)**: xG + xA per 90
- **Top xGI Players**: Bar chart ranking
- **xG vs Actual Goals**: Scatter plot
  - Above line: Outperforming (good finishers)
  - On line: As expected
  - Below line: Underperforming (unlucky)
- **Detailed Stats Table**: Goals, assists, xG, xA

#### c) 🎯 Position-Specific

**Goalkeepers** (GKP):
- Saves per 90
- xG Prevented
- Clean Sheet %
- Overall goalkeeper score

**Defenders** (DEF):
- Clean sheet probability
- Defensive quality (xGC-based)
- Attacking threat
- Most attacking defenders

**Midfielders** (MID):
- Creativity index
- xA per 90
- xGI per 90
- Creativity vs Goal involvement scatter

**Forwards** (FWD):
- Shot quality (xG per 90)
- Conversion rate
- Penalty box threat
- Shot quality vs Conversion scatter

#### d) 👑 Captain Analysis
- Captain score calculation
- Top 20 captain options
- Form leaders
- xGI leaders
- Multi-factor scoring

#### e) 💎 Differentials
- Low-owned gems
- Adjustable ownership threshold (default: <10%)
- Minimum points filter
- Differential score calculation
- Ownership vs Value scatter
- Position-specific differentials

#### f) 💰 Value Analysis
- Points per Million (PPM) leaders
- Filter by position and price
- Value by price bracket:
  - Budget (<£5m)
  - Mid (£5-7m)
  - Premium (£7-9m)
  - Elite (£9-11m)
  - Super Elite (>£11m)

#### g) 🎁 Bonus Points
- BPS (Bonus Point System) per 90
- Top bonus magnets
- Bonus point frequency
- Average bonus by position

---

## 🔌 API Integration

### FPL Official API

The dashboard uses the **official FPL API** (free, no authentication needed):

**Endpoints Used**:
- `https://fantasy.premierleague.com/api/bootstrap-static/`
  - Player data (stats, costs, points)
  - Team data
  - Gameweek info

**Data Fetched**:
- Player stats (600+ players)
- Real-time pricing
- Current gameweek
- Team information
- Form, points, ownership
- Expected stats (xG, xA)
- Bonus point system data

**Caching**:
- Data cached for 1 hour
- Automatic refresh
- Click "R" to force refresh

**Rate Limits**:
- No strict limits on FPL API
- Cached to minimize requests

---

## 🎨 User Interface

### Color Scheme
- **Primary**: #37003c (FPL Purple)
- **Secondary**: #00ff87 (FPL Green)
- **Positions**:
  - GKP: Gold (#FFD700)
  - DEF: Blue (#4169E1)
  - MID: Green (#32CD32)
  - FWD: Red (#DC143C)

### Layout
- **Sidebar**: Navigation and filters
- **Main Area**: Content with tabs and columns
- **Wide Layout**: Maximum screen usage
- **Responsive**: Works on desktop and tablet

### Interactive Elements
- Hover tooltips on charts
- Clickable legends
- Sortable tables
- Expandable sections
- Dynamic updates

---

## 🐛 Troubleshooting

### Common Issues

#### 1. App Won't Start

**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install -r requirements.txt
```

#### 2. Data Loading Fails

**Error**: "Failed to load FPL data"

**Solutions**:
- Check internet connection
- FPL API might be down (rare)
- Try refreshing the page
- Wait a few minutes and try again

#### 3. Slow Performance

**Causes**:
- Large dataset filtering
- Multiple visualizations

**Solutions**:
- Increase minimum minutes filter
- Close unused browser tabs
- Use more specific filters

#### 4. Charts Not Displaying

**Solutions**:
- Check browser compatibility (Chrome, Firefox, Edge)
- Disable browser extensions
- Clear browser cache
- Try incognito mode

#### 5. Team Builder Not Saving

**Solution**:
- Session state resets on page reload
- Use export feature to save team
- Don't refresh page while building

### Debug Mode

Run with debug information:
```bash
streamlit run app.py --logger.level=debug
```

### Browser Compatibility

**Supported**:
- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Edge
- ✅ Safari

**Not Supported**:
- ❌ Internet Explorer

---

## 💡 Tips & Tricks

### 1. Performance Optimization
- Set minimum minutes filter (>300) to reduce data
- Use position filters to narrow results
- Close unused tabs

### 2. Best Practices
- **Player Comparison**: Compare similar positions
- **Team Builder**: Build in one session
- **Analytics**: Start with Overview, then dive deep

### 3. Keyboard Shortcuts
- `R`: Refresh/Reload data
- `Ctrl/Cmd + K`: Command palette
- `Ctrl/Cmd + Shift + C`: Clear cache

### 4. Mobile Usage
- App works on tablets (landscape mode)
- Not optimized for phones (use desktop)

### 5. Data Export
- Use export buttons to save data
- Import to Excel/Google Sheets for further analysis
- Share team codes with friends

---

## 📚 Advanced Features

### Custom Formations
Build team in any valid formation:
- Attacking: 3-4-3, 3-5-2
- Balanced: 4-4-2, 4-3-3
- Defensive: 5-4-1, 5-3-2

### Metric Definitions

**PPM (Points per Million)**: Total points ÷ Cost
- **Good**: > 5.0 (budget), > 4.0 (premium)

**xGI (Expected Goal Involvements)**: xG + xA per 90
- **Good**: > 0.8 (attackers)

**BPS (Bonus Point System)**: FPL's bonus algorithm
- **32+ BPS** = 3 bonus points
- **24-31 BPS** = 2 bonus points
- **18-23 BPS** = 1 bonus point

**Form**: Average points over last few games
- **Good**: > 5.0

### Filter Combinations

**Finding Value**:
- Position: Any
- Min Minutes: 500
- Sort: PPM
- Cost: 4.0-7.0

**Finding Differentials**:
- Ownership: < 10%
- Min Points: 30
- Sort: Form
- Any position

**Finding Captains**:
- Min Minutes: 500
- Sort: Captain Score
- Position: MID or FWD
- Cost: > 9.0

---

## 🔄 Updates & Maintenance

### Data Freshness
- Cache: 1 hour
- API updates: Real-time
- Prices: Updated daily (1:30am GMT)
- Stats: Updated after matches

### Version History
- v1.0: Initial release
- Features: Comparison, Builder, Analytics
- Pages: 4 (Home, Comparison, Builder, Analytics)

### Future Features
- [ ] Historical gameweek data
- [ ] Fixture difficulty rating
- [ ] Price change predictions
- [ ] Transfer suggestions
- [ ] ML price predictions
- [ ] User authentication
- [ ] Save multiple teams

---

## 📞 Support

### Getting Help

**Documentation**:
- This guide (UI_GUIDE.md)
- Main README.md
- Code comments

**Issues**:
- GitHub Issues (if applicable)
- Check troubleshooting section

**Community**:
- FPL subreddit: r/FantasyPL
- FPL Discord servers
- Twitter: #FPL

---

## 🎉 Enjoy!

You now have a powerful FPL analytics tool at your fingertips!

**Quick Start**:
1. Run `streamlit run app.py`
2. Explore the Home page
3. Try Player Comparison
4. Build your team in Team Builder
5. Dive into Advanced Analytics

**Pro Tips**:
- Use filters to narrow results
- Compare similar-priced players
- Build team early in the season
- Check analytics weekly for form
- Export data for records

**Happy FPLing! ⚽🏆**

---

*Last Updated: 2025*
*Made with ❤️ using Streamlit, FPL API, and Python*
