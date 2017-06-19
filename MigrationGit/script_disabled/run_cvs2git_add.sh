#!/bin/bash

echo Start cvs2git Add repo

date

# Add repo
cd /home/mbisch/mig_cvs2git
rm /home/mbisch/script/logs/Add.log
cvs2git --options=Add.options > /home/mbisch/script/logs/Add.log 2>&1 

echo done


