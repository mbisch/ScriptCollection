import os
import shutil
import sys
import fileinput
import re

from time import gmtime, strftime


#**************************************
# Helper function to create backup dir
#**************************************
def ensure_dir(f):
   d = os.path.dirname(f)
   if not os.path.exists(d):
      os.makedirs(d)
      

#*****
# MAIN
#*****
print ("Start directory:")

log_file_name_base = os.path.join('.', 'Log_')

log_cnt=1
while(os.path.isfile(log_file_name_base+str(log_cnt)+'.txt')):
   log_cnt += 1
logfile = open(log_file_name_base+str(log_cnt)+'.txt','w')

logfile.write('Add Zusatz to *DBDESC*.CPP files ('+strftime("%Y-%m-%d %H:%M:%S", gmtime())+')\n')

StartDirectory = input( "> " )

# Check if file
#**************
if os.path.isfile(StartDirectory):
   print ("Path should be directory not file!")
#   # File   
#   filename = os.path.basename(StartDirectory)
#   dirname = os.path.dirname(StartDirectory)
#   
#   print(dirname)
#   print(filename)
#   
#   logfile.write('File: '+ StartDirectory +'\n')
#   filename_split = os.path.splitext(filename.upper())
#   if (re.search('DBDESC',filename_split[0])) and (filename_split[1]=='.CPP'):
#      replace_line_cnt = add_zusatz(dirname,filename)
#      if(replace_line_cnt>0):
#         logfile.write(os.path.join(dirname, filename) +' - '+ str(replace_line_cnt) + ' lines replaced\n')
#      else:
#         logfile.write(os.path.join(dirname, filename) +' - No change\n')
else:
   #Directory
   logfile.write('Start Directory: '+ StartDirectory +'\n')
   
   #Anayse DBDESC Zusatz
   #####################
                
   # DBDESC 
   ########
   
   tot_line_cnt = 0;
   error_cnt  = 0
   logfile.write('File name, Line Count')
   for dirname, dirnames, filenames in os.walk(StartDirectory):  
      # print path to all filenames.
      for filename in filenames:    
         filename_split = os.path.splitext(filename.upper())
         if (   filename_split[1]=='.CPP' or filename_split[1]=='.H' or filename_split[1]=='.RC' or filename_split[1]=='.DEF'):
            file_name_in = file_name_in = os.path.join(dirname, filename)
            infile = open(file_name_in,'r')
            file_line_cnt = 0;
            
            try:
               for line in infile:
                 file_line_cnt += 1
             
               logfile.write(os.path.join(dirname, filename) +' , ' + str(file_line_cnt) + '\n')
               tot_line_cnt = tot_line_cnt + file_line_cnt
               infile.close()
            except (UnicodeDecodeError):
               error_cnt += 1
               logfile.write(os.path.join(dirname, filename) +' , Error reading file ()')
            
   logfile.write('Total, '+ str(tot_line_cnt) + '\n')
   logfile.write('Errors, '+ str(error_cnt) + '\n' )
   print('Total number of lines: ' + str(tot_line_cnt))
   print('Errors, '+ str(error_cnt))
logfile.close();       