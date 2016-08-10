import os
import sys
import fileinput
import re

dbdesc_list = []

#a_pattern = "^\s*\{{1} [^,]*,{1}[^,{}]*,{1}[^,{}]*,{1}[^,]*,{1}[^,]*,{1}[^,]*,{1}[^,]*,{1}"
a_pattern = "(^[^{]*{{1}) (([^,{}]*,{1}){7}([^,{}]*,{1})*[^,{}]*)(}{1}\s*,{1})"

a_string = '//    { 111 , 222 , 333, 444, T("555"), 666, 777, asdasd, ccc, aaa,sss,ddd,3312ss},'
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

      