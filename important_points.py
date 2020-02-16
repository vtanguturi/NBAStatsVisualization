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
headers = get_headers()

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

## Imports for this logic:
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import winprobabilitypbp

def plot_game_win_probability(win_probability, title):
    home_pct = win_probability['HOME_PCT'].values
    visit_pct = win_probability['VISITOR_PCT'].values
    ind = range(len(home_pct))
    baseline = [0.5] * len(home_pct)
    plt.plot(ind, home_pct, 'g.')
    plt.plot(ind, visit_pct, 'r^')
    plt.plot(ind, baseline, 'k-')
    plt.title(title)
    if '@' in title:
        home_team = title[-3:]
        away_team = title[:3]
    else:
        home_team = title[:3]
        away_team = title[-3:]
    plt.legend((home_team, away_team))
    teams = {'home': home_team, 'visit': away_team}
    
    ## Annotate the graph with the important points and print out all the plays:
    game_pct = np.abs(home_pct - visit_pct)
    game_inflection = get_inflection_point_occurences(game_pct, 2)

    plt.plot(game_inflection[0:10], 10*[0.5], 'bX', markersize=20)

    print("Game important plays: ")
    get_influential_plays(win_probability, game_inflection, teams)     
    plt.show()

def generate_win_probability_team(team, NUMBER_GAMES):
    gpbp = teamgamelog.TeamGameLog(team_id=team_to_id[team], headers=headers)
    tgl = gpbp.get_data_frames()[0]
    games = tgl['Game_ID'].values
    matchups = tgl['MATCHUP'].values
    results = tgl['WL'].values
    i = 0
    selected_games = games[0:NUMBER_GAMES]
    for game in selected_games:
        wpp = winprobabilitypbp.WinProbabilityPBP(game_id=game, headers=headers)
        wp = wpp.get_data_frames()[0]
        plot_game_win_probability(wp, matchups[i])
        print("This game resulted with %s getting the %s" % (team, results[i]))
        print("====================================================================")
        i += 1

def get_inflection_point_occurences(team_data, derivative_type):
    second_deriv = np.diff(team_data, n=derivative_type).tolist()
    second_deriv_sorted = sorted(second_deriv, reverse=True)
    inflection_occurences = []
    for i in second_deriv_sorted:
        inflection_occurences.append(second_deriv.index(i) + 2)
    return inflection_occurences    

def get_influential_plays(wp, inflection_occurences, teams):
    events = wp['EVENT_NUM'].values
    descriptions = wp['DESCRIPTION'].values
    quarter = wp['PERIOD'].values
    time_in_quarter = wp['SECONDS_REMAINING'].values
    home_possession = wp['HOME_POSS_IND'].values
    
    event_inflect = events[inflection_occurences]
    di = descriptions[inflection_occurences]
    qi = quarter[inflection_occurences]
    ti = time_in_quarter[inflection_occurences]
    hpi = home_possession[inflection_occurences]
    
    put_the_output(di, ti, qi, hpi, teams)
    
def put_the_output(desc_inflect, tiq_inflect, quarter_inflect, home_posessions, teams):
    number = 10
    home_plays = 0
    visit_plays = 0
     print("Top turning point descriptions: ")
     print("========================================================")
    for i in range(len(desc_inflect)):
        d = desc_inflect[i]
        if d is not None:
            number = number - 1
            if home_posessions[i] == 1:
                home_plays += 1
            else:
                visit_plays += 1
             print('Q%s: %s left %s' % (quarter_inflect[i], convert_secs_into_gametime(tiq_inflect[i]), d))
        if number <= 0:
            break
     print("========================================================")
    print("Important plays: \n%s:%d\n%s:%d" % (teams['home'], home_plays, teams['visit'], visit_plays))
    
def convert_secs_into_gametime(time_left_quarters):
    seconds = time_left_quarters % 60
    minutes = (time_left_quarters - seconds) / 60
    return '%d:%d' % (minutes, seconds)