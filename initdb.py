# Initializes a MySQL Database
# 1) connect to server
# 2) create database with cursor
# 3) connect to created database
# 4) create tables with cursor
# 6) exit

import sys
import csv
import mysql.connector
import dbmanager
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
    "   `NUM_RETURNS` float(15,4) NOT NULL,"
    "   `TOTAL_INCOME` float(15,4) NOT NULL,"
    "   PRIMARY KEY (STATE, ZIPCODE, AGI_STUB)"
    ") ENGINE=InnoDB")

TABLES['starbucks'] = (
    "CREATE TABLE `starbucks` ("
    "   `STORE_NUMBER` varchar(20) NOT NULL,"
    "   `CITY` char(50) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `ZIPCODE` char(5) NOT NULL,"
    "   `LONG` varchar(10) NOT NULL,"
    "   `LAT` varchar(10) NOT NULL,"
    "   PRIMARY KEY (STORE_NUMBER)"
    ") ENGINE=InnoDB")

TABLES['diversity'] = (
    "CREATE TABLE `diversity` ("
    "   `COUNTY` varchar(50) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `INDEX` float(7,6) NOT NULL,"
    "   `1` float(3,1) NOT NULL,"
    "   `2` float(3,1) NOT NULL,"
    "   `3` float(3,1) NOT NULL,"
    "   `4` float(3,1) NOT NULL,"
    "   `5` float(3,1) NOT NULL,"
    "   `6` float(3,1) NOT NULL,"
    "   `7` float(3,1)NOT NULL,"
    "   PRIMARY KEY (COUNTY, STATE)"
    ") ENGINE=InnoDB")

TABLES['locations'] = (
    "CREATE TABLE `locations` ("
    "   `ZIPCODE` varchar(25) NOT NULL,"
    "   `CITY` char(50) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `COUNTY` char(50) NOT NULL,"
    "   PRIMARY KEY (ZIPCODE, COUNTY)"
    ") ENGINE=InnoDB")

# SQL insert queries for each table
SQL_INSERT = dict()
SQL_INSERT['income'] = "INSERT INTO income " \
                       "VALUES(%s, %s, %s, %s, %s, %s);"
SQL_INSERT['starbucks'] = "INSERT INTO starbucks " \
                          "VALUES(%s, %s, %s, %s, %s, %s);"
SQL_INSERT['diversity'] = "INSERT INTO diversity " \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
SQL_INSERT['locations'] = "INSERT INTO locations " \
                          "VALUES(%s, %s, %s, %s);"

# Data sets for each table
DATASETS = dict()
DATASETS['income'] = csv.reader(open('datasets\income-data.csv'))
DATASETS['starbucks'] = csv.reader(open('datasets\\starbucks.csv'))
DATASETS['diversity'] = csv.reader(open('datasets\\diversity.csv'))
DATASETS['locations'] = csv.reader(open('datasets\\locations.csv'))


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


def insert_data(cursor, connection):
    complete = 1
    for name, data in DATASETS.items():
        next(data)
        total = len(DATASETS)
        print("({}/{})Inserting data into {}...".format(complete, total, name))
        complete += 1
        for row in data:
            cursor.execute(SQL_INSERT[name], row)


def main(username='', password=''):
    if __name__ == '__main__': main()

    if username == "" or password=="":
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

    # Start a transaction
    mysql_connection.start_transaction()

    # Create database
    create_database(connection_cursor, mysql_connection)
    # Create tables
    create_tables(connection_cursor, mysql_connection)
    # insert data
    insert_data(connection_cursor, mysql_connection)

    # Commit transaction
    mysql_connection.commit()

    # Close cursor
    connection_cursor.close()
    # Close connection
    mysql_connection.close()

    # Print completed
    print("Database set up completed.")


