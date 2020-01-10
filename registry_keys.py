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
        print
    elif (geefHKEY == ""):
        print
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
            print("HKEY not found, try again.")
            return

        return explorer

    except:
        print("Please enter a valid path choice. Try again.")
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

    except:
        print ("Please enter a valid path choice. Try again.")
        main()

    return regristry


def save_keys(regristry):
    #print tabel naar scherm
    header = regristry[0].keys()
    rows = [x.values() for x in regristry]
    tableproceslist = tabulate.tabulate(rows, header, tablefmt='rst')
    print(tableproceslist)

    #schrijf de tabel met uitkomsten naar een .txt bestand.
    if osp.isfile("RegistryKeys.txt"):
        f = open('RegistryKeys.txt', 'w')
    else:
        f = open('RegistryKeys.txt', 'x')

    f.write(tableproceslist)
    f.close()






def main():
    save_keys(reg_reader(choice_menu()))

if __name__ == '__main__':
    main()
