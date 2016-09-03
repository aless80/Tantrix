# Tantrix
Python code for the Tantrix game

## Launch server and two clients
cd ~/tantrix/
python ./server.py
python ./tantrix.py
python ./tantrix.py

## Description of this version
In version 12 I fixed several bugs with change of turn, see post_confirm in deck.py. cfg.history records the moves.
A known bug to fix happens when a forced tile cannot be placed because it causes an impossible tile with three colors. 
Player name cannot be already taken and must start with non-numeric character

## TODO
confirm dialog when quit
are random always the same sequence? otherwise I would have to communicate extracted tile with server!
colors: create dialog for solitaire
alert when quitting wroom. self problem in clientListener
quit server more gracefully if channel is already taken?
Quit game goes back to room?
Shift with two players: once I shifted one of them before confirming. I saw error: "move: You cannot move the tile as it is to this hexagon"
Check if score works
TRYING is still needed?

#BUG
put tile in other player's tab

#BUG
"Error in motionCallback. itemids=" because id is None

#BUG
Once I saw: no turn change after single forced tile. I think i cannot reproduce this in debug mode
#BUG 
Once I saw: 1 tile, shift down, place tile next to it, it says "is not adjacent"

#BUG
1 forced tile is shown even if it leads to an impossible place because of 3 colors
	impossible_neighbor is only called in is_confirmable
	Plan: Add impossible_neighbor check to check_forced?, but I have to consider a virtual tile somehow
check_forced found a tile "s" with 3 neighs. 
for each of the tiles fitting there:
	find the possible orientations
	for each orientation:
		check=impossible_neighbor(self, rowcolnum, add_tilenum_at_rowcolnum_rot = [1, (0,0,0), 60])
		if check = False, break first for loop
	if check contains only True:
		do not add s
	else: 
		add s

Test:
cfg.deck.get_neighboring_colors((0,1,0), add_tilenum_at_rowcolnum_rot = [1, (0,0,0), 0])  #ryybrb	[('b', 0, 0)]
cfg.deck.get_neighboring_colors((0,1,0), add_tilenum_at_rowcolnum_rot = [1, (0,0,0), 60]) #bryybr	[('y', 0, 0)]



