# Deze bevat nog cpu_usage, alleen cpu_usage valt niet op te halen.
import psutil
from datetime import datetime
import tabulate
from ast import literal_eval


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

def filterprocesses(processes):
    filteredlist = []

    #filteroptie op File size
    # size1 = input('Do you want to filter on file size? Y/N?: ')
    # if size1 == 'Y':
        # size2 = input('Type the file size you want to filter on. (bytes): ')
        # size2 = int(size2)
        # sizelist = filter(lambda x: x['File size (bytes)'] == size2, processes)
        # sizelist2 = list(sizelist)
        # for item in sizelist2:
            # sizestr = str(item)
            # sizestr2 = sizestr.replace('[', '')
            # sizestr3 = sizestr2.replace(']', '')
            # if sizestr3 == '':
                # print('No results found')
            # else:
                # sizelistdict = literal_eval(sizestr3)
                # filteredlist.append(sizelistdict)
    # else:
        # print('ok')

    #filteroptie op File name
    names = input('Wilt u filteren op naam? J/N?: ')
    if names == 'J':
        name2 = input('Vul de naam in waarop je wilt filteren: ')
        namelist = filter(lambda x: x['File name'] == name2, processes)
        namelist2 = list(namelist)
        for item in namelist2:
            namestr = str(item)
            namestr2 = namestr.replace('[', '')
            namestr3 = namestr2.replace(']', '')
            if namestr3 == '':
                print('No results found')
            else:
                namelistdict = literal_eval(namestr3)
                filteredlist.append(namelistdict)
    else:
        print('ok')

    return filteredlist

def save_file(processes):

    # print(processes)

    # Hiermee wordt de lijst netjes weergegeven in de console.
    header = processes[0].keys()
    rows = [x.values() for x in processes]
    tableproceslist = tabulate.tabulate(rows, header, tablefmt='rst')
    print(tableproceslist)

    save = input('Wilt u de resultaten oplsaan? (J/N)?: ')
    if save == 'J':
        f = open('C://Users/romyw/Documents/ipfit5/Proces_list.txt', 'w')  # extern opslaan
        # f = open('Proces_list.txt', 'w')  # intern opslaan
        f.write(tableproceslist)
        f.close()

        # locatie moet nog worden bepaald
        print(
            '\nDe results zijn opgeslagen in een bestand genaamd; Proces_list.txt op de locatie C://Users/romyw/Documents/ipfit5/Proces_list.txt')
    else:
        print('De resultaten zijn niet opgeslagen.')

    # Hiermee wordt de lijst met uitkomsten opgeslagen in een .txt bestand.
    # f = open('C://Users/romyw/Documents/ipfit5/Proces_list.txt', 'w')  # extern opslaan
    # f = open('Proces_list.txt', 'w')  # intern opslaan
    # f.write(tableproceslist)
    # f.close()

    # Keuze geven om het bestand wel of niet op te slaan.
    # save = input('Wilt u de resultaten oplsaan? (J/N)?: ')
    # if save == 'J':
    # f = open('C://Users/romyw/Documents/ipfit5/Proces_list.txt', 'w')  # extern opslaan
    # f = open('Proces_list.txt', 'w')  # intern opslaan
    # f.write(tableproceslist)
    # f.close()

    # locatie moet nog worden bepaald
    # print('\nDe results zijn opgeslagen in een bestand genaamd; Proces_list.txt op de locatie C://Users/romyw/Documents/ipfit5/Proces_list.txt')
    # else:
    # print('De resultaten zijn niet opgeslagen.')


def main():
    proces_list()


if __name__ == '__main__':
    main()

# Proces vinden by name
def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(attrs=['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls
