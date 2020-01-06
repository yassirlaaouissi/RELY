import psutil
from datetime import datetime

# De lijst die alle proccessen bevat in een lijst van dictionaries.
def process_list():
    processes = []
    for process in psutil.process_iter():
    # Verkrijg alle proces informatie in een keer.
        with process.oneshot():
            # Verkrijg het proces ID
            pid = process.pid
            # krijg de naam van het uitgevoerde bestand
            name = process.name()
            # krijg de tijd dat het proces is voortgebracht
            create_time = datetime.fromtimestamp(process.create_time())
            try:
                # verkrijg het aantal CPU-cores dat dit proces kan uitvoeren
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
                # verkrijg het CPU-gebruikpercentage
            cpu_usage = process.cpu_percent()
            # de status van het proces ophalen (actief, inactief, enz.)
            status = process.status()
            #try:
                # get the process priority (a lower value means a more prioritized process)
                #nice = int(process.nice())
            #except psutil.AccessDenied:
                #nice = 0
            try:
                # get the memory usage of this process in bytes
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
            # totale proces gelezen en geschreven bytes
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes
            # haal het aantal totale threads op dat door dit proces wordt voortgebracht
            #n_threads = process.num_threads()
            # ontvang de gebruikersnaam van gebruiker die het proces heeft voortgebracht
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"
    processes.append({
        'pid' : pid, 'name' : name, 'create_time' : create_time, 'cores' : cores, 'cpu_usage' : cpu_usage, 'status' : status, 'memory_usage' : memory_usage, 'read_bytes' : read_bytes, 'write_bytes' : write_bytes, 'username' : username,
    })

#def save_processlist_to_file(list_to_save):
    #filename = 'processlist.txt'
    #with open(filename, 'w') as f:
        #f.write(" Process ID    ||  Name    ||  Create time     ||      Cores    ||     CPU usage       ||      Status      ||      Read bytes      ||      Write bytes     ||      Username    \n")
        #want_to_print_list = input("Wil je de resultaten van het proces opslaan? (Y of N): ")
        #for task in list_to_save:


#if __name__ == '__main__':
 #   process_list()

def save_list_to_file(list_to_save):
    filename = 'Proces_list.txt'
    with open(filename, 'w') as f:
        f.write(
            "   Process ID      ||      Name     ||        Create time      ||      Cores     ||      CPU usage    ||     Status     ||      Memory usage      ||      Read bytes     ||      Write bytes     ||      n treads    ||   Username  \n")
        want_to_print_list = input("Do you want to print the results of the proces list scan? (Y or N): ")
        for task in list_to_save:
            tempTask = str(task)
            tempTask2 = tempTask.replace("[", "")
            tempTask3 = tempTask2.replace("]", "")
            tempTask4 = tempTask3.replace(",", "  ")
            if (want_to_print_list == "Y"):
                print(
                    "   Process ID   ||      Name     ||        Create time      ||      Cores     ||      CPU usage    ||     Status     ||      Memory usage      ||      Read bytes     ||      Write bytes     ||      n treads    ||   Username  ")
                print(tempTask4)
            f.write("%s\n" % tempTask4)

        if (want_to_print_list == "N"):
            print(
                "File with results will be saved in the same folder as scheduledtasks.py. Name of the file is " + filename)
        else:
            print(
                "File with results will be saved in the same folder as scheduledtasks.py. Name of the file is " + filename)


save_list_to_file(processes)


