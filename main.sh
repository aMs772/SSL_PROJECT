#!/usr/bin/bash

player1=""  

login() {
        while true; do
                read -p "Enter username: " name
           if [[ $player1 == $name ]]; then                   
                   echo "Nice try"
                   echo "You can not play with yourself"
                   continue
           else
                if grep -q "^$name[[:space:]]" users.tsv; then  
                        while true; do
                                read -sp "Enter password: " password
                                echo ""
                                password_hash=$( echo -n "$password" | sha256sum | awk '{print $1}' )
                                if grep -q "^$name[[:space:]]$password_hash" users.tsv; then
                                        echo "login of player $name is successful"
                                        player=$name
                                        break 2
                                else
                                        echo "Nice try"
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
                        
