import goldsberry
import pandas as pd

#playerid = '201939'
gameid = '0021500268'
season = '2015'

allplayers = pd.DataFrame(goldsberry.PlayerList(season))

gdat = goldsberry.game.boxscore_summary(gameid).game_summary()[0]

home_players = allplayers[allplayers['TEAM_ID'] == gdat['HOME_TEAM_ID']]

visitor_players = allplayers[allplayers['TEAM_ID'] == gdat['VISITOR_TEAM_ID']]

home_list = home_players['PERSON_ID'].tolist()
visitor_list = visitor_players['PERSON_ID'].tolist()

hshotlog = pd.DataFrame()

for playerid in home_list:
	plog = pd.DataFrame(goldsberry.player.shot_log(playerid).log())
	if not plog.empty:
		plog = plog[plog['GAME_ID'] == gameid]
		plog['PERSON_ID'] = playerid
		hshotlog = hshotlog.append(plog, ignore_index=True)


vshotlog = pd.DataFrame()

for playerid in visitor_list:
	plog = pd.DataFrame(goldsberry.player.shot_log(playerid).log())
	if not plog.empty:
		plog = plog[plog['GAME_ID'] == gameid]
		plog['PERSON_ID'] = playerid
		vshotlog = vshotlog.append(plog, ignore_index=True)

#pbp = pd.DataFrame(goldsberry.game.play_by_play(gameid).plays())



#shotdb = pd.DataFrame(goldsberry.player.shot_dashboard(playerid).closest_defender())


#print shotlog
#print shotdb
#print list(shotdb.columns.values)
#print gdat
#print home_players
#print visitor_players

print hshotlog
print vshotlog
