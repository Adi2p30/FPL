"""
FPL Team Data API
=================

Fetch and manage FPL team data from the official API
Supports importing teams by ID and tracking famous FPL managers
"""

import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class FPLManager:
    """Famous FPL YouTuber/Content Creator"""
    name: str
    team_id: int
    youtube_channel: str
    description: str


# Famous FPL Content Creators with their team IDs
FAMOUS_MANAGERS = [
    FPLManager(
        name="Andy (Let's Talk FPL)",
        team_id=5094,  # Andy's team ID
        youtube_channel="Let's Talk FPL",
        description="One of the biggest FPL YouTube channels"
    ),
    FPLManager(
        name="FPL Focal",
        team_id=2523,  # FPL Focal team ID
        youtube_channel="FPL Focal",
        description="Data-driven FPL analysis"
    ),
    FPLManager(
        name="FPL Harry",
        team_id=23,  # FPL Harry's team ID
        youtube_channel="FPL Harry",
        description="Top FPL content creator"
    ),
    FPLManager(
        name="FPL Mate",
        team_id=145,  # FPL Mate team ID
        youtube_channel="FPL Mate",
        description="Popular FPL YouTuber"
    ),
    FPLManager(
        name="FPL Wire",
        team_id=91928,  # FPL Wire team ID
        youtube_channel="FPL Wire",
        description="Community-driven FPL updates"
    ),
    FPLManager(
        name="FPL General",
        team_id=1633,  # FPL General team ID
        youtube_channel="FPL General",
        description="FPL strategy and analysis"
    ),
    FPLManager(
        name="FPL BlackBox",
        team_id=3523,  # FPL BlackBox team ID
        youtube_channel="FPL BlackBox",
        description="Advanced FPL metrics"
    ),
    FPLManager(
        name="FPL Raptor",
        team_id=789,  # FPL Raptor team ID
        youtube_channel="FPL Raptor",
        description="FPL tips and strategy"
    ),
]


class FPLTeamAPI:
    """API client for FPL team data"""

    BASE_URL = "https://fantasy.premierleague.com/api"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_team_info(self, team_id: int) -> Optional[Dict]:
        """
        Get basic team information

        Args:
            team_id: FPL team ID

        Returns:
            Team info dict or None if error
        """
        try:
            url = f"{self.BASE_URL}/entry/{team_id}/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching team {team_id}: {e}")
            return None

    def get_team_picks(self, team_id: int, gameweek: int) -> Optional[Dict]:
        """
        Get team picks for a specific gameweek

        Args:
            team_id: FPL team ID
            gameweek: Gameweek number

        Returns:
            Picks data or None if error
        """
        try:
            url = f"{self.BASE_URL}/entry/{team_id}/event/{gameweek}/picks/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching picks for team {team_id} GW{gameweek}: {e}")
            return None

    def get_current_gameweek(self) -> int:
        """
        Get current gameweek number

        Returns:
            Current gameweek number
        """
        try:
            url = f"{self.BASE_URL}/bootstrap-static/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Find current gameweek
            for event in data['events']:
                if event['is_current']:
                    return event['id']

            # If no current GW, return next
            for event in data['events']:
                if event['is_next']:
                    return event['id']

            return 1
        except Exception as e:
            print(f"Error fetching current gameweek: {e}")
            return 1

    def get_team_history(self, team_id: int) -> Optional[Dict]:
        """
        Get team history (past seasons, current season)

        Args:
            team_id: FPL team ID

        Returns:
            History data or None if error
        """
        try:
            url = f"{self.BASE_URL}/entry/{team_id}/history/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching history for team {team_id}: {e}")
            return None

    def get_team_transfers(self, team_id: int) -> Optional[List[Dict]]:
        """
        Get team transfer history

        Args:
            team_id: FPL team ID

        Returns:
            Transfer history or None if error
        """
        try:
            url = f"{self.BASE_URL}/entry/{team_id}/transfers/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching transfers for team {team_id}: {e}")
            return None

    def get_full_team_data(self, team_id: int, gameweek: Optional[int] = None) -> Dict:
        """
        Get complete team data including info, picks, history

        Args:
            team_id: FPL team ID
            gameweek: Specific gameweek (None = current)

        Returns:
            Complete team data dictionary
        """
        if gameweek is None:
            gameweek = self.get_current_gameweek()

        team_info = self.get_team_info(team_id)
        team_picks = self.get_team_picks(team_id, gameweek)
        team_history = self.get_team_history(team_id)
        team_transfers = self.get_team_transfers(team_id)

        return {
            'team_id': team_id,
            'gameweek': gameweek,
            'info': team_info,
            'picks': team_picks,
            'history': team_history,
            'transfers': team_transfers
        }

    def get_famous_teams(self) -> List[Dict]:
        """
        Get all famous FPL YouTuber teams

        Returns:
            List of team data for famous managers
        """
        current_gw = self.get_current_gameweek()
        teams = []

        for manager in FAMOUS_MANAGERS:
            team_data = self.get_full_team_data(manager.team_id, current_gw)
            team_data['manager_info'] = {
                'name': manager.name,
                'youtube_channel': manager.youtube_channel,
                'description': manager.description
            }
            teams.append(team_data)

        return teams

    def get_player_data(self) -> Optional[Dict]:
        """
        Get all player data from bootstrap-static

        Returns:
            Player data dict or None
        """
        try:
            url = f"{self.BASE_URL}/bootstrap-static/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching player data: {e}")
            return None

    def get_team_from_url(self, url: str) -> Optional[Dict]:
        """
        Extract team ID from FPL URL and fetch team data

        Supports URLs like:
        - https://fantasy.premierleague.com/entry/123456/event/10
        - https://fantasy.premierleague.com/entry/123456/history

        Args:
            url: FPL team URL

        Returns:
            Team data or None
        """
        import re

        # Extract team ID from URL
        match = re.search(r'/entry/(\d+)', url)
        if not match:
            print(f"Could not extract team ID from URL: {url}")
            return None

        team_id = int(match.group(1))

        # Extract gameweek if present
        gw_match = re.search(r'/event/(\d+)', url)
        gameweek = int(gw_match.group(1)) if gw_match else None

        return self.get_full_team_data(team_id, gameweek)


def export_famous_teams():
    """Export famous teams data to JSON for frontend"""
    api = FPLTeamAPI()
    teams = api.get_famous_teams()

    with open('famous_teams.json', 'w') as f:
        json.dump(teams, f, indent=2)

    print(f"Exported {len(teams)} famous teams to famous_teams.json")


if __name__ == "__main__":
    # Test the API
    api = FPLTeamAPI()

    # Test with a team ID
    print("Testing FPL Team API...")
    test_team_id = 5094  # Andy's team

    team_data = api.get_full_team_data(test_team_id)
    print(f"\nTeam Info for {test_team_id}:")
    if team_data['info']:
        print(f"Manager: {team_data['info']['player_first_name']} {team_data['info']['player_last_name']}")
        print(f"Team Name: {team_data['info']['name']}")
        print(f"Overall Points: {team_data['info']['summary_overall_points']}")
        print(f"Overall Rank: {team_data['info']['summary_overall_rank']}")

    print(f"\nCurrent Gameweek: {team_data['gameweek']}")

    if team_data['picks']:
        print(f"Number of picks: {len(team_data['picks']['picks'])}")

    # Export famous teams
    print("\n" + "="*50)
    print("Exporting famous FPL teams...")
    export_famous_teams()
