#!/bin/bash

echo start replace repo Add
date

# Add repo
cd /home/git/repositories/jdekis.git 
rm -rf /home/git/repositories/jdekis.git/*
git init --bare  
cat /home/mbisch/mig_cvs2git/jdekis/blob/git-blob.dat /home/mbisch/mig_cvs2git/jdekis/tmp/git-dump.dat | git fast-import

#exit
echo done


