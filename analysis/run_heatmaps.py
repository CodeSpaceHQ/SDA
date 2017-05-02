import dbmanager
import csv
from exceptions import MySqlError

sql = ("SELECT ZIPCODE, SUM(TOTAL_INCOME) AS total, "
       "       CASE "
       "            WHEN SUM(TOTAL_INCOME) > 1000000 THEN 6 "
       "            WHEN SUM(TOTAL_INCOME) BETWEEN 500000 AND 1000000 THEN 5 "
       "            WHEN SUM(TOTAL_INCOME) BETWEEN 100000 AND 500000 THEN 4 "
       "            WHEN SUM(TOTAL_INCOME) BETWEEN 50000 AND 100000 THEN 3 "
       "            WHEN SUM(TOTAL_INCOME) BETWEEN 25000 AND 50000 THEN 2 "
       "            ELSE 1 "
       "       END AS weight "
       "  FROM starbucksdb.income "
       " WHERE total_income > 0 AND zipcode <> '00000' "
       " GROUP BY ZIPCODE; ")


def run(connection):
    """ Run the SQL of this analysis against the database

    This module gathers all total income values for each zipcode and
    a 1 if a Starbucks location exists there, or a 0 otherwise.

    Args:
        connection: the connection to the MySQL Server database

    Example results:

    """
    print("Data for Heatmaps")
    res = []
    try:
        res = dbmanager.exec_sql(connection, sql)
    except MySqlError as err:  # except a MySQL error from dbmanager.exec_sql()
        raise MySqlError(message=err.message, args=err.args)

    export_csv(res)


def export_csv(data):
    print("Exporting to `./analysis/heatmaps_data.csv")
    with open('heatmaps_data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


def main():
    cnx = dbmanager.init_connection('root', 'password')
    run(cnx)


if __name__ == '__main__':
    main()
