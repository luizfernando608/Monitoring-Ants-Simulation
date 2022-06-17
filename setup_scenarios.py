from operator import sub
import subprocess
import shlex
#%%
import time
num_scenarios = 10
comand = " & ".join(["python3 scenario.py"]*num_scenarios)
print(comand)
subprocess.run(comand, shell=True)
