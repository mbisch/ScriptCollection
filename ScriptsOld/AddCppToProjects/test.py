import os
import sys
import fileinput
import re

dbdesc_list = []

#a_pattern = "^\s*\{{1} [^,]*,{1}[^,{}]*,{1}[^,{}]*,{1}[^,]*,{1}[^,]*,{1}[^,]*,{1}[^,]*,{1}"
a_pattern = "(^[^{]*{{1}) (([^,{}]*,{1}){7}([^,{}]*,{1})*[^,{}]*)(}{1}\s*,{1})"

comment_ln_dd = re.compile('(^\s*//\s*)(\*{15}\**\s*$)')
comment_ln_both = re.compile('(^\s*/{1}\*{1})(\*{15}\**/\s*$)')
comment_ln_left = re.compile('(^\s*/{1}\*{1})(\*{15}\**\s*$)')
comment_ln_right = re.compile('(^\s*)(\*{15}\**/\s*$)')
ln_re_zusatz = re.compile('(^[^{]*{{1})(([^,{}]*,{1})*[^,{}]*)(}{1}\s*,{1})')
fld_re = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')

a_string = '//    { 111 , 222 , 333, 444, T("555"), 666, 777, asdasd, ccc, aaa,sss,ddd,3312ss},'
a_string_zusatz = '//    { 111 , "TASD, BDbs" , "asd,dd,s"},'
a_comment1 = '  //  ****************************************   '
a_comment2 = '  /****************************/'
a_comment3 = '  /****************************'
a_comment4 = '   ****************************/'

#a_string = '    { 1 , 2 , 3, 4,5 ,7, 8,9 end} ,'

pattern = re.compile(a_pattern)
result = pattern.match(a_string)
#result = re.match(a_pattern, a_string)

dbdesc_list.append(result.group(2).split(",")) 
dbdesc_list.append(True)

print(result.group(0))
print(result.group(1))
print(result.group(2))

for dbdesc_line in dbdesc_list:
   if dbdesc_line:
      print(dbdesc_line)

a_str = '   adad  '
print(len(a_str.strip()))

result = re.match(comment_ln_dd,a_comment1);
print(result.group(1)+'|'+result.group(2))

result = re.match(comment_ln_both,a_comment2);
print(result.group(1)+'|'+result.group(2))

result = re.match(comment_ln_left,a_comment3);
print(result.group(1)+'|'+result.group(2))

result = re.match(comment_ln_right,a_comment4);
print(result.group(1)+'|'+result.group(2))


result = re.match(ln_re_zusatz,a_string_zusatz);
print(result.group(1)+'|'+result.group(2))
dbdesc_line = fld_re.split(result.group(2))[1::2]
print (dbdesc_line)

result = re.match(ln_re_zusatz,a_string);
print(result.group(1)+'|'+result.group(2))
dbdesc_line = fld_re.split(result.group(2))[1::2]
print (dbdesc_line)


szLanguag = '"asdasd")'
print (szLanguag.replace('_T(',''))