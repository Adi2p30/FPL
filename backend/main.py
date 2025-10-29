"""
FPL Backend API - FastAPI Server
=================================

REST API for FPL analytics with team import functionality
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Fpl_api import FPLapi_main_endpoint, players as get_players, teamdata
from advanced_metrics import AdvancedMetrics
from fpl_team_api import FPLTeamAPI, FAMOUS_MANAGERS

app = FastAPI(title="FPL Analytics API", version="1.0.0")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize FPL Team API
team_api = FPLTeamAPI()


# Request/Response Models
class TeamImportRequest(BaseModel):
    team_id: Optional[int] = None
    url: Optional[str] = None
    gameweek: Optional[int] = None


class PlayerUpdateRequest(BaseModel):
    team_id: int
    player_in_id: int
    player_out_id: int
    gameweek: int


# ============================================================================
# PLAYER DATA ENDPOINTS
# ============================================================================

@app.get("/api/players")
async def get_all_players():
    """Get all FPL players with stats"""
    try:
        fpl_data = FPLapi_main_endpoint()
        players_df = get_players(fpl_data)

        # Convert to dict for JSON response
        players_dict = players_df.to_dict('records')

        return {
            "success": True,
            "count": len(players_dict),
            "players": players_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/players/{player_id}")
async def get_player(player_id: int):
    """Get specific player data"""
    try:
        fpl_data = FPLapi_main_endpoint()
        players_df = get_players(fpl_data)

        player = players_df[players_df['id'] == player_id]

        if player.empty:
            raise HTTPException(status_code=404, detail="Player not found")

        return {
            "success": True,
            "player": player.to_dict('records')[0]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/teams")
async def get_all_teams():
    """Get all FPL teams"""
    try:
        fpl_data = FPLapi_main_endpoint()
        teams_df = teamdata(fpl_data)

        teams_dict = teams_df.to_dict('records')

        return {
            "success": True,
            "count": len(teams_dict),
            "teams": teams_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ADVANCED METRICS ENDPOINTS
# ============================================================================

@app.get("/api/metrics/comprehensive")
async def get_comprehensive_metrics():
    """Get comprehensive analysis with all metrics"""
    try:
        fpl_data = FPLapi_main_endpoint()
        players_df = get_players(fpl_data)

        metrics = AdvancedMetrics(players_df)
        analysis_df = metrics.get_comprehensive_analysis()

        return {
            "success": True,
            "count": len(analysis_df),
            "analysis": analysis_df.to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/captains")
async def get_captain_picks():
    """Get top captain picks"""
    try:
        fpl_data = FPLapi_main_endpoint()
        players_df = get_players(fpl_data)

        metrics = AdvancedMetrics(players_df)
        captains_df = metrics.calculate_captain_score()

        return {
            "success": True,
            "captains": captains_df.head(20).to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/differentials")
async def get_differentials(max_ownership: float = 10.0, min_points: int = 30):
    """Get differential players"""
    try:
        fpl_data = FPLapi_main_endpoint()
        players_df = get_players(fpl_data)

        metrics = AdvancedMetrics(players_df)
        diffs_df = metrics.find_differentials(max_ownership, min_points)

        return {
            "success": True,
            "differentials": diffs_df.to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/position/{position}")
async def get_position_metrics(position: str):
    """Get position-specific metrics (GKP, DEF, MID, FWD)"""
    try:
        fpl_data = FPLapi_main_endpoint()
        players_df = get_players(fpl_data)

        metrics = AdvancedMetrics(players_df)

        if position.upper() == 'GKP':
            result_df = metrics.calculate_goalkeeper_metrics()
        elif position.upper() == 'DEF':
            result_df = metrics.calculate_defender_metrics()
        elif position.upper() == 'MID':
            result_df = metrics.calculate_midfielder_metrics()
        elif position.upper() == 'FWD':
            result_df = metrics.calculate_forward_metrics()
        else:
            raise HTTPException(status_code=400, detail="Invalid position")

        return {
            "success": True,
            "position": position.upper(),
            "metrics": result_df.to_dict('records')
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TEAM IMPORT ENDPOINTS
# ============================================================================

@app.post("/api/team/import")
async def import_team(request: TeamImportRequest):
    """Import FPL team by ID or URL"""
    try:
        team_data = None

        if request.url:
            # Import from URL
            team_data = team_api.get_team_from_url(request.url)
        elif request.team_id:
            # Import by ID
            team_data = team_api.get_full_team_data(
                request.team_id,
                request.gameweek
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Must provide team_id or url"
            )

        if not team_data or not team_data['info']:
            raise HTTPException(
                status_code=404,
                detail="Team not found or API error"
            )

        return {
            "success": True,
            "team": team_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/team/{team_id}")
async def get_team(team_id: int, gameweek: Optional[int] = None):
    """Get FPL team data"""
    try:
        team_data = team_api.get_full_team_data(team_id, gameweek)

        if not team_data['info']:
            raise HTTPException(status_code=404, detail="Team not found")

        return {
            "success": True,
            "team": team_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/team/{team_id}/picks")
async def get_team_picks(team_id: int, gameweek: Optional[int] = None):
    """Get team picks for a gameweek"""
    try:
        if gameweek is None:
            gameweek = team_api.get_current_gameweek()

        picks = team_api.get_team_picks(team_id, gameweek)

        if not picks:
            raise HTTPException(status_code=404, detail="Picks not found")

        return {
            "success": True,
            "team_id": team_id,
            "gameweek": gameweek,
            "picks": picks
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# FAMOUS MANAGERS ENDPOINTS
# ============================================================================

@app.get("/api/famous-managers")
async def get_famous_managers():
    """Get list of famous FPL managers"""
    return {
        "success": True,
        "managers": [
            {
                "name": m.name,
                "team_id": m.team_id,
                "youtube_channel": m.youtube_channel,
                "description": m.description
            }
            for m in FAMOUS_MANAGERS
        ]
    }


@app.get("/api/famous-teams")
async def get_famous_teams():
    """Get all famous FPL teams data"""
    try:
        teams = team_api.get_famous_teams()

        return {
            "success": True,
            "count": len(teams),
            "teams": teams
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/famous-teams/{manager_name}")
async def get_famous_team(manager_name: str):
    """Get specific famous manager's team"""
    try:
        # Find manager
        manager = None
        for m in FAMOUS_MANAGERS:
            if manager_name.lower() in m.name.lower():
                manager = m
                break

        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")

        team_data = team_api.get_full_team_data(manager.team_id)
        team_data['manager_info'] = {
            'name': manager.name,
            'youtube_channel': manager.youtube_channel,
            'description': manager.description
        }

        return {
            "success": True,
            "team": team_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/api/gameweek/current")
async def get_current_gameweek():
    """Get current gameweek number"""
    try:
        gw = team_api.get_current_gameweek()
        return {
            "success": True,
            "current_gameweek": gw
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "FPL Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "players": "/api/players",
            "teams": "/api/teams",
            "metrics": "/api/metrics/comprehensive",
            "captains": "/api/metrics/captains",
            "differentials": "/api/metrics/differentials",
            "import_team": "/api/team/import",
            "famous_managers": "/api/famous-managers",
            "famous_teams": "/api/famous-teams"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
