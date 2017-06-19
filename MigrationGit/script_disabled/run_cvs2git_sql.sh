#!/bin/bash

echo Start cvs2git Sql repo

date

# Sql repo
cd /home/mbisch/mig_cvs2git
rm /home/mbisch/script/logs/Sql.log
cvs2git --options=Sql.options > /home/mbisch/script/logs/Sql.log 2>&1 

echo done


