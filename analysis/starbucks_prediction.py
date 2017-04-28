import csv
import dbmanager
from exceptions import MySqlError

# machine learning imports
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
import pandas
import numpy

sql_income = "SELECT SUM(i.TOTAL_INCOME) as total_income, i.NUM_RETURNS as num_returns, " \
             "i.TOTAL_INCOME / i.NUM_RETURNS as per_capita_income, " \
             "CASE " \
             "WHEN s.STORE_NUMBER IS NOT NULL THEN 1 " \
             "ELSE 0 " \
             "END AS has_starbucks " \
             "FROM	income as i " \
             "LEFT	OUTER JOIN starbucks as s " \
             "ON	i.ZIPCODE = s.ZIPCODE " \
             "WHERE num_returns > 0 " \
             "GROUP	BY i.ZIPCODE "

ml_models = {"random forest": RandomForestClassifier()}


def run(connection, sql):
    """ Run the SQL of this analysis against the database

    This module gathers all total income values for each zipcode and
    a 1 if a Starbucks location exists there, or a 0 otherwise.

    Args:
        connection: the connection to the MySQL Server database

    Example results:

    """
    print("Income vs Starbucks Locations")
    try:
        res = dbmanager.exec_sql(connection, sql)
    except MySqlError as err:  # except a MySQL error from dbmanager.exec_sql()
        raise MySqlError(message=err.message, args=err.args)

    return res


def split_data(data, target):
    """ Splits a dataset into the feature columns and the target/label column.

    :param data: Original dataset
    :return: feature columns, target column (both as DataFrames)
    """
    x_data = data.drop(target, 1).reset_index(drop=True)
    y_data = data[target].reset_index(drop=True)
    return x_data, y_data


def equalize_binary_data(data, positive, negative, ratio=1):
    """ Equalizes the number of 0s and 1s according to the ratio specified, default 1:1

    :param data: Dataset to equalize
    :param positive: The number of 1s
    :param negative: The number of 0s
    :param ratio: The weight to apply to the number of 1s
    :return: The equalized dataset
    """
    indices = []
    diff = negative - positive * ratio

    for index, row in data.iterrows():
        if diff > 0 and row[data.shape[1] - 1] == 0:
            indices.append(index)
            diff -= 1

    return data.drop(data.index[indices])


def binary_equalizer(data, equalize=0):
    """ Randomizes the data and selects a subset if it needs to be equalized by the ratio of binary
    target outputs.

    :param data: The data to be selected from
    :param equalize: Whether or not to equalize the data
    :return: A randomized dataset with possible equal ratio of binary targets
    """

    # Must happen before equalization to maintain integrity of results
    randomized_data = data.reindex(numpy.random.permutation(data.index)).reset_index(drop=True) # randomize/reset index

    if equalize:
        locations = randomized_data["has_location"].value_counts()[1]
        non_locations = randomized_data["has_location"].value_counts()[0]
        randomized_data = equalize_binary_data(randomized_data, locations, non_locations)

    return randomized_data


def get_train_test(data, target, ratio=0.3):
    train, test = model_selection.train_test_split(data, test_size=ratio)

    x_train, y_train = split_data(train, target)
    y_train = y_train.values.reshape((len(y_train.values.tolist()), 1))
    x_test, y_test = split_data(test, target)
    y_test = y_test.values.reshape((len(y_test.values.tolist()), 1))

    return x_train, y_train, x_test, y_test


def get_results(x_test, y_test, trained_model, key):
    print("Results for " + key + ":")
    print(trained_model.score(x_test, y_test))


def run_all_classifiers(data):
    for key, model in ml_models.items():
        # data preparation for machine learning
        randomized_data = binary_equalizer(data, equalize=1)
        x_train, y_train, x_test, y_test = get_train_test(randomized_data, "has_location")

        trained_model = model.fit(x_train, y_train)
        get_results(x_test, y_test, trained_model, key)


def main():
    # data retrieval
    cnx = dbmanager.init_connection()
    data = pandas.DataFrame(run(cnx, sql_income), columns=["income", "num_returns", "per_capita_income", "has_location"])

    # classifier runner
    run_all_classifiers(data)


if __name__ == '__main__':
    main()
