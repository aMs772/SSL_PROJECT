#!/bin/bash
#computes wins, losses, and W/L ratio for each player per game.
sort_option=$1
awk -F, '
{
    game = $4
    gsub(/\r/, "", game)
    win_id = game "," $1
    lose_id = game "," $2

    wins[win_id]++
    losses[lose_id]++
    
    all_players[win_id] = 1
    all_players[lose_id] = 1
}
END {
    for (id in all_players) {
        split(id, info, ",")
        w = wins[id] + 0
        l = losses[id] + 0
        
        if (l == 0) { ratio = w }
        else { ratio = w / l }
        
        print info[1] "," info[2] "," w "," l "," ratio
    }
}' history.csv > data.txt #stores the data into data.txt
#according to sort option prints the table in terminal
if [ "$sort_option" == "L" ]; then
    col=4
elif [ "$sort_option" == "W/L" ]; then
    col=5
else
    col=3
fi
#shows the table
for g in TicTacToe Othello Connect4 Popit; do
    echo "--- $g ---"
    echo "PLAYER|WINS|LOSSES|W/L"
    
    grep "^$g," data.txt | sort -t, -k$col -nr | awk -F, '{print $2 "|" $3 "|" $4 "|" $5}'
    
    echo ""
done | column -t -s "|"
