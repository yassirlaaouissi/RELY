# Importeer de juiste bibliotheken om de registry te kunnen lezen
import winreg
import tabulate
import os.path as osp


def choice_menu():
    # input vragen aan de gebruiker.
    geefHKEY = input("Please give an HKEY (e.g. HKEY_LOCAL_MACHINE): ")
    geefPad = input("Please give the path you want to be scanned: ")





    # Wanneer er een enter wordt ingevoerd geeft het programma een fout melding
    if (geefPad == ""):
        print("Path not found, please enter a valid path choice. Try again.")
        main()
    elif (geefHKEY == ""):
        print("HKEY not found, please enter a valid HKEY choice. Try again.")
        main()

    #Leest de gegeven HKEY-input van de gebruiker uit.
    try:
        HKEYFound = False
        if (geefHKEY == "HKEY_CLASSES_ROOT"):
            explorer = winreg.OpenKey(
                winreg.HKEY_CLASSES_ROOT, geefPad)
            HKEYFound = True
        elif (geefHKEY == "HKEY_CURRENT_USER"):
            explorer = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, geefPad)
            HKEYFound = True
        elif (geefHKEY == "HKEY_LOCAL_MACHINE"):
            explorer = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, geefPad)
            HKEYFound = True
        elif (geefHKEY == "HKEY_USERS"):
            explorer = winreg.OpenKey(
                winreg.HKEY_USERS, geefPad)
            HKEYFound = True
        elif (geefHKEY == "HKEY_PERFORMANCE_DATA"):
            explorer = winreg.OpenKey(
                winreg.HKEY_PERFORMANCE_DATA, geefPad)
            HKEYFound = True
        elif (geefHKEY == "HKEY_CURRENT_CONFIG"):
            explorer = winreg.OpenKey(
                winreg.HKEY_CURRENT_CONFIG, geefPad)
            HKEYFound = True
        elif (geefHKEY == "HKEY_DYN_DATA"):
            explorer = winreg.OpenKey(
                winreg.HKEY_DYN_DATA, geefPad)
            HKEYFound = True

        if (HKEYFound == False):
            print("HKEY not found, please enter a valid HKEY choice. Try again.")
            main()
            return

        return explorer

    except:
        print("Path not found, please enter a valid path choice. Try again.")
        main()




def reg_reader(exp):
    regristry = []

    #Geeft bij 'Type' de bijbehoorende state naam aan.
    TYPE_STATE = {0: 'REG_NONE',
                  1: 'REG_SZ',
                  2: 'REG_EXPAND_SZ',
                  3: 'REG_BINARY',
                  4: 'REG_DWORD ',
                  5: 'REG_DWORD_BIG_ENDIAN',
                  6: 'REG_LINK',
                  7: 'REG_MULTI_SZ',
                  8: 'REG_RESOURCE_LIST',
                  9: 'REG_FULL_RESOURCE_DESCRIPTOR',
                  10: 'REG_RESOURCE_REQUIREMENTS_LIST',
                  11: 'REG_QWORD '}


    # Waardes in de lijst van de registry keys
    try:
        i = 0
        while 1:
            name, data, type = winreg.EnumValue(exp, i)
            #print("Name: " + str(name) + " || " + " Type: " + TYPE_STATE.get(type) + " || " + " Data: " + str(data))
            i += 1

            #Tabelontwerp creeëren
            name = str(name)
            type = str(TYPE_STATE.get(type))
            data = str(data)

            regristry.append({
                'Name': name, 'Type': type, 'Data': data,
            })


    except WindowsError:
        print

    return regristry


def save_keys(regristry):
    geefNaam = input("Do you want to filter on name? Y/N: ")
    #geefType = input("Do you want to filter on type? Y/N: ")
    #geefData = input("Do you want to filter on data? Y/N: ")

    #print tabel naar scherm
    header = regristry[0].keys()
    rows = [x.values() for x in regristry]
    tableregkey = tabulate.tabulate(rows, header, tablefmt='rst')
    print(tableregkey)

    #schrijf de tabel met uitkomsten naar een .txt bestand.
    if osp.isfile("RegistryKeys.txt"):
        f = open('RegistryKeys.txt', 'w')
    else:
        f = open('RegistryKeys.txt', 'x')

    f.write(tableregkey)

    # Filter input van de gebruiker
    if geefNaam == "Y":
        print (regristry[1])


    f.close()





def main():
    save_keys(reg_reader(choice_menu()))

if __name__ == '__main__':
    main()
