#!/bin/bash


echo reset gitolite

cd /home/mbisch/gitolite-admin
git pull --rebase

cp /home/mbisch/gitolite-conf/gitolite.conf.off /home/mbisch/gitolite-admin/conf/gitolite.conf
git commit -a -m 'disable repos'
git push

cp /home/mbisch/gitolite-conf/gitolite.conf.on /home/mbisch/gitolite-admin/conf/gitolite.conf
git commit -a -m 'enable repos'
git push

#exit
echo done


