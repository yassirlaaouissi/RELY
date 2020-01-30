# Functionaliteit van Romy.
# Deze functionaliteit bevat geen CPU_usage meer.
# psutil is een platformonafhankelijke bibliotheek voor het ophalen van informatie over actieve processen en systeemgebruik in Python.
import hashlib
import sys

import psutil
from datetime import datetime
import tabulate
import logging


logger = logging.getLogger('Proces list')
logging.basicConfig(handlers=[logging.FileHandler('logboek.log', 'w', 'utf-8')], format='%(name)s: %(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logger.info('This file includes info of the steps that the program makes.')

processes = []


def proces_list():
    global processes
    # Lijst die alle proces dictionaries bevat.
    # processes = []
    for process in psutil.process_iter():

        # Verkrijg alle proces informatie met one shot. Hulpprogramma context manager die het ophalen van meerdere procesinformatie tegelijkertijd aanzienlijk versnelt
        with process.oneshot():
            # Verkrijgen van het proces ID.
            pid = process.pid
            logger.info('Program is getting process id (pid), Process ID:' + str(pid))
            # Naam verkrijgen van het uitgevoerde bestand.
            name = process.name()
            logger.info('Program is getting process name (name): ' + name)
            # Tijd verkrijgen van wanneer het proces gecreeerd is.
            create_time = datetime.fromtimestamp(process.create_time())
            logger.info('Program is getting process creation time (create_time): ' + str(create_time))
            try:
                # Verkrijg het aantal CPU-cores dat dit proces kan uitvoeren.
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
            logger.info('Program is getting cores used by the process (cores): ' + str(cores))
            # Verkrijg de status van het proces.
            status = process.status()
            logger.info('Program is getting the status of the process (status): ' + status)
            try:
                # Verkrijgen van het geheugen gebruik in bytes.
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
            logger.info(
                'Program is getting information about memory used by the process (memory_usage): ' + str(memory_usage))
            # Totale proces gelezen en geschreven bytes.
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            logger.info('Program is getting read bytes used by the process (read_bytes): ' + str(read_bytes))
            write_bytes = io_counters.write_bytes
            logger.info('Program is getting written bytes used by the process (write_bytes): ' + str(write_bytes))
            # Het ophalen van het aantal totale threads dat door het proces wordt voortgebracht
            threads = process.num_threads()
            logger.info('Program is getting threads used by the process (treads): ' + str(threads))
            # Ontvang de gebruikersnaam van gebruiker die het proces heeft voortgebracht
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"
            logger.info('Program is getting the username related to the process (username): ' + name)
            try:
                path = process.exe()
            except psutil.AccessDenied:
                path = "-"
            logger.info('Program is getting the path of the process (path): ' + str(path))
        processes.append({
            'pid': pid, 'name': name, 'create_time': create_time,
            'cores': cores, 'status': status, 'memory_usage': memory_usage,
            'read_bytes': read_bytes, 'write_bytes': write_bytes,
            'n_threads': threads, 'username': username, 'path': path,
        })

    # print("Test")


def filter_processes(processes, filter_question, filter_name, filter_path):
    # not_filtered_list = processes
    filtered_list = []
    logger.info("input for filter the processes: " + filter_question)


    if filter_question.upper() == "N":
        return processes
    elif(filter_question.upper() == "Y"):
        # gefilterde_lijst.append(filter_naam)
        logger.info("input to filter on name: " + filter_name)
        logger.info("input to filter on path: " + filter_path)

        if filter_name == "" and filter_path == "":
            return processes
        else:
            if filter_name != "":
                for key in processes:
                    if key in filtered_list:
                        continue
                    elif key['name'] == filter_name:
                        # print("made it")
                        filtered_list.append(key)
                logger.info("Proces list is filtered on name.")
                if len(filtered_list) == 0:
                    print("Name not found in list of processes\n")
                    logger.info("Name not found in the processes list.")

            if filter_path != "":
                for key in processes:
                    if key in filtered_list:
                        continue
                    elif key['path'] == filter_path:
                        filtered_list.append(key)
                        logger.info("Proces list is filtered on type.")
                if len(filtered_list) == 0:
                    print("Type not found in list of processes \n")
                    logger.info("Type not found in the proces list.")

            if filtered_list == []:
                print("Did not find IOC in: Proces list ")
            else:
                print("Found IOC, possible malware in: Proces list ")

            return filtered_list


    else:
        print("The input you gave did not correspond Y or N.")
        logger.info("The input did not correspond with Y or N.")
        #sys.exit(1)
    # save_file()

def save_file(final_list):

    # Hiermee wordt de lijst netjes weergegeven in de console.
    header = final_list[0].keys()
    rows = [x.values() for x in final_list]
    tableproceslist = tabulate.tabulate(rows, header, tablefmt='rst')
    print(tableproceslist)

    # Hiermee wordt de lijst met uitkomsten opgeslagen in een .txt bestand.
    #f = open('C://Users/romyw/Documents/ipfit5/Proces_list.txt', 'w')  # extern opslaan
    f = open('Proces_list.txt', 'w')  # intern opslaan
    logger.info('The output of the program is being saved in a file.')
    f.write(tableproceslist)
    f.close()
    logger.info('The output of the program has been saved to a file.')
    logger.info('Program got all the information.')

    # hashing
    hasher = hashlib.md5()
    with open('Proces_list.txt', 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    hash1 = 'Proces_list.txt MD5 Hashwaarde: ' + hasher.hexdigest()
    logger.debug('Generating MD5 hash: ' + hasher.hexdigest())

    hashersha = hashlib.sha256()
    with open('Proces_list.txt', 'rb') as afile:
        buf = afile.read()
        hashersha.update(buf)
    hash2 = 'Proces_list.txt SHA256 Hashwaarde: ' + hashersha.hexdigest()
    logger.debug('Generating SHA256 hash: ' + hashersha.hexdigest())

    f = open('hashfile.txt', 'a', encoding="utf-8")
    logger.info('open file: hashfile.txt')
    f.write(hash1 + '\n' + hash2 + '\n')
    logger.info('writing md5 hash to file')
    f.close()
    logger.info('close file: hashfile.txt')


def main(filter_question, filter_name, filter_path):
    proces_list()
    final_list = filter_processes(processes, filter_question, filter_name, filter_path)
    if final_list == []:
        print()
    else:
        save_file(final_list)
    #proces_list()


