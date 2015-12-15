import goldsberry
import time

gdat = goldsberry.league.daily_scoreboard(time.strftime("%d/%m/%Y")).game_header()

pgames = 0
if len(gdat) > 0:
	for game in gdat:
		if game['GAME_STATUS_ID'] > 1:
			print "gamecode: " + game['GAMECODE'] + " gameid: " + game['GAME_ID']
			pgames += 1		
if pgames < 1:
	print "Sorry, there are no live games right now."


