#  python file used for managing the database
import os

# function to start an instance of the database
def startUp():
    os.system("mysql.server start")

# function to close an instance of the database
def stop():
    os.system("mysql.server stop")

# function to check if the database exist, if not then create one
def verifyTables(dnName):
    os.system("")
