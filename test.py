# Importeer de juiste bibliotheken om de registry te kunnen lezen
import winreg
import tabulate
import os.path as osp


def choice_menu():

    geefHKEY = input("Please give an HKEY (e.g. HKEY_LOCAL_MACHINE): ")
    geefPad = input("Please give the path you want to be scanned: ")

    if (geefPad == ""):
        print("Please enter a valid choice. Try again by restarting the program")
    elif (geefHKEY == ""):
        print("Please enter a valid choice. Try again by restarting the program")

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
        print("HKEY not found, please restart the program.")
        return

    return explorer

def reg_reader(exp):
    regristry = []
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


    # list values owned by this registry key
    try:
        i = 0
        while 1:
            name, data, type = winreg.EnumValue(exp, i)
            print("Name: " + str(name) + " || " + " Type: " + TYPE_STATE.get(type) + " || " + " Data: " + str(data))
            i += 1

            #
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

    header = regristry[0].keys()
    rows = [x.values() for x in regristry]
    tableproceslist = tabulate.tabulate(rows, header, tablefmt='rst')
    print(tableproceslist)

    # Hiermee wordt de lijst met uitkomsten opgeslagen in een .txt bestand.
    if osp.isfile("RegistryKeys.txt"):
        f = open('RegistryKeys.txt', 'w')
    else:
        f = open('RegistryKeys.txt', 'x')

    f.write(tableproceslist)
    f.close()







if __name__ == '__main__':
    save_keys(reg_reader(choice_menu()))
