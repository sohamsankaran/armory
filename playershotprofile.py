import goldsberry
import pandas as pd
from copy import deepcopy

def getbucket(shot, criterion, bucketref):
	for bucket in bucketref[criterion]['bucketlist']:
		if shot[criterion] <= bucket[0]:
			return bucket[1]
	return bucketref[criterion]['default']


def getplayershotprofile(playerid, bucketref):

	shotlist = goldsberry.player.shot_log(playerid).log()

	playerprofile = {
		'layup' : {
			'tight' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'close' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'open' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'wideopen' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None}
		},
		'shortmid' : {
			'tight' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'close' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'open' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'wideopen' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None}
		},
		'long2' : {
			'tight' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'close' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'open' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'wideopen' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None}
		},
		'outside' : {
			'tight' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'close' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'open' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None},
			'wideopen' : {'2p' : [0, 0], '3p' : [0, 0], 'efg' : None}
		}
	}



	for shot in shotlist:
		shot_range = getbucket(shot, 'SHOT_DIST', bucketref)
		defender_range = getbucket(shot, 'CLOSE_DEF_DIST', bucketref)
		shot_type = getbucket(shot, 'PTS_TYPE', bucketref)
		if shot['FGM']:
			playerprofile[shot_range][defender_range][shot_type][0] += 1
		playerprofile[shot_range][defender_range][shot_type][1] += 1

	for sbucket in playerprofile:
		for dbucket in playerprofile[sbucket]:
			kbucket = playerprofile[sbucket][dbucket]
			totalshots = kbucket['3p'][1] + kbucket['2p'][1]
			if totalshots:
				kbucket['efg'] = ((1.5 * float(kbucket['3p'][0])) + float(kbucket['2p'][0])) / float(totalshots)

	return playerprofile

def getgameshotprofile(shotlog, bucketref, playerprofiles):
	gameprofile = {
		'layup' : {
			'tight' : {},
			'close' : {},
			'open' : {},
			'wideopen' : {}
		},
		'shortmid' : {
			'tight' : {},
			'close' : {},
			'open' : {},
			'wideopen' : {}
		},
		'long2' : {
			'tight' : {},
			'close' : {},
			'open' : {},
			'wideopen' : {}
		},
		'outside' : {
			'tight' : {},
			'close' : {},
			'open' : {},
			'wideopen' : {}
		}
	}

	empty_player = {'shots_made' : 0, 'total_shots' : 0, 'efg' : 0.0}

	for shot in shotlog:
		shot_range = getbucket(shot, 'SHOT_DIST', bucketref)
		defender_range = getbucket(shot, 'CLOSE_DEF_DIST', bucketref)
		playerid = shot['PERSON_ID']
		if playerid not in gameprofile[shot_range][defender_range]:
			gameprofile[shot_range][defender_range][playerid] = deepcopy(empty_player)
			gameprofile[shot_range][defender_range][playerid]['efg'] = playerprofiles[playerid][shot_range][defender_range]['efg']
		gameprofile[shot_range][defender_range][playerid]['total_shots'] += 1
		if shot['FGM']:
			gameprofile[shot_range][defender_range][playerid]['shots_made'] += 1

	return gameprofile

