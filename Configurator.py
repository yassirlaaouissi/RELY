import logging
import sys

import File_system
import proces_list
import registry_key
import scheduled_tasks
from pyfiglet import *

#from stringcolor import *

f = open('hashfile.txt', 'w', encoding="utf-8")
f.close()

#Logger is aangeroepen over het hele project

logging.basicConfig(handlers=[logging.FileHandler('logboek.log', 'w', 'utf-8')], format='%(name)s: %(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)


#Welcome banner
ascii_banner = Figlet(font='STANDARD')
ascii_banner2 = ascii_banner.renderText("Welcome to RELY")
print(ascii_banner2)
ascii_banner = Figlet(font='digital')
ascii_underbanner = ascii_banner.renderText("Team firebreathing rubberduckies")
print(ascii_underbanner)



# File System
Wanna_use_FS = input("Do you want to scan on file system (Y or N)? ")
filter1 = ''
filtersize = ''
sizef = ''
filtername = ''
namef = ''
filterpath = ''
pathf = ''
pathname = ""
save = ""
if (Wanna_use_FS.upper() == "N"):
    uselessvar=""
elif (Wanna_use_FS.upper() == "Y"):

    pathname = input('Type in the path you want to analyze (.\.idea): ')

    filter1 = input('Do you want to filter the results? (Y/N): ')
    if filter1.upper() == 'Y':

        filtersize = input('Do you want to filter on file size? (Y/N): ')
        if filtersize.upper() == 'Y':
            sizef = input('Type the file size you want to filter on. (bytes): ')
        elif filtersize.upper() == 'N':
            uselessvar = ""
        else:
            print("Did not select Y or N, please restart program and try again")

        filtername = input('Do you want to filter on file name? (Y/N): ')
        if filtername.upper() == 'Y':
            namef = input('Type the file name you want to filter on (e.g: blank.pys): ')
        elif filtername.upper() == 'N':
            uselessvar=""
        else:
            print("Did not select Y or N, please restart program and try again")

        filterpath = input('Do you want to filter on path? (Y/N): ')
        if filterpath.upper() == 'Y':
            pathf = input('Type the path you want to filter on (e.g: .\dist\Configurator ): ')
        elif filterpath.upper() == 'N':
            uselessvar=""
        else:
            print("Did not select Y or N, please restart program and try again")

    elif filter1.upper() == 'N':
        uselessvar=""
    else:
        print("Did not select Y or N, please restart program and try again")

    save = input('Do you want to save te results to a file? (Y/N)?: ')
    if save.upper() == 'N' or save.upper() == 'Y':
        uselessvar=""
    else:
        print("Did not select Y or N, please restart program and try again")

else:
    print("Did not select Y or N, please restart program and try again")
    sys.exit(1)

z = open("OneTimeScan/params.txt","w+")
z.write("##Filesystem Params##\n")
z.write("pathname: " + str(pathname) + "\n")
z.write("filter1: " + str(filter1) + "\n")
z.write("filtersize: " + str(filtersize) + "\n")
z.write("filtername: " + str(filtername) + "\n")
z.write("filterpath: " + str(filterpath) + "\n")
z.write("save: " + str(save) + "\n")
z.write("sizef: " + str(sizef) + "\n")
z.write("namef: " + str(namef) + "\n")
z.write("pathf: " + str(pathf) + "\n")
z.write("\n")


#scheduled tasks

print()
WantToFilter = ""
filterOnName = ""
filterOnState = ""
filterOnPath = ""
WantToPrintList = ""
Wanna_use_Tasks = input("Do you want to scan on Scheduled Tasks (Y or N)? ")
if(Wanna_use_Tasks.upper() == "N"):
    uselessvar=""
elif(Wanna_use_Tasks.upper() == "Y"):

    WantToFilter = input("Do you want to filter the scheduled tasks? (Y or N): ")
    if(WantToFilter.upper() == "Y"):
        filterOnName = input("If you want to filter on name of task please give the name, otherwise leave blank and press enter (e.g: CCleanerSkipUAC ): ")
        filterOnState = input("If you want to filter on state of task please give the state, otherwise leave blank and press enter (e.g: Completed): ")
        filterOnPath = input("If you want to filter on path of task please give the path, otherwise leave blank and press enter (e.g: \CCleanerSkipUAC): ")
    WantToPrintList = input("Do you want to print the results of the scheduled task scan? (Y or N): ")

else:
    print("Did not select Y or N, please restart program and try again")
    sys.exit(1)

z.write("##Scheduled tasks Params##\n")
z.write("Name: " + str(filterOnName) + "\n")
z.write("State: " + str(filterOnState) + "\n")
z.write("Path: " + str(filterOnPath) + "\n")
z.write("printlist: " + str(WantToPrintList) + "\n")
z.write("WantToFilter: " + str(WantToFilter) + "\n")
z.write("\n")




#Registry Keys
print()
geef_HKEY = ""
geef_pad = ""
filter_vraag = ""
filter_naam = ""
filter_type = ""
Wanna_use_Keys = input("Do you want to scan on Registry keys (Y or N)? ")

if (Wanna_use_Keys.upper() == "N"):
    uselessvar=""
elif (Wanna_use_Keys.upper() == "Y"):



    geef_HKEY = input("Please give an HKEY (e.g. HKEY_LOCAL_MACHINE): ")
    geef_pad = input(
        "Please give the path you want to be scanned (e.g: " + r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Git_is1" + "): ")

    filter_vraag = input("Do you want to filter the registry keys? Y/N: ")
    if filter_vraag.upper() == "Y":
        filter_naam = input("Do you want to filter on name? Please give the name otherwise leave blank and press enter (e.g: DisplayName): ")
        filter_type = input("Do you want to filter on type? Please give the type otherwise leave blank and press enter (e.g: REG_SZ): ")
    if filter_vraag.upper() == "N":
        uselessvar=""
else:
    print("Did not select Y or N, please restart program and try again")


z.write("##Registry keys Params##\n")
z.write("HKEY: " + str(geef_HKEY) + "\n")
z.write("Path: " + str(geef_pad) + "\n")
z.write("WannaFilter: " + str(filter_vraag) + "\n")
z.write("Name: " + str(filter_naam) + "\n")
z.write("Type: " + str(filter_type) + "\n")
z.write("\n")


# Proces List
print()
filter_question = ""
filter_name = ""
filter_path = ""
want_to_use_proceslist = input("Do you want to scan on Processes (Y or N)? ")
if (want_to_use_proceslist.upper() == "N"):
    uselessvar=""
elif (want_to_use_proceslist.upper() == "Y"):
    filter_question = input("Do you want to filter the processes? Y/N: ")
    if(filter_question.upper() == "Y"):
        filter_name = input("Do you want to filter on name? Please give the name otherwise leave blank and press enter (e.g. svchost.exe): ")
        filter_path = input("Do you want to filter on type? Please give the type otherwise leave blank and press enter (e.g. C:\Windows\System32\dllhost.exe): ")
else:
    print("Did not select Y or N, please restart program and try again")
    sys.exit(1)

z.write("##Proces list Params##\n")
z.write("WannaFilter: " + str(filter_question) + "\n")
z.write("Name: " + str(filter_name) + "\n")
z.write("Pad: " + str(filter_path) + "\n")

z.write("\n")



#pre EXE
print()
if (Wanna_use_FS.upper() == "Y"):
    File_system.main(pathname, filter1, filtersize, sizef, filtername, namef, filterpath, pathf, save)

print()
if(Wanna_use_Tasks.upper() == "Y"):
    scheduled_tasks.main(WantToFilter, filterOnName, filterOnState, filterOnPath, WantToPrintList)

print()
if(Wanna_use_Keys.upper() == "Y"):
    registry_key.main(geef_HKEY, geef_pad, filter_vraag, filter_naam, filter_type)

print()
if(want_to_use_proceslist.upper() == "Y"):
    proces_list.main(filter_question, filter_name, filter_path)

print()
WannaExit = input("To exit the program press Y? ")
if WannaExit.upper() == "Y":
    sys.exit(1)



