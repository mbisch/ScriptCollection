#!/bin/bash

export MIGR_SPLIT_SQL="YES"

echo start
date

echo start rsync 1
rsync --exclude 'memorial*' --exclude sungard --delete-before -avz -e ssh oracle@emeazrhsol01:/app/cvs /app/


echo delete converted cvs 
rm -rf  /app/split_cvs/cvs_small/repository/CVSROOT
rm -rf  /app/split_cvs/cvs_small/.lock
rm -rf  /app/split_cvs/cvs_small/repository/windekis/*
rm -rf  /app/split_cvs/cvs_small/repository/jdekis/*
rm -rf  /app/split_cvs/cvs_add/repository/CVSROOT
rm -rf  /app/split_cvs/cvs_add/.lock
rm -rf  /app/split_cvs/cvs_add/repository/windekis/*

if [ "$MIGR_SPLIT_SQL" == "YES" ]
then
  rm -rf  /app/split_cvs/cvs_sql/repository/CVSROOT
  rm -rf  /app/split_cvs/cvs_sql/.lock
  rm -rf  /app/split_cvs/cvs_sql/repository/windekis/
fi



echo start rsync 2
rsync -av --iconv=CP1252,utf8 /app/cvs/repository /app/split_cvs/cvs_small/

echo start rsync 3
rsync -av --iconv=CP1252,utf8 /app/cvs/.lock /app/split_cvs/cvs_small/


echo copy broken files explicitly
cp -r "/app/Broken_Latin1/windekis/Weg/RMS/SQL/2007/1010/03 Verknüpfung WinDekis - RMS Datenbanken/CVS/fileattr.xml" "/app/split_cvs/cvs_small/repository/windekis/Weg/RMS/SQL/2007/1010/"
cp "/app/Broken_Latin1/windekis/Weg/Windekis/WinDekis/Out32/Vertrag Test/164_BV1 Basisvertrag natürliche Personen.pdf,v" "/app/split_cvs/cvs_small/repository/windekis/Weg/Windekis/WinDekis/Out32/Vertrag Test/"
cp "/app/Broken_Latin1/windekis/Dexia/SQL/AccessControl/Version 1.00/WinDekis Zugriffskonzept für Dexia.doc.v" "/app/split_cvs/cvs_small/repository/windekis/Dexia/SQL/AccessControl/Version 1.00/"


echo move add files
cd /app/split_cvs/cvs_small/repository/windekis

find . -type f -regextype  posix-extended  -iregex '.*\.(obj,v|dll,v|csm,v|tds,v|drc,v|~de,v|dsw,v|map,v|met,v|mlt,v|res,v|obr,v|zip,v|zipx,v|exe,v|local,v|dsk,v|xls,v|status,v|ilc,v|ild,v|ilf,v|ils,v|pch,v|doc,v|dot,v|docx,v|docm,v|dotx,v|dotm,v|docb,v|xls,v|xlsx,v|xlsm,v|xltx,v|chm,v|ppt,v|pptx,v|pdf,v|bad,v|rar,v)|(.*?(\bOUT32\b)[^$]*)|[^~]+ [\~]+[^.]+|[^~]+[\~]+[^.]+[\.]+[^.]+|[^.]+[\.]+[#]+[^/]+|(.*?(\b__history\b)[^$]*)|(.*?(\b00\ CvsUtils\b)[^$]*)|(.*?(\b01\ Dokumentation\b)[^$]*)|(.*?(\b02\ Komponenten\b)[^$]*)|(.*?(\b04\b)\sPräsentation[^$]*)|(.*?(\b05\ Help\b)[^$]*)|(.*?(\b/Dokumente/\b)[^$]*)|(.*?(\b/windekis/\b)[^/]*(\b/Doku/\b)[^$]*)' -exec sh -c '
  for x do
    mkdir -p "$0/${x%/*}"
    mv "$x" "$0/$x"
  done
' "/app/split_cvs/cvs_add/repository/windekis/" {} +

# Split SQL

if [ "$MIGR_SPLIT_SQL" == "YES" ]
then

echo move sql folders

find . -iregex  '.*\(sql\)$' -type d -exec sh -c '
  for x do
    mkdir -p "$0/${x%/*}"
    mv "$x" "$0/$x"
  done
' "/app/split_cvs/cvs_sql/repository/windekis/" {} +

  rm --force /app/split_cvs/cvs_sql/repository/windekis/.gitignore,v
  cp /app/split_cvs/cvs_small/repository/windekis/gitignore_small.txt,v /app/split_cvs/cvs_sql/repository/windekis/.gitignore,v
fi

rm --force /app/split_cvs/cvs_small/repository/jdekis/.gitignore,v
cp /app/split_cvs/cvs_small/repository/windekis/gitignore_small.txt,v  /app/split_cvs/cvs_small/repository/jdekis/.gitignore,v

mv --force /app/split_cvs/cvs_small/repository/windekis/gitignore_small.txt,v /app/split_cvs/cvs_small/repository/windekis/.gitignore,v
mv --force /app/split_cvs/cvs_small/repository/windekis/gitignore_add.txt,v   /app/split_cvs/cvs_add/repository/windekis/.gitignore,v 


find /app/split_cvs/cvs_small/repository/windekis/. -type d -empty -delete
cp -r /app/split_cvs/cvs_small/repository/CVSROOT /app/split_cvs/cvs_add/repository/
cp -r /app/split_cvs/cvs_small/.lock /app/split_cvs/cvs_add/


if [ "$MIGR_SPLIT_SQL" == "YES" ]
then
  cp -r /app/split_cvs/cvs_small/repository/CVSROOT /app/split_cvs/cvs_sql/repository/
  cp -r /app/split_cvs/cvs_small/.lock /app/split_cvs/cvs_sql/
fi


#rm -rf /app/cvs

echo finished rsync and split
date


