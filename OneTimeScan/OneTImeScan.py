if (Wanna_use_FS.upper() == "Y"):
    File_system.main(pathname, filter1, filtersize, sizef, filtername, namef, filterpath, pathf, save)

print()
if(Wanna_use_Tasks.upper() == "Y"):
    scheduled_tasks.main(WantToFilter, filterOnName, filterOnState, filterOnPath, WantToPrintList)

print()
if(Wanna_use_Keys.upper() == "Y"):
    registry_key.main(geef_HKEY, geef_pad, filter_vraag, filter_naam, filter_type)

print()
if(want_to_use_proceslist.upper() == "Y"):
    proces_list.main(filter_question, filter_name, filter_path)