#!/usr/bin/bash

# using salt to make the passwords more secure. This salt is to be added after the password before hashing
# This way even if one gets the hash by some means, they can't guess the password.
# In this file we have choosen salt to be "ssl" (for obivious reasons)

salt="ssl"

player1=""  # initialising player1

login() {    # a function for logging into the game
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
                # read -s is for secret it will not show what the user is typying
                # but this will not output the default \n so for formatting purposes we added echo "" 
                                read -sp "Enter password: " password
                                echo ""
                # for hashing the password We used sha256sum command and to get the first field (where the hash is present) We used awk
                                password_hash=$( echo -n "$password$salt" | sha256sum | awk '{print $1}' )
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
                else  
                #Registration starts here
				#username not found in users.tsv 
                        echo "Username $name is not registered. Do you want to register?(y/n)"
                        read truth
			    #asking user to register or not
                        if [[ $truth == "y" || $truth == "Y" ]]; then
                                while true; do
                                        read -sp "choose a password for username $name: " password 
                                        echo ""
                                        read -sp "confirm password: " password1
                                        echo "" 
			    #asking to make a password and confirm password		
                                        if [[ $password == $password1 ]]; then
                                                echo "$name is registered successfully"
			    #user and password created
                                                password_hash=$( echo -n "$password$salt" | sha256sum | awk '{print $1}')
                                                echo -e "$name\t$password_hash" >> users.tsv
			    #user details added to users.tsv
                                                read -p "Do you want to login with this credentials?(y/n)" truth
                                                if [[ $truth == "y" || $truth == "Y" ]]; then
                                                        echo "login of player $name is successful"
                                                        player=$name
                                                        break 2
			    #asking whether to login with these credentials.If yes then the 2 while loops break and login fn stops
                                                else
                                                        break
			    #user might want to play with other credentials after registration then the loop continues
                                                fi
                                        else
                                                echo "Passwords do not match"
                                                continue
			    #Password ,confirm password makes user to choose and confirm password again in loop
                                        fi
                                done
                        else
			    #If user doesn’t want to register then again the loop continues
                                continue
                        fi
                fi
           fi
        done
  }

echo "Enter details for player1: "
login
player1=$player
echo "Enter details for player2: "
login
player2=$player
echo "$player1"
echo "$player2"
		#displaying player names before the game starts
python3 game.py "$player1" "$player2"






  
                        
