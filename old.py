# Deze bevat nog cpu_usage, alleen cpu_usage valt niet op te halen.
import psutil
from datetime import datetime
import tabulate


def proces_list():
    # Lijst die alle proces dictionaries bevat.
    processes = []
    for process in psutil.process_iter():

        # Verkrijg alle proces informatie met one shot.
        with process.oneshot():
            # Verkrijgen van het proces ID.
            pid = process.pid
            # Naam verkrijgen van het uitgevoerde bestand.
            name = process.name()
            # Tijd verkrijgen van wanneer het proces gecreeerd is.
            create_time = datetime.fromtimestamp(process.create_time())
            try:
                # Verkrijg het aantal CPU-cores dat dit proces kan uitvoeren.
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
            # Verkrijg het CPU-gebruikerspercentage
            cpu_usage = process.cpu_percent()
            # Verkrijg de status van het proces.
            status = process.status()
            try:
                # Verkrijgen van het geheugen gebruik in bytes.
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
            # Totale proces gelezen en geschreven bytes.
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes
            # Het ophalen van het aantal totale threads dat door het proces wordt voortgebracht
            n_threads = process.num_threads()
            # Ontvang de gebruikersnaam van gebruiker die het proces heeft voortgebracht
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"

        processes.append({
            'pid': pid, 'name': name, 'create_time': create_time,
            'cores': cores, 'status': status, 'memory_usage': memory_usage,
            'read_bytes': read_bytes, 'write_bytes': write_bytes,
            'n_threads': n_threads, 'cpu_usage' : cpu_usage, 'username': username,
        })

    # print(processes)

    save_file(processes)


def save_file(processes):

    # print(processes)

    # Hiermee wordt de lijst netjes weergegeven in de console.
    header = processes[0].keys()
    rows = [x.values() for x in processes]
    tableproceslist = tabulate.tabulate(rows, header, tablefmt='rst')
    print(tableproceslist)

    # Hiermee wordt de lijst met uitkomsten opgeslagen in een .txt bestand.
    f = open('C://Users/romyw/Documents/ipfit5/Proces_list.txt', 'w')  # extern opslaan
    # f = open('Proces_list.txt', 'w')  # intern opslaan
    f.write(tableproceslist)
    f.close()


def main():
    proces_list()


if __name__ == '__main__':
    main()
