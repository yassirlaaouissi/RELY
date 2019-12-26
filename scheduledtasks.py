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
    #hier maak je een list aan waaraan de tasks worden toegevoegd die gefilterd zijn
    FilteredAllTaskDetails = []

    #Wil je uberhaupt wel filteren
    WantToFilter = input("Do you want to filter the scheduled tasks? (Y or N): ")
    if(WantToFilter == "Y"):
        print("selected yes \n")

        #-------------------------------------!HIER BEGINT NAAM FILTERING!----------------------------------------------
        NameToFilterOn = input("If you want to filter on task names give the name and press enter, else leave blank and press enter: ")

        #Als de ingevoerde naam overeenkomt met naam uit AllTaskDetail dan hele task toevoegen aan FilteredAllTaskDetails
        AddedNameToFilteredList = False
        if(NameToFilterOn != ""):
            for task in AllTaskDetails:
                if(NameToFilterOn == task[0]):
                    FilteredAllTaskDetails.append(task)
                    AddedNameToFilteredList = True
            if (AddedNameToFilteredList == False):
                print("The name you entered was not found in the scheduled tasks, please restart the program and try again or proceed to the next step")


        #field is blank
        elif(NameToFilterOn == ""):
            print("You have left the field above blank, will proceed to next step\n")

        # -------------------------------------!HIER BEGINT STATE FILTERING!----------------------------------------------
        StateToFilterOn = input("If you want to filter on task states give the state and press enter, else leave blank and press enter: ")

        # Als de ingevoerde state overeenkomt met state uit AllTaskDetail dan hele task toevoegen aan FilteredAllTaskDetails
        AddedStateToFilteredList = False
        if (StateToFilterOn != ""):
            for task in AllTaskDetails:
                if task in FilteredAllTaskDetails:
                    continue
                elif(StateToFilterOn == task[2]):
                    FilteredAllTaskDetails.append(task)
                    AddedStateToFilteredList = True
            if (AddedStateToFilteredList == False):
                print("The state you entered was not found in the scheduled tasks, please restart the program and try again or proceed to the next step")


        # field is blank
        elif (StateToFilterOn == ""):
            print("You have left the field above blank, will proceed to next step\n")

        # -------------------------------------!HIER BEGINT PATH FILTERING!----------------------------------------------
        PathToFilterOn = input("If you want to filter on task path give the path and press enter, else leave blank and press enter: ")

        # Als de ingevoerde path overeenkomt met path uit AllTaskDetail dan hele task toevoegen aan FilteredAllTaskDetails
        AddedPathToFilteredList = False
        if(PathToFilterOn != ""):
            for task in AllTaskDetails:
                if task in FilteredAllTaskDetails:
                    continue
                elif (PathToFilterOn == task[2]):
                    FilteredAllTaskDetails.append(task)
                    AddedPathToFilteredList = True
            if(AddedPathToFilteredList == False):
                print("The path you entered was not found in the scheduled tasks, please restart the program and try again or proceed to the next step")


        # field is blank
        elif(PathToFilterOn == ""):
            print("You have left the field above blank, will proceed to next step\n")







        if(AddedNameToFilteredList & AddedPathToFilteredList & AddedStateToFilteredList == False):
            print("-----------------------------------------------------------------------")
            print("No filtering was applied, will now proceed to saving unfiltered scheduled tasks")
            print("-----------------------------------------------------------------------\n")
            return AllTaskDetails
        else:
            print("-----------------------------------------------------------------------")
            print("Filtering was applied, will now proceed to saving unfiltered scheduled tasks")
            print("-----------------------------------------------------------------------\n")
            return FilteredAllTaskDetails

    #Als je niet wilt filteren op de scheduled tasks
    elif(WantToFilter == "N"):
        print("-----------------------------------------------------------------------")
        print("selected no, will now proceed to saving unfiltered scheduled tasks")
        print("-----------------------------------------------------------------------\n")
        return AllTaskDetails

    else:
        print("You did not select Y or N, please restart the tool and try again")




def save_list_to_file(ListToSave):
    with open('ScheduledTasks.txt', 'w') as f:
        f.write("   Name of the task   ||      Path    ||        Status     ||      Last time runned    \n")
        for task in ListToSave:
            tempTask = str(task)
            tempTask2 = tempTask.replace("[","")
            tempTask3 = tempTask2.replace("]", "")
            tempTask4 = tempTask3.replace(",", " || ")
            print(tempTask4)
            f.write("%s\n" % tempTask4)


if __name__ == '__main__':
    save_list_to_file(filter_tasks(read_folders_of_tasks()))
