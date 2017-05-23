import os
import cx_Oracle
import xlsxwriter
import re
import wx

import sql_const as SqlConst

col_map = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']

class JmsDocGenerator:
    def __init__(self, is_wx = False):
        self.connection = None
        self.workbook = None
        self.is_wx = is_wx
        self.code_gen = False
        self.max_col_width = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.col_scale = 1.2
        self.bold = None
        self.yellow = None
        self.first_data_row = 5

        self.column = {
            'Column':7
             ,'Field':0
             ,'Key':1
             ,'Type':2
             ,'Description':3
             ,'Reference':4
             ,'Ref. Type':5
             ,'Remark':6
             ,'Code1':10
             ,'Code2':12}

    def enable_code_gen(self,enable):
        self.code_gen = enable

    def close_all(self):
        if self.workbook != None:
            self.workbook.close()
        if self.connection != None:
            self.connection.close()

    def log(self,msg,type = 'ERROR'):
        if not is_wx:
            print(type+': '+msg)
        else:
            wx.MessageBox(type+': '+msg)

    def getConnection(self, user, pw, db):
        try:
            self.connection = cx_Oracle.connect(user,pw,db)
        except:
            self.log('could not connect to database ' + db)

    def openWorkbook(self, filename):
        try:
            self.workbook = xlsxwriter.Workbook(filename)
            b = self.workbook.add_format({'bold': 1})
            y = self.workbook.add_format()
            y.set_pattern(1)
            y.set_bg_color('yellow')
            self.bold = b
            self.yellow = y
        except:
            self.log('Could not open file ' + filename)


    def fillExcel(self,destination):
        if self.workbook == None:
            self.log('workbook is not open')
        if self.connection == None:
            self.log('connection is not open')

        cursor = self.connection.cursor()
        cursor.execute(SqlConst.sql_stmt, (destination, destination))

        old_table = '_'
        xrow = self.first_data_row

        self.max_col_width = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        worksheet = None
        for row in cursor:
            cd = row[0]
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
            ref_msg_name = row[17]
            ref_msg_fld_name = row[18]
            ref_tab_type = row[19]
            remark = row[20]

            if old_table != tab_name:
                if self.max_col_width[0] > 0:
                    scale = 1.2
                    for col in range(0, len(self.max_col_width)):
                        worksheet.set_column(col, col, self.max_col_width[col] * scale)

                if msg_name != None:
                    worksheet = self.workbook.add_worksheet(msg_name)
                    worksheet.write(0, 0, 'Message: ' + msg_name, self.bold)
                else:
                    worksheet = self.workbook.add_worksheet(tab_name)

                old_table = tab_name

                worksheet.write(1, 0, 'Table: ' + tab_name, self.bold)
                worksheet.write(2, 0, '* - key field', self.bold)

                worksheet.write(self.first_data_row - 1, self.column['Column'], 'Column', self.bold)
                worksheet.write(self.first_data_row - 1, self.column['Field'], 'Field', self.bold)
                worksheet.write(self.first_data_row - 1, self.column['Key'], 'Key', self.bold)
                worksheet.write(self.first_data_row - 1, self.column['Type'], 'Type', self.bold)
                worksheet.write(self.first_data_row - 1, self.column['Description'], 'Description', self.bold)
                worksheet.write(self.first_data_row - 1, self.column['Reference'], 'Reference', self.bold)
                worksheet.write(self.first_data_row - 1, self.column['Ref. Type'], 'Ref. Type', self.bold)
                worksheet.write(self.first_data_row - 1, self.column['Remark'], 'Remark', self.bold)
                worksheet.write(self.first_data_row - 1, self.column['Code1'], 'Code1', self.bold)
                worksheet.write(self.first_data_row - 1, self.column['Code2'], 'Code2', self.bold)
                xrow = self.first_data_row
                self.max_col_width = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]

            type_str = type_cd
            if length != None or tot_digits != None or decimal_digits != None:
                type_str += '('
                if length != None:
                    type_str += str(length)
                if tot_digits != None:
                    type_str += str(tot_digits)
                if decimal_digits != None:
                    type_str += ',' + str(decimal_digits)
                type_str += ')'

            col = self.column['Column']
            worksheet.write(xrow, col, fld_name)
            if len(fld_name) > self.max_col_width[col]:
                self.max_col_width[col] = len(fld_name)

            col = self.column['Field']
            if msg_fld_name != None:
                worksheet.write(xrow, col, msg_fld_name)
                if len(msg_fld_name) > self.max_col_width[col]:
                    self.max_col_width[col] = len(msg_fld_name)

            col = self.column['Key']
            key_str = ''
            if is_key == 'J':
                key_str += '*'
            worksheet.write(xrow, col, key_str)
            self.max_col_width[col] = len('Key')

            col = self.column['Type']
            worksheet.write(xrow, col, type_str)
            if len(type_str) > self.max_col_width[col]:
                self.max_col_width[col] = len(type_str)

            col = self.column['Description']
            desc_str = description
            format = None

            if description == fld_name:
                if re.search(r'_', description) != None:
                    format = self.yellow
            worksheet.write(xrow, col, desc_str, format)

            if len(desc_str) > self.max_col_width[col]:
                self.max_col_width[col] = len(desc_str)

            col = self.column['Reference']
            if ref_msg_fld_name != None:
                l_ref_fld = str(ref_msg_name) + '.' + str(ref_msg_fld_name)
                worksheet.write(xrow, col, l_ref_fld)
                if len(l_ref_fld) > self.max_col_width[col]:
                    self.max_col_width[col] = len(l_ref_fld)

            col = self.column['Ref. Type']
            worksheet.write(xrow, col, ref_tab_type)
            if len(str(ref_tab_type)) > self.max_col_width[col]:
                self.max_col_width[col] = len(str(ref_tab_type))

            col = self.column['Remark']
            worksheet.write(xrow, col, remark)
            if len(str(remark)) > self.max_col_width[col]:
                self.max_col_width[col] = len(str(remark))

            if self.code_gen:
                col = self.column['Code1']
                update_str1 = '{=CONCATENATE("update msg_out_fld_config set msg_fld_name = \'",'+col_map[self.column['Field']] + str(
                    xrow + 1) + ',"\' where cd = \'' + cd + '\';")}'
                worksheet.write_formula(xrow, col, update_str1)
                if len(str(update_str1)) > self.max_col_width[col]:
                    self.max_col_width[col] = len(str(update_str1))

                col = self.column['Code2']
                update_str2 = '{=CONCATENATE("update msg_out_fld set description = \'",'+col_map[self.column['Description']] + str(
                    xrow + 1) + ',"\' where tab_name = \'' + tab_name + '\' and fld_name = \'' + fld_name + '\';")}'
                worksheet.write_formula(xrow, col, update_str2)
                if len(str(update_str2)) > self.max_col_width[col]:
                    self.max_col_width[col] = len(str(update_str2))

            xrow += 1

        if self.max_col_width[0] > 0:
            scale = self.col_scale
            for col in range(0, len(self.max_col_width)):
                worksheet.set_column(col, col, self.max_col_width[col] * scale)
        cursor.close()


if __name__ == "__main__":
    DocGen = JmsDocGenerator(False)

    DocGen.getConnection('AMBIT_CIM','AMBIT_CIM','lp077')
    DocGen.openWorkbook('demo2.xlsx')
    DocGen.enable_code_gen(True)
    DocGen.fillExcel('MYDESK')
    DocGen.close_all()