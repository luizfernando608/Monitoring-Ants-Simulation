import subprocess
import sys
import getopt
from os import name

def myfunc(argv):
    num_processes = int()
    arg_help = "{0} -n <num_processes>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "n:", ["number="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-n", "--number"):
            num_processes = int(arg)
    
    return num_processes



num_scenarios = myfunc(sys.argv)

if name == "nt":
    python_comand = "python"
else:
    python_comand = "python3"

comand = " & ".join([f"{python_comand} scenario.py"]*num_scenarios)
print(comand)
subprocess.run(comand, shell=True)



