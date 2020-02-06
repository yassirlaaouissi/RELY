import logging
import sys

from pyfiglet import Figlet

import File_system
import proces_list
import registry_key
import scheduled_tasks



f = open('hashfile.txt', 'w', encoding="utf-8")
f.close()

logging.basicConfig(handlers=[logging.FileHandler('logboek.log', 'w', 'utf-8')], format='%(name)s: %(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)


#Welcome banner
ascii_banner = Figlet(font='STANDARD')
ascii_banner2 = ascii_banner.renderText("Welcome to RELY")
print(ascii_banner2)
ascii_banner = Figlet(font='digital')
ascii_underbanner = ascii_banner.renderText("Team firebreathing rubberduckies")
print(ascii_underbanner)

#Filesystem read
with open('./params_FS.txt') as f:
    lines = f.readlines()
    unfilteredPath = lines[1]
    unfilteredFilter1 = lines[2]
    unfilteredfiltersize = lines[3]
    unfilteredfiltername = lines[4]
    unfilteredfilterpath = lines[5]
    unfilteredsave = lines[6]
    unfilteredsizef = lines[7]
    unfilterednamef = lines[8]
    unfilteredpathf = lines[9]
    unfilteredWannaUse = lines[10]

#file system filter
    pathname1 = unfilteredPath.replace("pathname: ", "")
    pathname = pathname1.replace(",\n", "")

    filter11 = unfilteredFilter1.replace("filter1: ", "")
    filter1 = filter11.replace(",\n","")

    filtersize1 = unfilteredfiltersize.replace("filtersize: ","")
    filtersize = filtersize1.replace(",\n","")

    sizef1 = unfilteredsizef.replace("sizef: ","")
    sizef = sizef1.replace(",\n","")

    filtername1 = unfilteredfiltername.replace("filtername: ","")
    filtername = filtername1.replace(",\n","")

    namef1 = unfilterednamef.replace("namef: ","")
    namef = namef1.replace(",\n","")

    filterpath1 = unfilteredfilterpath.replace("filterpath: ","")
    filterpath = filterpath1.replace(",\n","")

    pathf1 = unfilteredpathf.replace("pathf: ", "")
    pathf = pathf1.replace(",\n", "")

    save1 = unfilteredsave.replace("save: ", "")
    save = save1.replace(",\n", "")

    Wanna_use_FS1 = unfilteredWannaUse.replace("Wanna_use_FS: ", "")
    Wanna_use_FS = Wanna_use_FS1.replace(",\n", "")

    #print(lines)

#Proces List read

with open('./params_PL.txt') as a:
    lines = a.readlines()
    unfilteredWannaFilterProc = lines[1]
    unfilteredName = lines[2]
    unfilteredPad = lines[3]
    unfilteredWannaUseProcList = lines[4]

#Proces list filter
    filter_question1 = unfilteredWannaFilterProc.replace("WannaFilter: ", "")
    filter_question = filter_question1.replace(",\n", "")

    filter_name1 = unfilteredName.replace("Name: ", "")
    filter_name = filter_name1.replace(",\n", "")

    filter_path1 = unfilteredPad.replace("Pad: ", "")
    filter_path = filter_path1.replace(",\n", "")

    want_to_use_proceslist1 = unfilteredWannaUseProcList.replace("want_to_use_proceslist: ", "")
    want_to_use_proceslist = want_to_use_proceslist1.replace(",\n", "")

    #print(lines)

#Registry keys read
with open('./params_RK.txt') as b:
    lines = b.readlines()
    unfilteredHKEY = lines[1]
    unfilteredPath = lines[2]
    unfilteredWannaFilterReg = lines[3]
    unfilteredName = lines[4]
    unfilteredType = lines[5]
    unfilteredWannaUseKeys = lines[6]
    unfilteredData = lines[7]
#Reg filter
    geef_HKEY1 = unfilteredHKEY.replace("HKEY: ", "")
    geef_HKEY = geef_HKEY1.replace(",\n", "")

    geef_pad1 = unfilteredPath.replace("Path: ", "")
    geef_pad = geef_pad1.replace(",\n", "")

    filter_vraag1 = unfilteredWannaFilterReg.replace("WannaFilter: ", "")
    filter_vraag = filter_vraag1.replace(",\n", "")

    filter_naam1 = unfilteredName.replace("Name: ", "")
    filter_naam = filter_naam1.replace(",\n", "")

    filter_type1 = unfilteredType.replace("Type: ", "")
    filter_type = filter_type1.replace(",\n", "")

    Wanna_use_Keys1 = unfilteredWannaUseKeys.replace("Wanna_use_Keys: ", "")
    Wanna_use_Keys = Wanna_use_Keys1.replace(",\n", "")

    filter_data1 = unfilteredData.replace("Data: ", "")
    filter_data = filter_data1.replace(",\n", "")

    #print(lines)

#Scheduled tasks read
with open('./params_ST.txt') as c:
    lines = c.readlines()

    unfilteredName = lines[1]
    unfilteredState = lines[2]
    unfilteredPadTasks = lines[3]
    unfilteredPrintList = lines[4]
    unfilteredWannaFilterTasks = lines[5]
    unfilteredWannaUseTasks = lines[6]

#Tasks filter
    WantToFilter1 = unfilteredWannaFilterTasks.replace("WantToFilter: ", "")
    WantToFilter = WantToFilter1.replace(",\n", "")

    FilterOnName1 = unfilteredName.replace("Name: ", "")
    filterOnName = FilterOnName1.replace(",\n", "")

    FilterOnState1 = unfilteredState.replace("State: ", "")
    filterOnState = FilterOnState1.replace(",\n", "")

    FilterOnPath1 = unfilteredPadTasks.replace("Path: ", "")
    filterOnPath = FilterOnPath1.replace(",\n", "")

    WantToPrintList1 = unfilteredPrintList.replace("printlist: ", "")
    WantToPrintList = WantToPrintList1.replace(",\n", "")

    Wanna_use_Tasks1 = unfilteredWannaUseTasks.replace("Wanna_use_Tasks: ", "")
    Wanna_use_Tasks = Wanna_use_Tasks1.replace(",\n", "")


    #print(lines)





if (Wanna_use_FS.upper() == "Y"):
    File_system.main(pathname, filter1, filtersize, sizef, filtername, namef, filterpath, pathf, save)

print()
if(Wanna_use_Tasks.upper() == "Y"):
    scheduled_tasks.main(WantToFilter, filterOnName, filterOnState, filterOnPath, WantToPrintList)

print()
if(Wanna_use_Keys.upper() == "Y"):
    registry_key.main(geef_HKEY, geef_pad, filter_vraag, filter_naam, filter_type, filter_data)

print()
if(want_to_use_proceslist.upper() == "Y"):
    proces_list.main(filter_question, filter_name, filter_path)


print()
WannaExit = input("To exit the program press Y and then enter: ")
if WannaExit.upper() == "Y":
    sys.exit(1)
