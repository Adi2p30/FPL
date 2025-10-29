# FPL Next.js Frontend - EA FC Style

## 🎮 Tech Stack

- **Frontend**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with EA FC game theme
- **Backend**: FastAPI (Python)
- **API**: FPL Official API
- **AI Assistant**: Google Gemini Pro LLM

## 🎨 Design Theme

### Colors (EA FC / Premier League)
- **Primary Purple**: #37003c (FPL official)
- **Accent Pink**: #e90052 (Premier League)
- **Accent Cyan**: #04f5ff (Gaming accent)
- **Background**: #0a0a0b (Dark mode)
- **Card**: #12121a (Subtle elevation)

### UI Style
- **Small, subtle buttons** (not heavily rounded)
- **Dark mode** with glow effects
- **Smooth animations** and transitions
- **EA FC-inspired** typography and layout
- **Gradient accents** on interactive elements

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home page
│   ├── globals.css          # EA FC styles
│   ├── team-import/         # Team import feature
│   ├── team-builder/        # Team builder with editor
│   ├── famous-teams/        # YouTuber teams
│   └── compare/             # Player comparison
├── components/
│   ├── Navigation.tsx       # Top nav with EA FC style
│   ├── TeamImportModal.tsx  # Import by ID/URL
│   ├── PlayerCard.tsx       # Player cards (pitch style)
│   ├── FormationView.tsx    # FIFA-style pitch
│   ├── FamousManagerCard.tsx # YouTuber team cards
│   └── StatsDisplay.tsx     # Stat boxes
├── lib/
│   ├── api.ts               # Backend API client
│   └── utils.ts             # Helper functions
└── package.json
```

## 🚀 Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Variables

**Frontend** - Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend** - Create `backend/.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

### 3. Run Development Server

```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## 🎯 Features

### 1. Team Import
- **Import by Team ID**: Direct FPL team ID input
- **Import by URL**: Paste FPL URL (extracts ID automatically)
- **Gameweek Selection**: Choose specific gameweek
- **Instant Preview**: See team formation immediately

### 2. Famous YouTuber Teams
Pre-loaded teams:
- Andy (Let's Talk FPL)
- FPL Focal
- FPL Harry
- FPL Mate
- FPL Wire
- FPL General
- FPL BlackBox
- FPL Raptor

### 3. Team Editor
- Drag-and-drop player changes
- Real-time budget tracking
- Formation visualization
- Transfer suggestions
- Save multiple versions

### 4. Player Comparison
- Side-by-side stats
- Radar charts with EA FC style
- Position-specific metrics
- xG/xA analysis

### 5. AI Assistant (Gemini-Powered)
- Collapsible chat interface (bottom-right)
- Context-aware responses about your team
- Understands all 30+ metrics
- Can explain features and strategies
- Quick action buttons for common queries
- Team analysis and transfer suggestions

## 🎨 UI Components

### Button Styles (EA FC)
```tsx
<button className="btn btn-primary btn-sm">
  Primary Action
</button>
```

Variants:
- `btn-primary`: Gradient pink/purple glow
- `btn-secondary`: Outlined with hover glow
- `btn-ghost`: Transparent with subtle hover
- `btn-sm`: Small, compact (main style)

### Card Styles
```tsx
<div className="card card-hover card-glow">
  Content
</div>
```

Features:
- Dark background with subtle border
- Glow effect on hover
- Smooth animations
- Gradient overlays

### Player Cards (Pitch Style)
```tsx
<div className="player-card player-card-selected">
  <div className="badge badge-mid">MID</div>
  <div className="stat-value">150</div>
  <div className="stat-label">Points</div>
</div>
```

## 🔌 API Integration

### Backend Connection

```typescript
import { importTeam, getFamousTeams } from '@/lib/api';

// Import team
const team = await importTeam(123456);

// Get famous teams
const famousTeams = await getFamousTeams();
```

### Available Endpoints

**Players**:
- `GET /api/players` - All players
- `GET /api/players/:id` - Single player

**Teams**:
- `POST /api/team/import` - Import team
- `GET /api/team/:id` - Get team data
- `GET /api/team/:id/picks` - Team picks for GW

**Famous**:
- `GET /api/famous-managers` - List of YouTubers
- `GET /api/famous-teams` - All YouTuber teams

**Metrics**:
- `GET /api/metrics/comprehensive` - All metrics
- `GET /api/metrics/captains` - Captain picks
- `GET /api/metrics/differentials` - Low-owned gems

**AI Assistant**:
- `POST /api/ai/chat` - Chat with AI assistant
- `GET /api/ai/help/{page}` - Get page-specific help
- `POST /api/ai/analyze-team` - Analyze team composition
- `POST /api/ai/transfer-suggestions` - Get transfer recommendations
- `GET /api/ai/explain-metric/{metric}` - Explain specific metrics
- `POST /api/ai/reset` - Reset chat history

## 💻 Development

### Running Backend

```bash
cd backend
pip install -r requirements.txt
# OR manually:
# pip install fastapi uvicorn requests pandas numpy google-generativeai

# Create .env file with your Gemini API key
# GEMINI_API_KEY=your_key_here

uvicorn main:app --reload
```

Backend runs on `http://localhost:8000`

### Running Frontend

```bash
cd frontend
npm run dev
```

### Building for Production

```bash
npm run build
npm start
```

## 🎮 Key Features Implemented

### 1. Team Import Modal
- Input: Team ID or URL
- Validation: Real-time
- Preview: Instant team display
- Error handling: User-friendly messages

### 2. Formation View (FIFA Style)
- Dark green pitch
- Position-based layout
- Player avatars with stats
- Captain indicator
- Bench visualization

### 3. Famous Teams Gallery
- Grid of YouTuber cards
- Click to load team
- Real-time data fetch
- Manager info display

### 4. Team Editor
- Click player to replace
- Filter by position/price
- Budget tracker (live)
- Save changes
- Export team

## 🎨 Styling Guide

### Colors Usage

**Primary Actions**:
```css
bg-gradient-to-r from-primary to-accent-pink
```

**Hover Effects**:
```css
hover:shadow-glow-sm hover:scale-105
```

**Badges**:
- GKP: Yellow `badge-gkp`
- DEF: Blue `badge-def`
- MID: Green `badge-mid`
- FWD: Red `badge-fwd`

### Typography

**Headers**:
```tsx
<h1 className="text-3xl font-bold text-glow">
  FPL Analytics
</h1>
```

**Stats**:
```tsx
<div className="stat-value">150</div>
<div className="stat-label">Points</div>
```

### Animations

**Fade In**:
```css
animate-fade-in
```

**Glow Pulse**:
```css
animate-glow
```

**Slide Up**:
```css
animate-slide-up
```

## 📱 Responsive Design

- Desktop: Full features
- Tablet: Adapted layout
- Mobile: Optimized for touch

## 🔧 Customization

### Changing Colors

Edit `tailwind.config.ts`:

```typescript
colors: {
  primary: '#37003c',    // Your primary
  accent: {
    pink: '#e90052',     // Your pink
  }
}
```

### Adding Animations

Edit `globals.css`:

```css
@keyframes yourAnimation {
  from { ... }
  to { ... }
}
```

## 🐛 Troubleshooting

**Backend not connecting**:
- Check if backend is running on port 8000
- Verify CORS settings in `backend/main.py`
- Check `.env.local` API_URL

**Styles not loading**:
- Run `npm run dev` again
- Clear browser cache
- Check Tailwind config

**Team import failing**:
- Verify team ID is correct
- Check FPL API status
- Try with a famous team first

## 📊 Performance

- API responses cached (1 hour)
- Images lazy-loaded
- Components code-split
- Optimized bundle size

## 🎯 Next Steps

1. Start backend: `uvicorn backend.main:app --reload`
2. Start frontend: `npm run dev`
3. Open `http://localhost:3000`
4. Import a team or browse famous teams
5. Compare players and build teams

## 🌟 Features Highlight

✅ **Team Import**: By ID or URL
✅ **Famous Teams**: 8 YouTubers pre-loaded
✅ **Team Editor**: Real-time editing with save/load
✅ **30+ Metrics**: PPM, xGI, form ratings, buy/sell scores
✅ **Player Comparison**: Multi-select side-by-side comparison
✅ **AI Assistant**: Gemini-powered chat for help and analysis
✅ **EA FC Style**: Dark mode, pink/purple theme
✅ **Small Buttons**: Subtle, not rounded
✅ **Smooth Animations**: Game-like feel
✅ **Live Data**: FPL API integration
✅ **Backend API**: FastAPI with Python

Enjoy your EA FC-styled FPL dashboard with AI assistant! ⚽🎮🤖
