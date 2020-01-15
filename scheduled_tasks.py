from operator import contains

import tabulate
import win32com.client
import logging
import os.path


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
def filter_tasks(AllTaskDetails):
    UnfilteredList = AllTaskDetails
    FilteredList = []

    WantToFilter = input("Do you want to filter the scheduled tasks? (Y or N): ")



    if(WantToFilter == "N"):
        logger.debug('Selected yes as filtering choice.')
        return UnfilteredList
    elif(WantToFilter == "Y"):
        logger.debug('Selected no as filtering choice.')
        #Give values to filter on
        filterOnName = input("If you want to filter on name of task please give the name, else leave blank and press enter (e.g: CCleanerSkipUAC ): ")
        logger.debug('Selected' + filterOnName + 'as name to filter on.')
        filterOnState = input("If you want to filter on state of task please give the state, else leave blank and press enter (e.g: Completed): ")
        logger.debug('Selected' + filterOnState + 'as state to filter on.')
        filterOnPath = input("If you want to filter on path of task please give the path, else leave blank and press enter (e.g: \CCleanerSkipUAC): ")
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
            #for task in FilteredList:
            #    print(task)



            #return the filtered list after done with filtering
            return FilteredList
            logger.debug('Returned list of task attributes.')
    else:
        print("The input you gave did not correspond Y or N, please restart the program and try again.")
        logger.error('Input did not correspond with Y or N.')

def show_results(list):
    headers = ["Name", "Path", "State", "Last time runned"]
    for key in list:
        row = list
    #rows = [x.values() for x in list]
    tablelist = tabulate.tabulate(row, headers, tablefmt='rst')
    filename = 'ScheduledTasks.txt'



    WantToPrintList = input("Do you want to print the results of the scheduled task scan? (Y or N): ")
    if(WantToPrintList == "Y"):
        print(tablelist)
        logger.info('Returned and printed list of task attributes with table view.')
        return tablelist
    elif(WantToPrintList == "N"):
        print("File with results will be saved in the same folder as scheduledtasks.py. Name of the file is " + filename)
        logger.info('Returned  list of task attributes with table view.')
        return tablelist
    else:
        print("File with results will be saved in the same folder as scheduledtasks.py. Name of the file is " + filename)
        return tablelist
        logger.info('Returned and printed list of task attributes with table view.')

def save_list_to_file(ListToSave):
    filename = 'ScheduledTasks.txt'
    with open(filename, 'w') as f:
        f.write(ListToSave)
        logger.info('Saved list of task attributes with table view.')


def main():
    save_list_to_file(show_results(filter_tasks(read_folders_of_tasks())))