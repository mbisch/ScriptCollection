import os
import shutil
import sys
import fileinput
import re
from time import gmtime, strftime

macro_name = 'ADD_ZUSATZ_COL'
exclude_list = ['DBDESC.CPP']
ln_re = re.compile('(^[^{]*{{1})(([^,{}]*,{1}){7}([^,{}]*,{1})*[^,{}]*)(}{1}\s*,{1})')
fld_re = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')

#**************************************
# Helper function to create backup dir
#**************************************
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

#***********************************************
# Add Zusatz, cleanup line, check column length
#***********************************************
def clean_line(dbdesc_line,column_length):
   max_col_nr = len(column_length)
   for i in range(len(dbdesc_line)):
      if (i==6) and (dbdesc_line[i].find(macro_name)<0) and (dbdesc_line[i].find('szName')<0):
         dbdesc_line[i] = macro_name+'(' + dbdesc_line[i].strip()  
      else:   
         dbdesc_line[i] = dbdesc_line[i].strip()
      if (i<max_col_nr):
         if (column_length[i]<len(dbdesc_line[i])):
            column_length[i] = len(dbdesc_line[i])
      else:
         column_length.append(len(dbdesc_line[i]))
         

#***********************************
# Format lines and add empty column
#***********************************
def add_zusatz(dirname,filename):
   file_name_in = os.path.join(dirname, filename)
   dir_out = dirname+'\\dbdesc_backup\\'
   ensure_dir(dir_out)
   file_name_out = os.path.join(dir_out, filename+'.tmp')
   file_name_bak = os.path.join(dir_out, filename+'.bak')

   replace_cnt = 0

   dbdesc_list = []
   column_length  = []
   line_start  = []
   
   # analyse infile:
   # ***************
   
   infile = open(file_name_in,'r')
   for line in infile:
      m_match = ln_re.match(line)
      if (m_match):
         dbdesc_line = fld_re.split(m_match.group(2))[1::2]
         line_start.append(m_match.group(1))
         clean_line(dbdesc_line,column_length)
         dbdesc_list.append(dbdesc_line)
         replace_cnt += 1
      else:
         dbdesc_list.append(None)
         line_start.append(None)
   infile.close()
      
   
   # write formatted file
   # ********************
   if (replace_cnt>0):
      infile = open(file_name_in,'r')
      outfile = open(file_name_out,'w')
   
      line_cnt = 0
      for line in infile:
         if (dbdesc_list[line_cnt]):
            out_line=line_start[line_cnt].ljust(7)
            for col_idx in range(len(column_length)):
               fld_length = column_length[col_idx]+3
               if col_idx<len(dbdesc_list[line_cnt]):
                  if (col_idx>0):
                     out_line +=','
                     
                  if (col_idx==6) and (dbdesc_list[line_cnt][col_idx].find(',_T(""))')<0):
                     if (dbdesc_list[line_cnt][col_idx].find('szName')<0):
                        out_line += dbdesc_list[line_cnt][col_idx].ljust(fld_length)+',_T(""))   '.ljust(len(',szNameLanguage1   ') +',_T(""))   '.ljust(len(',szNameLanguage2   ')
                     else:
                        #Add Title
                        out_line += dbdesc_list[line_cnt][col_idx].ljust(fld_length)+',szNameLanguage1   ' + ',szNameLanguage2   '
                  else:
                     out_line += dbdesc_list[line_cnt][col_idx].ljust(fld_length)
               else:
                  out_line += ' '.ljust(fld_length+1)
            out_line+='},\n'
         else:
            out_line=line
         outfile.write(out_line)
         line_cnt+=1
          
      infile.close()
      outfile.close()   

      # Replace old with new files
      shutil.move(file_name_in,file_name_bak)
      shutil.move(file_name_out,file_name_in)
   
   return replace_cnt
      

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
   # File   
   filename = os.path.basename(StartDirectory)
   dirname = os.path.dirname(StartDirectory)
   
   print(dirname)
   print(filename)
   
   logfile.write('File: '+ StartDirectory +'\n')
   filename_split = os.path.splitext(filename.upper())
   if (re.search('DBDESC',filename_split[0])) and (filename_split[1]=='.CPP'):
      replace_line_cnt = add_zusatz(dirname,filename)
      if(replace_line_cnt>0):
         logfile.write(os.path.join(dirname, filename) +' - '+ str(replace_line_cnt) + ' lines replaced\n')
      else:
         logfile.write(os.path.join(dirname, filename) +' - No change\n')
else:
   #Directory
   logfile.write('Start Directory: '+ StartDirectory +'\n')
   
   for dirname, dirnames, filenames in os.walk(StartDirectory):  

      # print path to all filenames.
      for filename in filenames:
         #exclude list
         if filename not in exclude_list:         
            filename_split = os.path.splitext(filename.upper())
            if (re.search('DBDESC',filename_split[0])) and (filename_split[1]=='.CPP'):
               replace_line_cnt = add_zusatz(dirname,filename)
               if(replace_line_cnt>0):
                  logfile.write(os.path.join(dirname, filename) +' - '+ str(replace_line_cnt) + ' lines replaced\n')
               else:
                  logfile.write(os.path.join(dirname, filename) +' - No change\n')
logfile.close();
       