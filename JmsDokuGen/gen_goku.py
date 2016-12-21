import os
import cx_Oracle
import xlsxwriter
import re

 
sql_stmt = """with CONF_TAB                                                     
              as (SELECT mtc.tab_name,                                                  
                    mfc.cd,                                                              
                    mfc.fld_name,                                                        
                    mtc.msg_name,                                                        
                    mfc.msg_fld_name,                                                    
                    mf.description,                                                      
                    mf.type_cd,                                                          
                    mft.description type,                                                
                    mf.length,                                                           
                    mf.tot_digits,                                                       
                    mf.decimal_digits,                                                   
                    mf.is_key                                                            
              from msg_out_fld mf                                                       
                 ,msg_out_tab_config mtc                                               
                 ,msg_out_fld_config mfc                                               
                 ,msg_out_fld_type mft                                                 
              where     mf.tab_name = mtc.tab_name                                       
                    and mfc.fld_name = mf.fld_name                                       
                    and mfc.tab_config_cd = mtc.cd                                       
                    and mf.type_cd = mft.cd                                              
                    and nvl (mf.loesch_cd, 'N') != 'J'                                   
                    and nvl (mtc.loesch_cd, 'N') != 'J'                                  
                    and nvl (mfc.loesch_cd, 'N') != 'J'                                  
                    and nvl (mfc.send_cd, 'J') = 'J')                                    
           select ct1.cd,                                                              
                    ct1.tab_name,                                                        
                    ct1.fld_name,                                                        
                    ct1.msg_name,                                                        
                    ct1.msg_fld_name,                                                    
                    ct1.description,                                                     
                    ct2.tab_name hist_tab_name,                                          
                    ct2.fld_name hist_fld_name,                                          
                    ct2.msg_name hist_msg_name,                                          
                    ct2.msg_fld_name hist_msg_fld_name,                                  
                    ct2.description hist_description,                                    
                    ct1.type_cd,                                                         
                    ct1.type,                                                            
                    ct1.length,                                                          
                    ct1.tot_digits,                                                      
                    ct1.decimal_digits,                                                  
                    ct1.is_key                                                           
           from conf_tab ct1                                                           
           full outer join conf_tab ct2                                                
           on ct1.tab_name || '_HIST'= ct2.tab_name and ct1.fld_name  = ct2.fld_name   
           where  ct1.tab_name  not like '%_HIST'                                      
           order by ct1.tab_name, case when is_key = 'J' then '_' else msg_fld_name end"""                                                       
 
 
connection = cx_Oracle.connect('AMBIT_CIM/AMBIT_CIM@lp077')
 
workbook = xlsxwriter.Workbook('demo.xlsx')
bold = workbook.add_format({'bold': 1})
yellow = workbook.add_format()
yellow.set_pattern(1)
yellow.set_bg_color('yellow')

# Widen the first column to make the text clearer.

cursor = connection.cursor()
cursor.execute(sql_stmt)

old_table = '_'
first_data_row = 5
xrow = first_data_row

max_width = [0,0,0,0,0,0,0]
worksheet = None
for row in cursor:
   cd       = row[0]
   tab_name = row[1]                                                        
   fld_name = row[2]                                                            
   msg_name = row[3]                                                            
   msg_fld_name = row[4]                                                        
   description = row[5]                                                         
   hist_tab_name = row[6]                                              
   hist_fld_name = row[7]                                               
   hist_msg_name = row[8]                                              
   hist_msg_fld_name = row[9]                                      
   hist_description = row[10]                                        
   type_cd = row[11]                                                              
   type = row[12]                                                                 
   length = row[13]                                                              
   tot_digits = row[14]                                                           
   decimal_digits = row[15]                                                      
   is_key = row[16]   

   if old_table != tab_name:
      if max_width[0] > 0:
         scale = 1.2
         worksheet.set_column(0,0,max_width[0]*scale)
         worksheet.set_column(1,1,max_width[1]*scale)
         worksheet.set_column(2,2,max_width[2]*scale)
         worksheet.set_column(3,3,max_width[3]*scale)
         worksheet.set_column(4,4,max_width[4]*scale)
         worksheet.set_column(5,5,max_width[5]*scale)
   
      worksheet = workbook.add_worksheet(msg_name)
      old_table = tab_name
      worksheet.write(0,0,'Message: '+msg_name,bold)
      worksheet.write(1,0,'Table: '+tab_name,bold)
      worksheet.write(2,0,'* - key field' ,bold)
      
      worksheet.write(first_data_row-1,0,'Column',bold)
      worksheet.write(first_data_row-1,1,'Field',bold)
      worksheet.write(first_data_row-1,2,'Key',bold)
      worksheet.write(first_data_row-1,3,'Type',bold)
      worksheet.write(first_data_row-1,4,'Description',bold)
      worksheet.write(first_data_row-1,5,'Code',bold)
      xrow = first_data_row
      max_width = [0,0,0,0,0,0,0]
   
   
   worksheet.write(xrow,0,msg_fld_name,bold)   
   type_str = type_cd
   if length != None or tot_digits != None or decimal_digits != None:
      type_str += '('
      if length != None:
          type_str += str(length)
      if tot_digits != None:
          type_str += str(tot_digits)      
      if decimal_digits != None:
          type_str += ','+ str(decimal_digits)
      type_str += ')'
      
   worksheet.write(xrow,0,fld_name)
   if len(fld_name) > max_width[0]:
      max_width[0] = len(fld_name)   
   
   msg_fld_str =  msg_fld_name       
   worksheet.write(xrow,1,msg_fld_str)
   if len(msg_fld_str) > max_width[1]:
      max_width[1] = len(msg_fld_str)     
   
   key_str = ''
   if is_key == 'J':
      key_str += '*'
   worksheet.write(xrow,2,key_str)
   max_width[2] = len('Key') 
      
   worksheet.write(xrow,3,type_str)
   if len(type_str) > max_width[3]:
      max_width[3] = len(type_str)  

   desc_str = description
   format = None
   
   if description == fld_name:
      if re.search(r'_',description) != None:
         format = yellow   
   worksheet.write(xrow,4,desc_str,format)
   
   if len(desc_str) > max_width[4]:
      max_width[4] = len(desc_str)  
    
   update_str = '{=CONCATENATE("update msg_out_fld_config set msg_fld_name = \'",B' +str(xrow+1)+ ',"\', description = \'",E' +str(xrow+1)+',"\' where cd = \'' +cd+ '\';")}'   
   worksheet.write_formula(xrow,5,update_str)
      
   xrow += 1
   
workbook.close()   
cursor.close()
connection.close()

