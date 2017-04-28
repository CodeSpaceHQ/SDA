import csv
import dbmanager
from exceptions import MySqlError

sql = "SELECT	SUM(i.TOTAL_INCOME) as total_income, " \
      "CASE " \
      "WHEN s.STORE_NUMBER IS NOT NULL THEN 1 " \
      "ELSE 0 " \
      "END AS has_starbucks " \
      "FROM	income as i " \
      "LEFT	OUTER JOIN starbucks as s " \
      "ON	i.ZIPCODE = s.ZIPCODE " \
      "GROUP	BY i.ZIPCODE "


def run(connection):
    """ Run the SQL of this analysis against the database
    
    This module gathers all total income values for each zipcode and
    a 1 if a Starbucks location exists there, or a 0 otherwise.
    
    Args:
        connection: the connection to the MySQL Server database
        
    Example results:
    
    """
    print("Income vs Starbucks Locations")
    res = []
    try:
        res = dbmanager.exec_sql(connection, sql)
        print(res)
    except MySqlError as err:  # except a MySQL error from dbmanager.exec_sql()
        raise MySqlError(message=err.message, args=err.args)

    export_csv(res)


def export_csv(data):
    print("Exporting to `./analysis/income_vs_starbucks.csv")
    with open('income_vs_starbucks.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


def main():
    cnx = dbmanager.init_connection('root', 'password')
    run(cnx)


if __name__ == '__main__':
    main()
