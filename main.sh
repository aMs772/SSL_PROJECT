#!/usr/bin/bash

player1=""  # initialising player1

login() {    # a function for logging into the game
    # while is written for lines 36,37,38 etc.
        while true; do
                read -p "Enter username: " name
           if [[ $player1 == $name ]]; then                  # not allowing a player to play with himself
                   echo "Nice try"
                   echo "You can not play with yourself"
                   continue
           else
                if grep -q "^$name[[:space:]]" users.tsv; then  # finding username in users.tsv
                                                                #  [[:space:]] matches any whitespace character including \n
                                                                # -q is for quiet i.e. not to print anything on standard output
                        while true; do
                # read -s is for secret it will not show what theuser is typying
                # but this will not output the default \n so for formatting purposes we added echo "" 
                                read -sp "Enter password: " password
                                echo ""
                # for hashing the password We used sha256sum command and to get the first field (where the hash is present) We used awk
                                password_hash=$( echo -n "$password" | sha256sum | awk '{print $1}' )
                # matching password in users.tsv
                                if grep -q "^$name[[:space:]]$password_hash" users.tsv; then
                                        echo "login of player $name is successful"
                                        player=$name
                # if login is completed we can break out of all loops
                                        break 2
                                else
                                        echo "Nice try"
                # sometimes the user might type incorrect username, hence to not get stuck in the loop,
                # Hence we are confirming whether the username is correct or not?
                                        read -p "Is your username $name?(y/n)" truth
                                        if [[ $truth == "y" || $truth == "Y" ]]; then
                                                continue
                                        else
                                                break
                                        fi
                                fi
                        done
                else   ### need to do registration part.
                fi
           fi
        done
  }
                        
