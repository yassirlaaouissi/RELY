import win32com.client
# hierin defineer je een key value dictionary waarmee je de staat van een scheduled task kan meegeven
TASK_STATE = {0: 'Unknown',
              1: 'Disabled',
              2: 'Queued',
              3: 'Completed',
              4: 'Running'}



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
            TaskLastRunned = task.LastRunTime
            TaskDetails = [TaskName, TaskPath, TaskState, TaskLastRunned]

            #voeg de list van alle printables toe aan een array zodat je deze kan returnen
            AllTaskDetails.append(TaskDetails)

            # per scheduled task in de folder print je de volgende info
            #print('Name task                  : %s' % TaskName)
            #print('Path (rootfolder)          : %s' % TaskPath)
            #print('State                      : %s' % TaskState)
            #print('Last Run (system date)     : %s\n' % TaskLastRunned)

    return AllTaskDetails

def filter_tasks(AllTaskDetails):
    WantToFilter = input("Do you want to filter the scheduled tasks? (Y or N): ")
    if(WantToFilter == "Y"):
        print("selected yes")
    elif(WantToFilter == "N"):
        print("selected no")
    else:
        print("You did not select Y or N, please restart the tool and try again")

    NameToFilterOn = ""
    PathToFilterOn = ""
    StateToFilterOn = ""

    for task in AllTaskDetails:
        Name = task[0]
        Path = task[1]
        State = task[2]
        LastRunned = task[3]


if __name__ == '__main__':
    filter_tasks(read_folders_of_tasks())
