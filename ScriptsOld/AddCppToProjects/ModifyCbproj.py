import os
import shutil
import sys
import fileinput
import re
from time import gmtime, strftime
from lxml import etree


IncludeDirectories = [] 
SourceFiles = ['windekis\Genix\ApWare32\WinDekis\Source\AddressDependencies.cpp','windekis\Genix\ApWare32\WinDekis\Source\AddressDependenciesReassignment.cpp']

exclude_list = ['NONE']
file_types   = ['.CBPROJ']


#***************
# modify_cbproj
#***************
def modify_cbproj(XmlTree,IncludeDirectories,SourceFiles):
   is_modified = False
   root = XmlTree.getroot() 
   ns = root.tag[:root.tag.find('Project')]
   
   MaxBuildOrderBelowK = 0;
   MinBuildOrderAboveK = 9999999;
   MaxBuildOrder       = 0;
   
   GenixPath = ''
   for fld in root.iter(ns + 'CppCompile'):
      #print(fld.attrib)
      pos = fld.attrib['Include'].upper().find('GENIX')
      if pos > 0:
         GenixPath = fld.attrib['Include'][0:pos]
         break
   
   for fld in root.iter(ns + 'BuildOrder'):
      Order = int(fld.text)
      if Order > MaxBuildOrder:
         MaxBuildOrder = Order               
         
   IncludeOrderNr = MaxBuildOrder
   
   for SourceFile in SourceFiles: 
      FilePathShort = SourceFile[SourceFile.upper().find('GENIX'):]
      RelSourceFile = GenixPath+FilePathShort   
      
      found = False
      for fld in root.iter(ns + 'CppCompile'):
         if fld.attrib['Include'].find(RelSourceFile) >= 0:
            found = True 
            #print(RelSourceFile + ' already included')
            break
      
      if not found:
         #print('Add ' + RelSourceFile) 
         IncludeOrderNr += 1   
         
         ItemGroupEle = root.findall(ns + 'ItemGroup')[0]

         MyAttrib = {"Include": RelSourceFile}
         CPPCompEle = etree.SubElement(ItemGroupEle, ns+'CppCompile',  attrib=MyAttrib)
         
         BOEle = etree.SubElement(CPPCompEle, ns+'BuildOrder')
         BOEle.text = str(IncludeOrderNr)
         is_modified = True         
         
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
            print('Delete text ' + str(pos) + '-' + str(pos+len(RelIncludePath)+1)) 
         RelIncludePathNS = RelIncludePath.rstrip('\\')            
         while fld.text.find(RelIncludePathNS) >=0:
            pos = fld.text.find(RelIncludePathNS)
            Text = fld.text[:pos] + fld.text[(pos+len(RelIncludePathNS)+1):]
            fld.text = Text
            print('Delete text ' + str(pos) + '-' + str(pos+len(RelIncludePathNS)+1)) 
            
   for IncludeDir in IncludeDirectories:
      IncludePathShort = IncludeDir[IncludeDir.upper().find('GENIX'):]      
      RelIncludePath   = GenixPath+IncludePathShort
      RelIncludePath   = RelIncludePath.rstrip('\\') + '\\'
      
      for fld in root.iter(ns + 'IncludePath'):
         if fld.text.find(RelIncludePath) < 0:
            #print('Add to include path: ' + RelIncludePath)
            pos = fld.text.find('$(IncludePath)')
            fld.text =  fld.text[:pos] + RelIncludePath + ';' + fld.text[pos:]
            is_modified = True
            break
         else:           
            #print(RelIncludePath +' already in include path')
            break 
   return is_modified
   
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
   
    files = ['C:\Projekte\windekis_src\WK\windekis/ABL/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/ABL_PKB/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/AMBIT_CIM/Windekis/WinDekis/AmbitCim.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Ansbacher_Nassau/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/apoBank/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Arab_Bank/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Arab_Bank/Windekis/WinDekis/WinDekisMaster.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BAB/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Bank von Roll/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BBB/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BBB/Windekis/WinDekis/WinDekis_NM.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BBVA/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BBVA/Windekis/WinDekis/WinDekisEnc.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BES/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BHF98_2/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BHF98_2/Windekis/WinDekis/WinDekisEnc.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BIL/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Bonhote/Windekis/WinDekis/AmbitCim.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BOV/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BOV/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BOV_PKB_Demo/Windekis/WinDekis/WinDekisPkbXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BPGE/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BPGE_Tresor/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BPMO/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BPMO_Tresor/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BPNA/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/BPNA_Tresor/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Bvv/WINDEKIS/WINDEKIS/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Bwl/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/ClaridenLeuSingapore/WinDekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/ClaridenLeuSingapore/WinDekis/WinDekis/WinDekisExtGuiXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/ClaridenLeuSingapore/WinDekis/WinDekis/WinDekisW.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/ClaridenLeuSingapore/WinDekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Credit-Suisse/Windekis/WinDekis/CreditSuisseAmbitDashboardVCL.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Credit-Suisse/Windekis/WinDekis/CreditSuisseAmbitVCL.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Credit-Suisse/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Credit-Suisse/Windekis/WinDekis/WinDekisSave.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Deltec/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Dexia/WinDekis/WINDEKIS/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Fidu/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Finter/Windekis/WinDekis/AmbitCIM.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Finter/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Finter/Windekis/WinDekis/WinDekisW.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Finter/Windekis/WinDekis/WinDekisWXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Finter/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Gonet/WinDekis/WINDEKIS/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Gonet/WinDekis/WINDEKIS/WinDekisSign.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Gonet_GON_CIM/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Gonet_GON_CIM/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/GUT/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/GUT/Windekis/WinDekis/WinDekisEnc.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/GUT/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/GUT DEMO/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Gutzwiller/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Hiv/Windekis/WinDekis/WinDekis-XE4.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Hiv/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/InCore/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/JCE Hottinger/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/JCE Hottinger/Windekis/WinDekis/WinDekisMaster.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/LBBW/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/LBLux_Phase_III/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/LBLux_Phase_III/Windekis/WinDekis/WinDekisEnc.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Macie/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/MediBank/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Metropol/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/MRV/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/NHB/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Nomura/WinDekis/WINDEKIS/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/PB_Ihag/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Piguet-Galland/Windekis/WinDekis/WinDekisEnc.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/PKB/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/PKB Fatca Workshop/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Private Investment Bank Nassau/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/RBL/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/RBL/Windekis/WinDekis/WinDekisEnc.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Scobag/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Selvi/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Sfb_MultiLanguage/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Sfb_Wdk/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/TBA/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Trafina/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Vbv/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Vbv_Tresor/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Weg/Windekis/WinDekis/NotensteinAmbitDashboardVCL.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Weg/Windekis/WinDekis/NotensteinAmbitVCL.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Weg/Windekis/WinDekis/WinDekis.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Weg/Windekis/WinDekis/WinDekisMerge.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Weg/Windekis/WinDekis/WinDekisXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Weg_Tresor_2013/Windekis/WinDekis/WinDekisTresorXE2.cbproj' ,'C:\Projekte\windekis_src\WK\windekis/Weg_Tresor_2013/Windekis/WinDekis/WinDekisXE2.cbproj']
   
    for file in files:          
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
           is_changed = modify_cbproj(tree,IncludeDirectories,SourceFiles)
           print('Modeify ' + str(file), is_changed)
           if is_changed:
               tree.write(file, pretty_print=True, encoding=encoding)
    
    logfile.close();
       