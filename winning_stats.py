## To make API calls to get all players, and indiv player info
from nba_api.stats.endpoints import franchiseplayers
from nba_api.stats.endpoints import playergamelog

from headers import get_headers
## This is to get the connection to the nba endpoints correctly (hot fix to work until they push changes)
headers = get_headers()

def determine_stats_win_index(player_game_data):  
    FG_PCT_THRESHOLD = 0.5
    
    stats_win_index = player_game_data.PTS + (2 * player_game_data.AST) 
    + (1.5 * player_game_data.REB) - 2 * (player_game_data.TOV + player_game_data.PF)
    + 2 * (player_game_data.STL + player_game_data.BLK)
    
    return stats_win_index

def plot_stats_to_winning(player_game_data, player_name):
    swi = determine_stats_win_index(player_game_data)
    plt.scatter(swi, player_game_data.PLUS_MINUS, s=300, c=player_game_data.FG_PCT)
    plt.title(player_name + ". His score is: " + str(determine_player_winning_score(player_game_data)))
    plt.show()

def determine_player_winning_score(player_game_data):
    swi = determine_stats_win_index(player_game_data)
    try:
        return np.round(np.mean(player_game_data.PLUS_MINUS.values * swi.values * player_game_data.MIN.values / 48),2)
    except ZeroDivisionError:
        return 0.01

def rank_player_winning_scores(team, efficiencies, n):
    top_n_players = sorted(efficiencies.keys(), reverse=True)
    print(top_n_players)
    print("Top " + str(n) + " players on the " + team)
    for i in range(n):
        print(str(i) + ". " + efficiencies[top_n_players[i]] + " has a stat win index score of: " + str(top_n_players[i]))

## All teams:
## Build the team name to team_id map
list_teams = ['ATL', 'BOS', 'CLE', 'NOP', 'CHI', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL'
        , 'MIA', 'MIL', 'MIN', 'BKN', 'NYK', 'ORL', 'IND', 'PHI', 'PHX', 'POR', 'SAC'
        , 'SAS', 'OKC', 'TOR', 'UTA', 'MEM', 'WAS', 'DET', 'CHA']
i = 0
team_to_id = {}
for t in list_teams:
    team_to_id.update({t: nba_teams[i]['id']})
    i += 1
print(team_to_id)

## Get all players in a team and figure out the stats to winning
def get_winning_stats_per_team(team):
    fp = franchiseplayers.FranchisePlayers(team_id=team_to_id[team], headers=headers)
    PLAYERS = fp.get_data_frames()[0]
    # Build the list of players in the 2019-2020 season
    active_players = PLAYERS.loc[PLAYERS['ACTIVE_WITH_TEAM'] == 1]
    ids_per_team = active_players['PERSON_ID'].values
    player_names = active_players['PLAYER'].values
    print(player_names)
    players_per_team = dict(zip(ids_per_team, player_names))
    effectiveness = []
    players = []
    ## Get the winning_stats_for a player
    for player in players_per_team:
        pgl = playergamelog.PlayerGameLog(player_id=player, headers=headers)
        player_game_data = pgl.get_data_frames()[0]
        effectiveness.append(determine_player_winning_score(player_game_data))
        players.append(players_per_team[player])
        plot_stats_to_winning(player_game_data, players_per_team[player])
        
    effect = dict(zip(effectiveness, players)) 
    rank_player_winning_scores(team, effect, 5)
    
## This will get all the graphs for that team
get_winning_stats_per_team("MIA")