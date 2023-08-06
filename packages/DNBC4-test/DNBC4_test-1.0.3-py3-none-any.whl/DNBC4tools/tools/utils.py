import os
import subprocess
from functools import wraps

_version = "1.0.1"

_pipelist = [
    "data",
    'count',
    #'analysis',
    #'report',
    #'clean',
    #'clean',
    #'run',
]
_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))

def str_mkdir(arg):
    if not os.path.exists(arg):
        os.system('mkdir -p %s'%arg)

def change_env():
    os.environ['PATH'] ="%s/miniconda3/envs/scRNA/bin"%_root_dir
    os.environ['LD_LIBRARY_PATH'] ="%s/miniconda3/envs/scRNA/lib"%_root_dir

def start_print_cmd(arg):
    print(arg)
    subprocess.check_call(arg,shell=True)



