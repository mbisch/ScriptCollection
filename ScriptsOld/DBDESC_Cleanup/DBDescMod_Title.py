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
comment_ln_dd = re.compile('(^\s*//\s*)(\*{320}\**\s*$)')
comment_ln_both = re.compile('(^\s*/{1}\*{1})(\*{320}\**/\s*$)')
comment_ln_left = re.compile('(^\s*/{1}\*{1})(\*{320}\**\s*$)')
comment_ln_right = re.compile('(^\s*)(\*{320}\**/\s*$)')

ln_re_zusatz = re.compile('(^[^{]*{{1})(([^,{}]*,{1})*[^,{}]*)(}{1}\s*,{1})')


#**************************************
# Helper function to create backup dir
#**************************************
def ensure_dir(f):
   d = os.path.dirname(f)
   if not os.path.exists(d):
      os.makedirs(d)

#***********************************************
# Cleanup line, check column length
#***********************************************
def clean_line(dbdesc_line,column_length):
   max_col_nr = len(column_length)
   for i in range(len(dbdesc_line)):
      dbdesc_line[i] = dbdesc_line[i].strip()
      if (i<max_col_nr):
         if (column_length[i]<len(dbdesc_line[i])):
            column_length[i] = len(dbdesc_line[i])
      else:
         column_length.append(len(dbdesc_line[i]))
         
#***********************************************
# Insert Zusatz
#***********************************************
def insert_zusatz(dbdesc_line,dirname,filename,_zusatz_map):
   length = len(dbdesc_line)
   if ((length < 9) or dbdesc_line[6].find('szName')<0 or (dbdesc_line[7].find('szNameLanguage2')<0) or (dbdesc_line[8].find('szNameLanguage2')<0)):
      return  
   
   IsFirstTitleLine = (dbdesc_line[0].find('Tabelle:Nr')>=0)
   for i in range(length):
      if (i==8):
         if(IsFirstTitleLine):
            dbdesc_line[i] = 'PrimaryKey'
         else:
            dbdesc_line[i] = 'ForeignKey'
      if (i==9):
         dbdesc_line[i] = 'Flags'     
      if (i==10):
         dbdesc_line[i] = 'QueryFlags'      
      if (i==11):
         dbdesc_line[i] = 'FlagsEx'      
      if (i==12):
         dbdesc_line[i] = 'HistoryFieldNr'      
      if (i==13):
         dbdesc_line[i] = 'Object'
   
   # Remove rest of elements
   while(len(dbdesc_line)>14):
      dbdesc_line.pop()
      #print (dbdesc_line)

         
#***********************************
# Format lines and add empty column
#***********************************
def add_zusatz(dirname,filename,_zusatz_map):
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
   IsAfterDBCON = False
   IsAfterDBDESC = False
   for line in infile:
      IsAfterDBCON = (IsAfterDBCON or re.search('DBCon\[MAX_DBCON\]',line))
      IsAfterDBDESC = (IsAfterDBDESC or re.search('DBDesc\[MAX_DBDESC\]',line))

      m_match = ln_re.match(line)
      
      if (m_match and ((not IsAfterDBCON) or IsAfterDBDESC)):
         dbdesc_line = fld_re.split(m_match.group(2))[1::2]         
         line_start.append(m_match.group(1))
         insert_zusatz(dbdesc_line,dirname,filename,_zusatz_map)
         clean_line(dbdesc_line,column_length)
         dbdesc_list.append(dbdesc_line)
         replace_cnt += 1
      else:
         # Check if separator line. e.g. /**...**/
         m_match_comment_dd    = comment_ln_dd.match(line)
         m_match_comment_both  = comment_ln_both.match(line)
         m_match_comment_left  = comment_ln_left.match(line)
         m_match_comment_right = comment_ln_right.match(line)
         
         if (m_match_comment_dd):
            print('COMMENT_DD')
            dbdesc_list.append('COMMENT_DD')
            line_start.append(m_match_comment_dd.group(1))
            replace_cnt += 1
         elif(m_match_comment_both):
            print('COMMENT_BOTH')
            dbdesc_list.append('COMMENT_BOTH')
            line_start.append(m_match_comment_both.group(1))
            replace_cnt += 1
         elif(m_match_comment_left):
            print('COMMENT_LEFT')
            dbdesc_list.append('COMMENT_LEFT')
            line_start.append(m_match_comment_left.group(1))
            replace_cnt += 1
         elif(m_match_comment_right):
            print('COMMENT_RIGHT')
            dbdesc_list.append('COMMENT_RIGHT')
            line_start.append(m_match_comment_right.group(1))
            replace_cnt += 1
         else:
            dbdesc_list.append(None)
            line_start.append(None)
   infile.close()
   
   max_line_length = 7; # Line Start
   for length in column_length:
      max_line_length+=length+4
   print (max_line_length)
   
   # write formatted file
   # ********************
   
   if (replace_cnt>0):
      infile = open(file_name_in,'r')
      outfile = open(file_name_out,'w')
   
      line_cnt = 0
      for line in infile:
         if (dbdesc_list[line_cnt]):
            if (dbdesc_list[line_cnt] == 'COMMENT_DD' or dbdesc_list[line_cnt] == 'COMMENT_LEFT'):
               out_line = line_start[line_cnt].ljust(max_line_length,'*') + '\n'
               print ('COMMENT_DD or COMMENT_LEFT')
            elif (dbdesc_list[line_cnt] == 'COMMENT_BOTH' or dbdesc_list[line_cnt] == 'COMMENT_RIGHT'):
               out_line = line_start[line_cnt].ljust(max_line_length-1,'*')+'/' + '\n'
               print ('COMMENT_DD or COMMENT_LEFT')
            else:
               out_line=line_start[line_cnt].ljust(7)
               for col_idx in range(len(column_length)):
                  fld_length = column_length[col_idx]+3
                  if col_idx<len(dbdesc_list[line_cnt]):
                     if (col_idx>0):
                        out_line +=','
                     out_line += dbdesc_list[line_cnt][col_idx].ljust(fld_length)
                  else:
                     out_line += ' '.ljust(fld_length+1)
               out_line+='},\n'
            #print ('Modify:' + out_line)
         else:
            out_line=line
         
#         if (line_cnt<100):
#            print (str(line_cnt)+':'+out_line)
         outfile.write(out_line)
         line_cnt+=1
          
      infile.close()
      outfile.close()   

      # Replace old with new files
      shutil.move(file_name_in,file_name_bak)
      shutil.move(file_name_out,file_name_in)
   
   return replace_cnt


#******************
# Key from filename
#******************
def key_from_filename(filename):
   _filename = filename.upper().replace('DBDESC','').replace('ZUSATZ','').replace('.CPP','')
   _filename = _filename
   return _filename


#***************
# Analyse Zusatz
#***************
def analyze_zusatz(dirname,filename,out_zusatz_map):

   # analyse infile:
   # ***************
   file_name_in = os.path.join(dirname, filename)
   
   file_name_key = key_from_filename(filename)
   
   duplicates = 0
   infile = open(file_name_in,'r')
   for line in infile:
      m_match = ln_re_zusatz.match(line)
      if (m_match):    
         zusatz_line = fld_re.split(m_match.group(2))[1::2]
         nrElement = len(zusatz_line)         
         if (nrElement == 3) or (nrElement>3 and not zusatz_line[3].strip()):
            key1 = zusatz_line[0].strip()
            key2 = dirname
            key3 = file_name_key
                       
            value = zusatz_line[2].strip()
            if (not value):
               value = '""'   
            if (value.find('_T(')<0):
               value = '_T(' + value.replace('_T(','') +')'               
            if (key1 in out_zusatz_map): 
               if (key2 in out_zusatz_map[key1]): 
                  if (key3 in out_zusatz_map[key1][key2]):
                     if (out_zusatz_map[key1][key2][key3] != value):
                        out_zusatz_map[key1][key2][key3] = '_T("__COPY_ZUSATZ_MANUAL__")' 
                        duplicates += 1
                  else:
                     out_zusatz_map[key1][key2][key3] = value
               else:
                  out_zusatz_map[key1][key2] = {}
                  out_zusatz_map[key1][key2][key3] = value
            else:             
               out_zusatz_map[key1] = {}
               out_zusatz_map[key1][key2] = {}
               out_zusatz_map[key1][key2][key3] = value     
   print ('File: '+ filename.ljust(50) +' Length:'+str(len(out_zusatz_map)).ljust(5)+' Duplicates:'+str(duplicates))            
        
      

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
   
   zusatz_map = {}
             
   # DBDESC 
   ########
   for dirname, dirnames, filenames in os.walk(StartDirectory):  
      # print path to all filenames.
      for filename in filenames:
         #exclude list
         if filename not in exclude_list:         
            filename_split = os.path.splitext(filename.upper())
            if (re.search('DBDESC',filename_split[0])) and (filename_split[1]=='.CPP'):
               replace_line_cnt = add_zusatz(dirname,filename,zusatz_map)
               if(replace_line_cnt>0):
                  logfile.write(os.path.join(dirname, filename) +' - '+ str(replace_line_cnt) + ' lines replaced\n')
               else:
                  logfile.write(os.path.join(dirname, filename) +' - No change\n')
logfile.close();
       