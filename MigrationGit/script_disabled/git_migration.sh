#!/bin/bash

echo start
date

echo start rsync 1
rsync --exclude 'memorial*' --exclude sungard  -avz -e ssh oracle@emeazrhsol01:/app/cvs /app/

echo start rsync 2
rsync -av  --iconv=CP1252,utf8 /app/cvs/repository /app/split_cvs/cvs_small/

echo start rsync 3
rsync -av  --iconv=CP1252,utf8 /app/cvs/.lock /app/split_cvs/cvs_small/

rm -rf  /app/split_cvs/cvs_add/repository/CVSROOT
rm -rf  /app/split_cvs/cvs_add/.lock 
rm -rf  /app/split_cvs/cvs_add/repository/windekis/*

cd /app/split_cvs/cvs_small/repository/windekis

find . -type f -regextype  posix-extended  -iregex '.*\.(obj,v|csm,v|tds,v|drc,v|~de,v|dsw,v|map,v|met,v|mlt,v|res,v|obr,v|zip,v|zipx,v|ex e,v|local,v|dsk,v|xls,v|status,v|ilc,v|ild,v|ilf,v|ils,v|pch,v|doc,v|dot,v|docx,v|docm,v|dotx,v|dotm,v|docb,v|xls,v|xlsx,v|xlsm,v|xltx,v|chm,v|ppt,v|pptx,v|pdf,v|bad,v|rar,v)|(.*?(\bOUT32\b)[^$]*)|[^~]+ [\~]+[^.]+|[^~]+[\~]+[^.]+[\.]+[^.]+|[^.]+[\.]+[#]+[^/]+|(.*?(\b__history\b)[^$]*)|(.*?(\b00\ CvsUtils\b)[^$]*)|(.*?(\b01\ Dokumentation\b)[^$]*)|(.*?(\b02\ Komponenten\b)[^$]*)|(.*?(\b04\b)\sPräsentation[^$]*)|(.*?(\b05\ Help\b)[^$]*)|(.*?(\b/Dokumente/\b)[^$]*)|(.*?(\b/windekis/\b)[^/]*(\b/Doku/\b)[^$]*)' -exec sh -c '
  for x do
    mkdir -p "$0/${x%/*}"
    mv "$x" "$0/$x"
  done
' "/app/split_cvs/cvs_add/repository/windekis/" {} +


find /app/split_cvs/cvs_small/repository/windekis/. -type d -empty -delete
cp -r /app/split_cvs/cvs_small/repository/CVSROOT /app/split_cvs/cvs_add/repository/
cp -r /app/split_cvs/cvs_small/.lock /app/split_cvs/cvs_add/


rm -rf /app/cvs

echo finished rsync and split
date

# Small repo
cd /home/mbisch/mig_cvs2git
rm /home/mbisch/script/logs/Small.log
cvs2git --options=Small.options > /home/mbisch/script/logs/Small.log 2>&1 

sudo -u git cd /home/git/repositories/windekis.git 
rm -rf /home/git/repositories/windekis.git/*
sudo -u git git init --bare  
sudo -u git cat /home/mbisch/mig_cvs2git/Small/blob/git-blob.dat /home/mbisch/mig_cvs2git/Small/tmp/git-dump.dat | git fast-import
rm -rf /home/mbisch/mig_cvs2git/Small/blob/*
rm -rf /home/mbisch/mig_cvs2git/Small/tmp/* 

echo finish small repo
date

# Add repo
cd /home/mbisch/mig_cvs2git
rm /home/mbisch/script/logs/Add.log
cvs2git --options=Add.options > /home/mbisch/script/logs/Add.log 2>&1 

cd /home/git/repositories/windekis_add.git 
rm -rf /home/git/repositories/windekis_add.git/*
sudo -u git git init --bare  
sudo -u git cat /home/mbisch/mig_cvs2git/Add/blob/git-blob.dat /home/mbisch/mig_cvs2git/Add/tmp/git-dump.dat | git fast-import
rm -rf /home/mbisch/mig_cvs2git/Add/blob/*
rm -rf /home/mbisch/mig_cvs2git/Add/tmp/* 

echo finish add repo
date

cd /home/mbisch/gitolite-admin
cp /home/mbisch/gitolite-conf/gitolite.conf.off /home/mbisch/gitolite-admin/conf/
git commit -a -m 'disable repos'
git push

cp /home/mbisch/gitolite-conf/gitolite.conf.on /home/mbisch/gitolite-admin/conf/
mbisch git commit -a -m 'enable repos'
mbisch git push

#exit
echo done


