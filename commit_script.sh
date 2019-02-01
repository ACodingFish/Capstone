#!/bin/bash

read -p "Enter Commit Msg: " send_msg
git add .
git commit -m "$send_msg"
git push http://github.com/TheDemonfish/Capstone master
wait ${!}