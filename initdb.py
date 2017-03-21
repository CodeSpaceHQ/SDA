# Initializes a MySQL Database

import os
import csv
import mysql.connector

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
    "   `CITY` varchar(50) NOT NULL,"
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
    "   `ZIPCODE` char(5) NOT NULL,"
    "   `CITY` varchar(50) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `COUNTY` varchar(50) NOT NULL,"
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

# Load the data sets
DATASETS = dict()
DATASETS['income'] = csv.reader(open(os.path.join('datasets', 'income-data.csv')))
DATASETS['starbucks'] = csv.reader(open(os.path.join('datasets', 'starbucks.csv')))
DATASETS['diversity'] = csv.reader(open(os.path.join('datasets', 'diversity.csv')))
DATASETS['locations'] = csv.reader(open(os.path.join('datasets', 'locations.csv')))


def create_database(cursor):
    """
    Attempt to create the DB_NAME database
    """
    try:
        create_sda_db = "CREATE DATABASE {}".format(DB_NAME)
        print("Creating database {}".format(DB_NAME))
        cursor.execute(create_sda_db)
    except mysql.connector.Error as mysql_error:
        raise Exception('Failed creating database: {}'.format(mysql_error))


def connect_to_database(connection):
    """
    Attempt to connect to DB_NAME database
    """
    try:
        connection.database = DB_NAME
    except mysql.connector.Error as mysql_error:
        raise Exception('There was a problem connecting to the database {}:\n{}'.format(DB_NAME, mysql_error))


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
        except mysql.connector.Error as mysql_error:
            raise Exception('There was a problem creating table {}:\n{}'.format(name, mysql_error))


def insert_data(cursor):
    complete = 1
    for name, data in DATASETS.items():
        next(data)
        total = len(DATASETS)
        print("({}/{})Inserting data into {}".format(complete, total, name))
        complete += 1
        for row in data:
            cursor.execute(SQL_INSERT[name], row)


def main(username='', password=''):
    if username == "" or password == "":
        # Get username and password for desired account
        username = input("Username (root or other account): ")
        password = input("Password: ")

    # Connect to the MySQL server with user credentials
    # Will exit if MySQL Server is not started
    try:
        mysql_connection = mysql.connector.connect(user=username,
                                                   password=password)
    except mysql.connector.Error as err:
        raise Exception('There was a problem connecting to the server:\n{}'.format(err))

    # Get cursor from server connection
    mysql_cursor = mysql_connection.cursor()

    # Set autocommit to false for batch
    mysql_connection.autocommit = False

    # Start a transaction
    mysql_connection.start_transaction()

    # Create database
    create_database(mysql_cursor)

    # Create tables
    create_tables(mysql_cursor, mysql_connection)

    # insert data
    insert_data(mysql_cursor)

    # Commit transaction
    mysql_connection.commit()

    # Close cursor
    mysql_cursor.close()
    
    # Close connection
    mysql_connection.close()

if __name__ == '__main__':
    try:
        main()
    # TODO: make exceptions more specific
    except Exception as db_exception:
        print(db_exception)
