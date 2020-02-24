##Imports
%matplotlib inline
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import json
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import franchiseplayers
from headers import get_headers
## This is to get the connection to the nba endpoints correctly (hot fix to work until they push changes)
headers = get_headers()

# This is taken from one of the tutorials I followed:
## This is function to draw nba_court
from matplotlib.patches import Circle, Rectangle, Arc

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

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

from nba_api.stats.endpoints import franchiseplayers

def get_team_shotchart_for_year(team, year):
    beg_year = year.split('-')[0]
    # 1) Get all players for a team
    fp = franchiseplayers.FranchisePlayers(team_id=team_to_id[team], headers=headers)
    fps = fp.get_data_frames()[0]
    # 2) Get the shot chart for all the players
    curr_players = fps.loc[fps['ACTIVE_WITH_TEAM'] == 1]
    all_player_shot_chart = curr_players.apply(lambda row: get_shot_chart(row, beg_year), axis=1)
    team_shotchart = pd.concat(all_player_shot_chart.values)
    output_team_shot_chart(team, year, team_shotchart)

def get_season_strings(year1, year2):
    year_month = [year1 + '10', year1 + '11', year1 + '12', year2 + '01', year2 + '02', year2 + '03', year2 + '04']
    return tuple(year_month)

def get_shot_chart(row, year):
    sc = shotchartdetail.ShotChartDetail(team_id=row['TEAM_ID'], player_id=row['PERSON_ID'], headers=headers)
    allyrs_shotchart = sc.get_data_frames()[0]
    bool_series= allyrs_shotchart['GAME_DATE'].str.startswith(get_season_strings(year, str(int(year) + 1)))
    team_sc = allyrs_shotchart[bool_series]  
    return team_sc

def output_team_shot_chart(team, season, team_shotchart):
    jsct = sns.jointplot(team_shotchart.LOC_X, team_shotchart.LOC_Y, stat_func=None,
                                     kind='scatter', space=0, alpha=0.5)
    jsct.fig.set_size_inches(12,11)
    # A joint plot has 3 Axes, the first one called ax_joint
    # is the one we want to draw our court onto and adjust some other settings
    ax = jsct.ax_joint
    draw_court(ax)
    # Adjust the axis limits and orientation of the plot in order
    # to plot half court, with the hoop by the top of the plot
    ax.set_xlim(-250,250)
    ax.set_ylim(422.5, -47.5)
    # Get rid of axis labels and tick marks
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom='off', labelleft='off')
    # Add a title
    ax.set_title('%s %s Season Shotchart' % (team, season),
                 y=1.2, fontsize=18)


get_team_shotchart_for_year('MIA', '2019-2020')