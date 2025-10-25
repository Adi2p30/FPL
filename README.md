# ⚽ FPL Advanced Analytics Toolkit

A comprehensive Fantasy Premier League (FPL) analysis toolkit with **20+ advanced metrics** and strategies used by popular FPL content creators.

## 🌟 Features

### Advanced Metrics Modules

- **`advanced_metrics.py`** - 20+ position-specific metrics including xG, xA, xGI, BPS analysis
- **`fpl_strategy.py`** - Team building, transfer planning, chip strategy, and season planning
- **`Fpl_api.py`** - FPL API integration for live data
- **`FPL_Advanced_Metrics_Demo.ipynb`** - Interactive demonstration notebook

### Techniques from Popular FPL Content Creators

This toolkit implements strategies from:

- 📺 **FPL Focal** - xGI analysis, underlying stats
- 📺 **Let's Talk FPL** - Captain picks, weekly planning
- 📺 **FPL Wire** - Differential strategy, template teams
- 📺 **FPL General** - Fixture analysis
- 📺 **FPL BlackBox** - Advanced metrics, ROI
- 📺 **FPL Raptor** - Bonus point focus

---

## 📊 Complete Metrics List

### General Metrics (All Positions)

| # | Metric | Description | Used By |
|---|--------|-------------|---------|
| 1 | **Points per Million (PPM)** | Value efficiency - total points divided by cost | FPL Wire, All creators |
| 2 | **Form Index** | Weighted recent performance score | Let's Talk FPL |
| 3 | **xGI per 90** | Expected Goal Involvements (xG + xA) per 90 minutes | FPL Focal, FPL BlackBox |
| 4 | **Bonus Point Potential** | BPS (Bonus Point System) per 90 minutes | FPL Raptor |
| 5 | **Threat Index** | FPL's official threat metric normalized | FPL General |
| 6 | **ROI Metric** | Return on Investment - PPM adjusted for ownership | FPL BlackBox |

### Forward-Specific Metrics (FWD)

| # | Metric | Description | Application |
|---|--------|-------------|-------------|
| 7 | **Shot Quality Score** | xG per 90 - quality of chances | Identify clinical finishers |
| 8 | **Conversion Rate** | Actual goals vs expected goals | Find overperformers |
| 9 | **Penalty Box Threat** | Positional threat in danger areas | Target goal scorers |

### Midfielder-Specific Metrics (MID)

| # | Metric | Description | Application |
|---|--------|-------------|-------------|
| 10 | **Creativity Index** | FPL's creativity metric enhanced | Find assist providers |
| 11 | **xA per 90** | Expected assists per 90 minutes | Underlying playmaking ability |
| 12 | **Goal Involvement** | Combined xG + xA for midfielders | All-round attacking threat |

### Defender-Specific Metrics (DEF)

| # | Metric | Description | Application |
|---|--------|-------------|-------------|
| 13 | **Clean Sheet Probability** | Likelihood of keeping clean sheets | Target defensive assets |
| 14 | **Defensive Quality** | xGC-based rating (lower xGC = better) | Identify strong defenses |
| 15 | **Attacking Threat** | xGI for defenders (goals + assists) | Find attacking fullbacks |

### Goalkeeper-Specific Metrics (GKP)

| # | Metric | Description | Application |
|---|--------|-------------|-------------|
| 16 | **Saves per 90** | Save frequency and volume | High-save keepers (bonus pts) |
| 17 | **xG Prevented** | Performance vs expected (xGC - actual GC) | Overperforming keepers |
| 18 | **Clean Sheet Percentage** | CS rate over season | Reliable clean sheet options |

### Strategic Metrics

| # | Metric | Description | Application |
|---|--------|-------------|-------------|
| 19 | **Captain Score** | Multi-factor captaincy analysis | Weekly captain picks |
| 20 | **Differential Score** | Low-owned high-value players | Rank climbing strategy |
| 21 | **Form vs Fixture** | Current form + upcoming fixtures | Transfer planning |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd FPL

# Install dependencies
pip install pandas numpy matplotlib seaborn requests
```

### Basic Usage

```python
from Fpl_api import FPLapi_main_endpoint, players
from advanced_metrics import AdvancedMetrics

# Load FPL data
fpl_data = FPLapi_main_endpoint()
players_df = players(fpl_data)

# Initialize metrics calculator
metrics = AdvancedMetrics(players_df)

# Get comprehensive analysis
analysis = metrics.get_comprehensive_analysis()

# Find top players by xGI
top_xgi = analysis.nlargest(20, 'xgi_per_90')
print(top_xgi[['web_name', 'position', 'xgi_per_90', 'points_per_million']])

# Get captain picks
captains = metrics.calculate_captain_score()
print(captains.head(10))

# Find differentials (low ownership gems)
diffs = metrics.find_differentials(max_ownership=10.0)
print(diffs)
```

### Position-Specific Analysis

```python
# Analyze forwards
forwards = metrics.calculate_forward_metrics()
print(forwards.nlargest(10, 'forward_score'))

# Analyze midfielders
midfielders = metrics.calculate_midfielder_metrics()
print(midfielders.nlargest(10, 'midfielder_score'))

# Analyze defenders
defenders = metrics.calculate_defender_metrics()
print(defenders.nlargest(10, 'defender_score'))

# Analyze goalkeepers
goalkeepers = metrics.calculate_goalkeeper_metrics()
print(goalkeepers.nlargest(5, 'goalkeeper_score'))
```

### Team Building

```python
from fpl_strategy import FPLStrategy

strategy = FPLStrategy(players_df)

# Build optimal team
team = strategy.build_optimal_team(
    budget=100.0,
    formation="3-4-3",
    strategy="balanced"  # or "template", "differential", "premium_heavy"
)

print(f"Total cost: £{team['total_cost']}m")
for player in team['starters']:
    print(f"{player['name']} ({player['position']}) - £{player['cost']}m")
```

### Transfer Planning

```python
# Your current team (replace with actual players)
current_team = ['Salah', 'Haaland', 'Saka', 'Watkins', ...]

# Get transfer suggestions
suggestions = strategy.analyze_transfer_targets(
    current_team=current_team,
    budget=2.0,  # £2.0m in the bank
    free_transfers=1,
    gameweeks_ahead=5
)

for suggestion in suggestions[:5]:
    print(f"{suggestion.player_out} → {suggestion.player_in}")
    print(f"  Expected gain: {suggestion.expected_points_gain:.1f} pts")
    print(f"  Reason: {suggestion.reason}\n")
```

### Chip Strategy

```python
# Wildcard planning
current_gw = 15
wc_plan = strategy.wildcard_planning(current_gw)
print(f"Recommended: {wc_plan['recommended']}")
print(f"Strategy: {wc_plan['strategy']}")

# Bench Boost planning
bb_plan = strategy.bench_boost_planner(upcoming_dgw=26)
print(bb_plan)

# Triple Captain analysis
tc_plan = strategy.triple_captain_analysis(captain_picks)
print("Top TC targets:", tc_plan['top_targets'][:3])

# Free Hit strategy
fh_plan = strategy.free_hit_strategy(current_gw)
print(fh_plan['strategy'])
```

---

## 📓 Interactive Notebook

Open `FPL_Advanced_Metrics_Demo.ipynb` for a complete interactive demonstration:

```bash
jupyter notebook FPL_Advanced_Metrics_Demo.ipynb
```

The notebook includes:
- ✅ All 20+ metrics with examples
- ✅ Visualizations (scatter plots, box plots)
- ✅ Position-specific analysis
- ✅ Team building strategies
- ✅ Transfer planning
- ✅ Chip strategy guide
- ✅ Season planning
- ✅ Mini-league strategy
- ✅ Weekly checklists

---

## 🎯 Strategy Guides

### 1. Team Building Strategies

#### Balanced Strategy
- Mix of premium and budget options
- Good for season-long stability
- Recommended for most managers

```python
team = strategy.build_optimal_team(strategy="balanced")
```

#### Template Strategy
- High ownership core
- Safe picks, reduce variance
- Good for protecting leads

```python
team = strategy.build_optimal_team(strategy="template")
```

#### Differential Strategy
- Low ownership focus
- High risk, high reward
- Good for chasing in mini-leagues

```python
team = strategy.build_optimal_team(strategy="differential")
```

#### Premium Heavy
- Triple premium + budget enablers
- Star-driven approach
- Popular in good fixture periods

```python
team = strategy.build_optimal_team(strategy="premium_heavy")
```

### 2. Chip Usage Timeline

#### First Wildcard (GW 8-10)
- Fix early mistakes
- Set up for first favorable fixture run
- Don't panic - wait for right moment

#### Second Wildcard (GW 16-18 or 25-27)
**GW 16-18**: Pre-holiday fixtures, target DGWs
**GW 25-27**: Post-January transfers, final run-in

#### Bench Boost (Double Gameweek)
- Ensure all 15 players have 2 fixtures
- Build team 1-2 GWs before
- Expected return: 20-40 points

#### Triple Captain (Double Gameweek)
- Premium player (Salah, Haaland, etc.)
- 2 favorable fixtures
- Strong recent form (xGI > 0.8)

#### Free Hit (Blank Gameweeks)
- Typical GWs: 29, 33
- Don't worry about team value
- Maximize playing players

### 3. Weekly Routine

1. **Monday-Tuesday**: Review previous GW performance
2. **Wednesday**: Check press conferences for injuries
3. **Thursday**: Analyze underlying stats (xG, xA)
4. **Friday**: Identify transfer targets
5. **Saturday**: Plan captaincy
6. **Saturday evening**: Make transfers (after final pressers)
7. **Before deadline**: Double-check team, bench order

### 4. Mini-League Strategy

#### If Leading (Top 25%)
- **Defensive approach**
- Template core + 1-2 differentials
- Safe captain picks
- Preserve rank

#### If Contending (25-50%)
- **Balanced approach**
- Mix template and differentials
- Calculated risks
- Build value

#### If Chasing (50%+)
- **Aggressive approach**
- High differentials
- Risky captains
- Take calculated hits

---

## 📈 Understanding Key Metrics

### xG (Expected Goals)
- Probability a shot will result in a goal
- Based on shot location, assist type, angle
- **Good xG**: >0.5 per 90 (forwards), >0.3 per 90 (mids)

### xA (Expected Assists)
- Probability a pass leads to a goal
- Based on pass type and shot quality
- **Good xA**: >0.3 per 90 (midfielders)

### xGI (Expected Goal Involvements)
- xG + xA combined
- Best measure of attacking threat
- **Good xGI**: >0.8 per 90 (attackers)

### BPS (Bonus Point System)
- FPL's algorithm for bonus points
- 32+ BPS = 3 bonus, 24-31 = 2 bonus, 18-23 = 1 bonus
- **Good BPS**: >30 per 90

### Points per Million (PPM)
- Total points ÷ (cost in £m)
- Best value metric
- **Good PPM**: >5.0 (budget), >4.0 (premium)

---

## 🎓 Advanced Techniques

### 1. Fixture Swing Analysis
Identify when teams' fixtures change from hard to easy:

```python
from advanced_metrics import FixtureAnalysis

fixture_analysis = FixtureAnalysis(fixtures_df, teams_df)
best_runs = fixture_analysis.find_best_fixture_runs(games=5)
print(best_runs)
```

### 2. Value Building
Maximize team value over the season:

```python
value_tips = strategy.optimize_team_value(current_team)
print(value_tips['price_rise_candidates'])
```

### 3. Bonus Point Hunting
Target bonus point magnets:

```python
from fpl_strategy import BonusPredictor

predictor = BonusPredictor(players_df)
bonus_predictions = predictor.predict_bonus_potential()
print(bonus_predictions.head(20))
```

### 4. Form vs Fixtures
Combine current form with upcoming fixtures:

```python
form_fixture = metrics.calculate_form_vs_fixture()
print(form_fixture.head(20))
```

---

## 📦 Module Reference

### AdvancedMetrics Class

```python
from advanced_metrics import AdvancedMetrics

metrics = AdvancedMetrics(players_df)
```

**Methods:**
- `calculate_points_per_million()` - PPM calculation
- `calculate_xgi_per_90()` - xGI per 90
- `calculate_bonus_point_potential()` - BPS per 90
- `calculate_forward_metrics()` - Forward-specific
- `calculate_midfielder_metrics()` - Midfielder-specific
- `calculate_defender_metrics()` - Defender-specific
- `calculate_goalkeeper_metrics()` - GKP-specific
- `calculate_captain_score()` - Captain analysis
- `find_differentials()` - Low-owned gems
- `get_comprehensive_analysis()` - All metrics combined
- `export_all_metrics()` - Export to DataFrames

### FPLStrategy Class

```python
from fpl_strategy import FPLStrategy

strategy = FPLStrategy(players_df)
```

**Methods:**
- `build_optimal_team()` - Team building
- `analyze_transfer_targets()` - Transfer suggestions
- `wildcard_planning()` - When to wildcard
- `bench_boost_planner()` - BB strategy
- `triple_captain_analysis()` - TC timing
- `free_hit_strategy()` - FH usage
- `mini_league_strategy()` - ML tactics

### GameweekPlanner Class

```python
from fpl_strategy import GameweekPlanner

planner = GameweekPlanner(current_gw=15)
```

**Methods:**
- `create_season_plan()` - Full season chip planning
- `weekly_checklist()` - Pre-deadline routine

---

## 🔍 Common Questions

### Q: Which metrics should I prioritize?

**For attacking players:**
1. xGI per 90 (underlying threat)
2. Points per Million (value)
3. Form (recent performance)
4. BPS per 90 (bonus potential)

**For defenders:**
1. Clean Sheet Probability
2. Defensive Quality (low xGC)
3. Attacking Threat (for fullbacks)
4. Points per Million

### Q: How do I find differential players?

```python
# Low ownership (<10%), decent points (>30)
diffs = metrics.find_differentials(max_ownership=10.0, min_points=30)
```

Look for:
- High xGI but low ownership
- Good fixtures coming up
- Playing for strong teams
- Nailed starters (high minutes)

### Q: When should I take a hit (-4 points)?

Only when:
- Expected points gain > 4-5 points
- Avoiding price drops on multiple players
- Fixture swing is dramatic
- Player is injured/suspended

General rule: **Avoid hits unless essential**

### Q: Best formations?

Popular formations:
- **3-4-3**: Balanced, good for premium forwards
- **3-5-2**: Midfielder-heavy, flexible
- **4-4-2**: Defensive, budget forwards
- **4-3-3**: Attacking, requires premium forwards

Match formation to your team structure and budget.

---

## 📚 Resources

### FPL Official
- [FPL Website](https://fantasy.premierleague.com/)
- [FPL API](https://fantasy.premierleague.com/api/)

### Popular FPL Content Creators
- FPL Focal - Advanced stats focus
- Let's Talk FPL - Weekly planning
- FPL Wire - Community updates
- FPL General - Fixture analysis
- FPL BlackBox - Data-driven
- FPL Raptor - Bonus points

### External Data Sources
- FPL Statistics (price predictions)
- Understat (xG data)
- FBref (advanced stats)

---

## 🤝 Contributing

Contributions welcome! Ideas for new metrics:
- Progressive carries analysis
- Underlying defensive stats
- Set piece threat
- Rotation risk prediction
- Historical fixture difficulty

---

## 📝 License

This project is for educational purposes. FPL data belongs to the Premier League.

---

## 🎉 Good Luck!

May your xG be high, your differentials haul, and your captain never blank!

**Happy FPLing! ⚽🏆**

---

## Version History

### v1.0 (Current)
- ✅ 20+ advanced metrics
- ✅ Position-specific analysis
- ✅ Team building strategies
- ✅ Transfer planning
- ✅ Chip strategy
- ✅ Season planning
- ✅ Interactive notebook

### Upcoming Features
- [ ] Fixture difficulty matrix
- [ ] Rotation risk prediction
- [ ] Set piece analysis
- [ ] Historical performance comparisons
- [ ] Machine learning price predictions
- [ ] Automated weekly reports
