#Functionaliteit van Romy.
import codecs
import os
import subprocess

def main():
    all_proc_info = get_proc_info('NAME="explorer.exe"')

    test.log("All names and values of first process found:");
    first_process = all_proc_info[0];
    for n, v in first_process.iteritems():
        test.log("  " + n + ": " + v);

    test.log("")

    test.log("Accessing a single value:")
    test.log("  CommandLine: " + first_process["CommandLine"])

def get_proc_info(search_expression=None):
    if search_expression is None:
        search_expression = ""
    else:
        search_expression = " WHERE " + search_expression

    # Execute with wmic and capture output:
    s = 'pushd "' + os.getcwd() + '" && wmic PROCESS ' + search_expression + ' GET * /format:csv <nul'
    d = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0];

    # Strip first empty line produced by wmic:
    d = d[3:]

    # Write to file (to later read via testData API):
    fn = "temp.csv"
    f = codecs.open(fn, "w", "utf8")
    f.write(d)
    f.close()

    # Read via testData API:
    dataset = testData.dataset(fn)
    all_proc_info = []
    for row in dataset:
        proc_info = {}
        field_names = testData.fieldNames(row)
        for n in field_names:
            v = testData.field(row, n)
            proc_info[n] = v
        all_proc_info.append(proc_info)
    os.remove(fn)
    return all_proc_info