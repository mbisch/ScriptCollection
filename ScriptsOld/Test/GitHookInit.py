#!/usr/bin/env python

from __future__ import print_function
import sys, os, datetime
import re, locale
import shutil
from git import Repo
from builtins import range

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

    if os.path.exists(config_root):
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