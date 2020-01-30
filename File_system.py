import os
import sys
from datetime import datetime
import tabulate
from ast import literal_eval
import logging
import hashlib

logger = logging.getLogger('File System')

allfilesystem_list = []

# print tabel naar scherm
def show_list(listname):
    try:
        header = listname[0].keys()
        rows = [x.values() for x in listname]
        tablefilesystem = tabulate.tabulate(rows, header, tablefmt='rst')
        logger.info('creating table of allfilesystem_list')
        print(tablefilesystem)
        logger.info('printed table to the screen')
        return tablefilesystem

    #voor als de invoer van het pad niet juist is
    except IndexError:
        logger.error('The input is incorrect')
        print('The input is incorrect, restart the program and try again (example: C:\\...)')

    #Voor als het gekozen pad te groot is om te analyseren
    except MemoryError:
        logger.error('The path size is too big')
        print('The path size is too big, restart the program and try a different of the path')


# schrijf tabel weg naar bestand
def save_list(listname):
    try:
        f = open('Filesystem.txt', 'w', encoding="utf-8")
        logger.info('open file: Filesystem.txt')
        f.write(listname)
        logger.info('writing results to file')
        f.close()
        logger.info('close file: Filesystem.txt')

        # locatie van de file
        print('\nThe results are saved into a file called Filesystem.txt on the location .\Filesystem.txt')
    except TypeError:
        print('')

    hasher = hashlib.md5()
    with open('Filesystem.txt', 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    hash1 = 'Filesystem.txt MD5 Hashwaarde: ' + hasher.hexdigest()
    logger.debug('Generating MD5 hash: ' + hasher.hexdigest())

    hashersha = hashlib.sha256()
    with open('Filesystem.txt', 'rb') as afile:
        buf = afile.read()
        hashersha.update(buf)
    hash2 = 'Filesystem.txt SHA256 Hashwaarde: ' + hashersha.hexdigest()
    logger.debug('Generating SHA256 hash: ' + hashersha.hexdigest())

    f = open('hashfile.txt', 'a', encoding="utf-8")
    logger.info('open file: hashfile.txt')
    f.write(hash1 + '\n' + hash2 + '\n')
    logger.info('writing md5 hash to file')
    f.close()
    logger.info('close file: hashfile.txt')


#om filesystem langs te lopen
def analysefilesystem(pathname):

    for (dirpath, dirnames, filenames) in os.walk(pathname):
        for f in filenames:
            try:
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
                logger.debug('Analyzing file system at the location: ' + dirpath)
                logger.debug('Analyzing file stats: ' + f)
                logger.info('Append file stats to allfilesystem_list')
                allfilesystem_list.append({'File path': dirpath, 'File name': f, 'File size (bytes)': file_size, 'last access': last_access, 'Last modified': last_modified, 'Creation time': creation_time})

            #voor als een file niet te vinden is, dat het programma dan die overslaat en verder gaat.
            except OSError:
                logger.warning('File not found: ' + f)

    return allfilesystem_list

def filterfiles(listname, size1, size2, name1, name2, path1, path2):
    filteredlist = []

    #filteroptie op File size
    if size1.upper() == 'Y':
        size2 = int(size2)
        sizelist = filter(lambda x: x['File size (bytes)'] == size2, listname)
        logger.info('filtering list')
        sizelist2 = list(sizelist)
        listc = str(sizelist2)
        if listc == '[]':
            logger.info('No results found on file size: ' + size1)
            print('File size not found in list of file system \n')

        for item in sizelist2:
            sizestr = str(item)
            sizestr2 = sizestr.replace('[', '')
            sizestr3 = sizestr2.replace(']', '')

            sizelistdict = literal_eval(sizestr3)
            filteredlist.append(sizelistdict)
            logger.info('found results')
            logger.info('append filtered files to allfilesystem_list')

    # filteroptie op File path
    if path1.upper() == 'Y':
        pathlist = filter(lambda x: x['File path'] == path2, listname)
        logger.info('filtering list')
        pathlist2 = list(pathlist)
        pathc = str(pathlist2)
        if pathc == '[]':
            logger.info('No results found on file path: ' + path1)
            print('Path not found in list of file system \n')

        for item in pathlist2:
            pathstr = str(item)
            pathstr2 = pathstr.replace('[', '')
            pathstr3 = pathstr2.replace(']', '')

            pathlistdict = literal_eval(pathstr3)
            filteredlist.append(pathlistdict)
            logger.info('found results')
            logger.info('append filtered files to allfilesystem_list')

    #filteroptie op File name
    if name1.upper() == 'Y':
        namelist = filter(lambda x: name2 in x['File name'], listname)
        logger.info('filtering list')
        namelist2 = list(namelist)
        namec = str(namelist2)
        if namec == '[]':
            logger.info('No results found on file name: ' + name1)
            print('Name not found in list of file system \n')

        for item in namelist2:
            namestr = str(item)
            namestr2 = namestr.replace('[', '')
            namestr3 = namestr2.replace(']', '')

            namelistdict = literal_eval(namestr3)
            filteredlist.append(namelistdict)
            logger.info('found results')
            logger.info('append filtered files to allfilesystem_list')

    if filteredlist == []:
        print("Did not find IOC in: File System ")
        #sys.exit(1)
    else:
        print("Found IOC, possible malware in: File System ")
    return filteredlist

def main(pathname, filter1, filtersize, sizef, filtername, namef, filterpath, pathf, save):
    logger.info('Started')
    filesystem_list = analysefilesystem(pathname)

    if filter1.upper() == 'Y':
        filesystem_list = filterfiles(filesystem_list, filtersize, sizef, filtername, namef, filterpath, pathf)
    if filesystem_list == []:
        print()
    else:
        tablelist = show_list(filesystem_list)

        if save.upper() == 'Y':
            save_list(tablelist)
    logger.info('Finished')

if __name__ == '__main__':
    main()