# 🚀 Quick Start Guide - FPL Dashboard

## ⚡ Get Started in 3 Steps

### 1️⃣ Install Dependencies

```bash
cd /home/user/FPL
pip install -r requirements.txt
```

### 2️⃣ Run the App

```bash
streamlit run app.py
```

### 3️⃣ Open Browser

The app will automatically open at: **http://localhost:8501**

---

## 🎯 What You Can Do

### 🔍 Player Comparison
Compare up to **4 players** with:
- Statistical tables
- Radar charts
- Bar graphs
- AI recommendations
- Position-specific stats

**Example Use**: "Should I pick Salah or Palmer?"

### ⚽ Team Builder
Build your FPL team with:
- **£100m budget** tracking
- **Position limits** (2-5-5-3)
- **Max 3 per team** rule
- Formation visualization
- Real-time validation

**Example Use**: "Build my starting XI for GW1"

### 📊 Advanced Analytics
Analyze with **20+ metrics**:
- xG (Expected Goals)
- xA (Expected Assists)
- PPM (Points per Million)
- BPS (Bonus Points)
- Captain picks
- Differentials
- Value analysis

**Example Use**: "Who are the best value midfielders?"

---

## 💡 Quick Tips

### Finding Value Players
1. Go to **Advanced Analytics**
2. Select **Value Analysis**
3. Filter by position
4. Set price range (e.g., £5-7m)
5. Sort by PPM

### Building a Team
1. Go to **Team Builder**
2. Select formation (e.g., 3-4-3)
3. Use tabs to add players per position
4. Watch budget gauge
5. Validate team (must be green!)

### Comparing Players
1. Go to **Player Comparison**
2. Filter by position
3. Select 2-4 players
4. View radar chart
5. Check AI recommendation

---

## 🎮 Controls

- **Sidebar**: Navigation and filters
- **Tabs**: Different views
- **Buttons**: Add/Remove players
- **Sliders**: Adjust thresholds
- **Dropdowns**: Select options
- **R Key**: Refresh data

---

## 📱 Features at a Glance

| Feature | Description | Page |
|---------|-------------|------|
| 👥 Player Cards | Visual player info | Comparison |
| 💰 Budget Gauge | Real-time budget | Team Builder |
| 📊 Radar Charts | Multi-metric comparison | Comparison |
| ⚽ Pitch View | Team formation visual | Team Builder |
| 📈 xG Analysis | Expected goals stats | Analytics |
| 💎 Differentials | Low-owned gems | Analytics |
| 👑 Captains | Best captain picks | Analytics |
| 🎁 Bonus Points | BPS predictions | Analytics |

---

## 🔥 Pro Tips

1. **Set Filters Early**: Narrow results by position/team
2. **Use Minimum Minutes**: Filter out non-starters (>300 mins)
3. **Check Form**: Recent form often > total points
4. **Budget Smart**: Leave £1m for transfers
5. **Balance Team**: Mix premiums + value picks
6. **Differentials**: Use for mini-league chasing
7. **Export Data**: Save comparisons for reference

---

## 🐛 Troubleshooting

**App won't start?**
```bash
pip install --upgrade streamlit pandas plotly
```

**No data showing?**
- Check internet connection
- FPL API might be updating
- Refresh page (press R)

**Charts not loading?**
- Use Chrome/Firefox
- Disable ad blockers
- Clear browser cache

---

## 📖 Full Documentation

See **UI_GUIDE.md** for complete documentation (500+ lines)

---

## 🎉 You're Ready!

```bash
streamlit run app.py
```

**Happy FPLing! ⚽🏆**
