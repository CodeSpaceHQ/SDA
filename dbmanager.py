#  python file used for managing the database
import os

# function to start an instance of the database
def startUp():
    os.system("runas /user:administrator \"net start mysql57\"")

# function to close an instance of the database
def stop():
    os.system("runas /user:administrator \"net stop mysql57\"")
