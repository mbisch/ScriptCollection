#!/usr/bin/env python

from __future__ import print_function
import sys, os, datetime
import re, locale
from subprocess import Popen,PIPE,STDOUT
import zipfile, glob
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED
    
### Globals    
tag_re = re.compile('(.+)(?=-v[0-9])(-)(.*)')

def get_zip_info(archive_name):
    """Get Info for ZIP Files"""
    zf = zipfile.ZipFile(archive_name)
    info_txt = ''
    for info in zf.infolist():
        info_txt += info.filename + '\n'
        info_txt += '\tModified:\t' + str(datetime.datetime(*info.date_time)) + '\n'
        info_txt += '\tZIP version:\t' + str(info.create_version) + '\n'
        info_txt += '\tCompressed:\t' + str(info.compress_size) + ' bytes' + '\n'
        info_txt += '\tUncompressed:\t' + str(info.file_size) + 'bytes' + '\n'
    return info_txt

def add_to_zip(dest, zipname, file_list, append = False):
    """ Add files to zip """    
    zip_modes = {zipfile.ZIP_DEFLATED: 'deflated',
                 zipfile.ZIP_STORED:   'stored',
                }
                
    dest_zipname = os.path.join(dest,zipname)            
    f_mode = 'w'
    if append:
        f_mode = 'a'
        
    zf = zipfile.ZipFile(dest_zipname, mode=f_mode)
    try:
        for file in file_list:
            print('adding '+file+' to '+zipname+' with compression mode', zip_modes[compression])
            zf.write(file, os.path.basename(file), compress_type=compression)
    except:
        print('Error while writing to '+ dest_zipname)
        return 1
    finally:
        zf.close()
     

def main(argv):
    if len(argv) < 1:
       print('Argument missing!')
       sys.exit(1)    
       
    tag = argv[0]
    project = tag_re.search(argv[0].lower())
    path_cmd = os.path.dirname(os.path.realpath(__file__))
               
    add_to_zip('C:\Projekte\other\Scripts\Test',tag+'.zip',['C:\Projekte\other\Scripts\CountLines\Log_1.txt','C:\Projekte\other\Scripts\CountLines\Log_2.txt'])
    add_to_zip('C:\Projekte\other\Scripts\Test',tag+'.zip',['C:\Projekte\other\Scripts\CountLines\Log_2.txt'],True)

    target_dir_base = ''
    try:
        target_dir_base = os.environ['AMBIT_CIM_OUT_DIR']
    except:
        print('ERROR: Environment variable AMBIT_CIM_OUT_DIR is not defined')
        sys.exit(1)
    print(target_dir_base) 
    
    target_path = os.path.join(target_dir_base,'Weg','AmbitCIM','*.exe')
    print(target_path)
    exe_file = glob.glob(target_path)
    print(exe_file)
    #exe_path = os.path.join()
    
    readme_txt = ''
    readme_txt += 'Build-Tag: ' + tag + '\n\n' 
    readme_txt += 'Date: ' + str(datetime.datetime.now()) + '\n\n' 
    readme_txt += 'ZIP Info: ' + 'FILE:ZIP'
    readme_txt += get_zip_info('C:\Projekte\other\Scripts\Test\Test.zip')
    print(readme_txt)
    
if __name__ == "__main__":
    main(sys.argv[1:])