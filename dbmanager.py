from exceptions import InputError, MySqlError
import mysql.connector

DB_NAME = 'starbucksdb'


def init_connection(username=None, password=None):
    """Establish a connection to database
    :arg username: the username required to access the server
    :arg password: the password required to access the server
    :returns None if no username or password was provided,
            a valid connection (if one was found) otherwise
    :raises An InputError (likely because no username or password was provided)
    """
    if not username or not password:
        return None
    try:
        connection = mysql.connector.connect(username=username,
                                             password=password,
                                             database=DB_NAME)
    except mysql.connector.Error as err:
        raise InputError(message='There was an error connecting to the server.',
                         args=err.args)
    return connection


def exec_sql(connection, sql):
    """Execute an sql statement on the connected database    
    :arg connection: the varaible holding a connection to the database
    :arg sql: the SQL statement to execute    
    :returns None if the connection or sql was None,
             a cursor containing the results of the statement otherwise
    :raises A MySqlError (likely due to an error in the SQL statement syntax)
    """
    cursor = None
    if sql and connection:
        cursor = connection.cursor()
        try:
            return cursor.execute(sql)
        except mysql.connector.Error as err:
            raise MySqlError(message=err.msg,
                             args=err.args)
    return cursor


def main(username=None, password=None, sql=None):
    # Attempt a connection to the server and database
    cnx = init_connection(username, password)
    # Execute the sql statement provided and return the result
    return exec_sql(cnx, sql)


if __name__ == '__main__':
    main()
