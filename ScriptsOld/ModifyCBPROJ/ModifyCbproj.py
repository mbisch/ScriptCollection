import os
import shutil
import sys
import fileinput
import re
from time import gmtime, strftime
from lxml import etree


IncludeDirectories = ['windekis\Genix\ApWare32\common\include', 'windekis\Genix\ApWare32\common\source','windekis\Genix\GXWARE32\common\include','windekis\Genix\GXWARE32\common\source'] 
SourceFiles = ['windekis\Genix\GXWARE32\common\source\*.cpp', 'windekis\Genix\ApWare32\common\source\*.cpp']

exclude_list = ['NONE']
file_types   = ['.CBPROJ']


#***************
# modify_cbproj
#***************
def modify_cbproj(XmlTree,IncludeDirectories,SourceFiles):
   root = XmlTree.getroot() 
   ns = root.tag[:root.tag.find('Project')]
   
   MaxBuildOrderBelowK = 0;
   MinBuildOrderAboveK = 9999999;
   MaxBuildOrder       = 0;
   
   GenixPath = ''
   for fld in root.iter(ns + 'CppCompile'):
      #print fld.attrib
      pos = fld.attrib['Include'].upper().find('GENIX')
      if pos > 0:
         GenixPath = fld.attrib['Include'][0:pos]
         break
   
   for fld in root.iter(ns + 'BuildOrder'):
      Order = int(fld.text)
      if Order > MaxBuildOrderBelowK and Order < 1000:
         MaxBuildOrderBelowK = Order
      if Order > MaxBuildOrder:
         MaxBuildOrder = Order               
      if Order < MinBuildOrderAboveK and Order >= 1000:
         MinBuildOrderAboveK = Order 
         
   IncludeOrderNr = MaxBuildOrder
   
   for SourceFile in SourceFiles: 
      FilePathShort = SourceFile[SourceFile.upper().find('GENIX'):]
      RelSourceFile = GenixPath+FilePathShort   
      
      found = False
      for fld in root.iter(ns + 'CppCompile'):
         if fld.attrib['Include'].find(RelSourceFile) >= 0:
            found = True 
            #print RelSourceFile + ' already included'
            break
      
      if not found:
         #print 'Add ' + RelSourceFile 
         IncludeOrderNr += 1   
         
         ItemGroupEle = root.findall(ns + 'ItemGroup')[0]
         FilePath = dirname + filename
         #print FilePath   

         MyAttrib = {"Include": RelSourceFile}
         CPPCompEle = etree.SubElement(ItemGroupEle, ns+'CppCompile',  attrib=MyAttrib)
         
         BOEle = etree.SubElement(CPPCompEle, ns+'BuildOrder')
         BOEle.text = str(IncludeOrderNr)
        
         
   #Fix Order
   if MaxBuildOrderBelowK < 999 and MaxBuildOrder >=1000:
      IncludeOrderNr = MaxBuildOrderBelowK + 1
      for fld in root.iter(ns + 'BuildOrder'):
         Order = int(fld.text)
         if Order >= 1000:
            IncludeOrderNr += 1;
            fld.text = str(IncludeOrderNr)          
         
   # Include Path
   for IncludeDir in IncludeDirectories:
      IncludePathShort = IncludeDir[IncludeDir.upper().find('GENIX'):]      
      RelIncludePath   = GenixPath+IncludePathShort
      RelIncludePath   = RelIncludePath.rstrip('\\') + '\\'
     
      for fld in root.iter(ns + 'IncludePath'):
         while fld.text.find(RelIncludePath) >=0:
            pos = fld.text.find(RelIncludePath)
            Text = fld.text[:pos] + fld.text[(pos+len(RelIncludePath)+1):]
            fld.text = Text
            print 'Delete text ' + str(pos) + '-' + str(pos+len(RelIncludePath)+1) 
         RelIncludePathNS = RelIncludePath.rstrip('\\')            
         while fld.text.find(RelIncludePathNS) >=0:
            pos = fld.text.find(RelIncludePathNS)
            Text = fld.text[:pos] + fld.text[(pos+len(RelIncludePathNS)+1):]
            fld.text = Text
            print 'Delete text ' + str(pos) + '-' + str(pos+len(RelIncludePathNS)+1) 
            
   for IncludeDir in IncludeDirectories:
      IncludePathShort = IncludeDir[IncludeDir.upper().find('GENIX'):]      
      RelIncludePath   = GenixPath+IncludePathShort
      RelIncludePath   = RelIncludePath.rstrip('\\') + '\\'
      
      for fld in root.iter(ns + 'IncludePath'):
         if fld.text.find(RelIncludePath) < 0:
            #print 'Add to include path: ' + RelIncludePath
            pos = fld.text.find('$(IncludePath)')
            fld.text =  fld.text[:pos] + RelIncludePath + ';' + fld.text[pos:]
            break
         else:           
            #print RelIncludePath +' already in include path' 
            break 
            
#*****
# MAIN
#*****

log_file_name_base = os.path.join('.', 'Log_')

log_cnt=1
while(os.path.isfile(log_file_name_base+str(log_cnt)+'.txt')):
   log_cnt += 1
logfile = open(log_file_name_base+str(log_cnt)+'.txt','w')

logfile.write('AModify CBPROJ files ('+strftime("%Y-%m-%d %H:%M:%S", gmtime())+')\n')

print ("Start directory:")
InputDirectory = str(raw_input( "> " ))
 
print InputDirectory

# Check if file
#**************
if os.path.isfile(InputDirectory):

   # File   
   OneFile_Name   = os.path.basename(InputDirectory)
   StartDirectory = os.path.dirname(InputDirectory)
   
else:
   StartDirectory = InputDirectory
   OneFile_Name   = ''
   
   #Directory
   logfile.write('Start Directory: '+ StartDirectory +'\n')
   
   for dirname, dirnames, filenames in os.walk(StartDirectory):  
      # print path to all filenames.
      for filename in filenames:
         #exclude list
         if filename not in exclude_list: #and (OneFile_Name == '' or OneFile_Name == filename):                     
            filename_split = os.path.splitext(filename.upper())           
            if (filename_split[1] in file_types):               
               FullPath = dirname + '\\' + filename              
               print 'Modify: ' + FullPath
               
               failed = False
               enc="utf-8"
               try:
                  parser = etree.XMLParser(remove_blank_text=True)               
                  tree = etree.parse(FullPath,parser)
                  modify_cbproj(tree,IncludeDirectories,SourceFiles)
                  tree.write(dirname + '\\' + filename ,pretty_print = True)                  
               except:
                  failed = True
                  print 'Could not open ' + FullPath +'. Try ANSI encoding'
               
               if failed:
                  failed = False
                  enc = "ansi"
                  try:
                     parserANSI = etree.XMLParser(remove_blank_text=True, encoding = enc)               
                     tree = etree.parse(FullPath,parserANSI)  
                     modify_cbproj(tree,IncludeDirectories,SourceFiles)
                     tree.write(dirname + '\\' + filename ,pretty_print = True, encoding = enc)   
                     
                  except:
                     failed = True
                     print 'Failed to open ' + FullPath + '.'
                     
               logfile.close();
       