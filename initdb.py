# Initializes a MySQL Database
# 1) connect to server
# 2) create database with cursor
# 3) connect to database
# 4) create tables with cursor
# 5) commit transactoins
# 6) exit

import sys
import mysql.connector
from mysql.connector import errorcode

# Define constants
DB_NAME = "starbucksdb"

TABLES = dict()
# Create table statements
TABLES['income'] = (
    "CREATE TABLE `income` ("
    "   `STATEFIPS` char(2) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `ZIPCODE` char(5) NOT NULL,"
    "   `AGI_STUB` tinyint NOT NULL,"
    "   `NUM_RETURNS` decimal(15,4) NOT NULL,"
    "   `TOTAL_INCOME` decimal(15,4) NOT NULL,"
    "   PRIMARY KEY (ZIPCODE)"
    ") ENGINE=InnoDB")

TABLES['starbucks-locations'] = (
    "CREATE TABLE `starbucks-locations` ("
    "   `STORE_NUMBER` varchar(20) NOT NULL,"
    "   `CITY` char(25) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `ZIPCODE` char(5) NOT NULL,"
    "   `LONG` varchar(10) NOT NULL,"
    "   `LAT` varchar(10) NOT NULL,"
    "   PRIMARY KEY (STORE_NUMBER)"
    ") ENGINE=InnoDB")

TABLES['diversity'] = (
    "CREATE TABLE `diversity` ("
    "   `COUNTY` varchar(20) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `INDEX` decimal(7,6) NOT NULL,"
    "   `1` decimal(3,1) NOT NULL,"
    "   `2` decimal(3,1) NOT NULL,"
    "   `3` decimal(3,1) NOT NULL,"
    "   `4` decimal(3,1) NOT NULL,"
    "   `5` decimal(3,1) NOT NULL,"
    "   `6` decimal(3,1) NOT NULL,"
    "   `7` decimal(3,1)NOT NULL,"
    "   PRIMARY KEY (COUNTY),"
    "   PRIMARY KEY (STATE)"
    ") ENGINE=InnoDB")

TABLES['locations'] = (
    "CREATE TABLE `locations` ("
    "   `ZIPCODE` varchar(25) NOT NULL,"
    "   `CITY` char(10) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `COUNTY` char(10) NOT NULL"
    ") ENGINE=InnoDB")


def create_database(cursor, connection):
    """
    Attempt to create the DB_NAME database
    """
    # Start transaction
    connection.start_transaction()
    try:
        create_sda_db = "CREATE DATABASE {}".format(DB_NAME)
        print("Creating database {}".format(DB_NAME))
        cursor.execute(create_sda_db)
    except mysql.connector.Error as mysqlError:
        print("Failed creating database: {}".format(mysqlError))
        sys.exit()
    # commit transactions
    connection.commit()


def connect_to_database(connection):
    """
    Attempt to connect to DB_NAME database
    """
    try:
        connection.database = DB_NAME
    except mysql.connector.Error as mysqlError:
        if mysqlError.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(mysqlError)
        sys.exit()


def create_tables(cursor, connection):
    """
    Attempt to execute each CREATE statement in TABLES
    to create tables.
    """
    # Connect to database
    connect_to_database(connection)
    # Start transaction
    connection.start_transaction()
    for name, query in TABLES.items():
        try:
            print("Creating table {}: ".format(name), end='')
            # Execute the CREATE xxx in TABLES
            cursor.execute(query)
        except mysql.connector.Error as mysqlError:
            if mysqlError.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists in {}".format(DB_NAME))
            elif mysqlError.errno == errorcode.ER_SYNTAX_ERROR:
                print(mysqlError)
            else:
                print(mysqlError.msg)
        else:
            print("OK")

        # commit transactions
        connection.commit()


# Get username and password for desired account
username = input("Username (root or other account): ")
password = input("Password: ")

# Connect to the MySQL server with user credentials
# Will exit if MySQL Server is not started
try:
    mysql_connection = mysql.connector.connect(user=username,
                                               password=password)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Username or Password was incorrect.")
    else:
        print(err)
    sys.exit()

# Get cursor from server connection
connection_cursor = mysql_connection.cursor()
# Set autocommit to false for batch
mysql_connection.autocommit = False
# Create database
create_database(connection_cursor, mysql_connection)
# Create tables
create_tables(connection_cursor, mysql_connection)
# Close cursor
connection_cursor.close()
# Close connection
mysql_connection.close()
