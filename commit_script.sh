#!/bin/bash
read -p "Enter Username: " u_name
git config --global user.name "$u_name"
read -p "Enter Email: " u_email
git config --global user.email "$u_email"
read -s -p "Enter password: " u_pw
echo $'\r'
read -p "Enter Commit Msg: " send_msg

git add .
git commit -m "$send_msg"
git push --repo http://$u_name:$u_pw@github.com/TheDemonfish/Capstone

wait ${!}
echo "done"$'\r'
sleep 10