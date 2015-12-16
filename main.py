
import goldsberry
import pandas as pd
from playershotprofile import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--season', default="2015", type=str)
parser.add_argument('--gameid', default="0021500259", type=str)
parser.add_argument('--hv', default="home", type=str)
parser.add_argument('--fudge_factor', default=0.0, type=float)
parser.add_argument('--min_usg_player', default=0.08, type=float)
parser.add_argument('--min_usg_dbucket', default=0.2, type=float)
parser.add_argument('--min_usg_range', default=0.1, type=float)
args = parser.parse_args()

#playerid = '201939'
season = args.season
gameid = args.gameid
home_vis = args.hv
fudge_factor = args.fudge_factor
min_usg_player = args.min_usg_player
min_usg_dbucket = args.min_usg_dbucket
min_usg_range = args.min_usg_range

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

#print pcperc
#print dcperc
#print rcperc


pclk = sorted(pcperc, key=lambda x: x[1])
dclk = sorted(dcperc, key=lambda x: x[1])
rclk = sorted(rcperc, key=lambda x: x[1])

if total_shots == 0:
	print "Shot logs not posted for this game yet. Please wait till Halftime or the end of the game."
	exit()

t_perc = (float(total_bad_shots)/float(total_shots))

rcd = {'layup':'layups', 'long2':'long two-point shots', 'shortmid':'midrange two-pointers', 'outside':'three-point shots'}
dcd = {'open':'relatively open', 'tight':'tightly guarded', 'close':'closely guarded', 'wideopen':'unguarded'}

best_player = " ".join(allplayers[allplayers['PERSON_ID'] == pclk[0][0]]['DISPLAY_LAST_COMMA_FIRST'].iloc[0].split(", ")[::-1])
worst_player = " ".join(allplayers[allplayers['PERSON_ID'] == pclk[-1][0]]['DISPLAY_LAST_COMMA_FIRST'].iloc[0].split(", ")[::-1])

expln = "{0:.0f}%".format(t_perc * 100.0) 
expln += " of the shots the team is taking are bad, "
if t_perc < 0.5:
	expln += "which indicates that the team is taking mostly good shots. I'd recommend staying the course generally,"
	expln += " though if I had to quibble, I'd suggest making a few changes. "
else:
	expln += "which indicates that the team is taking mostly bad shots and we should make a few changes. "
expln += worst_player + " is the player taking the worst shots by far - he's taking "
expln += "{0:.0f}%".format(pclk[-1][1] * 100.0) + " bad shots, and using up " 
expln += "{0:.0f}%".format((float(playerperc[pclk[-1][0]][1])/float(total_shots)) * 100.0)
expln += " of the team's shots. Either bench him or take the ball out of his hands. "
expln += "Try to get the ball to " + best_player + " more: he is the team's most efficient"
expln += " player in terms of shot selection today, taking " + "{0:.0f}%".format(100 - (pclk[0][1] * 100.0)) + " good shots. " 
expln += "The team is also taking far too many " + rcd[rclk[-1][0]] + ", "
expln += "{0:.0f}%".format(rclk[-1][1] * 100.0) + " of which are bad shots, using up "
expln += "{0:.0f}%".format((float(rangeperc[rclk[-1][0]][1])/float(total_shots)) * 100.0)
expln += " of the team's shots. "
expln += "In particular, there seems to be an issue with shots of this kind which are "
expln += dcd[dclk[-1][0]] + ", so try to avoid those. "
expln += "Instead, try to take more " + dcd[dclk[0][0]] + " " + rcd[rclk[0][0]] + ", which "
expln += "the defence has been giving up but we've been making over the course of the season."

print expln

#print str(pclk[-1][0]) + ":" + str(pclk[-1][1])
#print dclk[-1][0] + ":" + str(dclk[-1][1])
#print rclk[-1][0] + ":" + str(rclk[-1][1])
#print "total shots: " + str(total_shots)
#print float(total_bad_shots)/float(total_shots)

