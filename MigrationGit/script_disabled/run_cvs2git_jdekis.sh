#!/bin/bash

echo Start cvs2git jdekis repo

date

# Add repo
cd /home/mbisch/mig_cvs2git
rm /home/mbisch/script/logs/jdekis.log
cvs2git --options=jdekis.options > /home/mbisch/script/logs/jdekis.log 2>&1 

echo done


