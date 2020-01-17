import logging
import File_system
import registry_key
import scheduled_tasks
from pyfiglet import Figlet
from stringcolor import *

#Logger is aangeroepen over het hele project
logging.basicConfig(handlers=[logging.FileHandler('logboek.log', 'w', 'utf-8')], format='%(name)s: %(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

#cowsay.daemon("Welcome to RELY, the malware analyser made by team fire breathing rubber duckies")

ascii_banner = Figlet(font='STANDARD')
ascii_banner2 = ascii_banner.renderText("Welcome to RELY")
print(cs(ascii_banner2, "blue"))
ascii_banner = Figlet(font='digital')
ascii_underbanner = ascii_banner.renderText("Team firebreathing rubberduckies")
ascii_underbanner2 = ascii_underbanner.replace("|", " ")
print(cs(ascii_underbanner2, "yellow"))
#ascii_banner = pyfiglet.figlet_format("Welcome  to  RELY")
#ascii_under = pyfiglet.print_figlet("", "big", 33)


#Waarop wil je scannen
Wanna_use_FS = input("Do you want to scan on file system (Y or N)? ")
if(Wanna_use_FS == "N"):
    print("")
elif(Wanna_use_FS == "Y"):

    filter1 = ''
    filtersize = ''
    sizef = ''
    filtername = ''
    namef = ''
    filterpath = ''
    pathf = ''

    pathname = input('Type in the path you want to analyze (.\.idea): ')

    filter1 = input('Do you want to filter the results? (Y/N): ')
    if filter1 == 'Y':
        filtersize = input('Do You want to filter on file size? (Y/N): ')
        if filtersize == 'Y':
            sizef = input('Type the file size you want to filter on. (bytes): ')
        filtername = input('Do You want to filter on file name? (Y/N): ')
        if filtername == 'Y':
            namef = input('Type the file name you want to filter on: ')
        filterpath = input('Do You want to filter on path? (Y/N): ')
        if filterpath == 'Y':
            pathf = input('Type the path you want to filter on: ')

    save = input('Do you want to save te results to a file? (Y/N)?: ')
else:
    print("Did not select Y or N, please restart program and try again")


Wanna_use_Tasks = input("Do you want to scan on Scheduled Tasks (Y or N)? ")
Wanna_use_Keys = input("Do you want to scan on Registry keys (Y or N)? ")


if(Wanna_use_Tasks == "N"):
    print("")
elif(Wanna_use_Tasks == "Y"):
    scheduled_tasks.main()
else:
    print("Did not select Y or N, please restart program and try again")


if(Wanna_use_Keys == "N"):
    print("")
elif(Wanna_use_Keys == "Y"):
    registry_key.main()
else:
    print("Did not select Y or N, please restart program and try again")

if (Wanna_use_FS == "Y"):
    File_system.main(pathname, filter1, filtersize, sizef, filtername, namef, filterpath, pathf, save)