import goldsberry
import pandas as pd

# old test script

playerid = '201939'
gameid = '0021500268'

shotlog = pd.DataFrame(goldsberry.player.shot_log(playerid).log())

pbp = pd.DataFrame(goldsberry.game.play_by_play(gameid).plays())

shotdb = pd.DataFrame(goldsberry.player.shot_dashboard(playerid).closest_defender())


print shotlog
print pbp
print list(pbp.columns.values)
print pbp.head()
print shotdb
print list(shotdb.columns.values)


