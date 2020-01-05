import os
from datetime import datetime

#tijdelijke bestandslocatie
f = open('C:\\Users\lucil\OneDrive\Documenten\school\Filesystem.txt', 'w')
f.write('               File name                 File size              Last Access              Last modified              Creation time       \n')

#om de list naar het bestand toe te schrijven
def savelist(listname):
    for fileinfo in listname:
        filefile = str(fileinfo)

        f = open('C:\\Users\lucil\OneDrive\Documenten\school\Filesystem.txt', "a")
        f.write('%s\t\t' % filefile)
        f.close()
    f = open('C:\\Users\lucil\OneDrive\Documenten\school\Filesystem.txt', "a")
    f.write('\n')
    f.close()

#C:\\ met dubbele \
pathname = input('Type in the path you want to analyze: ')

#om filesystem langs te lopen
for (dirpath, dirnames, filenames) in os.walk(pathname):
    for f in filenames:

        file_stats = os.stat(dirpath)
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

        #resultaten voor op het scherm zelf
        print('\nFile name :', os.path.join(dirpath, f))
        print('File size:', file_stats.st_size, 'bytes')
        print('Time of last access:', datetime.fromtimestamp(lastaccess))
        print('Time of last modification:', datetime.fromtimestamp(lastmodified))
        print('Creation time:', datetime.fromtimestamp(creationtime))

        filesystem_list = [os.path.join(dirpath, f), file_stats.st_size, last_access, last_modified, creation_time]
        savelist(filesystem_list)

#locatie nog te bepalen
print('\nThe analysis is saved into a file called Filesystem.txt on the location ...')




