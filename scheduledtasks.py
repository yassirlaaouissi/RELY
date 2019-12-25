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
            TaskLastRunned = task.LastRunTime
            TaskDetails = [TaskName, TaskPath, TaskState, TaskLastRunned]

            #voeg de list van alle printables toe aan een array zodat je deze kan returnen
            AllTaskDetails.append(TaskDetails)
    return AllTaskDetails


#!!!!!!!!!!!!!!!!!!!!!!!!!!!FILTERING!!!!!!!!!!!!!!!!!!!!!!!
def filter_tasks(AllTaskDetails):
    #hier maak je een list aan waaraan de tasks worden toegevoegd die gefilterd zijn
    FilteredAllTaskDetails = []

    #Wil je uberhaupt wel filteren
    WantToFilter = input("Do you want to filter the scheduled tasks? (Y or N): ")
    if(WantToFilter == "Y"):
        print("selected yes")

        #-------------------------------------!HIER BEGINT NAAM FILTERING!----------------------------------------------
        NameToFilterOn = input("If you want to filter on task names give the name and press enter, else leave blank and press enter: ")

        #Als de ingevoerde naam overeenkomt met naam uit AllTaskDetail dan hele task toevoegen aan FilteredAllTaskDetails
        AddedNameToFilteredList = False
        if(NameToFilterOn != ""):
            for task in AllTaskDetails:
                if(NameToFilterOn == task[0]):
                    task.append(FilteredAllTaskDetails)
                    AddednameToFilteredList = True

        # Naam niet gevonden in tasks
        elif(AddedNameToFilteredList == False):
            print("The name you entered was not found in the scheduled tasks, please restart the program and try again or proceed to the next step")

        #field is blank
        elif(NameToFilterOn == ""):
            print("You have left the field above blank, will proceed to next step")

        #--------------------------------------------!HIER BEGINT PATH FILTERING!---------------------------------------
        PathToFilterOn = input("If you want to filter on path give the path, else leave blank: ")

        # Als de ingevoerde path overeenkomt met path uit AllTaskDetail dan hele task toevoegen aan FilteredAllTaskDetails
        AddedPathToFilteredList = False
        if (PathToFilterOn != ""):

            for task in AllTaskDetails:
                if (PathToFilterOn == task[1]):
                    task.append(FilteredAllTaskDetails)
                    AddedPathToFilteredList = True

        # path niet gevonden in tasks
        elif (AddedPathToFilteredList == False):
            print("The path you entered was not found in the scheduled tasks, please restart the program and try again or proceed to the next step")

        # field is blank
        elif (PathToFilterOn == ""):
            print("You have left the field above blank, will proceed to next step")


        #-----------------------------------------!HIER BEGINT STATE FILTERING!-----------------------------------------
        StateToFilterOn = input("If you want to filter on state of the task give the path, else leave blank: ")
        AddedStateToFilteredList = False
        if (StateToFilterOn != ""):
            for task in AllTaskDetails:
                if (StateToFilterOn == task[2]):
                    task.append(FilteredAllTaskDetails)
                    AddedStateToFilteredList = True

        # state niet gevonden in tasks
        elif (AddedStateToFilteredList == False):
            print("The state you entered was not found in the scheduled tasks, please restart the program and try again or proceed to the next step")

        # field is blank
        elif (PathToFilterOn == ""):
            print("You have left the field above blank, will proceed to next step")


    #Als je niet wilt filteren op de scheduled tasks
    elif(WantToFilter == "N"):
        print("selected no")

    else:
        print("You did not select Y or N, please restart the tool and try again")

    return WantToFilter
    return FilteredAllTaskDetails

def save_tasks(WantToFilter, AllTaskDetails, FilteredAllTaskDetails):
    if(WantToFilter == "N"):
        print("There was no filtering applied to the scheduled task list")
        print(AllTaskDetails)
    elif(WantToFilter == "Y"):
        print("There was filtering applied to the scheduled task list")
        print(FilteredAllTaskDetails)


if __name__ == '__main__':
    #afvangen van returnables in variabelen
    PostReading = read_folders_of_tasks()
    PostFiltering = filter_tasks(read_folders_of_tasks())

    #Runnen van alle functies
    save_tasks(PostReading, PostFiltering, PostFiltering)
