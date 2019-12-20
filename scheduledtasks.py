import win32com.client
# hierin defineer je een key value dictionary waarmee je de staat van een scheduled task kan meegeven
TASK_STATE = {0: 'Unknown',
              1: 'Disabled',
              2: 'Queued',
              3: 'Completed',
              4: 'Running'}

#yeet



def readFoldersOfTasks():
    # je maakt een schedule reader aan en daar verbind je mee
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    # Leest de folders uit waarin de scheduled tasks staan en geeft bepaalde info weer zoals hieronder te zien is
    folders = [scheduler.GetFolder('\\')]
    while folders:
        folder = folders.pop(0)
        folders += list(folder.GetFolders(0))
        for task in folder.GetTasks(0):
            print('Path       : %s' % task.Path)
            print('State      : %s' % TASK_STATE[task.State])
            print('Last Run   : %s\n' % task.LastRunTime)

if __name__ == '__main__':
    readFoldersOfTasks()
