#!/bin/bash

echo set symlink for hooks
date


echo set hooks

for i in $( ls /home/git/repositories/ ); do
   cd /home/git/repositories/$i/hooks/
   ln -s  /home/git/hooks/pre-receive
done

#exit
echo done

