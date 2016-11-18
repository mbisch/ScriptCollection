import os
import shutil
import sys
import fileinput
import re
from time import gmtime, strftime
from lxml import etree

IncludeDirectories = []

exclude_list = ['NONE']
file_types = ['.CBPROJ']

match_zusatz = re.compile('(^.+)(dbdesc)([^\\.]*)(zusatz)([^.]*)(.cpp)', re.IGNORECASE)


# ***************
# modify_cbproj
# ***************
def modify_cbproj(XmlTree):
    is_changed = False
    root = XmlTree.getroot()
    ns = root.tag[:root.tag.find('Project')]

    found = False
    for fld in root.iter(ns + 'CppCompile'):
        cpp = fld.attrib['Include']
        result = re.match(match_zusatz, cpp);

        if result != None:
            is_changed = True
            print(cpp)
            fld.getparent().remove(fld)
    return is_changed

            # *****


# MAIN
# *****

log_file_name_base = os.path.join('.', 'Log_')

log_cnt = 1
while (os.path.isfile(log_file_name_base + str(log_cnt) + '.txt')):
    log_cnt += 1
logfile = open(log_file_name_base + str(log_cnt) + '.txt', 'w')

logfile.write('AModify CBPROJ files (' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ')\n')

parser = etree.XMLParser(remove_blank_text=True)
parserUTF8 = etree.XMLParser(remove_blank_text=True, encoding='utf-8')
parserANSI = etree.XMLParser(remove_blank_text=True, encoding='cp1252')

print("Start directory:")
InputDirectory = str(input("> "))

print(InputDirectory)

# Check if file
# **************
if os.path.isfile(InputDirectory):

    # File
    OneFile_Name = os.path.basename(InputDirectory)
    StartDirectory = os.path.dirname(InputDirectory)

else:
    StartDirectory = InputDirectory
    OneFile_Name = ''

    # Directory
    logfile.write('Start Directory: ' + StartDirectory + '\n')

    for dirname, dirnames, filenames in os.walk(StartDirectory):
        # print path to all filenames.
        for filename in filenames:
            # exclude list
            if filename not in exclude_list:  # and (OneFile_Name == '' or OneFile_Name == filename):
                filename_split = os.path.splitext(filename.upper())
                if (filename_split[1] in file_types):
                    file = dirname + '\\' + filename

                    # print('Processing file: ' + str(file))

                    encoding = None
                    failed = False
                    try:
                        tree = etree.parse(file, parser)
                    except:
                        failed = True
                        print('Could not open ' + str(file) + '. Try UTF8 encoding')

                    if failed:
                        failed = False
                        try:
                            tree = etree.parse(file, parserUTF8)
                        except:
                            failed = True
                            print('Could not open ' + str(file) + '. Try ANSI encoding')

                    if failed:
                        failed = False
                        try:
                            tree = etree.parse(file, parserANSI)
                        except:
                            failed = True
                            print('Failed to open ' + str(file))

                    if not failed:
                        is_changed = modify_cbproj(tree)
                        if is_changed:
                            tree.write(file, pretty_print=True, encoding=encoding)

    logfile.close();
