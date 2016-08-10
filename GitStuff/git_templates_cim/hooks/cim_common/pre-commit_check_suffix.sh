#!/usr/bin/env bash

# return value not equal 0 for an error

#echo "pre-commit_check_suffix: start"

#GIT_PATH=`which git`
#echo $GIT_PATH

# Needed for the for loop, delimiter should be only the end of line and not also the whitespaces
IFS_BACKUP=$IFS
IFS=$(echo -en "\n\b")

# Get all staged .cbproj files
for PROJECT_FILE in $(git diff --name-only --staged | grep '^.*.cbproj$')
do
   # Search for <Suffix>_0</Suffix>
   #echo "Check file $PROJECT_FILE for Suffix"
   SUFFIX=`grep '^[ ]*<Suffix>_[0123456789][0123456789]*</Suffix>$' "${PROJECT_FILE}"`
   #echo "SUFFIX = \"$SUFFIX\""
   if [ -n "$SUFFIX" ]; then
      echo ""
      echo "Found the string <Suffix>_number</Suffix> in the file \"${PROJECT_FILE}\" which will cause TwineCompile to not link the project"
      
      # Restore IFS
      IFS=$IFS_BACKUP
      
      exit 1
   fi
done

#echo "pre-commit_check_suffix: everything is ok"

# Restore IFS
IFS=$IFS_BACKUP

exit 0
