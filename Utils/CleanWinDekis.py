import os
import fnmatch

startdirs = ['C:\Projekte\windekis_src\WK\windekis','C:\Projekte\windekis_src\TEST\windekis']
#startdirs = ['C:\Projekte\windekis_src\WK\windekis\PKB\Windekis']
del_dir = ['out32','debug_build']
del_expr = ['*.pch','*.#*','*.obj']

size = 0
for startdir in startdirs:
    for dirname, dirnames, filenames in os.walk(startdir):  
        for filename in filenames:
            dir = os.path.basename(os.path.normpath(dirname))
            if dir.lower() in del_dir:
                for me in del_expr:
                    if fnmatch.fnmatch(filename.lower(), me):
                        FullPath = dirname + '\\' + filename
                        statinfo = os.stat(FullPath)
                        size += statinfo.st_size
                        print('Delete: ',FullPath)
                        try:
                           os.remove(FullPath)                       
                        except:
                           print('file probably locked')
                           
print('Recovered: ',round(size/1024/1024), 'Mb')