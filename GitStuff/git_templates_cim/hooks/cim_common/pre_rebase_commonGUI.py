#!/usr/bin/env python
# description: Detects if your rebase will rewrite commits that have been propagated to other branches, and stops the rebase if so.
# version: 0.1
# targets: ["pre-rebase"]
# helpers: []

import sys, subprocess, locale
try:
    # for Python2
    import Tkinter as tk
    import tkMessageBox as mb
except ImportError:
    # for Python3
    import tkinter as tk
    import tkinter.messagebox as mb
    

def pre_rebase_common(argv):

   target_branch = ''
   current_branch = ''
   encoding = locale.getdefaultlocale()[1] 

   if len(argv) > 0:
      target_branch = argv[0]   

   if len(argv) > 1:
      root_branch = argv[1].strip()      
   else:
      root_branch = subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD']).decode(encoding).strip()
   
   print('try to rebase ' + root_branch + ' onto ' + target_branch + '\n')       
      
   commits = subprocess.check_output(['git','rev-list',target_branch + '..' + root_branch]).decode(encoding).split()
   if len(commits) > 0:
      latest_commit = commits[-1]     
      all_branches_with_commit = subprocess.check_output(['git','branch','-a','--contains',latest_commit]).decode(encoding).split('\n')

      other_branches_with_commit = list(map(lambda s: s.lstrip('*'),all_branches_with_commit))      
      other_branches_with_commit = list(map(lambda s: s.strip(),other_branches_with_commit))
      other_branches_with_commit = list(filter(None, other_branches_with_commit))      
      other_branches_with_commit = list(filter(lambda i: i != root_branch, other_branches_with_commit))       
        
      if len(other_branches_with_commit) > 0:
         Message = "Running this rebase would cause commit " + latest_commit  + " be rewritten, but it's included in the history of branch " + " ,".join(other_branches_with_commit) + "\n\n"
         Message += subprocess.check_output(['git','show','--pretty=oneline',latest_commit]).decode(encoding)
         print(Message)   
         Message += "\n\nRebase anyway?"
         
         top = tk.Tk()
         top.withdraw()
         result = mb.askquestion("Override rebase hook?", Message, icon='warning',default='no')
         if result == 'yes':
            print('Override: Yes')
            return 0
         else:
            print('Override: No')
            return 1
      
      return 0
         
if __name__ == "__main__":
   pre_rebase_common(sys.argv[1:])
