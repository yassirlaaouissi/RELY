# Importeer de juiste bibliotheken om de registry te kunnen lezen
import sys
import winreg
import tabulate
import os.path as osp
import logging
import hashlib

logger = logging.getLogger('Registry Keys')
logging.basicConfig(handlers=[logging.FileHandler('registry_keys.log', 'w', 'utf-8')],
                    format='%(name)s: %(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def choice_menu(geef_HKEY, geef_pad):
    # input vragen aan de gebruiker.

    logger.info("Asked for input HKEY.")
    logger.info("Received input HKEY: " + geef_HKEY)
    logger.info("Asked for input path, ")
    logger.info("Received input path: " + geef_pad)

    # Wanneer er een enter wordt ingevoerd geeft het programma een fout melding
    if (geef_pad == ""):
        print("Path not found, please enter a valid path choice. Try again.")
        sys.exit(1)
    if (geef_HKEY == ""):
        print("HKEY not found, please enter a valid HKEY choice. Try again.")
        sys.exit(1)

    # Leest de gegeven HKEY-input van de gebruiker uit.
    try:
        HKEY_found = False
        logging.info("Analyzing HKEY and path choice")
        if (geef_HKEY == "HKEY_CLASSES_ROOT"):
            explorer = winreg.OpenKey(
                winreg.HKEY_CLASSES_ROOT, geef_pad)
            HKEY_found = True
        elif (geef_HKEY == "HKEY_CURRENT_USER"):
            explorer = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, geef_pad)
            HKEY_found = True
        elif (geef_HKEY == "HKEY_LOCAL_MACHINE"):
            explorer = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, geef_pad)
            HKEY_found = True
        elif (geef_HKEY == "HKEY_USERS"):
            explorer = winreg.OpenKey(
                winreg.HKEY_USERS, geef_pad)
            HKEY_found = True
        elif (geef_HKEY == "HKEY_PERFORMANCE_DATA"):
            explorer = winreg.OpenKey(
                winreg.HKEY_PERFORMANCE_DATA, geef_pad)
            HKEY_found = True
        elif (geef_HKEY == "HKEY_CURRENT_CONFIG"):
            explorer = winreg.OpenKey(
                winreg.HKEY_CURRENT_CONFIG, geef_pad)
            HKEY_found = True
        elif (geef_HKEY == "HKEY_DYN_DATA"):
            explorer = winreg.OpenKey(
                winreg.HKEY_DYN_DATA, geef_pad)
            HKEY_found = True

        if (HKEY_found == False):
            print("HKEY not found, please enter a valid HKEY choice. Try again.")
            logging.info("HKEY not found")
            sys.exit(1)
            return

        return explorer

    except:
        print("Path not found, please enter a valid path choice. Try again.")
        logging.info("Path not found")
        sys.exit(1)


def reg_reader(exp):
    registry = []

    # Geeft bij 'Type' de bijbehoorende state naam aan.
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
            i += 1

            # Tabelontwerp creeëren
            name = str(name)
            type = str(TYPE_STATE.get(type))
            data = str(data)

            registry.append({
                'Name': name, 'Type': type, 'Data': data,
            })

            logging.info("Append values to registry list.")

    except WindowsError:
        print

    return registry


def filter_reg(registry, filter_vraag, filter_naam, filter_type):
    ongefilterd_lijst = registry
    filter_lijst = []

    logging.info("input for filter the registry: " + filter_vraag)

    if (filter_vraag.upper() == "N"):
        return ongefilterd_lijst
    elif (filter_vraag.upper() == "Y"):
        logging.info("input to filter on name: " + filter_naam)
        logging.info("input to filter on type: " + filter_type)

        if (filter_naam + filter_type == ""):
            return ongefilterd_lijst
        else:
            if (filter_naam != ""):
                for key in ongefilterd_lijst:
                    if key in filter_lijst:
                        continue
                    elif (key['Name'] == filter_naam):
                        filter_lijst.append(key)
                        logging.info("Registry key list is filtered on name.")
                if (filter_lijst == []):
                    print("Name not found in list of registry keys \n")
                    logging.info("Name not found in the registry keys list.")

            if (filter_type != ""):
                for key in ongefilterd_lijst:
                    if key in filter_lijst:
                        continue
                    elif (key['Type'] == filter_type):
                        filter_lijst.append(key)
                        logging.info("Registry key list is filtered on type.")
                if (filter_lijst == []):
                    print("Type not found in list of registry keys \n")
                    logging.info("Type not found in the registry keys list.")

            return filter_lijst

    else:
        print("The input you gave did not correspond Y or N.")
        logging.info("The input did not correspond with Y or N.")


def save_keys(final_list):
    # print tabel naar scherm
    header = final_list[0].keys()
    rows = [x.values() for x in final_list]
    tableregkey = tabulate.tabulate(rows, header, tablefmt='rst')
    logging.info("Create table of registry keys.")
    print(tableregkey)
    logging.info("Printed table of registry keys.")

    # schrijf de tabel met uitkomsten naar een .txt bestand.
    if osp.isfile("RegistryKeys.txt"):
        f = open('RegistryKeys.txt', 'w')
    else:
        f = open('RegistryKeys.txt', 'x')
    logging.info("Save list of registry keys.")

    f.write(tableregkey)
    logger.info('writing results to file.')

    f.close()
    logger.info('close txt file.')

    # hashing
    hasher = hashlib.md5()
    with open('RegistryKeys.txt', 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    hash1 = 'RegistryKeys.txt MD5 Hashwaarde: ' + hasher.hexdigest()
    logger.debug('Generating MD5 hash: ' + hasher.hexdigest())

    hashersha = hashlib.sha256()
    with open('RegistryKeys.txt', 'rb') as afile:
        buf = afile.read()
        hashersha.update(buf)
    hash2 = 'RegistryKeys.txt SHA256 Hashwaarde: ' + hashersha.hexdigest()
    logger.debug('Generating SHA256 hash: ' + hashersha.hexdigest())

    f = open('hashfile.txt', 'a', encoding="utf-8")
    logger.info('open file: hashfile.txt')
    f.write(hash1 + '\n' + hash2 + '\n')
    logger.info('writing md5 hash to file')
    f.close()
    logger.info('close file: hashfile.txt')


def main(geef_HKEY, geef_pad, filter_vraag, filter_naam, filter_type):
    save_keys(filter_reg(reg_reader(choice_menu(geef_HKEY, geef_pad)), filter_vraag, filter_naam, filter_type))


if __name__ == '__main__':
    main()