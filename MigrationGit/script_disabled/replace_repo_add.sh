#!/bin/bash

echo start replace repo Add
date

# Add repo
cd /home/git/repositories/windekis_add.git 
rm -rf /home/git/repositories/windekis_add.git/*
git init --bare  
cat /home/mbisch/mig_cvs2git/Add/blob/git-blob.dat /home/mbisch/mig_cvs2git/Add/tmp/git-dump.dat | git fast-import

#exit
echo done


