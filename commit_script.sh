#!/bin/bash
read -p "Enter Username: " u_name
git config --global user.name "$u_name"
read -p "Enter Email: " u_email
git config --global user.email "$u_email"
read -p "Enter Commit Msg: " send_msg
git add .
git commit -m "$send_msg"
git push --repo http://"$u_name"@github.com/TheDemonfish/Capstone master

wait ${!}
echo "done"$'\r'
sleep 10