#!/bin/bash

echo start cvs2git Small Repo
date

echo $HOME

# Small repo
cd /home/mbisch/mig_cvs2git
rm /home/mbisch/script/logs/Small.log
cvs2git --options=Small.options > /home/mbisch/script/logs/Small.log 2>&1 

echo done
date


