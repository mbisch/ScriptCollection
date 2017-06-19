#!/bin/bash

export MIGR_SPLIT_SQL="YES"

sudo -H -u mbisch /home/mbisch/script/prepare_cvs.sh

sudo -H -u mbisch /home/mbisch/script/run_cvs2git_small.sh
sudo -H -u git    /home/mbisch/script/replace_repo_small.sh
sudo -H -u mbisch /home/mbisch/script/cleanup_small.sh

sudo -H -u mbisch /home/mbisch/script/run_cvs2git_add.sh
sudo -H -u git    /home/mbisch/script/replace_repo_add.sh 
sudo -H -u mbisch /home/mbisch/script/cleanup_add.sh


sudo -H -u mbisch /home/mbisch/script/run_cvs2git_jdekis.sh
sudo -H -u git    /home/mbisch/script/replace_repo_jdekis.sh
sudo -H -u mbisch /home/mbisch/script/cleanup_jdekis.sh


# SQL
if [ "$MIGR_SPLIT_SQL" == "YES" ]
then
  sudo -H -u mbisch /home/mbisch/script/run_cvs2git_sql.sh
  sudo -H -u git    /home/mbisch/script/replace_repo_sql.sh
  sudo -H -u mbisch /home/mbisch/script/cleanup_sql.sh
fi

sudo -H -u mbisch /home/mbisch/script/reset_gitolite.sh

sudo -H -u git    /home/mbisch/script/set_hooks.sh


# Split SQLs in subtrees
if [ "$MIGR_SPLIT_SQL" == "YES" ]
then
  sudo -H -u mbisch /home/mbisch/script/split_sql_subtree.sh
fi

sudo -H -u mbisch /home/mbisch/script/create_develop_branch.sh

sudo -H -u mbisch /home/mbisch/script/remove_masster_access.sh


