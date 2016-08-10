import os
import shutil
import sys
import fileinput
import re
from time import gmtime, strftime
from lxml import etree
from  scriptrunner.scriptrunner import ScriptRunner
import queue
import tkinter as tk


#***************
# modify_cbproj
#***************


class AddItemToProject():
    def __init__(self):
        self.sr          = ScriptRunner()
        self.logname     = tk.StringVar()
        self.logfile     = None
        self.incl_header = []
        self.incl_cpp    = []
        self.projs       = []
        self.txt_queue   = queue.Queue()
        self.parser      = etree.XMLParser(remove_blank_text=True)
        self.parserUTF8  = etree.XMLParser(remove_blank_text=True, encoding='utf-8')
        self.parserANSI  = etree.XMLParser(remove_blank_text=True, encoding='cp1252')

    def Log(self,txt):
        print('LOG:',txt)
        if self.logfile != None:
            self.logfile.write(str(txt) + '\n')
        self.txt_queue.put(str(txt) + '\n')

    def ModifyProj(self,XmlTree,file):
        root = XmlTree.getroot()
        ns = root.tag[:root.tag.find('Project')]
        file_path = os.path.split(file)[0]
        
        maxbuildorder = 0;

        for fld in root.iter(ns + 'BuildOrder'):
            order = int(fld.text)
            if order > maxbuildorder:
                maxbuildorder = order


        incl_order_nr = maxbuildorder

        for cpp in self.incl_cpp:
            rel_cpp_path = os.path.relpath(cpp,file_path)

            found = False
            for fld in root.iter(ns + 'CppCompile'):
                if fld.attrib['Include'].find(rel_cpp_path) >= 0:
                    found = True
                    break

            if not found:
                incl_order_nr += 1

                item_group_ele = root.findall(ns + 'ItemGroup')[0]

                myattrib = {"Include": rel_cpp_path}
                cpp_comp_ele = etree.SubElement(item_group_ele, ns + 'CppCompile', attrib=myattrib)

                bo_ele = etree.SubElement(cpp_comp_ele, ns + 'BuildOrder')
                bo_ele.text = str(incl_order_nr)

        # Include Path
        for inc_dir in self.incl_header:

            rel_include_path = os.path.relpath(inc_dir,file_path)
            rel_include_path = rel_include_path.rstrip('\\') + '\\'

            for fld in root.iter(ns + 'IncludePath'):
                while fld.text.find(rel_include_path) >= 0:
                    pos = fld.text.find(rel_include_path)
                    Text = fld.text[:pos] + fld.text[(pos + len(rel_include_path) + 1):]
                    fld.text = Text
                    Log('Delete text ' + str(pos) + '-' + str(pos + len(rel_include_path) + 1))
                rel_include_path_ns = rel_include_path.rstrip('\\')
                while fld.text.find(rel_include_path_ns) >= 0:
                    pos = fld.text.find(rel_include_path_ns)
                    Text = fld.text[:pos] + fld.text[(pos + len(rel_include_path_ns) + 1):]
                    fld.text = Text
                    Log('Delete text ' + str(pos) + '-' + str(pos + len(rel_include_path_ns) + 1))

            for fld in root.iter(ns + 'IncludePath'):
                if fld.text.find(rel_include_path) < 0:
                    # print 'Add to include path: ' + RelIncludePath
                    pos = fld.text.find('$(IncludePath)')
                    fld.text = fld.text[:pos] + rel_include_path + ';' + fld.text[pos:]
                    break
                else:
                    # print RelIncludePath +' already in include path'
                    break

    def Run(self):
        if len(self.logname.get()) > 0:
            self.logfile = open(self.logname.get(), 'w')

        self.Log('Start execution (' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ')')
        for file in self.projs:

            self.Log('Processing file: '+str(file))

            encoding = None
            failed = False
            try:
                tree = etree.parse(file, self.parser)
            except:
                failed = True
                self.Log('Could not open ' + str(file) + '. Try UTF8 encoding')

            if failed:
                failed = False
                try:
                    tree = etree.parse(file, self.parserUTF8)
                except:
                    failed = True
                    self.Log('Could not open ' + str(file) + '. Try ANSI encoding')

            if failed:
                failed = False
                try:
                    tree = etree.parse(file, self.parserANSI)
                except:
                    failed = True
                    self.Log('Failed to open ' + str(file))

            if not failed:
                self.ModifyProj(tree, file)
                tree.write(file, pretty_print=True,encoding=encoding)

        self.Log('End (' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ')')
        if self.logfile != None:
            self.logfile.close();

   
    def StartGui(self):

        config_elments = []
        config_elments += [{'Name': 'LogFile', 'Type': 'File', 'Label': 'Log File', 'Show': '', 'Var': self.logname}]
        config_elments += [{'Name': 'FileTree', 'Type': 'DirList', 'Label': 'Header',     'Show': '', 'Expandable': False,'FileTypes': '*.h', 'Var': self.incl_header}]
        config_elments += [{'Name': 'FileTree', 'Type': 'FileList', 'Label': 'Source/Lib', 'Show': '', 'Expandable': True,'FileTypes': '*.cpp;*.lib', 'Var': self.incl_cpp}]
        self.sr.add_elements(title='Config', elements=config_elments, new_pane=True, expand=True)
        config_elments = [{'Name': 'FileTree', 'Type': 'FileList', 'Label': 'Project Files', 'Show': '', 'Expandable': True, 'FileTypes': '*.cbproj', 'Var': self.projs}]
        self.sr.add_elements(title=None, elements=config_elments, new_pane=True, expand=True)

        action_elements = []
        action_elements += [{'Name': 'Run1', 'Type': 'Action', 'Label': None, 'Action': 'Run Script', 'Function': self.Run, 'StdoutName': 'TextPad', 'OutQueue' : self.txt_queue}]
        self.sr.add_elements(title='Actions', elements=action_elements, new_pane=False, expand=False)

        self.sr.add_textpad(name='TextPad', title='Output')
        self.sr.mainloop()

if __name__ == "__main__":
    prog = AddItemToProject()
    prog.StartGui()