from exceptions import InputError, MySqlError
import mysql.connector

DB_NAME = 'starbucksdb'

def init_connection(username=None, password=None):
    connection = None
    if username is None or password is None:
        return None

    try:
        connection = mysql.connector.connect(username=username,
                                              password=password,
                                              database=DB_NAME)
    except mysql.connector.Error as err:
        raise InputError(message='There was an error connecting to the server.',
                         args=err.args)
    return connection

def exec_sql(connection, sql=None):
    if sql and connection:
        cursor = connection.cursor()
        try:
            return cursor.execute(sql)

        except mysql.connector.Error  as err:
            raise MySqlError(message='There was a problem executing your query.',
                             args=err.args)


def main(username=None, password=None, sql=None):

    cnx = init_connection(username, password)
    return exec_sql(cnx, sql)

if __name__ == '__main__':
    main()