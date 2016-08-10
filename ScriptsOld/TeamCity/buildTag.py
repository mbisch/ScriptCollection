#!/usr/bin/env python

import sys
import re, locale
from subprocess import Popen,PIPE,STDOUT

from time import gmtime, strftime

tag_re = re.compile('(.+)(?=-v[0-9])(-)(.*)')

def main(argv):
   if len(argv) < 2:
      print('Arguments missing!')
      sys.exit(1)
         
   project = tag_re.search(argv[0].lower())
   path_cmd = argv[1]
   
   if project != None:
      key = project.group(1)
      version = project.group(3)
      
      project_conf = {
         'ansbacher'      : [path_cmd+'/Build-Ansbacher.cmd'     ,'Ansbacher_Nassau'],
         'arab'           : [path_cmd+'/Build-Arab.cmd'          ,'Arab_Bank'],
         'bab'            : [path_cmd+'/Build-BAB.cmd'           ,'BAB'],
         'bbb'            : [path_cmd+'/Build-BBB.cmd'           ,'BBB'],
         'bbva'           : [path_cmd+'/Build-BBVA.cmd.redundant','BBVA'],
         'berenberg'      : [path_cmd+'/Build-Berenberg.cmd'     ,'Berenberg'],
         'bes'            : [path_cmd+'/Build-BES.cmd'           ,'BES'],
         'bhf'            : [path_cmd+'/Build-BHF.cmd'           ,'BHF98_2'],
         'bil'            : [path_cmd+'/Build-BIL.cmd'           ,'BIL'],
         'bov'            : [path_cmd+'/Build-BOV.cmd'           ,'BOV'],
         'bwl'            : [path_cmd+'/Build-BWL.cmd'           ,'Bwl'],
         'credit-suisse'  : [path_cmd+'/Build-Credit-Suisse.cmd' ,'Credit-Suisse'],
         'deltec'         : [path_cmd+'/Build-Deltec.cmd'        ,'Deltec'],
         'finter'         : [path_cmd+'/Build-Finter.cmd'        ,'Finter'],
         'goncim'         : [path_cmd+'/Build-GonCim.cmd'        ,'Gonet_GON_CIM'],
         'gutzwiller'     : [path_cmd+'/Build-Gutzwiller.cmd'    ,'Gutzwiller'],
         'hiv'            : [path_cmd+'/Build-HIV.cmd'           ,'Hiv'],
         'jceh'           : [path_cmd+'/Build-JCE.cmd'           ,'JCE Hottinger'],
         'lbbw'           : [path_cmd+'/Build-LBBW.cmd'          ,'LBBW'],
         'lblux'          : [path_cmd+'/Build-LBLUX.cmd'         ,'LBLux_Phase_III'],
         'lgt'            : [path_cmd+'/Build-LGT.cmd'           ,'LGT_BOSS_CH'],
         'metropol'       : [path_cmd+'/Build-Metropol.cmd'      ,'Metropol'],
         'morval'         : [path_cmd+'/Build-Morval.cmd'        ,'MRV'],
         'nhb'            : [path_cmd+'/Build-NHB.cmd'           ,'NHB'],
         'nomura'         : [path_cmd+'/Build-Nomura.cmd'        ,'Nomura'],
         'pbihag'         : [path_cmd+'/Build-Pbihag.cmd'        ,'PB_Ihag'],
         'piguet-galland' : [path_cmd+'/Build-Piguet-Galland.cmd','Piguet-Galland'],
         'pkb'            : [path_cmd+'/Build-Pkb.cmd'           ,'PKB'],
         'rbl'            : [path_cmd+'/Build-RBL.cmd'           ,'RBL'],
         'vbv'            : [path_cmd+'/Build-Vbv.cmd'           ,'Vbv'],
         'weg'            : [path_cmd+'/Build-WEG.cmd'           ,'Weg'],
         'wegmerge'       : [path_cmd+'/Build-WEG-Merge.cmd'     ,'Weg'],
         'wegrms'         : [path_cmd+'/Build-WEG-RMS.cmd'       ,'WegRms'],
      }  
   
      if key in project_conf:  
         proc = Popen([project_conf.get(key)[0]], shell=False, stdout=PIPE)
         proc.wait()
         encoding = locale.getdefaultlocale()[1]
         print((proc.communicate()[0]).decode(encoding))
         sys.exit(proc.returncode)

   print("Project key " + key + " unknown")   
   sys.exit(1)            


if __name__ == "__main__":
   main(sys.argv[1:])