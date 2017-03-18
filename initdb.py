# Initializes a MySQL Database
# 1) connect to server
# 2) create database with cursor
# 3) connect to database
# 4) create tables with cursor
# 5) commit transactoins
# 6) exit

import sys
import mysql.connector
import dbmanager
from mysql.connector import errorcode

# Start up a database instance
db.startUp()

# Define constants
DB_NAME = "starbucksdb"

TABLES = dict()
# Create table statments
# replace with own schema

# https://www.kaggle.com/starbucks/store-locations
TABLES['locations'] = (
    "CREATE TABLE `locations` ("
    "   `brand` varchar(15) NOT NULL,"
    "   `store_number` varchar(20) NOT NULL,"
    "   `store_name` varchar(15) NOT NULL,"
    "   `ownership_type` varchar(10) NOT NULL,"
    "   `street_address` varchar(25) NOT NULL,"
    "   `city` varchar(15) NOT NULL,"
    "   `state` varchar(2) NOT NULL,"
    "   `country` varchar(2) NOT NULL,"
    "   `postcode` varchar(10),"
    "   `phone_number` varchar(11),"
    "   `timezone` varchar(20) NOT NULL,"
    "   `longitude` decimal(4,2) NOT NULL,"
    "   `latitude` decimal(4,2) NOT NULL"
    ") ENGINE=InnoDB")

# https://github.com/kdallas2/diversity/blob/master/di.csv
TABLES['diversity'] = (
    "CREATE TABLE `diversity` ("
    "   `location` varchar(15) NOT NULL,"
    "   `diversity_index` decimal(7,6) NOT NULL,"
    "   `african_american` decimal(4,2) NOT NULL,"
    "   `american_indian` decimal(4,2) NOT NULL,"
    "   `asian` decimal(4,2) NOT NULL,"
    "   `pacific_islander` decimal(4,2) NOT NULL,"
    "   `two_or_more` decimal(4,2) NOT NULL,"
    "   `hispanic_latino` decimal(4,2) NOT NULL,"
    "   `white_only` decimal(4,2) NOT NULL"
    ") ENGINE=InnoDB")


def create_database(cursor, connection):
    """
    Attempt to create the DB_NAME database
    """
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
    Attempt to connecect to DB_NAME database
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
try:
    mysql_connection = mysql.connector.connect(user=username,
                                               password=password)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Username or Password was incorrect.")
    else: print(err)

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
