import logging
import sys
import proces_list

f = open('hashfile.txt', 'w', encoding="utf-8")
f.close()

#Logger is aangeroepen over het hele project
logging.basicConfig(handlers=[logging.FileHandler('logboek.log', 'w', 'utf-8')], format='%(name)s: %(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)


# Proces List
filter_question = ""
filter_name = ""
filter_path = ""
want_to_use_proceslist = input("Do you want to scan on Processes (Y or N)? ")
if (want_to_use_proceslist.upper() == "N"):
    print("")
elif (want_to_use_proceslist.upper() == "Y"):
    filter_question = input("Do you want to filter the processes? Y/N: ")
    if(filter_question.upper() == "Y"):
        filter_name = input("Do you want to filter on name? Please give the name else leave blank and press enter: ")
        filter_path = input("Do you want to filter on type? Please give the type else leave blank and press enter: ")
else:
    print("Did not select Y or N, please restart program and try again")
    sys.exit(1)

#pre EXE
if(want_to_use_proceslist.upper() == "Y"):
    proces_list.main(filter_question, filter_name, filter_path)