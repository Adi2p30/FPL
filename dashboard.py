import requests, json, ssl
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
ssl._create_default_https_context = ssl._create_unverified_context
from pprint import pprint

#TODO: def summary_primierleague():
#TODO: def awards():





#TODO: def visulization():





def FPLapi_main_endpoint():
    base_url = 'https://fantasy.premierleague.com/api/'
    data = requests.get(base_url + 'bootstrap-static/').json()
    return data

def players(data):
    players = data['elements']
    players = pd.DataFrame(players)
    return players

def playerdata_json(players):
    players = players[['id', 'first_name', 'second_name', 'web_name', 'element_type', 'team', 'now_cost', 'selected_by_percent', 'total_points', 'points_per_game', 'minutes', 'goals_scored', 'assists', 'clean_sheets','expected_goals_per_90', 'saves_per_90', 'expected_assists_per_90','expected_goal_involvements_per_90', 'expected_goals_conceded_per_90' , 'goals_conceded', 'penalties_saved', 'penalties_missed', 'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat', 'ict_index']]
    players.to_json("Data/players_" + str(datetime.date.today()), orient='records')

def playerdata_csv(players):
    players = players[
        ['first_name', 'second_name', 'web_name', 'element_type', 'team', 'now_cost', 'selected_by_percent',
         'total_points', 'points_per_game', 'minutes', 'goals_scored', 'assists', 'clean_sheets',
         'expected_goals_per_90', 'saves_per_90', 'expected_assists_per_90', 'expected_goal_involvements_per_90',
         'expected_goals_conceded_per_90', 'goals_conceded', 'penalties_saved', 'penalties_missed', 'saves', 'bonus',
         'bps', 'influence', 'creativity', 'threat', 'ict_index']]
    players.to_csv("Data/players_" + str(datetime.date.today()) + ".csv")

def teamdata(data):
    teams = data['teams']
    teams = pd.DataFrame(teams)
    return teams


def search_player_ID(ID):
    data = FPLapi_main_endpoint()
    players = data['elements']
    for player in players:
        if player['id'] == ID:
            return player

def search_player_name(name):
    data = FPLapi_main_endpoint()
    players = data['elements']
    for player in players:
        if player['web_name'] == name:
            return player

def FPLapi_fixtures_endpoint():
    base_url = 'https://fantasy.premierleague.com/api/fixtures/'
    data = requests.get(base_url).json()
    return data

def search_fixture(code):
    data = FPLapi_fixtures_endpoint()
    for fixture in data:
        if fixture['code'] == code:
            return fixture

def search_fixture_team(team):
    data = FPLapi_fixtures_endpoint()
    fixtures = []
    for fixture in data:
        if fixture['team_a'] == team or fixture['team_h'] == team:
            fixtures.append(fixture)
    return fixtures

def gameweek(number):
    data = FPLapi_main_endpoint()
    gameweek = data['events']
    for gw in gameweek:
        if gw['id'] == number:
            return gw




