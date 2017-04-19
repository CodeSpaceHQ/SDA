from exceptions import InputError, MySqlError
import mysql.connector

DB_NAME = 'starbucksdb'


def init_connection(username=None, password=None):
    """Initializes connection to running MySQL server

    Connects to a running MySQL server using a username/password
    and returns the connection if successful.
    Args:
        username: the username of the account on the server to connect with
        password: the password of the account on the server to connect with
    Returns:
        connection: the open connection to the MySQL server
    Raises:
        InputError: The username or password input was incorrect
    """
    if not username or not password:
        username = input("Username: ")
        password = input("Password: ")

    try:
        connection = mysql.connector.connect(user=username,
                                             password=password,
                                             database=DB_NAME)
    except mysql.connector.Error as err:
        raise InputError(message='There was a problem connecting. Please check'
                                 ' your username and password, and make sure'
                                 ' the server is running.',
                         args=err.args)
    return connection


def exec_sql(connection, sql):
    """Execute an sql statement on the connected database    
    :arg connection: the varaible holding a connection to the database
    :arg sql: the SQL statement to execute    
    :returns None if the connection or sql was None,
             a cursor containing the results of the statement otherwise
    :raises A MySqlError (likely due to an error in the SQL statement syntax)
    
    example: 
        
        in a separate python file `your_file_name.py`:
            import dbmanager
            connection = dbmanager.init_connection('MySQLusername', 'MySQLpassword')
            sql = 'SELECT * FROM locations LIMIT 10;'
            result = dbmanager.exec_sql(connection, sql)
            print(result)
    """
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except mysql.connector.Error as err:
        raise MySqlError(message=err.msg,
                            args=err.args)
    return cursor.fetchall()  # return a list of tuples


def main(username=None, password=None, sql=None):
    # Attempt a connection to the server and database
    cnx = init_connection(username, password)
    if not sql:
        sql = input('What SQL would you like to execute?: ')
    # Execute the sql statement provided and return the result
    try:
        data = exec_sql(cnx, sql)  # data is a list of tuples
        return data
    except MySqlError as err:
        print(err.message)


if __name__ == '__main__':
    main()
