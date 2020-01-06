import os
from datetime import datetime
import tabulate

allfilesystem_list = []

#om de list naar het bestand toe te schrijven en naar scherm te printen
def savelist(listname):

    #print tabel naar scherm
    header = allfilesystem_list[0].keys()
    rows = [x.values() for x in allfilesystem_list]
    tablefilesystem = tabulate.tabulate(rows, header, tablefmt='rst')
    print(tablefilesystem)

    #schrijf tabel weg naar bestand
    f = open('C:\\Users\lucil\OneDrive\Documenten\school\Filesystem.txt', 'w')
    f.write(tablefilesystem)
    f.close()

    #locatie moet nog worden bepaald
    print('\nThe analysis is saved into a file called Filesystem.txt on the location ...')

#om filesystem langs te lopen
def analysefilesystem():

    # C:\\ met dubbele \
    pathname = input('Type in the path you want to analyze: ')

    for (dirpath, dirnames, filenames) in os.walk(pathname):
        for f in filenames:

            path = os.path.join(dirpath, f)
            file_stats = os.stat(path)
            lastaccess = file_stats.st_atime
            lastmodified = file_stats.st_mtime
            creationtime = file_stats.st_ctime

            #om de datetime te veranderen naar een string
            last_access = datetime.fromtimestamp(lastaccess)
            last_access = last_access.strftime('%d/%m/%Y %H:%M:%S')
            last_modified = datetime.fromtimestamp(lastmodified)
            last_modified = last_modified.strftime('%d/%m/%Y %H:%M:%S')
            creation_time = datetime.fromtimestamp(creationtime)
            creation_time = creation_time.strftime('%d/%m/%Y %H:%M:%S')
            file_size = file_stats.st_size

            allfilesystem_list.append({'File path': path, 'File name': f, 'File size (bytes)': file_size, 'last access': last_access, 'Last modified': last_modified, 'Creation time': creation_time})


if __name__ == '__main__':

    analysefilesystem()
    savelist(allfilesystem_list)

