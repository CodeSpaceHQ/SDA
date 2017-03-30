import dbmanager
import initdb
import ctypes

print("\t*****************************")
print("\t***** Choose an option ******")
print("\t*****************************")
print("\n")
print("[1] Initialize the SDA database and tables")
print("[q] Quit")

choice = ''
while choice != 'q':
    choice = input("option: ")

    if choice == 'q':
        print("GoodBye!")
    elif choice == '1':
        initdb.main()
    else:
        print("\n!!Invalid Input!!")
