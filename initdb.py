import os
import csv
from exceptions import InputError, MySqlError
from dbmanager import init_connection
import mysql.connector

# Define constants
DB_NAME = "starbucksdb"

# SQL CREATE statements for each table
TABLES = dict()
TABLES['income'] = (
    "CREATE TABLE IF NOT EXISTS `income` ("
    "   `STATEFIPS` char(2) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `ZIPCODE` char(5) NOT NULL,"
    "   `AGI_STUB` tinyint NOT NULL,"
    "   `NUM_RETURNS` float(15,4) NOT NULL,"
    "   `TOTAL_INCOME` float(15,4) NOT NULL,"
    "   PRIMARY KEY (`STATE`, `ZIPCODE`, `AGI_STUB`)"
    ") ENGINE=InnoDB")

TABLES['starbucks'] = (
    "CREATE TABLE IF NOT EXISTS `starbucks` ("
    "   `STORE_NUMBER` varchar(20) NOT NULL,"
    "   `CITY` varchar(50) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `ZIPCODE` char(5) NOT NULL,"
    "   `LONG` varchar(10) NOT NULL,"
    "   `LAT` varchar(10) NOT NULL,"
    "   PRIMARY KEY (`STORE_NUMBER`)"
    ") ENGINE=InnoDB")

TABLES['diversity'] = (
    "CREATE TABLE IF NOT EXISTS `diversity` ("
    "   `COUNTY` varchar(50) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `INDEX` float(7,6) NOT NULL,"
    "   `1` float(3,1) NOT NULL,"
    "   `2` float(3,1) NOT NULL,"
    "   `3` float(3,1) NOT NULL,"
    "   `4` float(3,1) NOT NULL,"
    "   `5` float(3,1) NOT NULL,"
    "   `6` float(3,1) NOT NULL,"
    "   `7` float(3,1) NOT NULL,"
    "   PRIMARY KEY (`COUNTY`, `STATE`)"
    ") ENGINE=InnoDB")

TABLES['locations'] = (
    "CREATE TABLE IF NOT EXISTS `locations` ("
    "   `ZIPCODE` char(5) NOT NULL,"
    "   `CITY` varchar(50) NOT NULL,"
    "   `STATE` char(2) NOT NULL,"
    "   `COUNTY` varchar(50) NOT NULL,"
    "   PRIMARY KEY (`ZIPCODE`, `COUNTY`)"
    ") ENGINE=InnoDB")

VIEWS = dict()
VIEWS['diversity_view'] = ("CREATE VIEW `diversity_view`"
                           "(`COUNTY, `STATE`, `INDEX`, `1`, `2`, `3`, `4`, "
                           "`5`, `6`, `7`, `ZIPCODE`) "
                           "AS "
                           "SELECT d.*, l.zipcode"
                           "FROM diversity AS d "
                           "INNER JOIN locations AS l "
                           "ON l.county = REPLACE(d.county, ' County', '')"
                           "GROUP BY l.county "
                           "WITH CASCADED CHECK OPTION")

INDEX = dict()
INDEX['starbucks_zipcode'] = ("CREATE INDEX `starbucks_zipcode` "
                              "ON `starbucks` (`ZIPCODE`)")
INDEX['income_zipcode'] = ("CREATE INDEX `income_zipcode` "
                           "ON `starbucks` (`ZIPCODE`)")
INDEX['starbucks_state'] = ("CREATE INDEX `starbucks_state` "
                            "ON `starbucks` (`STATE`)")
INDEX['starbucks_city'] = ("CREATE INDEX `starbucks_city` "
                           "ON `starbucks` (`CITY`)")
INDEX['income_zipcode'] = ("CREATE INDEX `income_zipcode` "
                           "ON `income` (`ZIPCODE`)")
INDEX['diversity_state'] = ("CREATE INDEX `diversity_state` "
                            "ON `diversity` (`STATE`)")

# SQL INSERT statements for each table
SQL_INSERT = {}
SQL_INSERT['income'] = "INSERT INTO income " \
                       "VALUES(%s, %s, %s, %s, %s, %s);"
SQL_INSERT['starbucks'] = "INSERT INTO starbucks " \
                          "VALUES(%s, %s, %s, %s, %s, %s);"
SQL_INSERT['diversity'] = "INSERT INTO diversity " \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
SQL_INSERT['locations'] = "INSERT INTO locations " \
                          "VALUES(%s, %s, %s, %s);"

# Load each data set
DATASETS = dict()
DATASETS['income'] = csv.reader(open(os.path.join('datasets',
                                                  'income-data.csv')))
DATASETS['starbucks'] = csv.reader(open(os.path.join('datasets',
                                                     'starbucks.csv')))
DATASETS['diversity'] = csv.reader(open(os.path.join('datasets',
                                                     'diversity.csv')))
DATASETS['locations'] = csv.reader(open(os.path.join('datasets',
                                                     'locations.csv')))


def init_database(connection):
    """Initialize the database for use.
    
    Creates the DB_NAME database and creates any tables defined
    in TABLES dictionary inside of the newly created database
    Args:
         connection: the connection to the MySQL Server
    Raises:
         MySqlError: Raised if there is a connection error or SQL syntax error
    """
    create_db = 'CREATE DATABASE IF NOT EXISTS {}'.format(DB_NAME)
    try:
        cursor = connection.cursor()
        cursor.execute(create_db)  # Create the database
        connection.database = DB_NAME  # Connect to the database

        for name, sql in TABLES.items():  # Create each table in the database
            print('Creating table {}'.format(name))
            cursor.execute(sql)
        for name, sql in VIEWS.items():  # Create each view
            print('Creating view {}'.format(name))
            cursor.execute(sql)
        for name, sql in INDEX.items():
            print('Creating index {}'.format(name))  # Create column indexes
            cursor.execute(sql)

        cursor.close()
    except mysql.connector.Error as err:
        print(err)
        raise MySqlError(message='There was a problem initializing'
                                 ' the database.',
                         args=err.args)


def init_data(connection):
    """Insert data from `DATASETS` into `TABLES` in the database
    
    For each data set in `DATASETS`, use the corresponding
    SQL statement in `SQL_INSERT` to insert each record of each
    data set into the data sets corresponding table.
    NOTE: MySQL server has a `max_allowed_packet` which defaults
          to 1MB. For this reason we split our data up into thirds.
          larger data sets may need splitting up into smaller fractions.
          All inserts are done in one transaction and are rolled back
          on any error.
    Args:
        connection: the open connection to the MySQL Server
    Raises:
        MySqlError: typically a error in SQL syntax, may be an insertion
                       that is larger than the `max_allowed_packet` size
    """
    try:
        cursor = connection.cursor()
        connection.start_transaction()

        for name, data in DATASETS.items():
            print("Inserting data into {}...".format(name))
            next(data)  # skip the header row
            data = list(data)
            third = len(data) // 3  # Split the data set into thirds
            data_blob_1 = data[:third]
            data_blob_2 = data[third:third * 2]
            data_blob_3 = data[third * 2:]
            cursor.executemany(SQL_INSERT[name], data_blob_1)
            cursor.executemany(SQL_INSERT[name], data_blob_2)
            cursor.executemany(SQL_INSERT[name], data_blob_3)

        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        connection.rollback()
        raise MySqlError(message='Error inserting data: ' + err.msg,
                         args=err.args)


def main(username=None, password=None):
    cnx = init_connection(username, password, False)
    init_database(cnx)
    init_data(cnx)
    cnx.close()


if __name__ == '__main__':
    try:
        main()
    except (InputError, MySqlError) as db_exception:
        print(db_exception.message)
