#!/bin/bash

echo remove symlink for hooks
date


echo remove hooks

for i in $( ls /home/git/repositories/ ); do
   cd /home/git/repositories/$i/hooks/
   rm pre-receive
done

#exit
echo done

