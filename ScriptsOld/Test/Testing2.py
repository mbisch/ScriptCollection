#!/usr/bin/env python

from __future__ import print_function
from git import Repo
import sys, re, os, operator, locale, datetime
    
### Globals    
tag_re = re.compile('(.+)(?=-v[0-9])(-)(.*)')
log_re = re.compile( '([0-9]{4}-[0-9]{2}-[0-9]{2})(\s+)(\({1}[^\)]*\){1}\s?)?(.*)')

encoding = locale.getdefaultlocale()[1] 

def get_tags(repo,main_branch,project_name,current_tag):
    """List of ordered tags for project smaller version or older than current tag"""
    tag_range = []
    project_tag_re = re.compile(project_name + '-v[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+_b[0-9]+-?.*')
    project_tags = {}
    
    current_version_str = '99999'+'99999'+'99999'+'99999'+'99999' 
    current_tag_date = 9999999999 
    if current_tag != "":
       if project_tag_re.match(current_tag):
           print('CURRENT TAG: ',current_tag)
           versions = re.findall(r'\d+',current_tag)[:5]
           current_version_str = str(versions[0]).zfill(5) + str(versions[1]).zfill(5) + str(versions[2]).zfill(5) + str(versions[3]).zfill(5) + str(versions[4]).zfill(5)
       else:       
           for tag in repo.tags:
               if current_tag == str(tag):
                   current_tag_date = tag.commit.committed_date                

    for tag in repo.tags:
        tag_str = str(tag)
        if project_tag_re.match(tag_str):
            if tag.commit.committed_date <= current_tag_date:
                branches = repo.git.branch('--contains',tag_str).split('\n')
                if len(branches)> 0 and sum(branch[0:1] == '*' for branch in branches):
                    versions = re.findall(r'\d+',tag_str)[:5]
                    version_str = str(versions[0]).zfill(5) + str(versions[1]).zfill(5) + str(versions[2]).zfill(5) + str(versions[3]).zfill(5) + str(versions[4]).zfill(5) 
                    if version_str <= current_version_str:
                        project_tags[tag_str] = version_str
                     
        if tag_str == 'bab-v1.98.00.0_b0-Start':
            project_tags['bab-v1.98.00.0_b0-Start'] = '00000'+'00000'+'00000'+'00000'+'00000'
            
    return sorted(project_tags.items(), key=operator.itemgetter(1))  
       
def change_log(repo,start_commit, end_commit, project_name):
    """Run the git command that outputs the merge commits (both subject
    and body) to stdout, and return the output.
    """
    log_txt = '';
    project_tag_re = re.compile('(tag:\s+)(' + project_name + '-v[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+_b[0-9]+-?[^\)]*)(.*)')
    print(start_commit,end_commit)
    messages = repo.git.log('--oneline','--date=short','--pretty=%ad %d %s',start_commit+'..'+end_commit).split('\n')

    for msg in messages:
       log_msg = log_re.search(msg)
       if log_msg != None:
           if log_msg.group(3) != None:
              for tag_expr in log_msg.group(3).split(u','):
                 tag_vers = project_tag_re.search(tag_expr)
                 if tag_vers != None:
                    print('Version:',tag_vers.group(2))
                    verstion_txt = 'Version: ' + tag_vers.group(2)
                    if len(log_txt) > 0:
                        log_txt += '\n'
                    log_txt += '-'.rjust(len(verstion_txt)+4,'-') + '\n'
                    log_txt += '- ' + verstion_txt + ' -\n'
                    log_txt += '-'.rjust(len(verstion_txt)+4,'-') + '\n'
           if log_msg.group(4) != '*** empty log message ***':
              log_txt += log_msg.group(1) + ' ' + log_msg.group(4) + '\n'
    return log_txt
        
        
def main(argv):
    if len(argv) < 1:
       print('Argument missing!')
       sys.exit(1)
       
       
    tag = argv[0]
    project = tag_re.search(argv[0].lower())
    
    key = ''
    if project != None:
        key = project.group(1)    
    
    path_cmd = os.path.dirname(os.path.realpath(__file__))
               

    git_root = 'D:\Projekte\windekis_src\windekis_git'
    print(git_root)
    repo = Repo(git_root)
    
    print(tag)
    tags = get_tags(repo,'develop',key,tag)
    print(tags)
    
    nVersions = 5
    startTag = tags[0][0]
    endTag = tags[-1][0]
    if len(tags) >= nVersions:
        endTag = tags[-nVersions][0]
      
    print(change_log(repo,startTag,endTag,key))
    
    
if __name__ == "__main__":
    main(sys.argv[1:])