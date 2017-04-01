import initdb
import ctypes

def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAdmin()
    except:
        return False

print("\t*****************************")
print("\t***** Choose an option ******")
print("\t*****************************")
print("\n")
print("[1] Start up the database")
print("[2] Stop the database instance")
print("[3] Initialize the SDA database and tables")
print("[q] Quit")

choice = ''
while choice != 'q':
    choice = input("option: ")

    if choice == 'q':
        print("GoodBye!")
    elif choice == '1':
        dbmanager.startUp(isAdmin())
    elif choice == '2':
        dbmanager.stop(isAdmin)
    elif choice == '3':
        initdb.main()
    else:
        print("\n!!Invalid Input!!")
