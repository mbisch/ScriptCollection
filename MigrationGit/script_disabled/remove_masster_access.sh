#!/bin/bash


echo reset gitolite

cd /home/mbisch/gitolite-admin

cp /home/mbisch/gitolite-conf/gitolite.conf.on2 /home/mbisch/gitolite-admin/conf/gitolite.conf
git commit -a -m 'disable master access'
git push

#exit
echo done


