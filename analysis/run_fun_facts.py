import dbmanager
from exceptions import MySqlError

FACTS = dict()

FACTS['stores_in_us'] = [(
    "SELECT COUNT(STORE_NUMBER) FROM starbucks;"
)]
FACTS['city_w_most_stores'] = [(
    "SELECT	STATE, CITY, COUNT(STORE_NUMBER) as store_count "
    "FROM	starbucks "
    "GROUP	BY STATE, CITY "
    "ORDER	BY store_count DESC "
    "LIMIT	1;"
)]
FACTS['state_w_most_starbucks'] = [(
    "SELECT	STATE, COUNT(STORE_NUMBER) as store_count "
    "FROM	starbucks "
    "GROUP	BY STATE "
    "ORDER	BY store_count DESC "
    "LIMIT	1;"
)]
FACTS['state_w_least_starbucks'] = [(
    "SELECT	l.STATE, COUNT(s.STORE_NUMBER) as store_count "
    "FROM	starbucks as s "
    "RIGHT	OUTER JOIN locations as l "
    "ON	    s.STATE = l.STATE "
    "AND	s.CITY = l.CITY "
    "GROUP	BY l.STATE "
    "HAVING	store_count > 0 "
    "ORDER	BY store_count ASC "
    "LIMIT	1;"
)]
FACTS['num_cities_without_starbucks'] = [(
    "SELECT	COUNT(DISTINCT l.CITY, l.STATE) as city_count "
    "FROM	starbucks as s "
    "RIGHT	OUTER JOIN locations as l "
    "ON	    s.STATE = l.STATE "
    "AND	s.CITY = l.CITY "
    "WHERE	s.STORE_NUMBER IS NULL; "
)]
FACTS['num_starbucks_lubbock'] = [(
    "SELECT COUNT(STORE_NUMBER) as store_count "
    "FROM   starbucks "
    "WHERE  STATE = 'TX' "
    "AND    CITY = 'Lubbock'; "
)]

def run(connection):
    """ Run the SQL of this analysis against the database

    This module gathers all total income values for each zipcode and
    a 1 if a Starbucks location exists there, or a 0 otherwise.

    Args:
        connection: the connection to the MySQL Server database

    Example results:

    """
    print("Starbucks Fun Facts")
    res = []
    try:
        for name, stuff in FACTS.items():
            res = dbmanager.exec_sql(connection, stuff[0])
            FACTS[name].append(res)
    except MySqlError as err:  # except a MySQL error from dbmanager.exec_sql()
        raise MySqlError(message=err.message, args=err.args)

    export_txt(res)


def export_txt(data):
    print("Exporting to `./analysis/fun_facts.txt")
    with open('fun_facts.txt', 'w') as txt_file:
        for name, stuff in FACTS.items():
            txt_file.write(name + " :" + str(stuff[1]) + "\n")


def main():
    cnx = dbmanager.init_connection('root', 'password')
    run(cnx)


if __name__ == '__main__':
    main()
