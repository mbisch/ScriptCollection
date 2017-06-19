#!/bin/bash

echo start replace repo Small
date

cd /home/git/repositories/windekis.git 
rm -rf /home/git/repositories/windekis.git/*
git init --bare  
cat /home/mbisch/mig_cvs2git/Small/blob/git-blob.dat /home/mbisch/mig_cvs2git/Small/tmp/git-dump.dat | git fast-import


echo done


