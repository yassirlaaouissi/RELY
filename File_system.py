import os
from datetime import datetime
import tabulate
from ast import literal_eval

allfilesystem_list = []

# print tabel naar scherm
def show_list(listname):
    header = listname[0].keys()
    rows = [x.values() for x in listname]
    tablefilesystem = tabulate.tabulate(rows, header, tablefmt='rst')
    print(tablefilesystem)
    return tablefilesystem

# schrijf tabel weg naar bestand
def save_list(listname):
    save = input('Do you want to save te results to a file? (Y/N)?: ')
    if save == 'Y':
        f = open('C:\\Users\lucil\PycharmProjects\RELY\Filesystem.txt', 'w')
        f.write(listname)
        f.close()

        # locatie moet nog worden bepaald
        print('\nThe results are saved into a file called Filesystem.txt on the location C:\\Users\lucil\PycharmProjects\RELY\Filesystem.txt')
    else:
        print('The results are not saved.')

#om filesystem langs te lopen
def analysefilesystem():

    # C:\\ met dubbele \
    pathname = input('Type in the path you want to analyze: ')

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

                allfilesystem_list.append({'File path': path, 'File name': f, 'File size (bytes)': file_size, 'last access': last_access, 'Last modified': last_modified, 'Creation time': creation_time})
            except OSError:
                print

    return allfilesystem_list

def filterfiles(listname):
    filteredlist = []

    #filteroptie op File size
    size1 = input('Do you want to filter on file size? Y/N?: ')
    if size1 == 'Y':
        size2 = input('Type the file size you want to filter on. (bytes): ')
        size2 = int(size2)
        sizelist = filter(lambda x: x['File size (bytes)'] == size2, listname)
        sizelist2 = list(sizelist)
        for item in sizelist2:
            sizestr = str(item)
            sizestr2 = sizestr.replace('[', '')
            sizestr3 = sizestr2.replace(']', '')
            if sizestr3 == '':
                print('No results found')
            else:
                sizelistdict = literal_eval(sizestr3)
                filteredlist.append(sizelistdict)
    else:
        print('ok')

    #filteroptie op File name
    name1 = input('Do you want to filter on file name? Y/N?: ')
    if name1 == 'Y':
        name2 = input('Type the name of the file you want to filter on: ')
        namelist = filter(lambda x: x['File name'] == name2, listname)
        namelist2 = list(namelist)
        for item in namelist2:
            namestr = str(item)
            namestr2 = namestr.replace('[', '')
            namestr3 = namestr2.replace(']', '')
            if namestr3 == '':
                print('No results found')
            else:
                namelistdict = literal_eval(namestr3)
                filteredlist.append(namelistdict)
    else:
        print('ok')

    return filteredlist


if __name__ == '__main__':

    resultlist = analysefilesystem()
    tablelist = show_list(resultlist)

    filtervraag = input('Do you want to filter the results? (Y/N)?: ')
    if filtervraag == 'Y':
        filteredlist = filterfiles(allfilesystem_list)
        tablelist = show_list(filteredlist)

    save_list(tablelist)