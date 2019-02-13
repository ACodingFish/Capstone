#!/bin/bash

read -p "Enter Username: " u_name
git config --global user.name "$u_name"
read -p "Enter Email: " u_email
git config --global user.email "$u_email"
git push --set-upstream http://github.com/TheDemonfish/Capstone master
wait ${!}
echo "done"
sleep 10