
import goldsberry
import pandas as pd
from playershotprofile import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--season', default="2015", type=str)
parser.add_argument('--gameid', default="0021500259", type=str)
parser.add_argument('--hv', default="home", type=str)
args = parser.parse_args()

#playerid = '201939'
season = args.season
gameid = args.gameid
home_vis = args.hv
fudge_factor = 0.0
min_usg_player = 0.08
min_usg_dbucket = 0.2
min_usg_range = 0.1

bucketref = {
		'SHOT_DIST' : {	'default': 'outside', 
						'bucketlist' : [ (2.0, 'layup'), (9.0, 'shortmid'), (16.0, 'long2'), (23.0, 'outside') ]},
		'CLOSE_DEF_DIST' : {	'default': 'wideopen', 
						'bucketlist' : [ (2.0, 'tight'), (4.0, 'close'), (6.0, 'open'), (10.0, 'wideopen') ]},
		'PTS_TYPE' : {	'default': '2p', 
						'bucketlist' : [ (2, '2p'), (3, '3p') ]}
	}

def calcperc(tlk):
	retj = []
        for ent in tlk:
		retj.append((ent[0],float(ent[1][0])/float(ent[1][1])))
	return retj


allplayers = pd.DataFrame(goldsberry.PlayerList(season))

gdat = goldsberry.game.boxscore_summary(gameid).game_summary()[0]

home_players = allplayers[allplayers['TEAM_ID'] == gdat['HOME_TEAM_ID']]

visitor_players = allplayers[allplayers['TEAM_ID'] == gdat['VISITOR_TEAM_ID']]

home_list = home_players['PERSON_ID'].tolist()
visitor_list = visitor_players['PERSON_ID'].tolist()

if home_vis == 'home':
	player_list = home_list
	team_id = gdat['HOME_TEAM_ID']
else:
	player_list = visitor_list
	team_id = gdat['VISITOR_TEAM_ID']

shotlog = pd.DataFrame()
playerprofiles = {}

for playerid in player_list:

	#make player profile
	playerprofiles[playerid] = getplayershotprofile(playerid, bucketref)

	#append player shots in current game to shotlog
	plog = pd.DataFrame(goldsberry.player.shot_log(playerid).log())
	if not plog.empty:
		plog = plog[plog['GAME_ID'] == gameid]
		plog['PERSON_ID'] = playerid
		shotlog = shotlog.append(plog, ignore_index=True)

gameprofile = getgameshotprofile(shotlog.to_dict('records'), bucketref, playerprofiles)

tsplits_wl = goldsberry.team.splits(team_id, measuretype = 2).wins_losses()

efgw = 0.0

for drow in tsplits_wl:
	if drow['GROUP_VALUE'] == 'Wins':
		efgw = drow['EFG_PCT']

efgwf = efgw + fudge_factor

total_bad_shots = 0
total_shots = 0

playerperc = {}
dperc = {}
rangeperc = {}

for rangebucket in gameprofile:
	for dbucket in gameprofile[rangebucket]:
		for playerid in gameprofile[rangebucket][dbucket]:
			total_shots += gameprofile[rangebucket][dbucket][playerid]['total_shots']
			if playerid not in playerperc:
				playerperc[playerid] = [0,0]
			playerperc[playerid][1] += gameprofile[rangebucket][dbucket][playerid]['total_shots']
			if dbucket not in dperc:
				dperc[dbucket] = [0,0]
			dperc[dbucket][1] += gameprofile[rangebucket][dbucket][playerid]['total_shots']
			if rangebucket not in rangeperc:
				rangeperc[rangebucket] = [0,0]
			rangeperc[rangebucket][1] += gameprofile[rangebucket][dbucket][playerid]['total_shots']
			if gameprofile[rangebucket][dbucket][playerid]['efg'] <= efgwf:
				total_bad_shots += gameprofile[rangebucket][dbucket][playerid]['total_shots']
				playerperc[playerid][0] += gameprofile[rangebucket][dbucket][playerid]['total_shots']
				dperc[dbucket][0] += gameprofile[rangebucket][dbucket][playerid]['total_shots']
				rangeperc[rangebucket][0] += gameprofile[rangebucket][dbucket][playerid]['total_shots']

playerperci = playerperc.items()
dperci = dperc.items()
rangeperci = rangeperc.items()

playerperci = [vv for vv in playerperci if float(vv[1][1]) > min_usg_player*float(total_shots)]
dcperci = [vv for vv in dperci if float(vv[1][1]) > min_usg_dbucket*float(total_shots)]
rangeperci = [vv for vv in rangeperci if float(vv[1][1]) > min_usg_range*float(total_shots)]

pcperc = calcperc(playerperci)
dcperc = calcperc(dperci)
rcperc = calcperc(rangeperci)

print pcperc
print dcperc
print rcperc


pclk = sorted(pcperc, key=lambda x: x[1])
dclk = sorted(dcperc, key=lambda x: x[1])
rclk = sorted(rcperc, key=lambda x: x[1])

print str(pclk[-1][0]) + ":" + str(pclk[-1][1])
print dclk[-1][0] + ":" + str(dclk[-1][1])
print rclk[-1][0] + ":" + str(rclk[-1][1])
print "total shots: " + str(total_shots)
print float(total_bad_shots)/float(total_shots)

