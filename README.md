# chess-jenny (Work in progress)
## Overview 
Chess jenny (chess generator) is designed to create and persist Chess puzzles. It's a script that runs Stockfish against itself indefinitely monitoring the game for certain criteria. 
Currently the types of puzzles it generates are: 
* Spot the killer move (extend an advantage significantly) 
* Spot the swing move (turn a disadvantage to an advantage) 
* Spot the absolute pin
* Mate in N scenarios   

## Setup
1. Ensure a MySQL connection and execute 'db_setup.sql'
2. Create a new config.ini file with your database credentials and place it in the 'generator' directory next to the runner.py file.
```
[DB_CREDENTIALS]
host=localhost
user=root
password=password
```
3. Run runner.py for a while to populate the db with puzzles
