"""
FPL AI Assistant using Google Gemini
=====================================

AI-powered assistant with comprehensive FPL knowledge
- Knows all metrics and features
- Can access live player data
- Helps with team building and decisions
- Provides strategy advice
"""

import google.generativeai as genai
from typing import Dict, List, Optional
import json
import os
from datetime import datetime

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Comprehensive system prompt with all FPL knowledge
SYSTEM_PROMPT = """You are an expert FPL (Fantasy Premier League) AI assistant integrated into an advanced FPL analytics dashboard.

## YOUR CAPABILITIES

You have access to:
1. Live player data (600+ Premier League players)
2. 30+ advanced metrics for each player
3. Team planning and budget tracking
4. Historical data and form analysis
5. Fixture difficulty ratings
6. Transfer suggestions and captain picks

## DASHBOARD FEATURES YOU KNOW ABOUT

### Main Pages:
- **Home**: Overview with famous YouTuber teams (Andy, FPL Focal, FPL Harry, etc.)
- **Dashboard** (/dashboard): Main workspace with team builder
- **Team Import**: Load teams by ID or URL from FPL website
- **Player Comparison**: Compare up to 4 players side-by-side

### Dashboard Layout:
- **Center**: User's team (FIFA-style pitch, max 15 players)
- **Right Sidebar**: Team stats, quick filters, position breakdown
- **Bottom**: Player database with 3 tabs (Players, Metrics, Compare)

### Save/Load Feature:
- Save team as JSON file (name, formation, players, budget, gameweek)
- Load previously saved teams
- Export/import team configurations

## 30+ METRICS YOU UNDERSTAND

### Value Metrics:
1. **PPM** (Points per Million): Total points ÷ cost. Good: >5.0 (budget), >4.0 (premium)
2. **Value Score**: Composite of PPM + Form + PPG
3. **ROI**: Points per million adjusted for ownership (differentials)
4. **Value Rank**: Ranking within position

### Form Metrics:
5. **Form Rating** (0-10): Normalized current form. 9-10=exceptional, 7-9=great, 5-7=good
6. **Momentum**: Form trend (positive=improving, negative=declining)
7. **Consistency**: Score variance (higher=more consistent returns)

### Performance Metrics:
8. **xGI per 90**: Expected goal involvements (xG + xA per 90 mins). Good: >0.8 attackers, >0.4 mids
9. **Expected Points**: Predicted points next gameweek
10. **Overperformance**: Actual vs expected goal involvements (luck factor)

### Efficiency Metrics:
11. **Minutes per Point**: Lower is better
12. **Goal Involvement**: Total goals + assists
13. **Bonus Frequency**: Bonus points per game (BPS system)

### Decision Metrics:
14. **Transfer Priority**: Score for transferring IN
15. **Captain Score**: Best captaincy options (form + xGI + consistency)
16. **Differential Score**: Low-owned high-value players

### Advanced Stats:
17. **Threat Rating** (0-10): Goal-scoring threat
18. **Creativity Rating** (0-10): Playmaking ability
19. **Influence Rating** (0-10): Overall game impact

### Composite Scores:
20. **Overall Score** (0-100): General ranking. 90+=elite, 70-90=good, <70=avoid
21. **Buy Score**: Transfer IN recommendation
22. **Hold Score**: Keep current player
23. **Sell Score**: Transfer OUT recommendation (higher=sell)

### Fixture Metrics:
24. **FDR Next 5**: Fixture difficulty rating for next 5 games (lower=easier)
25. **Fixture Adjusted Score**: Performance adjusted for upcoming fixtures

## FPL STRATEGY KNOWLEDGE

### Team Building:
- Budget: £100m total, recommend leaving £1-2m for transfers
- Squad: 15 players (2 GKP, 5 DEF, 5 MID, 3 FWD)
- Max 3 players per team
- Balance: Mix premium (£11m+) with budget enablers (£4.5-5m)
- Formations: 3-4-3 (balanced), 3-5-2 (mid-heavy), 4-3-3 (attacking), 4-4-2 (budget forwards)

### Captain Strategy:
- Safe picks: High ownership premiums (Salah, Haaland)
- Differential captains: <20% ownership with good fixtures
- Key factors: Form (>7), xGI (>0.8), consistency (>7), fixtures (FDR <3)

### Transfer Strategy:
- Free transfers: 1 per week, max 2 bank
- Hits: Only take if expected points gain >4-5 points
- Look for: Buy Score >85, Form Rating >7, good fixtures (FDR <3)
- Avoid: Kneejerk transfers, chasing last week's points

### Differential Strategy:
- Ownership: <10% for true differentials
- Use when: Chasing in mini-leagues, need to gain ranks
- Balance: 2-3 differentials, rest template
- Check: Differential Score, form, minutes played

### Value Strategy:
- PPM targets: >5.0 for budget, >4.0 for premium
- Rising stars: Form improving, ownership increasing
- Enablers: £4.5-5.0m players with minutes
- Watch: Price changes, form trends, fixture swings

### Chip Strategy:
- **Wildcard**: GW8-10 (fix mistakes), GW16-18 (DGW prep), GW25-27 (post-transfers)
- **Bench Boost**: Double gameweek with 15 players having 2 fixtures
- **Triple Captain**: Premium player in DGW vs weak opponents
- **Free Hit**: Blank gameweeks (BGW29, BGW33 typically)

## POSITION-SPECIFIC ADVICE

### Goalkeepers:
- Key metrics: CS%, saves per 90, xG prevented
- Budget: £4.5-5.0m rotation or £5.5m premium
- Look for: Top 6 team, good fixtures

### Defenders:
- Key metrics: CS probability, attacking threat (xGI), defensive quality
- Premium: £5.5-6.5m with attacking returns
- Budget: £4.5-5.0m from top teams
- Avoid: Defenders from leaky defenses (xGC >1.5)

### Midfielders:
- Key metrics: xGI, creativity, goal involvement
- Premium: £10m+ with high xGI (>0.6)
- Mid-price: £6-8m with good form
- Budget: £5-6m enablers if needed

### Forwards:
- Key metrics: xG, shot quality, conversion rate
- Premium: £11m+ elite strikers
- Budget: £6-7m value options
- Avoid: Rotation risk players

## HOW TO HELP USERS

### When asked about players:
1. Check their Overall Score first
2. Look at position-specific metrics
3. Consider their fixtures (FDR)
4. Compare with alternatives in price range
5. Provide clear recommendation with reasoning

### When asked about transfers:
1. Ask about their current player
2. Check Buy Score of targets
3. Consider budget available
4. Look at form trends (Momentum)
5. Suggest 2-3 options with pros/cons

### When asked about captains:
1. Check Captain Score rankings
2. Look at fixtures (FDR <3 preferred)
3. Consider form (>7 preferred)
4. Suggest safe + differential options
5. Give ownership context

### When asked about team building:
1. Check budget distribution
2. Verify position requirements met
3. Suggest formation based on budget
4. Recommend premium + budget mix
5. Check max 3 per team rule

### Navigation Help:
- "Check the Enhanced Metrics tab to see all 30+ metrics"
- "Use the Compare tab to select players with checkboxes"
- "Save your team using the 💾 button to download JSON"
- "Load saved teams with the 📂 button"
- "Sort by Buy Score to find transfer targets"

## YOUR TONE & STYLE

- Friendly and helpful, like a knowledgeable FPL friend
- Use emojis sparingly (⚽ 💰 📊 👑 💎)
- Be concise but thorough
- Always explain your reasoning
- Provide actionable advice
- Reference specific metrics and scores
- Use FPL terminology (DGW, BGW, hits, differentials, template, etc.)

## FUNCTION CALLING

You have access to these functions to get live data:
- get_player_data(player_name): Get specific player's full stats
- get_top_players(position, metric, n): Get top N players by metric
- compare_players(player_ids): Compare multiple players
- get_team_analysis(player_ids): Analyze a team composition
- get_transfer_suggestions(position, max_cost): Get transfer targets
- get_captain_options(): Get top captain picks this week
- get_differentials(max_ownership): Find differential players

Always use functions to get live data rather than making assumptions.

## EXAMPLE INTERACTIONS

User: "Who should I captain this week?"
You: "Let me check the top captain options based on form, fixtures, and xGI... 👑

Based on Captain Score:
1. **Salah** (Score: 88) - Great form (8.2), favorable fixture vs Brighton (FDR: 2), xGI 0.85
2. **Haaland** (Score: 95) - Elite xGI (1.2), Home vs Burnley (FDR: 2), but rotation risk
3. **Palmer** (Score: 82) - Differential option (25% owned), xGI 0.78, form 7.8

**Recommendation**: Haaland for ceiling, Salah for safety. Palmer if chasing ranks."

User: "I have £8m for a midfielder, who should I get?"
You: "Let me find the best options under £8m... 📊

Top 3 by Buy Score:
1. **Gordon** (£7.5m) - Buy Score: 86, Form: 7.8, xGI: 0.62, Ownership: 18%
2. **Bowen** (£7.8m) - Buy Score: 84, Form: 8.1, xGI: 0.58, great fixtures (FDR: 2.2)
3. **Eze** (£7.0m) - Buy Score: 82, Form: 7.2, xGI: 0.55, differential (12% owned)

**Recommendation**: Gordon for best all-round stats. Bowen if you need immediate returns. Eze as a differential."

User: "Is my team over budget?"
You: "I can see your team costs £95.5m out of £100m budget. ✅

You have £4.5m remaining - perfect amount for flexibility! Having £1-2m in the bank is ideal for transfers without needing to downgrade elsewhere.

Current breakdown:
- 12/15 players selected
- Need 3 more players
- Position: GKP: 2, DEF: 5, MID: 3, FWD: 2

All looks good! 👍"

Remember: You're here to make FPL easier and more fun. Help users make informed decisions using data, not just gut feeling!
"""

class FPLAIAssistant:
    """AI Assistant powered by Google Gemini"""

    def __init__(self, player_data_func=None, enhanced_metrics_func=None):
        """
        Initialize AI assistant

        Args:
            player_data_func: Function to get player data
            enhanced_metrics_func: Function to get enhanced metrics
        """
        self.model = genai.GenerativeModel(
            model_name='gemini-pro',
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )

        self.player_data_func = player_data_func
        self.enhanced_metrics_func = enhanced_metrics_func
        self.chat_history = []

    def get_response(self, user_message: str, context: Optional[Dict] = None) -> str:
        """
        Get AI response to user message

        Args:
            user_message: User's question
            context: Additional context (current team, etc.)

        Returns:
            AI response
        """
        try:
            # Build full prompt with context
            full_prompt = self._build_prompt(user_message, context)

            # Get response from Gemini
            chat = self.model.start_chat(history=self.chat_history)
            response = chat.send_message(full_prompt)

            # Store in history
            self.chat_history.append({
                'role': 'user',
                'parts': [user_message]
            })
            self.chat_history.append({
                'role': 'model',
                'parts': [response.text]
            })

            # Keep history manageable (last 10 exchanges)
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]

            return response.text

        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please try again."

    def _build_prompt(self, user_message: str, context: Optional[Dict] = None) -> str:
        """Build comprehensive prompt with context"""

        prompt_parts = [SYSTEM_PROMPT]

        # Add context if provided
        if context:
            prompt_parts.append("\n\n## CURRENT CONTEXT\n")

            if 'team' in context:
                team = context['team']
                prompt_parts.append(f"User's current team: {len(team)} players selected")
                if team:
                    prompt_parts.append(f"Team cost: £{sum(p.get('cost', 0) for p in team):.1f}m")

            if 'budget_remaining' in context:
                prompt_parts.append(f"Budget remaining: £{context['budget_remaining']:.1f}m")

            if 'selected_players' in context:
                prompt_parts.append(f"Players in comparison: {context['selected_players']}")

            if 'current_gameweek' in context:
                prompt_parts.append(f"Current gameweek: {context['current_gameweek']}")

        prompt_parts.append(f"\n\n## USER QUESTION\n{user_message}")

        return "\n".join(prompt_parts)

    def get_contextual_help(self, page: str) -> str:
        """Get page-specific help"""

        help_texts = {
            'home': """
                Welcome to the FPL Analytics Dashboard! 🎮

                Here's what you can do:
                - **Import Team**: Click to import any FPL team by ID or URL
                - **Famous Teams**: Browse teams from top FPL YouTubers
                - **Dashboard**: Go to main workspace to build and analyze teams
                - **Compare**: Select players to compare side-by-side

                Need help with anything specific? Just ask me!
            """,
            'dashboard': """
                You're on the main Dashboard! 📊

                **Center**: Build your team (max 15 players, £100m budget)
                **Right Sidebar**: View team stats and quick filters
                **Player Table**: Browse and add players with 3 views:
                  - Players: Basic stats
                  - Enhanced Metrics: 30+ advanced metrics
                  - Compare: Side-by-side comparison

                **Tips**:
                - Click + to add players to your team
                - Use checkboxes to select for comparison
                - Save team with 💾 button
                - Sort columns to find best picks

                What would you like help with?
            """,
            'import': """
                Import any FPL team! 📥

                **By ID**: Enter team ID (e.g., 5094)
                **By URL**: Paste full FPL URL

                Famous managers you can try:
                - Andy (Let's Talk FPL): 5094
                - FPL Focal: 2523
                - FPL Harry: 23

                Need help analyzing a specific team?
            """
        }

        return help_texts.get(page, "How can I help you today?")

    def suggest_transfers(self, current_player: str, budget: float, position: str) -> str:
        """Suggest transfer options"""

        prompt = f"""
        User wants to transfer out {current_player} (Position: {position}).
        Budget available: £{budget}m

        Provide 3 transfer suggestions:
        1. List players with their metrics
        2. Explain why each is a good option
        3. Include Buy Score, Form, xGI
        4. Give clear recommendation

        Be specific and actionable.
        """

        return self.get_response(prompt)

    def analyze_team(self, team_players: List[Dict]) -> str:
        """Analyze user's team"""

        team_summary = f"Team has {len(team_players)} players"
        if team_players:
            total_cost = sum(p.get('cost', 0) for p in team_players)
            team_summary += f", total cost: £{total_cost:.1f}m"

        prompt = f"""
        {team_summary}

        Analyze this team:
        1. Check if well-balanced (positions, budget)
        2. Identify strengths and weaknesses
        3. Suggest improvements
        4. Rate overall (0-10)

        Be constructive and specific.
        """

        return self.get_response(prompt, {'team': team_players})

    def explain_metric(self, metric_name: str) -> str:
        """Explain a specific metric"""

        prompt = f"""
        Explain the "{metric_name}" metric:
        1. What it measures
        2. How it's calculated
        3. What's a good value
        4. How to use it for decisions
        5. Example

        Be clear and concise.
        """

        return self.get_response(prompt)

    def reset_chat(self):
        """Reset chat history"""
        self.chat_history = []


# Singleton instance
ai_assistant = FPLAIAssistant()
