from headers import get_headers
## This is to get the connection to the nba endpoints correctly (hot fix to work until they push changes)
headers = get_headers

# Make API Call for players across all seasons for a particular franchise
from nba_api.stats.endpoints import franchiseplayers
## Get all players:
nba2019_2020players = {}
for team in list_teams:
    fp = franchiseplayers.FranchisePlayers(team_id=team_to_id[team], headers=headers)
    players = fp.get_data_frames()[0]
    active_players = players.loc[players['ACTIVE_WITH_TEAM'] == 1]
    ids_per_team = active_players['PERSON_ID'].values
    player_names = active_players['PLAYER'].values
    players_per_team = dict(zip(ids_per_team, player_names))
    nba2019_2020players.update(players_per_team)


## Determine_condition or ret true if you cant
def dc(values, sign, threshold): 
    if len(values) > 0:
        if sign == 'l':
            return np.mean(values) < threshold
        elif sign == "g":
            return np.mean(values) > threshold
    else:
        return True

def classify_players(players):
    three_and_d_players = []
    facilitators = []
    spot_up_shooters = []
    defenders = []
    athletic = []
    elite_two_way = []
    iso = []
    other = []
    for player in players:
        pgl = playergamelog.PlayerGameLog(player_id=player, headers=headers)
        gamelog = pgl.get_data_frames()[0]
        if dc(gamelog.FG3_PCT.values, 'g', 0.38) and dc(gamelog.STL.values, 'g', 1.5) and dc(gamelog.BLK.values, 'g', 0.5):
            three_and_d_players.append((player, players[player]))
        elif dc(gamelog.AST.values, 'g', 7.0) and dc(gamelog.PTS.values, 'l', 18) and dc(gamelog.FG_PCT.values, 'g', 0.45):
            facilitators.append((player, players[player]))
        elif dc(gamelog.FG_PCT.values, 'g', 0.5) and dc(gamelog.FG3_PCT.values, 'g', 0.4) and dc(gamelog.FG3A.values, 'g', 7):
            spot_up_shooters.append((player, players[player]))
        elif dc(gamelog.REB.values, 'g', 5) and dc(gamelog.STL.values, 'g', 1.5) and dc(gamelog.BLK.values, 'g', 0.7):
            defenders.append((player, players[player]))
        elif dc(gamelog.REB.values, 'g', 7) and dc(gamelog.PTS.values, 'g', 20) and dc(gamelog.STL.values, 'g', 1) and dc(gamelog.BLK.values, 'g', 1):
            athletic.append((player, players[player]))
        elif dc(gamelog.PTS.values, 'g', 25) and dc(gamelog.REB.values, 'g', 6) and dc(gamelog.FG_PCT.values, 'g', 0.52) and dc(gamelog.AST.values, 'g', 5) and dc(gamelog.STL.values, 'g', 1) and dc(gamelog.BLK.values, 'g', 0.8):
            elite_two_way.append((player, players[player]))
        elif dc(gamelog.PTS.values, 'g', 20) and dc(gamelog.AST.values, 'l', 5) and dc(gamelog.FG_PCT.values, 'g', 0.4):
            iso.append((player, players[player]))
        else:
            other.append((player, players[player]))

    print("3-D players are: ")
    print(three_and_d_players)
    print("Facilitators are: ")
    print(facilitators)
    print("Spot up shooters are: ")
    print(spot_up_shooters)
    print("Defenders are: ")
    print(defenders)
    print("Athletic players are: ")
    print(athletic)
    print("elite 2 way players are: ")
    print(elite_two_way)
    print("iso players are: ")
    print(iso)
    #print("other 'role' players are: ")
    #print(other)
    return (three_and_d_players, facilitators, spot_up_shooters, defenders, athletic, elite_two_way, iso, other)


## Clustering with kmeans (M A C H I N E L E A R N I N G T I M E :D)
def build_player_counting_stats(players):
    total_stats = []
    for player in players:
        pgl = playergamelog.PlayerGameLog(player_id=player[0], headers=headers)
        gamelog = pgl.get_data_frames()[0]
        if len(gamelog.PTS.values) > 0 and len(gamelog.AST.values) > 0 and len(gamelog.REB.values) > 0 and len(gamelog.STL.values) > 0 and len(gamelog.BLK.values) > 0 and len(gamelog.FG_PCT.values) > 0 and len(gamelog.FG3_PCT.values) > 0 and len(gamelog.FT_PCT.values) > 0:
            total_stats.append([np.round(np.mean(gamelog.PTS.values),2), np.round(np.mean(gamelog.AST.values),2),
                                np.round(np.mean(gamelog.REB.values),2), np.round(np.mean(gamelog.FG_PCT.values),2),
                                np.round(np.mean(gamelog.STL.values),2), np.round(np.mean(gamelog.FG3_PCT.values),2),
                                np.round(np.mean(gamelog.BLK.values),2), np.round(np.mean(gamelog.FT_PCT.values),2)])
        else:
            total_stats.append([0,0,0,0,0,0,0,0])
    return total_stats

def build_table_for_clusters(players, labels):
    data = []
    for i in range(len(players)):
        data.append([players[i][1], labels[i]])
    return pd.DataFrame(data, columns=['Player Name', 'Label'])


from sklearn.cluster import KMeans
import numpy as np
X = build_player_counting_stats(role)
kmeans = KMeans(n_clusters=7, random_state=0).fit(X)
table = build_table_for_clusters(role, kmeans.labels_)
print(table.shape)