#!/usr/bin/env python

from __future__ import print_function
import sys, os, datetime
import re, locale
import shutil
from builtins import range
import os
import winreg

def which(program):
   def is_exe(fpath):
      return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
   
   fpath, fname = os.path.split(program)
   if fpath:
      if is_exe(program):
         return program
   else:
      for path in os.environ["PATH"].split(os.pathsep):
         path = path.strip('"')
         exe_file = os.path.join(path, program)
         if is_exe(exe_file):
            return exe_file
   return None
 
k = None
try:
    r = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    k = winreg.OpenKey(r, r'SOFTWARE\GitForWindows')
except:
    print("GitForWindows not found in HKEY_LOCAL_MACHINE")
if k == None:
   try:
       r = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
       k = winreg.OpenKey(r, r'SOFTWARE\GitForWindows')
   except:
       print("GitForWindows not found in HKEY_CURRENT_USER")      

if(k != None):  
    install_path = winreg.QueryValueEx(k, 'InstallPath')[0]
    git_path =  os.path.join(install_path, 'bin/git.exe')
    assert os.path.exists(git_path), "Git path not found"
    os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = git_path
    print('using git: ' + git_path)
else:
    git_path = which('git.exe')
    if git_path == None:
        git_path = which('C:\Program Files\Git\bin\git.exe')    
    if git_path == None:
        git_path = which('C:\Program Files (x86)\Git\bin\git.exe') 
    if git_path == None:
        print("Git path not found")
        sys.exit(1)
    os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = git_path
    print('using git: ' + git_path)  
    
from git import Repo

config_root = 'C:\\Projekte\\windekis_src\\configuration\\git_templates_cim'

def add_unique_postfix(fn):
    if not os.path.exists(fn):
        return fn

    path, name = os.path.split(fn)
    name, ext = os.path.splitext(name)

    make_fn = lambda i: os.path.join(path, '%s%d%s' % (name, i, ext))

    for i in range(2, 1000):
        uni_fn = make_fn(i)
        if not os.path.exists(uni_fn):
            return uni_fn

    return None

    
def main(argv):
    StartDirectory = 'C:\\Projekte\\windekis_src\\'
    if len(argv) > 0:
       StartDirectory = argv[0]
       
    print(config_root) 

    if os.path.exists(os.path.join(config_root,'.git')):
        print('Update repo git_templates_cim')    
        repo = Repo(config_root)   
        o = repo.remotes.origin
        o.pull('--rebase')
    else:
        print('Clone repo git_templates_cim')
        os.makedirs(config_root)        
        Repo.clone_from('git@emeazrhsol03:git_templates_cim', config_root)
    
    template_dir = os.getenv('GIT_TEMPLATE_DIR', 'EMPTY')
    if template_dir != config_root:
        print('Temporarily set environment variable GIT_TEMPLATE_DIR to',config_root)
        os.environ['GIT_TEMPLATE_DIR'] = config_root   
    
    for dirname, dirnames, filenames in os.walk(StartDirectory):  
       # print path to all filenames.
       for dir in dirnames:
          if dir == 'hooks':
              parent_dir = os.path.abspath(os.path.join(dirname, dir, os.pardir))
              if os.path.split(parent_dir)[1] == '.git':
                  hook_dir = os.path.join(dirname, 'hooks')
                  hook_bak = add_unique_postfix(hook_dir + '_bak')
                  print('Backup hooks')
                  shutil.move(hook_dir,hook_bak)
                  repo_dir = os.path.abspath(os.path.join(dirname, os.pardir))
                  print('Reset hooks in repo: ', repo_dir)
                  Repo.init(repo_dir)
    
if __name__ == "__main__":
    main(sys.argv[1:])