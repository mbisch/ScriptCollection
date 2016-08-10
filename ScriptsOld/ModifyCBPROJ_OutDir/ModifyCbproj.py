import os
import glob
import shutil
import sys
import fileinput
import re
from time import gmtime, strftime
from lxml import etree

SourceDir     = 'C:\Projekte\windekis_src\sungardIntegration\windekis\Berenberg'
OutputBaseDir = 'C:\Projekte\windekis_appl' 

exclude_list = ['NONE']
exclude_dir_list = ['C:\\Projekte\\windekis_src\\sungardIntegration\\windekis\\02 Komponenten','C:\\Projekte\\windekis_src\\sungardIntegration\\windekis\\Genix']
file_types   = ['.CBPROJ']

#***************
# GetProjectName
#***************
def GetProjectName(Directory):
   Base = os.path.abspath(SourceDir)
   BaseLen = len(Base)
   
   ProjectDir = os.path.abspath(Directory)
   
   ProjectBase = ProjectDir[BaseLen:]
   while ProjectDir != Base and ProjectDir.find(Base) >= 0:
      ProjectBase = ProjectDir[BaseLen+1:]
      ProjectDir = os.path.abspath(ProjectDir + '\\..')     
   
   ProjectDir2 = os.path.abspath(Directory)
   ProjectN = os.path.abspath(ProjectDir2)[len(os.path.abspath(ProjectDir2 + '\\..')):]
   while len(glob.glob(os.path.abspath(ProjectDir2 + '\\*.groupproj'))) == 0 and ProjectDir2.find(Base) >= 0:
      ProjectN = os.path.abspath(ProjectDir2)[len(os.path.abspath(ProjectDir2 + '\\..'))+1:]
      ProjectDir2 = os.path.abspath(ProjectDir2 + '\\..')
       
   
   Name = ProjectBase
  
   if ProjectDir != os.path.abspath(ProjectDir2 + '\\..'):
      Name = ProjectBase + '_' + ProjectN
 
   print Directory + ' ' + Name
      
   return Name         

   

#***************
# modify_cbproj
#***************
def modify_cbproj(XmlTree,ExeBaseDir,ProjectName):
   root = XmlTree.getroot() 
   ns = root.tag[:root.tag.find('Project')]
   
   ExeDir = ExeBaseDir.rstrip('\\') + '\\' + ProjectName + '\\AmbitCIM'
   
   for fld in root.iter(ns + 'FinalOutputDir'):
      fld.text = ExeDir   
            
#*****
# MAIN
#*****

log_file_name_base = os.path.join('.', 'Log_')

log_cnt=1
while(os.path.isfile(log_file_name_base+str(log_cnt)+'.txt')):
   log_cnt += 1
logfile = open(log_file_name_base+str(log_cnt)+'.txt','w')

logfile.write('AModify CBPROJ files ('+strftime("%Y-%m-%d %H:%M:%S", gmtime())+')\n')

print ("Start directory:" + SourceDir)
InputDirectory = SourceDir
 
print InputDirectory

# Check if file
#**************
if os.path.isfile(InputDirectory):

   # File   
   OneFile_Name   = os.path.basename(InputDirectory)
   StartDirectory = os.path.dirname(InputDirectory)
   
else:
   StartDirectory = InputDirectory
   OneFile_Name   = ''
   
   #Directory
   logfile.write('Start Directory: '+ StartDirectory +'\n')
   
   for dirname, dirnames, filenames in os.walk(StartDirectory):
      IsDirExcluded = False
      for ExclDir in exclude_dir_list:
         if os.path.abspath(dirname).find(os.path.abspath(ExclDir)) >= 0:
            IsDirExcluded = True
            break 
      if IsDirExcluded:
         continue
         
      # print path to all filenames.
      for filename in filenames:
         #exclude list
         if filename not in exclude_list:                     
            filename_split = os.path.splitext(filename.upper())           
            if (filename_split[1] in file_types):
               ProjectName = GetProjectName(dirname)            
               FullPath = dirname + '\\' + filename              
               print 'Modify: ' + FullPath
               
               failed = False
               enc="utf-8"
               try:
                  parser = etree.XMLParser(remove_blank_text=True)               
                  tree = etree.parse(FullPath,parser)                
               except:
                  failed = True
                  print 'Could not open ' + FullPath +'. Try ANSI encoding'
               
               if not failed:
                  modify_cbproj(tree,OutputBaseDir,ProjectName)
                  tree.write(dirname + '\\' + filename,pretty_print = True)                 
               else:
                  failed = False
                  enc = "ansi"
                  try:
                     parserANSI = etree.XMLParser(remove_blank_text=True, encoding = enc)               
                     tree = etree.parse(FullPath,parserANSI)                       
                  except:
                     failed = True
                     print 'Failed to open ' + FullPath + '.'
               
               if not failed:               
                  modify_cbproj(tree,OutputBaseDir,ProjectName)
                  tree.write(dirname + '\\' + filename ,pretty_print = True, encoding = enc)   
               
               logfile.close();
       