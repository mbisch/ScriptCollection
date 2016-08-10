import os, errno
import shutil
import sys
import re

exclude_dir = ['.git']
exclude_files = ['NONE']
exclude_file_types   = ['.NONE']

#********
# mkdir_p
#********
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


#*****
# MAIN
#*****

print ("directory SUPER:")
SuperDirectory = str(raw_input( "> " ))
SuperDirectory = os.path.normpath(SuperDirectory)

print ("directory SUB:")
SubDirectory = str(raw_input( "> " ))
SubDirectory = os.path.normpath(SubDirectory)
 
print ("Destination directory:")
DestDirectory = str(raw_input( "> " ))
DestDirectory = os.path.normpath(DestDirectory)

for dirname, dirnames, filenames in os.walk(SuperDirectory):  
   # print path to all filenames.
   if dirname not in exclude_dir:
      for filename in filenames:
         #exclude list
         if filename not in exclude_files:                     
            filename_split = os.path.splitext(filename.upper())           
            if (filename_split[1] not in exclude_file_types):               
               CommonPath = dirname[dirname.find('SuperDirectory'):]
               SuperFile = dirname + '\\' + filename
               SubPath   = SubDirectory.rstrip('\\')  + '\\' + CommonPath.lstrip('\\')              
               DestPath  = DestDirectory.rstrip('\\')  + '\\' + CommonPath.lstrip('\\') 
               
               DestFile = DestPath + '\\' + filename
               
               if (not os.path.exists(SubFile)) && os.path.isfile(SuperFile):                  
                  print "copy " + SuperFile
                  try:
                     shutil.copy2(SuperFile,DestPath)                  
                  except: 
                     mkdir_p(DestPath)               
                     shutil.copy2(SuperFile,DestPath)
                     
                  

    