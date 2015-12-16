#Armory

####A live NBA shot-selection evaluation and adjustment recommendation system

######Summary

Armory is an automated shot-selection evaluator for basketball coaches to use during games. The idea is that coaches can run it at the end of each quarter of play to evaluate whether the shots their team is taking are efficient and how they can change their shot selection based on their historical efficiency, the shots the opposition seems to be allowing and the players they have available.

Armory returns advice about shot selection to the coach (i.e. the person running armory) in plain English.

######Authorship details

This is a project by Soham Sankaran (sgs44) for Yale's CS 458 (Fall 2015).  
  
Github URL: https://github.com/sohamsankaran/armory/

Armory wouldn't have been possible without the excellent py-goldsberry (https://github.com/bradleyfay/py-Goldsberry) by Bradley Fay and pandas (http://pandas.pydata.org/) by the pydata team.
Mad props to Bill Simmons and Grantland (RIP) for inspiring my obsession with the NBA.

######Installation

First, install git, python-dev|python-devel and pip if they aren't already installed. Next, if you haven't already, download armory as such:

	git clone https://github.com/sohamsankaran/armory.git

Next, navigate to the armory directory. Finally, execute the following command from inside the armory folder.

	cat requirements.txt | xargs -n 1 pip install

######Usage

	usage: main.py [-h] [--season SEASON] [--gameid GAMEID] [--hv HV]
        	       [--fudge_factor FUDGE_FACTOR] [--min_usg_player MIN_USG_PLAYER]
        	       [--min_usg_dbucket MIN_USG_DBUCKET]
        	       [--min_usg_range MIN_USG_RANGE]

	optional arguments:
 			-h, --help            show this help message and exit
  			--season SEASON (for example, 2015)
  			--gameid GAMEID
  			--hv HV (home or vis)
  			--fudge_factor FUDGE_FACTOR (between 0 and 1)
  			--min_usg_player MIN_USG_PLAYER (between 0 and 1)
  			--min_usg_dbucket MIN_USG_DBUCKET (between 0 and 1)
  			--min_usg_range MIN_USG_RANGE (between 0 and 1)
  			
gameids can be obtained from http://stats.nba.com, and current live game ids can be obtained by running the following command:

	python livegames.py

hv is to choose between running as the home(home) and visitor(vis) teams for a game.

fudge_factor is the percentage difference betwen the effective field goal percentage in wins and the effective field goal of a shot in the past allowed for a shot to be classified as good.

min_usg_player is the minimum percentage of the team's shots a player needs to take before he is considered for most or least efficient player.

min_usg_dbucket is the minimum percentage of shots within a certain defender classification required for that classification to be considered as the best or worst.

min_usg_range is the same as the above but for shot range classification.

Note that armory requires an active internet connection to run.

######Motivation

In basketball, especially outside of NBA professional basketball, coaches often use their intuition to make judgements shot selection and player efficiency to make adjustments on the fly. Augmenting these intuitions with empirical calculations of team performance on the fly would serve to improve the efficacy of these adjustments.
 
######Method

Effective field goal percentage is a useful measure of the expected value of a shot since it takes into account both a player's ability to make the shot and whether the shot is a two or three point shot. This allows for all types of shots to be compared on a relatively even playing field.

It is calculated as follows:

	effective_field_goal_percentage = (2_pointers_made + (1.5 x 3_pointers_made)) / total_shot_attempts

Armory works by comparing each shot each player on the team has taken in the current game so far to the effective field goal percentage for the same player in the same or similar situations in previous games in the season as measured across the metrics of distance from nearest defender and distance from basket to assign a boolean efficiency value, either good or bad, to each of these shots. A shot is said to be good if the effective field goal percentage for a player in that situation is >= the effective field goal percentage of the team, on average, in wins (+ some fudge factor). Having calculated this, the program then calculates the overall percentage of good shots the team is taking in this game as well as identifies the player taking the least efficient shots, the player taking the most efficient shots, the least efficient shots being taken, and the most efficent shots being underutilized while still on offer from the defence in the current game. This data is formatted into actionable advice for the coach in terms of strategy modification and returned in the form of a paragraph of plain English text.

######Implementation

Armory is written in python and is able to run in realtime against any NBA game. To run it, refer to the usage guide above.

######Future Work

In theory, this system could be expanded to any basketball league, including high school and college, where enough information about each shot is maintained and available in realtime. This could be fed in manually to the system during play if tracking technology is not available.

######Testing

Sample Test Inputs:

	python main.py --gameid 0021500160 --hv vis
	python main.py --gameid 0021500359
	python main.py --gameid 0021500160 --hv vis --min_usg_range 0.01





