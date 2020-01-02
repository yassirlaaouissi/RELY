from operator import contains

import win32com.client
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

    # begint in root folder
    folders = [scheduler.GetFolder('\\')]
    while folders:
        #loopt door alle folders + subfolders heen popt steeds een en scant voor scheduled tasks
        folder = folders.pop(0)
        folders += list(folder.GetFolders(0))
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
    return AllTaskDetails


#!!!!!!!!!!!!!!!!!!!!!!!!!!!FILTERING!!!!!!!!!!!!!!!!!!!!!!!
def filter_tasks(AllTaskDetails):
    UnfilteredList = AllTaskDetails
    FilteredList = []

    WantToFilter = input("Do you want to filter the scheduled tasks? (Y or N): ")

    if(WantToFilter == "N" or "n"):

        return UnfilteredList
    elif(WantToFilter == "Y" or "y"):
        #Give values to filter on
        filterOnName = input("If you want to filter on name of task please give the name, else leave blank and press enter: ")
        filterOnState = input("If you want to filter on state of task please give the state, else leave blank and press enter: ")
        filterOnPath = input("If you want to filter on path of task please give the path, else leave blank and press enter: ")

        #The actual filtering
        if(filterOnName + filterOnState + filterOnPath == "" ):
            #print(UnfilteredList)
            return UnfilteredList
        else:
            if(filterOnName != ""):
                for task in UnfilteredList:
                    if task in FilteredList:
                        continue
                    elif(task[0] == filterOnName):
                        FilteredList.append(task)
                if(FilteredList == []):
                    print("Name not found in list of scheduled tasks \n")
            #for task in FilteredList:
            #    print(task)

            if (filterOnState != ""):
                for task in UnfilteredList:
                    if task in FilteredList:
                        continue
                    elif (task[2] == filterOnState):
                        FilteredList.append(task)
                if (FilteredList == []):
                    print("State not found in list of scheduled tasks \n")
            #for task in FilteredList:
            #    print(task)

            if (filterOnPath != ""):
                for task in UnfilteredList:
                    if task in FilteredList:
                        continue
                    elif (task[1] == filterOnPath):
                        FilteredList.append(task)
                if (FilteredList == []):
                    print("Path not found in list of scheduled tasks \n")
            #for task in FilteredList:
            #    print(task)



            #return the filtered list after done with filtering
            return FilteredList
    else:
        print("The input you gave did not correspond Y or N, please restart the program and try again.")




def save_list_to_file(ListToSave):
    filename = 'ScheduledTasks.txt'
    with open(filename, 'w') as f:
        f.write("   Name of the task   ||      Path    ||        Status     ||      Last time runned    \n")
        WantToPrintList = input("Do you want to print the results of the scheduled task scan? (Y or N): ")
        for task in ListToSave:
            tempTask = str(task)
            tempTask2 = tempTask.replace("[","")
            tempTask3 = tempTask2.replace("]", "")
            tempTask4 = tempTask3.replace(",", " || ")
            if(WantToPrintList == "Y" or "y"):
                print("   Name of the task   ||      Path    ||        Status     ||      Last time runned   ")
                print(tempTask4)
            f.write("%s\n" % tempTask4)

        if(WantToPrintList == "N" or "n"):
            print("File with results will be saved in the same folder as scheduledtasks.py. Name of the file is " + filename)


if __name__ == '__main__':
    save_list_to_file(filter_tasks(read_folders_of_tasks()))
    #filter_tasks(read_folders_of_tasks())