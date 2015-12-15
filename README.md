#Armory

####A live NBA shot-selection evaluation and adjustment recommendation system

	usage: main.py [-h] [--season SEASON] [--gameid GAMEID] [--hv HV]
        	       [--fudge_factor FUDGE_FACTOR] [--min_usg_player MIN_USG_PLAYER]
        	       [--min_usg_dbucket MIN_USG_DBUCKET]
        	       [--min_usg_range MIN_USG_RANGE]

	optional arguments:
 			-h, --help            show this help message and exit
  			--season SEASON
  			--gameid GAMEID
  			--hv HV [home or vis]
  			--fudge_factor FUDGE_FACTOR [between 0 and 1] 
  			--min_usg_player MIN_USG_PLAYER [between 0 and 1]
  			--min_usg_dbucket MIN_USG_DBUCKET [between 0 and 1]
  			--min_usg_range MIN_USG_RANGE [between 0 and 1]

In basketball, especially outside of NBA professional basketball, coaches often use their intuition to make judgements shot selection and player efficiency to make adjustments on the fly. Augmenting these intuitions with empirical calculations of team performance on the fly would serve to improve the efficacy of these adjustments.
 

Armory is an automated shot-selection evaluator for basketball coaches to use during games. The idea is that coaches can run it at the end of each quarter of play to evaluate whether the shots their team is taking are efficient and how they can change their shot selection based on their historical efficiency, the shots the opposition seems to be allowing and the players they have available.
 

The system works by comparing the shots each player on the team is taking to efficiency rates for the same player in the same or similar situations in previous games in the season as well as in previous seasons, with a bias toward recency, and assigning an efficiency score to each of these shots. The program then attempts to ascertain which types of shots being taken in the game are least efficient, what said shots have in common, and what efficient shots are being underutilized, then turns that into actionable advice.

Armory is written in python and is able to run in realtime against any NBA game. To run it, refer to the usage guide above.

In theory, this system could be expanded to any basketball league, including high school and college, where enough information about each shot is maintained and available in realtime. This could be fed in manually to the system during play if tracking technology is not available.

Test Inputs:

	python main.py --gameid 0021500160 --hv vis
	python main.py --gameid 0021500359
	python main.py --gameid 0021500160 --hv vis --min_usg_range 0.01





