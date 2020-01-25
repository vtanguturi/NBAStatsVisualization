## Intiailizing stuff common across all files
##Imports
%matplotlib inline
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import json

from headers import get_headers
## This is to get the connection to the nba endpoints correctly (hot fix to work until they push changes)
headers = get_headers

## Build the team name to team_id map
from nba_api.stats.static import teams
nba_teams = teams.get_teams()
list_teams = ['ATL', 'BOS', 'CLE', 'NOP', 'CHI', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL'
        , 'MIA', 'MIL', 'MIN', 'BKN', 'NYK', 'ORL', 'IND', 'PHI', 'PHX', 'POR', 'SAC'
        , 'SAS', 'OKC', 'TOR', 'UTA', 'MEM', 'WAS', 'DET', 'CHA']
i = 0
team_to_id = {}
for t in list_teams:
    team_to_id.update({t: nba_teams[i]['id']})
    i += 1

## Select a color for each team
# https://teamcolorcodes.com/nba-team-color-codes/
list_teams = ['ATL', 'BOS', 'CLE', 'NOP', 'CHI', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL'
        , 'MIA', 'MIL', 'MIN', 'BKN', 'NYK', 'ORL', 'IND', 'PHI', 'PHX', 'POR', 'SAC'
        , 'SAS', 'OKC', 'TOR', 'UTA', 'MEM', 'WAS', 'DET', 'CHA']
color_teams = ['#E03A3E', '#007A33', '#860038', '#0C2340', '#CE1141',
               '#00538C', '#0E2240', '#1D428A', '#BA0C2F', '#1D428A', '#FDB927',
               '#DB3EB1', '#EEE1C6', '#236192', '#000000', '#F58426', '#0077C0',
               '#002D62', '#ED174C', '#B95915', '#E03A3E', '#5A2D81', '#C4CED4',
               '#007AC1', '#B4975A', '#00471B', '#5D76A9', '#002B5C', '#1D42BA', '#00788C']
team_to_color = {}
i = 0
for t in list_teams:
    team_to_color.update({t: color_teams[i]})
    i += 1

## Imports relative to the intent of methods in this file
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import playbyplay
from nba_api.stats.library import eventmsgtype

## Generate a list of tuples in this format
## (game_id, is_home, opponent)
def build_games_for_team(team):
    gpbp = teamgamelog.TeamGameLog(team_id=team_to_id[team], headers=headers)
    tgl = gpbp.get_data_frames()[0]
    game_ids = tgl['Game_ID'].values
    games = []
    matchups = tgl['MATCHUP'].values
    for i in range(len(matchups)):
        curr = matchups[i]
        is_home = True
        if '@' in curr:
            is_home = False
        opponent = curr[-3:]
        games.append((game_ids[i], is_home, opponent))
    return games

## Use the play by play for a given game to look for instances of the wanted
## event and return quarter-bucketized totals for each team
def get_home_and_away_event(event, pbp_game):
    home_team = []
    visitor_team = []
    for i in range(4):
        ## HAve it as fieldgoalmade bc tested with that field, can compare others too
        fieldgoalmade = pbp_game.loc[(pbp_game['EVENTMSGTYPE'] == event) & (pbp_game['PERIOD'] == i+1)]
        home = fieldgoalmade.loc[~(fieldgoalmade['HOMEDESCRIPTION'].values == None)]
        visitor= fieldgoalmade.loc[~(fieldgoalmade['VISITORDESCRIPTION'].values == None)]
        home_team.append(home.shape[0])
        visitor_team.append(visitor.shape[0])
    return home_team, visitor_team

## Visualize all this data built for a particular stat, and a home/away team
def plot_game_fgs(stat_compare, ht, vt):
    N = 4
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure(figsize=(5,4))
    ax = fig.add_subplot(111)

    rects1 = ax.bar(ind, ht[2], width, color=ht[1])
    rects2 = ax.bar(ind+width, vt[2], width, color=vt[1])

    ax.set_ylabel(stat_compare)
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels( ('Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4') )
    ax.legend( (rects1[0], rects2[0]), (ht[0], vt[0]) )
    plt.show()

## Main function to do the whole thing for a given custom made 
## game instance (which is in the form of a tuple)
def compare_matchup(game, event, team):
    gpbp = playbyplay.PlayByPlay(game_id=game[0], headers=headers)
    playByPlay = gpbp.get_data_frames()[0]
    home, visitor = get_home_and_away_event(event.value, playByPlay)
    ## If its a home game for the team
    if game[1]:
        plot_game_fgs(str(event), (team, team_to_color[team], home), (game[2], team_to_color[game[2]], visitor))
    else:
        plot_game_fgs(str(event), (game[2], team_to_color[game[2]], home), (team, team_to_color[team], visitor))

## At long last example to run
team = 'LAL'
games = build_games_for_team(team)
for game in games:
    compare_matchup(game, eventmsgtype.EventMsgType.REBOUND, team)