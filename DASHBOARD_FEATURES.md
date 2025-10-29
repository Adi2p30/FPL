# 🎮 FPL Dashboard - Complete Feature Guide

## 🚀 Quick Start

```bash
# Terminal 1: Backend
cd backend && python -m uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

**Access Dashboard**: http://localhost:3000/dashboard

---

## 📊 Dashboard Overview

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        HEADER (Sticky)                          │
│                    FPL DASHBOARD                                │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┬────────────────────────────┐
│                                  │    RIGHT SIDEBAR           │
│   MY TEAM (CENTER - PITCH VIEW)  │    ┌──────────────────┐   │
│                                  │    │  Team Stats      │   │
│   ┌────────────────────────┐     │    │  - Players: X/15 │   │
│   │  Team Name + Formation │     │    │  - Budget: £XXm  │   │
│   │  Budget: £XX.Xm / £100m│     │    │  - Remaining:£X  │   │
│   └────────────────────────┘     │    └──────────────────┘   │
│                                  │                            │
│   ┌────────────────────────┐     │    ┌──────────────────┐   │
│   │   PITCH (11 PLAYERS)   │     │    │  Quick Filters   │   │
│   │    [P] [P] [P] [P]     │     │    │  - In Form       │   │
│   │    [P] [P] [P] [P]     │     │    │  - Differentials │   │
│   │    [P] [P] [P]         │     │    │  - Captains      │   │
│   └────────────────────────┘     │    │  - Value         │   │
│                                  │    └──────────────────┘   │
│   [Save] [Load] [Clear]          │                            │
│                                  │    ┌──────────────────┐   │
├──────────────────────────────────┤    │ Position Breakdown│   │
│                                  │    │  GKP: X  DEF: X  │   │
│  PLAYER DATABASE                 │    │  MID: X  FWD: X  │   │
│  ┌────────────────────────────┐  │    └──────────────────┘   │
│  │ [Players] [Metrics] [Compare]│ │                            │
│  └────────────────────────────┘  │                            │
│                                  │                            │
│  ┌─────────────────────────────┐ │                            │
│  │  SEARCHABLE TABLE           │ │                            │
│  │  □ Player | Pos | Cost | Pts│ │                            │
│  │  □ Salah  | MID | £13  | 150│ │                            │
│  │  ...                        │ │                            │
│  └─────────────────────────────┘ │                            │
└──────────────────────────────────┴────────────────────────────┘
```

---

## 🎯 Core Features

### 1. Team Building (Center Section)

**Pitch Display**:
- FIFA-style green pitch background
- Grid layout for 11 starters
- Player initials in colored circles
- Click ✕ to remove player
- Formation display (3-4-3, etc.)

**Team Management**:
```
✅ Add players from table (+ button)
✅ Remove players from pitch (✕ button)
✅ Max 15 players enforced
✅ Budget validation (£100m total)
✅ Real-time cost calculation
✅ Position breakdown tracking
```

**Save/Load Functionality**:
```typescript
// Save team to JSON
{
  name: "My Team",
  formation: "3-4-3",
  players: [1, 2, 3, ...],  // Player IDs
  budget: 100,
  created_at: "2025-01-22T...",
  gameweek: 20
}
```

**Actions**:
- 💾 **Save Team**: Downloads JSON file
- 📂 **Load Team**: Upload JSON to restore team
- 🗑️ **Clear**: Remove all players

---

### 2. Player Database (3 Tabs)

#### Tab 1: Players

**Columns**:
```
Select | Player | Pos | Cost | Pts | Form | Own% | Action
────────────────────────────────────────────────────────
  □    Salah    MID  £13.0m 150   8.2   35%    [+]
  □    Haaland  FWD  £14.0m 145   7.8   50%    [+]
  ...
```

**Features**:
- ✅ Checkbox multi-select for comparison
- ✅ Position badges (color-coded)
- ✅ Add to team button (+)
- ✅ Disabled if team full or already selected
- ✅ Hover effects on rows
- ✅ Scrollable table

#### Tab 2: Enhanced Metrics

**Columns**:
```
Player  | PPM  | Form | xGI | Score | Buy | Capt
──────────────────────────────────────────────────
Salah   | 11.5 | 8.2  |0.85 |  95   | 92  | 88
Haaland | 10.4 | 7.8  |1.2  |  98   | 95  | 95
...
```

**Metrics Explained**:
- **PPM**: Points per Million (value efficiency)
- **Form**: Current form rating (0-10)
- **xGI**: Expected Goal Involvements per 90
- **Score**: Overall score (0-100)
- **Buy**: Transfer IN recommendation score
- **Capt**: Captain selection score

**All 30+ Metrics Available**:
1. PPM (Points per Million)
2. Value Score
3. Form Rating (0-10)
4. Momentum
5. Consistency
6. xGI per 90
7. Expected Points
8. Overperformance
9. Minutes per Point
10. Goal Involvement
11. Bonus Frequency
12. Transfer Priority
13. Captain Score
14. Differential Score
15. Threat Rating (0-10)
16. Creativity Rating (0-10)
17. Influence Rating (0-10)
18. ROI (Return on Investment)
19. Value Rank
20. Overall Score (0-100)
21. Buy Score
22. Hold Score
23. Sell Score
24. FDR Next 5
25. Fixture Adjusted Score
26. ...and more!

#### Tab 3: Compare

**Features**:
- Shows selected players (checkbox selections)
- Side-by-side comparison cards
- Key metrics displayed:
  - Cost, Points, Form
  - PPM, Overall Score, Buy Score
  - All enhanced metrics
- ✕ button to remove from comparison
- Responsive grid (1-3 columns)

---

### 3. Right Sidebar (Sticky)

#### Team Stats Card
```
Players:     12/15
Budget:      £95.5m / £100m  ✅
Remaining:   £4.5m
```

Colors:
- Green: Under budget
- Red: Over budget

#### Quick Filters
```
🔥 In Form        - Top form players
💎 Differentials  - Low ownership
👑 Captains       - Best captain picks
💰 Value          - High PPM players
```

#### Position Breakdown
```
GKP: 2  (Yellow badge)
DEF: 5  (Blue badge)
MID: 3  (Green badge)
FWD: 2  (Red badge)
```

---

## 💾 Save/Load Team Feature

### How to Save Team

1. Build your 15-player team
2. Click **💾 Save Team** button
3. JSON file downloads: `My-FPL-Team.json`
4. Store file for later use

**JSON Structure**:
```json
{
  "name": "My FPL Team",
  "formation": "3-4-3",
  "players": [
    1, 2, 3, 14, 25, 36, 47, 58, 69, 70,
    81, 92, 103, 114, 125
  ],
  "budget": 100,
  "created_at": "2025-01-22T10:30:00.000Z",
  "gameweek": 20
}
```

### How to Load Team

1. Click **📂 Load Team** button
2. Select your `.json` file
3. Team automatically loads:
   - Player selections restored
   - Formation set
   - Budget configured
   - Team name displayed

### Use Cases

✅ **Save multiple teams**: Try different strategies
✅ **Plan ahead**: Save teams for future gameweeks
✅ **Share with friends**: Export and share JSON
✅ **Backup**: Don't lose your team planning
✅ **Compare setups**: Load different teams to compare

---

## 📊 Metrics Deep Dive

### Decision-Making Metrics

#### 1. Overall Score (0-100)
```
Calculation:
= (Form Rating × 30%) +
  (Value Score × 40%) +
  (xGI × 30%)

Usage:
- Quick player ranking
- General performance indicator
- 90+ = Elite
- 70-90 = Good
- <70 = Avoid
```

#### 2. Buy Score
```
Calculation:
= (Transfer Priority × 40%) +
  (Value Score × 30%) +
  (Expected Points × 30%)

Usage:
- Which players to transfer IN
- Higher = better buy
- Filter by position
- Sort by Buy Score
```

#### 3. Captain Score
```
Calculation:
= (Form × 4) +
  (xGI × 8) +
  (Consistency) +
  (Nailed Bonus)

Usage:
- Weekly captain picks
- Reliable performers
- High ceiling players
- Sort by Captain Score
```

#### 4. Differential Score
```
Calculation:
= ((100 - Ownership) × 30%) +
  (PPM × 40%) +
  (Form × 30%)

Usage:
- Find low-owned gems
- Rank climbing strategy
- Mini-league differentials
- Filter: Ownership <10%
```

### Performance Metrics

#### PPM (Points per Million)
```
Formula: Total Points ÷ (Cost in £m)

Example:
Player: Salah
Points: 150
Cost: £13.0m
PPM: 150 ÷ 13 = 11.5

Good PPM:
>5.0 (Budget players)
>4.0 (Premium players)
```

#### xGI per 90
```
Formula: (xG + xA) per 90 minutes

Example:
xG per 90: 0.60
xA per 90: 0.25
xGI per 90: 0.85

Good xGI:
>0.8 (Attackers)
>0.4 (Midfielders)
```

#### Form Rating (0-10)
```
Formula: Current form normalized to 0-10 scale

Rating Guide:
9-10: Exceptional
7-9:  Great
5-7:  Good
3-5:  Average
<3:   Poor
```

---

## 🎮 How to Use the Dashboard

### Workflow 1: Build a New Team

1. **Browse Players Tab**
   - Sort by cost, points, form
   - Check position badges

2. **Check Enhanced Metrics**
   - Switch to Metrics tab
   - Look at Overall Score
   - Find high Buy Score players

3. **Add to Team**
   - Click + button on players
   - Watch budget in sidebar
   - Fill all positions

4. **Review on Pitch**
   - See team formation
   - Check position distribution
   - Verify budget remaining

5. **Save Team**
   - Click 💾 Save Team
   - Download JSON file
   - Store for later

### Workflow 2: Compare Players

1. **Select Players**
   - Click checkboxes in Players tab
   - Select 2-4 players

2. **Switch to Compare Tab**
   - View side-by-side cards
   - Check all metrics
   - Compare key stats

3. **Make Decision**
   - Look at Overall Score
   - Check Buy Score
   - Consider cost difference

4. **Add Best Pick**
   - Click + on best option
   - Remove from comparison

### Workflow 3: Find Differentials

1. **Enhanced Metrics Tab**
   - Sort by Differential Score
   - Look for <10% ownership

2. **Check Form & Value**
   - Ensure good Form Rating
   - High PPM is bonus

3. **Add to Team**
   - Pick 2-3 differentials
   - Balance with template

### Workflow 4: Plan Multiple Teams

1. **Build Team #1**
   - Standard template team
   - Save as `template-team.json`

2. **Build Team #2**
   - Differential strategy
   - Save as `differential-team.json`

3. **Build Team #3**
   - Premium-heavy
   - Save as `premium-team.json`

4. **Load & Compare**
   - Load each JSON
   - Check total points potential
   - Choose best strategy

---

## 🔥 Quick Tips

### Finding Value Players
1. Sort by **PPM** in Metrics tab
2. Filter budget: £4.5-7.0m
3. Check **Form Rating** > 6
4. Look at **xGI** > 0.3
5. Add to team if good fixtures

### Captain Picks Weekly
1. Sort by **Captain Score**
2. Top 3-5 options
3. Check ownership (high = safe, low = risky)
4. Consider fixtures
5. Choose based on strategy

### Transfer Planning
1. Sort by **Buy Score**
2. Set max cost = your budget
3. Filter by position needed
4. Compare with current player
5. Transfer if score difference >10

### Differential Hunting
1. Filter **Ownership** <10%
2. Sort by **Differential Score**
3. Min points: 30+
4. Check **Form Rating**
5. Add 2-3 to team

---

## 🎨 UI Elements

### Color Coding

**Positions**:
- 🟡 GKP (Yellow)
- 🔵 DEF (Blue)
- 🟢 MID (Green)
- 🔴 FWD (Red)

**Values**:
- 🟢 Green: Good/Under budget
- 🔴 Red: Bad/Over budget
- 🟣 Pink/Purple: Key scores
- ⚪ White: Neutral

**Interactive**:
- Hover: Glow effect
- Active: Border highlight
- Disabled: Gray, no interaction

### Buttons

**Primary** (Gradient pink/purple):
```tsx
<button className="btn btn-primary btn-sm">
  Import Team
</button>
```

**Secondary** (Outlined):
```tsx
<button className="btn btn-secondary btn-sm">
  Quick Filter
</button>
```

**Ghost** (Transparent):
```tsx
<button className="btn btn-ghost btn-sm">
  Clear
</button>
```

---

## 📱 Responsive Design

**Desktop (1200px+)**:
- 3-column layout
- Full sidebar
- Wide tables

**Tablet (768-1200px)**:
- 2-column layout
- Collapsed sidebar
- Scrollable tables

**Mobile (<768px)**:
- Single column
- Stacked cards
- Touch-optimized buttons

---

## 🔌 API Integration

### Frontend → Backend Flow

```
Frontend Request:
GET /api/enhanced/all-metrics
         ↓
Backend Processing:
1. Fetch FPL data
2. Create EnhancedMetrics instance
3. Calculate 30+ metrics
4. Return JSON
         ↓
Frontend Display:
- Populate tables
- Enable comparisons
- Show in metrics tab
```

### Available Endpoints

```
GET  /api/enhanced/all-metrics           - All metrics
GET  /api/enhanced/top-picks?position=3  - Top midfielders
GET  /api/enhanced/transfers-in?max_cost=10 - Budget options
GET  /api/enhanced/differentials?max_ownership=5 - Rare gems
POST /api/enhanced/compare [1,2,3]       - Compare players
GET  /api/enhanced/metric-descriptions   - Metric info
```

---

## 🚀 Performance

- **Initial Load**: ~2-3 seconds
- **Metric Calculations**: ~1-2 seconds
- **Table Rendering**: Instant
- **Save/Load**: <100ms
- **Comparison**: Instant

**Optimizations**:
- Load top 100 players initially
- Lazy load more on scroll
- Cache metric calculations
- Debounced search/filter

---

## 🎯 Summary

### What You Can Do

✅ **Build Teams**: 15-player squads with budget
✅ **Save/Load**: Export and import teams as JSON
✅ **Compare**: Multi-player side-by-side
✅ **Analyze**: 30+ metrics per player
✅ **Decide**: Overall/Buy/Captain scores
✅ **Filter**: Quick filters for strategies
✅ **Plan**: Multiple team versions

### Key Metrics to Watch

1. **Overall Score** - General ranking
2. **Buy Score** - Transfer targets
3. **Captain Score** - Weekly picks
4. **PPM** - Value efficiency
5. **Form Rating** - Current performance
6. **xGI** - Underlying stats

### Workflows Supported

✅ Team building from scratch
✅ Transfer planning (who to buy)
✅ Captain selection (who to captain)
✅ Differential hunting (rank climbing)
✅ Value finding (budget options)
✅ Multi-team planning (save multiple)

---

**Access Dashboard**: http://localhost:3000/dashboard

**Enjoy planning your FPL success! ⚽🏆**
