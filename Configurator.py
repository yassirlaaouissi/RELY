import logging
import File_system
import scheduled_tasks
import cowsay

#Logger is aangeroepen over het hele project
logging.basicConfig(filename="logboek.log", format='%(name)s: %(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

Welcomemessage = "Welcome to "

#Waarop wil je scannen
Wanna_use_FS = input("Do you want to scan on file system (Y or N)? ")
Wanna_use_Tasks = input("Do you want to scan on Scheduled Tasks (Y or N)? ")

if(Wanna_use_FS == "N"):
    print("")
elif(Wanna_use_FS == "Y"):
    File_system.main()
else:
    print("Did not select Y or N, please restart program and try again")


if(Wanna_use_Tasks == "N"):
    print("")
elif(Wanna_use_Tasks == "Y"):
    scheduled_tasks.main()
else:
    print("Did not select Y or N, please restart program and try again")