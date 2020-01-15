import os
from datetime import datetime
import tabulate
from ast import literal_eval
import logging

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
        logger.error('The input is incorrect, restarting file_system.py')
        print('The input is incorrect, try again (example: C:\\...)')
        main()

    #Voor als het gekozen pad te groot is om te analyseren
    except MemoryError:
        logger.error('The path size is too big, restarting file_system.py')
        print('The path size is too big, try a subfolder of the path')
        main()

# schrijf tabel weg naar bestand
def save_list(listname):
    logger.info('Asked input to save results to file')
    save = input('Do you want to save te results to a file? (Y/N)?: ')
    logger.debug('input to save result to file: ' + save)
    if save == 'Y':
        f = open('C:\\Users\lucil\PycharmProjects\RELY\Filesystem.txt', 'w', encoding="utf-8")
        logger.info('open file: Filesystem.txt')
        f.write(listname)
        logger.info('writing results to file')
        f.close()
        logger.info('close file: Filesystem.txt')

        # locatie van de file
        print('\nThe results are saved into a file called Filesystem.txt on the location C:\\Users\lucil\PycharmProjects\RELY\Filesystem.txt')
    else:
        print('The results are not saved.')

#om filesystem langs te lopen
def analysefilesystem():

    logger.info('Asked input pathname')
    # C:\\ met dubbele \
    pathname = input('Type in the path you want to analyze (e.g: .\.git): ')
    logger.info('Received input pathname: ' + pathname)
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

def filterfiles(listname):
    filteredlist = []

    logger.info('asked input to filter on file size')
    #filteroptie op File size
    size1 = input('Do you want to filter on file size? Y/N?: ')
    logger.debug('input to filter on file size: ' + size1)
    if size1 == 'Y':
        logger.info('asked input to type the file size in bytes')
        size2 = input('Type the file size you want to filter on. (bytes): ')
        logger.debug('input file size to filter on: ' + size2)
        size2 = int(size2)
        sizelist = filter(lambda x: x['File size (bytes)'] == size2, listname)
        logger.info('filtering list')
        sizelist2 = list(sizelist)
        for item in sizelist2:
            sizestr = str(item)
            sizestr2 = sizestr.replace('[', '')
            sizestr3 = sizestr2.replace(']', '')
            if sizestr3 == '':
                logger.info('No results found on file size: ' + size1)
            else:
                sizelistdict = literal_eval(sizestr3)
                filteredlist.append(sizelistdict)
                logger.info('found results')
                logger.info('append filtered files to allfilesystem_list')
    else:
        print('ok')

    logger.info('asked input to filter on file path')
    # filteroptie op File path
    path1 = input('Do you want to filter on file path? Y/N?: ')
    logger.debug('input to filter on file path: ' + path1)
    if path1 == 'Y':
        logger.info('asked input to type the file path')
        path2 = input('Type the file path you want to filter on: ')
        logger.debug('input file path to filter on: ' + path2)
        pathlist = filter(lambda x: x['File path'] == path2, listname)
        logger.info('filtering list')
        pathlist2 = list(pathlist)
        for item in pathlist2:
            pathstr = str(item)
            pathstr2 = pathstr.replace('[', '')
            pathstr3 = pathstr2.replace(']', '')
            if pathstr3 == '':
                logger.info('No results found on file path: ' + path1)
            else:
                pathlistdict = literal_eval(pathstr3)
                filteredlist.append(pathlistdict)
                logger.info('found results')
                logger.info('append filtered files to allfilesystem_list')
    else:
        print('ok')

    logger.info('asked input to filter on file name')
    #filteroptie op File name
    name1 = input('Do you want to filter on file name? Y/N?: ')
    logger.debug('input to filter on file name: ' + name1)
    if name1 == 'Y':
        logger.info('asked input to type the file name')
        name2 = input('Type the name of the file you want to filter on: ')
        logger.debug('input file name to filter on: ' + name2)
        namelist = filter(lambda x: x['File name'] == name2, listname)
        logger.info('filtering list')
        namelist2 = list(namelist)
        for item in namelist2:
            namestr = str(item)
            namestr2 = namestr.replace('[', '')
            namestr3 = namestr2.replace(']', '')
            if namestr3 == '':
                logger.info('No results found on file name: ' + name1)
            else:
                namelistdict = literal_eval(namestr3)
                filteredlist.append(namelistdict)
                logger.info('found results')
                logger.info('append filtered files to allfilesystem_list')
    else:
        print('ok')
    if filteredlist == []:
        print('No results found')
        return listname
    else:
        return filteredlist

def main():
    resultlist = analysefilesystem()
    tablelist = show_list(resultlist)

    logger.info('Asked input to filter the results')
    filtervraag = input('Do you want to filter the results? (Y/N)?: ')
    logger.debug('received input: ' + filtervraag)
    if filtervraag == 'Y':
        filteredlist = filterfiles(allfilesystem_list)
        tablelist = show_list(filteredlist)

    save_list(tablelist)

if __name__ == '__main__':
    logger.info('Started')
    main()
    logger.info('Finished')