import logging
import sys

import File_system
import proces_list
import registry_key
import scheduled_tasks
from pyfiglet import Figlet
from stringcolor import *

f = open('hashfile.txt', 'w', encoding="utf-8")
f.close()

#Logger is aangeroepen over het hele project
logging.basicConfig(handlers=[logging.FileHandler('logboek.log', 'w', 'utf-8')], format='%(name)s: %(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)


#Welcome banner
ascii_banner = Figlet(font='STANDARD')
ascii_banner2 = ascii_banner.renderText("Welcome to RELY")
print(cs(ascii_banner2, "blue"))
ascii_banner = Figlet(font='digital')
ascii_underbanner = ascii_banner.renderText("Team firebreathing rubberduckies")
ascii_underbanner2 = ascii_underbanner.replace("|", " ")
print(cs(ascii_underbanner2, "yellow"))
#ascii_banner = pyfiglet.figlet_format("Welcome  to  RELY")
#ascii_under = pyfiglet.print_figlet("", "big", 33)


# File System
Wanna_use_FS = input("Do you want to scan on file system (Y or N)? ")
#Wanna_use_Tasks = input("Do you want to scan on Scheduled Tasks (Y or N)? ")
#Wanna_use_Keys = input("Do you want to scan on Registry keys (Y or N)? ")

if(Wanna_use_FS.upper() == "N"):
    print("")
elif(Wanna_use_FS.upper() == "Y"):

    filter1 = ''
    filtersize = ''
    sizef = ''
    filtername = ''
    namef = ''
    filterpath = ''
    pathf = ''

    pathname = input('Type in the path you want to analyze (.\.idea): ')

    filter1 = input('Do you want to filter the results? (Y/N): ')
    if filter1.upper() == 'Y':
        filtersize = input('Do You want to filter on file size? (Y/N): ')
        if filtersize.upper() == 'Y':
            sizef = input('Type the file size you want to filter on. (bytes): ')
        if filtersize.upper() == 'N':
            print()
        if filtersize.upper() != 'Y' + filtersize.upper() != 'N':
            print("Did not select Y or N, please restart program and try again")
            sys.exit(1)
        filtername = input('Do You want to filter on file name? (Y/N): ')
        if filtername.upper() == 'Y':
            namef = input('Type the file name you want to filter on: ')
        if filtername.upper() == 'N':
            print()
        if filtername.upper() != 'Y' + filtername.upper() != 'N':
            print("Did not select Y or N, please restart program and try again")
            sys.exit(1)

        filterpath = input('Do You want to filter on path? (Y/N): ')
        if filterpath.upper() == 'Y':
            pathf = input('Type the path you want to filter on: ')
        if filterpath.upper() == 'N':
            print()
        if filterpath.upper() != 'Y' + filterpath.upper() != 'N':
            print("Did not select Y or N, please restart program and try again")
            sys.exit(1)


    if filter1.upper() == 'N':
        print()
    else:
        print("Did not select Y or N, please restart program and try again")
        sys.exit(1)

    save = input('Do you want to save te results to a file? (Y/N)?: ')

else:
    print("Did not select Y or N, please restart program and try again")
    sys.exit(1)



#scheduled tasks


Wanna_use_Tasks = input("Do you want to scan on Scheduled Tasks (Y or N)? ")
if(Wanna_use_Tasks.upper() == "N"):
    print("")
elif(Wanna_use_Tasks.upper() == "Y"):
    WantToFilter = ""
    filterOnName = ""
    filterOnState = ""
    filterOnPath = ""
    WantToPrintList = ""
    WantToFilter = input("Do you want to filter the scheduled tasks? (Y or N): ")
    if(WantToFilter.upper() == "Y"):
        filterOnName = input("If you want to filter on name of task please give the name, else leave blank and press enter (e.g: CCleanerSkipUAC ): ")
        filterOnState = input("If you want to filter on state of task please give the state, else leave blank and press enter (e.g: Completed): ")
        filterOnPath = input("If you want to filter on path of task please give the path, else leave blank and press enter (e.g: \CCleanerSkipUAC): ")
    WantToPrintList = input("Do you want to print the results of the scheduled task scan? (Y or N): ")

else:
    print("Did not select Y or N, please restart program and try again")
    sys.exit(1)

#Registry Keys
Wanna_use_Keys = input("Do you want to scan on Registry keys (Y or N)? ")

if (Wanna_use_Keys.upper() == "N"):
    print("")
elif (Wanna_use_Keys.upper() == "Y"):

    geefHKEY = ""
    geefPad = ""
    filterVraag = ""
    filterNaam = ""
    filterType = ""

    geefHKEY = input("Please give an HKEY (e.g. HKEY_LOCAL_MACHINE): ")
    geefPad = input(
        "Please give the path you want to be scanned (e.g: " + r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Git_is1" + "): ")

    filterVraag = input("Do you want to filter the registry keys? Y/N: ")
    if filterVraag.upper() == "Y":
        filterNaam = input("Do you want to filter on name? Please give the name else leave blank and press enter: ")
        filterType = input("Do you want to filter on type? Please give the type else leave blank and press enter: ")
    if filterVraag.upper() == "N":
        print()
else:
    print("Did not select Y or N, please restart program and try again")



# Proces List
filter_question = ""
filter_name = ""
filter_path = ""
want_to_use_proceslist = input("Do you want to scan on Processes (Y or N)? ")
if (want_to_use_proceslist.upper() == "N"):
    print("")
elif (want_to_use_proceslist.upper() == "Y"):
    filter_question = input("Do you want to filter the processes? Y/N: ")
    if(filter_question.upper() == "Y"):
        filter_name = input("Do you want to filter on name? Please give the name else leave blank and press enter: ")
        filter_path = input("Do you want to filter on type? Please give the type else leave blank and press enter: ")
else:
    print("Did not select Y or N, please restart program and try again")
    sys.exit(1)









#pre EXE
if (Wanna_use_FS.upper() == "Y"):
    File_system.main(pathname, filter1, filtersize, sizef, filtername, namef, filterpath, pathf, save)

if(Wanna_use_Tasks.upper() == "Y"):
    scheduled_tasks.main(WantToFilter, filterOnName, filterOnState, filterOnPath, WantToPrintList)

if(Wanna_use_Keys.upper() == "Y"):
    registry_key.main(geefHKEY, geefPad, filterVraag, filterNaam, filterType)

if(want_to_use_proceslist.upper() == "Y"):
    proces_list.main(filter_question, filter_name, filter_path)