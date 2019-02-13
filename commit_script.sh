#!/bin/bash
read -p "Enter Username: " u_name
git config --global user.name "$u_name"
read -p "Enter Email: " u_email
git config --global user.email "$u_email"
read -p "Enter Commit Msg: " send_msg
git add .
git commit -m "$send_msg"
git push http://github.com/TheDemonfish/Capstone master << `echo "$u_name"`

wait ${!}
echo "done"$'\r'
sleep 10