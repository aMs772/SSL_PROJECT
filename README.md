# SSL_PROJECT
Project of CS108 course. Task is to build a multi-user gamehub of atleast 3 games using pygames and integrate bash scripting for user authentication and show analytics of games.

This repository consists of the following directory structure

hub/ 

    ├── main.sh 

    ├── users.tsv

    ├── game.py

    ├── leaderboard.sh 
  
    ├── games/

       ├── computer-ticTacToe.py

       ├── computer-othello.py

       ├── computer-popit.py
  
       ├── tictactoe.py 
       
       ├── othello.py
              
       └── connect4.py 
       
    └── history.csv 

# INSTALLATION
``` bash
git clone <repository-url>
cd repo
pip install -r requirements.txt
```
# USAGE 

For playing games, go to terminal and type
``` bash
bash main.sh
```
then you will be prompted for usernames of players. If players arent logged in then you will be prompted for registration. After this a popup window for games menu will be opened. Click the game icon you wish to play and a popup window of that game will open. The games are turn based games and player's turn will be indicated. 

After the game is ended 
The winner will be shown on the screen followed by a screen asking for sortoption which is used by leaderboard.sh to print the leaderboard in terminal according to sortoption.
Matplot statistics would be shown in pygame window which on pressing space key shows the next screen which shows the player options of play again,quit,back to menu.

During the game for making the popup window full size, you can either press F11 or click on full screen option on top right corner

For popIt game, after completing your turn you must press space bar for completing your move

For playing against computer, enter the second player info is 
```bash
username = ###AI###
password = ###AI###
```

# RULES FOR GAMES

# Tic Tac Toe

Game board consists of a grid of 10*10 cells. In each cell a player must place X or O. One player places X and another O. Players play thier move one after another. The game ends when 5 X's or 5 O's are in a line. If all the cells are placed with X or O and nobody has won, then the game is a tie

For further info
```bash
https://en.wikipedia.org/wiki/Tic-tac-toe
```
# Connect 4

Game board consists of a grid of 7*7 cells. This game board is vertical and players have to drop a coin in one of the columns. players have to play one after another using different coloured coins. Player wins when any of their 4 coins lie on a line. If all the cells are filled and nobody has won then the game is a tie.

For further info
```bash
https://en.wikipedia.org/wiki/Connect_Four
```

# Othello 

Game board consists of a grid of 8*8 cells. One player plays with black coins while other player plays with white coins. Initially 2 black coins and 2 white coins are placed on the board alternatively. A player can place his coin only in places where after placing his coin, some of the opponents coins should be enclosed by his newly placed coin and another coin of him. There shouldnt be any empty coins between his two coins while placing his coin. After placing his coin all the coins of opponent enclosed by his newly placed coin another coin are replaced by his coins. Player play thier move alternatively and if a player has no valid moves then his turn is skipped. The game ends when there are no valid moves left. The player with highest number of coins is the winner

For further info
```bash
https://en.wikipedia.org/wiki/Othello
```

# PopIt

This game consists of multiple colred rows. Each row consists of multiple bubbles. A player in his move can pop any number of bubbles but only in a single row. Players play their move alternatively. The player who pops the last bubble loses

# Note
In computer mode only a 4*4 grid is implemented for tictactoe and othello, and only a 3*3 grid is implemented for popit
An alternate computer version of othello game is implemented in 8*8 grid
To play this alternate version click on connect$ game icon
In this alternate version the computer is greedy and may loose sometimes

# SOME ADDITIONAL INFO OF SOME FILES

# 1) main.sh

In order for players to play games, they must execute main.sh . Once main.sh is executed, it prompts for details of players
and registers the players who aren't found in users.tsv .It appends the details of newly registered players to users.tsv .
The passwords are hashed using sha256sum command for better security. After both players are successfully logged into the game, main.sh executes game.py and the players enter into the game window.

User authentication:

A player cannot play with himself.
Any 2 registered users cannot have the same username.
Players need to confirm password when registering.
Usernames and passwords can have whiteSpace characters (for now).

# 2) users.tsv

This file is intended to store the details of registered players and is empty initially. This file is a Tab Separated Values file. users.tsv doesn't store the passwords of players, instead it stores the hash (sha256) generated by sha256sum command.
Usernames and passwords-hash are separated by a tab. Each line stores details of one registered player. When a new player registers main.sh appends their details to users.tsv .

Game Interface:
After a successful login players are taken as input for game.py from main.sh

# 3) game.py

game.py uses the pygame library in the code to create the GUI(graphical user interface).

The file takes two player names as input and opens a window named Game Zone. The window has
background , headings and different game options: Tic Tac Toe, Othello, and Connect4 etc
with their logos.

The menu stays open and keeps running until the user selects a game or closes the window.
The user can click on any game logo to choose a game, and the program will open that game.
A loop is used to keep the window active and check for user actions like mouse clicks. The
screen is updated continuously so that everything appears smoothly.

Images, fonts, and sounds are taken from their respective folders and used in the program.
convert() and convert_alpha() are used to make image display faster and smoother.
Background music is also played to improve the experience. The window size is controlled
using variables, so it can be adjusted easily.

After players complete playing a game,they would be asked to whether play again or quit.
The program uses sys.exit() to properly close when the user exits the window.

# 4) pygame files

These files uses game class defined in game.py and take arguments from game.py using subprocess. But for quick checking and debugging you can directly run this file with 2 arguments.

# THANK YOU

Thank you for going through our repository and playing our games 

HAVE FUN PLAYING OUR GAMES






























