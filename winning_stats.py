## To make API calls to get all players, and indiv player info
from nba_api.stats.endpoints import franchiseplayers
from nba_api.stats.endpoints import playergamelog

## This is to get the connection to the nba endpoints correctly (hot fix to work until they push changes)
headers = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def determine_stats_to_winning(player_game_data, player_name):  
    FG_PCT_THRESHOLD = 0.5
    
    stats_win_index = player_game_data.PTS + (2 * player_game_data.AST) 
    + (1.5 * player_game_data.REB) - 2 * (player_game_data.TOV + player_game_data.PF)
    + 2 * (player_game_data.STL + player_game_data.BLK)

    plt.scatter(stats_win_index, player_game_data.PLUS_MINUS, s=300, c=player_game_data.FG_PCT)
    plt.title(player_name)
    plt.show()

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
    players = fp.get_data_frames()[0]
    # Build the list of players in the 2019-2020 season
    active_players = players.loc[players['ACTIVE_WITH_TEAM'] == 1]
    ids_per_team = active_players['PERSON_ID'].values
    player_names = active_players['PLAYER'].values
    players_per_team = dict(zip(ids_per_team, player_names))
    ## Get the winning_stats_for a player
    for player in players_per_team:
        pgl = playergamelog.PlayerGameLog(player_id=player, headers=headers)
        player_game_data = pgl.get_data_frames()[0]
        determine_stats_to_winning(player_game_data, players_per_team[player])

## This will get all the graphs for that team
get_winning_stats_per_team("MIA")