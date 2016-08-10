#!/bin/bash

# This script checks gnome.org policy about how people are supposed to
# use git; the intent of the policy is to keep people from shooting
# themselves in the foot.
#
# Eventually, we'd like to have an ability to override policy; one way
# it could work is that if you did 'git push --exec=force' and you
# were a member of the right group, then run-git-or-special-cmd
# would set an environment variable that this script would interpret.

# Used in some of the messages
server=emeazrhsol03

GIT_DIR=$(git rev-parse --git-dir 2>/dev/null)

projects="ansbacher arab bab bbb bbva berenberg bes bhf bil bov bwl credit-suisse deltec goncim gutzwiller hiv jceh lbbw lblux lgt metropol morval nhb nomura pbihag piguet-galland pkb rbl vbv weg"

#is_valid_tag() {
#    for proj in $projects; do
#       [[ $1 == ${proj}-v* ]] && return 0 
#    done
#    echo 0
#    return 1
#}
is_valid_tag() {
    for proj in $projects; do
       [[ $1 =~ ${proj}-v[0-9].* ]] && return 0 
    done
    echo 0
    return 1
}
if is_valid_tag "arab-v1"; then echo 'True'; else echo False; fi 


exit 0