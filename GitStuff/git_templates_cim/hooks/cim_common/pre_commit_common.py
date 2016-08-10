#!/usr/bin/env python
# description: not implemented
# version: 0.1
# targets: ["pre-commit"]
# helpers: []

import sys, os, locale, posixpath
from subprocess import Popen,PIPE,STDOUT

from cim_common.which import *

def pre_commit_common(argv):
   """ Shell scripts """
   dirname = os.path.dirname(os.path.relpath(__file__))
   dirname = dirname.replace('\\','/')
   shell_scripts = []
   
   """ Check suffix """   
   shell_scripts += [posixpath.join(dirname, 'pre-commit_check_suffix.sh')]

   if len(shell_scripts)>0:
      sh_exe = which('sh.exe')
      if sh_exe == None:
         sh_exe = which('C:\Program Files\Git\bin\sh.exe')
      if sh_exe == None:
         sh_exe = which('C:\Program Files (x86)\Git\bin\sh.exe')            

      if sh_exe != None:          
         for script in shell_scripts:  
            proc = Popen([sh_exe,'--login','-c','--',script], shell=False, stdout=PIPE)
            proc.wait()
            encoding = locale.getdefaultlocale()[1]
            print((proc.communicate()[0]).decode(encoding))

            if proc.returncode != 0:
               print('rejected by local hook')
               sys.exit(proc.returncode)            
      else:
         print('sh.exe (.../Git/bin) not found')
         
   sys.exit(0)
         
if __name__ == "__main__":
   pre_commit_common(sys.argv[1:])

