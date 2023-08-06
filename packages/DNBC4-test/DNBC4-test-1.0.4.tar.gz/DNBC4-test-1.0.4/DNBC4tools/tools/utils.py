import os
import subprocess
from functools import wraps

def str_mkdir(arg):
    if not os.path.exists(arg):
        os.system('mkdir -p %s'%arg)

def start_print_cmd(arg):
    print(arg)
    subprocess.check_call(arg,shell=True)

def change_ld_path():
    python_path = os.environ.get("_")
    os.environ['LD_LIBRARY_PATH'] = '/'.join(str(python_path).split('/')[0:-2]) + '/lib'


