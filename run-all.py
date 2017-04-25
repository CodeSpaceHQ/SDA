" Script to run all analysis scripts """
import glob
import os
import ntpath
from importlib import import_module
from dbmanager import init_connection

def get_name(path):
    """ Extracts the file name from a filepath"""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def get_script_names():
    """ Gets a list of all the module names that meet the regex:
        ./analysis/run_*.py """
    ntpath.basename('./analysis/')
    files = glob.glob('./analysis/run_*.py')
    filenames = [get_name(file) for file in files]
    return [os.path.splitext(name)[0] for name in filenames]



def run_all(username=None, password=None):
    """ Calls run() method for every analysis script, passing in db connection
    as an argument. Handles connection handling. """
    print("Starting")
    modules = get_script_names()
    connection = init_connection(username, password)
    for module in modules:
        script = import_module('analysis.{}'.format(module))
        print(script)
        script.run(connection)

    connection.close()

if __name__ == '__main__':
    run_all()
