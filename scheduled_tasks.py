import sys

import tabulate
import win32com.client
import logging

import hashlib


# Logging definities

logger = logging.getLogger('Scheduled Tasks')


# hierin defineer je een key value dictionary waarmee je de staat van een scheduled task kan meegeven
TASK_STATE = {0: 'Unknown',
              1: 'Disabled',
              2: 'Queued',
              3: 'Completed',
              4: 'Running'}


#!!!!!!!!!!!!!!!!!!!UITLEZEN!!!!!!!!!!!!!!!!!!!!!!!!!s
def read_folders_of_tasks():
    AllTaskDetails = []



    # je maakt een schedule reader aan en daar verbind je mee
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    logger.info('Created list of taskdetails and connected to scheduled task reader.')
    logger.info('Reading scheduled task directory.')


    # begint in root folder
    folders = [scheduler.GetFolder('\\')]
    while folders:
        #loopt door alle folders + subfolders heen popt steeds een en scant voor scheduled tasks
        folder = folders.pop(0)
        folders += list(folder.GetFolders(0))
        logger.info('Listing all folders in directory.')
        for task in folder.GetTasks(0):
            #store alle printables in een variabele en voeg deze toe aan een list
            TaskName = task.name
            TaskPath = task.Path
            TaskState = TASK_STATE[task.State]
            TaskLastRunnedOG = str(task.LastRunTime)
            TaskLastRunned = TaskLastRunnedOG.replace("+00:00", " (Central EU Time)")
            TaskDetails = [TaskName, TaskPath, TaskState, TaskLastRunned]


            #voeg de list van alle printables toe aan een array zodat je deze kan returnen
            AllTaskDetails.append(TaskDetails)

            logger.info('Added task attributes to list.')
            logger.debug('Returned list of task attributes.')
    return AllTaskDetails


#!!!!!!!!!!!!!!!!!!!!!!!!!!!FILTERING!!!!!!!!!!!!!!!!!!!!!!!
def filter_tasks(AllTaskDetails, WantToFilter, filterOnName, filterOnState, filterOnPath):
    UnfilteredList = AllTaskDetails
    FilteredList = []

    if(WantToFilter.upper() == "N"):
        logger.debug('Selected no as filtering choice.')
        return UnfilteredList
    elif(WantToFilter.upper() == "Y"):
        logger.debug('Selected yes as filtering choice.')
        logger.debug('Selected' + filterOnName + 'as name to filter on.')
        logger.debug('Selected' + filterOnState + 'as state to filter on.')
        logger.debug('Selected' + filterOnPath + 'as path to filter on.')

        #The actual filtering
        if(filterOnName + filterOnState + filterOnPath == "" ):
            #print(UnfilteredList)
            return UnfilteredList
            logger.debug('Returned list of task attributes.')
        else:
            if(filterOnName != ""):
                logger.info('Name field to filter on is left blank.')
                for task in UnfilteredList:
                    if task in FilteredList:
                        continue
                    elif(task[0] == filterOnName):
                        FilteredList.append(task)
                        logger.debug('added task to Filtered list')
                if(FilteredList == []):
                    print("Name not found in list of scheduled tasks \n")
                    logger.error('Name not found in the list of scheduled tasks.')
                    #sys.exit(1)
            #for task in FilteredList:
            #    print(task)

            if (filterOnState != ""):
                logger.info('State field to filter on is left blank.')
                for task in UnfilteredList:
                    if task in FilteredList:
                        continue
                    elif (task[2] == filterOnState):
                        FilteredList.append(task)
                        logger.debug('added task to Filtered list')
                if (FilteredList == []):
                    print("State not found in list of scheduled tasks \n")
                    logger.error('State not found in the list of scheduled tasks.')
                    #sys.exit(1)
            #for task in FilteredList:
            #    print(task)

            if (filterOnPath != ""):
                logger.info('Path field to filter on is left blank.')
                for task in UnfilteredList:
                    if task in FilteredList:
                        continue
                    elif (task[1] == filterOnPath):
                        FilteredList.append(task)
                        logger.debug('added task to Filtered list')
                if (FilteredList == []):
                    print("Path not found in list of scheduled tasks \n")
                    logger.error('Path not found in the list of scheduled tasks.')
                    #sys.exit(1)


            if FilteredList == []:
                print("Did not find IOC in: Scheduled Tasks ")
            else:
                print("Found IOC, possible malware in: Scheduled Tasks ")


            #return the filtered list after done with filtering
            return FilteredList
            logger.debug('Returned list of task attributes.')
    else:
        print("The input you gave did not correspond Y or N, please restart the program and try again.")
        logger.error('Input did not correspond with Y or N.')

def show_results(list, WantToPrintList):
    if list == []:
        print()
    else:
        headers = ["Name", "Path", "State", "Last time runned"]
        for key in list:
            row = list
        #rows = [x.values() for x in list]
        tablelist = tabulate.tabulate(row, headers, tablefmt='rst')
        filename = 'ScheduledTasks.txt'

        if(WantToPrintList.upper() == "Y"):
            print(tablelist)
            logger.info('Returned and printed list of task attributes with table view.')
            return tablelist
        elif(WantToPrintList.upper() == "N"):
            print("File with results will be saved in the same folder as scheduledtasks.py. Name of the file is " + filename)
            logger.info('Returned  list of task attributes with table view.')
            return tablelist
        else:
            print("File with results will be saved in the same folder as scheduledtasks.py. Name of the file is " + filename)
            return tablelist
            logger.info('Returned and printed list of task attributes with table view.')

def save_list_to_file(ListToSave):
    if ListToSave == None:
        print()
    else:
        filename = 'ScheduledTasks.txt'
        with open(filename, 'w') as f:
            f.write(ListToSave)
            logger.info('Saved list of task attributes with table view.')

        #hashing
        hasher = hashlib.md5()
        with open('ScheduledTasks.txt', 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        hash1 = 'ScheduledTasks.txt MD5 Hashwaarde: ' + hasher.hexdigest()
        logger.debug('Generating MD5 hash: ' + hasher.hexdigest())

        hashersha = hashlib.sha256()
        with open('ScheduledTasks.txt', 'rb') as afile:
            buf = afile.read()
            hashersha.update(buf)
        hash2 = 'ScheduledTasks.txt SHA256 Hashwaarde: ' + hashersha.hexdigest()
        logger.debug('Generating SHA256 hash: ' + hashersha.hexdigest())

        f = open('hashfile.txt', 'a', encoding="utf-8")
        logger.info('open file: hashfile.txt')
        f.write(hash1 + '\n' + hash2 + '\n')
        logger.info('writing md5 hash to file')
        f.close()
        logger.info('close file: hashfile.txt')


def main(WantToFilter, filterOnName, filterOnState, filterOnPath, WantToPrintList):

    save_list_to_file(show_results(filter_tasks(read_folders_of_tasks(), WantToFilter, filterOnName, filterOnState, filterOnPath), WantToPrintList))