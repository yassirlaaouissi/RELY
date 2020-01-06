# Importeer de juiste bibliotheken om de registry te kunnen lezen

from winreg import *
import os
import winreg


explorer = winreg.OpenKey(
    winreg.HKEY_LOCAL_MACHINE,
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Git_is1"
)

key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Git_is1"

print (key)


TYPE_STATE = {  0: 'REG_NONE',
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
        name, data, type = winreg.EnumValue(explorer, i)
        print("Name: " + str(name) + " || " + " Type: " + TYPE_STATE.get(type) + " || " + " Data: " + str(data))
        i += 1

except WindowsError:
    print ("NIET GEVONDEN")

















# Definieer het beginpunt van de registry
# voor hier zijn de HKEY_CLASSES_ROOT (gaat over de hele computer installatie)
# en HKEY_CURRENT_USER (gaat over de omgeving van de gebruiker = uitbreiding op de computer installatie)

roots_hives = {
    "HKEY_CLASSES_ROOT": HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE": HKEY_LOCAL_MACHINE,
    "HKEY_USERS": HKEY_USERS,
    "HKEY_PERFORMANCE_DATA": HKEY_PERFORMANCE_DATA,
    "HKEY_CURRENT_CONFIG": HKEY_CURRENT_CONFIG,
    "HKEY_DYN_DATA": HKEY_DYN_DATA
}

#Parse_key kijkt of het beginpunt wel bestaat in de beschijving hierboven

def parse_key(key):
    key = key.upper()
    parts = key.split('\\')
    root_hive_name = parts[0]
    root_hive = roots_hives.get(root_hive_name)
    partial_key = '\\'.join(parts[1:])

    if not root_hive:
        raise Exception('root hive "{}" was not found'.format(root_hive_name))

    return partial_key, root_hive

# get_syb_keys hakt de string bijv : HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths
# op in kleine leesbare stukken. Dit is nodig omdat je per tak \tak\tak\ weer subtakken kan krijgen
# op deze manier kan je door de boom lopen

def get_sub_keys(key):
    partial_key, root_hive = parse_key(key)

    with ConnectRegistry(None, root_hive) as reg:
        with OpenKey(reg, partial_key) as key_object:
            sub_keys_count, values_count, last_modified = QueryInfoKey(key_object)
            try:
                for i in range(sub_keys_count):
                    sub_key_name = EnumKey(key_object, i)
                    yield sub_key_name
            except WindowsError:
                pass

# get_values haalt de waardes op van de opgegeven velden (fields) aan het einde van de tak (key)

def get_values(key, fields):
    partial_key, root_hive = parse_key(key)

    with ConnectRegistry(None, root_hive) as reg:
        with OpenKey(reg, partial_key) as key_object:
            data = {}
            for field in fields:
                try:
                    value, type = QueryValueEx(key_object, field)
                    data[field] = value
                except WindowsError:
                    pass

            return data


def get_value(key, field):
    values = get_values(key, [field])
    return values.get(field)


def join(path, *paths):
    path = path.strip('/\\')
    paths = map(lambda x: x.strip('/\\'), paths)
    paths = list(paths)
    result = os.path.join(path, *paths)
    result = result.replace('/', '\\')
    return result

# Local Machine
print ("==============================================================")
print ("Applications on local machine")
print ("==============================================================")

key = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'

for sub_key in get_sub_keys(key):
    path = join(key, sub_key)
    value = get_values(path, ['DisplayName', 'UninstallString', 'InstallDate'])

    if value:
        print(value)

#Lijst van 32-bit programma's geinstalleerd op een Windows® X64 version.
key = r'HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432NODE\Microsoft\Windows\CurrentVersion\Uninstall'

for sub_key in get_sub_keys(key):
    path = join(key, sub_key)
    value = get_values(path, ['DisplayName', 'UninstallString', 'InstallDate'])

    if value:
        print(value)


# Local user

print ("==============================================================")
print ("Applications for local user")
print ("==============================================================")

key = r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'

for sub_key in get_sub_keys(key):
    path = join(key, sub_key)
    value = get_values(path, ['DisplayName', 'UninstallString', 'InstallDate'])

    if value:
        print(value)


# MSI installations

print ("==============================================================")
print ("MSI Installations")
print ("==============================================================")

key = r'HKEY_CLASSES_ROOT\INSTALLER\PRODUCTS'

for sub_key in get_sub_keys(key):
    path = join(key, sub_key)
    value = get_values(path, ['ProductName', 'ProductIcon'])

    if value:
        print(value)

key = r'HKEY_CURRENT_USER\SOFTWARE\MICROSOFT\INSTALLER\PRODUCTS'

for sub_key in get_sub_keys(key):
    path = join(key, sub_key)
    value = get_values(path, ['ProductName'])

    if value:
        print(value)

# Execution paths

print ("==============================================================")
print ("Installation paths")
print ("==============================================================")


key = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths'

for sub_key in get_sub_keys(key):
    path = join(key, sub_key)
    value = get_values(path, ['Path'])

    if value:
        print(sub_key,value)

key = r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths'

for sub_key in get_sub_keys(key):
    path = join(key, sub_key)
    value = get_values(path, ['Path'])

    if value:
        print(sub_key,value)

print ("==============================================================")
print ("Most recently used")
print ("==============================================================")

key = r'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run'

for sub_key in get_sub_keys(key):
    path = join(key, sub_key)
    value = get_values(path, ['OneDrive'])

    if value:
        print(sub_key,value)