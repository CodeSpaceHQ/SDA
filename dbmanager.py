#  python file used for managing the database
import os
import ctypes

# function to start an instance of the database
def startUp(isAdmin):
    if isAdmin:
        #os.system("runas /user:administrator \"net start mysql57\"")
        os.system("net start mysql57")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "net start mysql57", None, 1)

# function to close an instance of the database
def stop(isAdmin):
    if isAdmin:
        #os.system("runas /user:administrator \"net stop mysql57\"")
        os.system("net stop mysql57")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "net stop mysql57", None, 1)
