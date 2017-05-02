from exceptions import MySqlError
import dbmanager
import matplotlib.pyplot as plt

# machine learning imports
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
import pandas
import numpy

INC_COLNAMES = ["income", "num_returns", "per_capita_income", "has_location"]
SQL_INCOME = "SELECT SUM(i.TOTAL_INCOME) as total_income, SUM(i.NUM_RETURNS) as num_returns, " \
             "SUM(i.TOTAL_INCOME) / SUM(i.NUM_RETURNS) as per_capita_income, " \
             "CASE " \
             "WHEN s.STORE_NUMBER IS NOT NULL THEN 1 " \
             "ELSE 0 " \
             "END AS has_starbucks " \
             "FROM	income as i " \
             "LEFT	OUTER JOIN starbucks as s " \
             "ON	i.ZIPCODE = s.ZIPCODE " \
             "WHERE num_returns > 0 and i.ZIPCODE != '00000' " \
             "GROUP	BY i.ZIPCODE "

DIV_COLNAMES = ["1", "2", "3", "4", "5", "6", "7", "has_location"]
SQL_DIVERSITY = "SELECT d.1, d.2, d.3, d.4, d.5, d.6, d.7, " \
                "CASE WHEN s.STORE_NUMBER IS NOT NULL THEN 1 ELSE 0 END AS has_starbucks " \
                "FROM (SELECT * FROM starbucksdb.diversity_view) " \
                "as d LEFT OUTER JOIN starbucks as s ON d.ZIPCODE = s.ZIPCODE " \
                "GROUP BY d.ZIPCODE"


def run_query(connection, sql):
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

    # Must happen before equalization to maintain integrity of results. randomize/reset index
    randomized_data = data.reindex(numpy.random.permutation(data.index)).reset_index(drop=True)

    if equalize:
        locations = randomized_data["has_location"].value_counts()[1]
        non_locations = randomized_data["has_location"].value_counts()[0]
        randomized_data = equalize_binary_data(randomized_data, locations, non_locations)

    return randomized_data


def get_train_test(data, target, ratio=0.3):
    """ Splits the data into training and testing sets with an equal number of 0/1
    sample types in the testing set.

    :param data: The data to train and test on.
    :param target: The target column (prediction target)
    :param ratio: Ratio of training and test split
    :return: Separate objects for training and testing data, x matrix and y vector
    """
    train, test = model_selection.train_test_split(data, test_size=ratio)
    randomized_train = binary_equalizer(train, equalize=1)
    randomized_test = binary_equalizer(test, equalize=1)

    x_train, y_train = split_data(randomized_train, target)
    y_train = y_train.values.reshape((len(y_train.values.tolist()), 1))
    x_test, y_test = split_data(randomized_test, target)
    y_test = y_test.values.reshape((len(y_test.values.tolist()), 1))

    return x_train, y_train, x_test, y_test


def get_results(x_test, y_test, trained_model):
    """ Returns the accuracy rate of the model.

    :param x_test: Testing data to use for prediction
    :param y_test: Testing data real values
    :param trained_model: Trained classifier
    :return:
    """
    return trained_model.score(x_test, y_test)


def run_for_ratio_range(data, model):
    """ Runs the training and validation for a variety of train/test splits.

    :param data: Data for training and testing.
    :param model: A classifier to use.
    :return: Returns the ratios used for training and testing as well as the scores for each ratio.
    """
    ratio_scores = list()
    ratios = list()

    for ratio in range(5, 95):
        average_score = 0

        for iteration in range(10):
            # data preparation for machine learning
            average_score += simulation_iteration(data, ratio, model)

        ratio_scores.append(average_score / 10)
        ratios.append(ratio / 100)

    return ratios, ratio_scores


def simulation_iteration(data, ratio, model):
    """ Takes the data, a splitting ratio, and a classifier and returns the score.

    :param data: The data for training and testing
    :param ratio: The ratio for train/test split
    :param model: The classifier
    :return: The score for the split and classifier
    """
    x_train, y_train, x_test, y_test = get_train_test(data, "has_location", ratio / 100)
    trained_model = model.fit(x_train, y_train.reshape([len(y_train), ]))
    return get_results(x_test, y_test, trained_model)


def analysis(connection, query, cols):
    """ Predicts a starbucks location based on data selected by a query.

    :param connection: Database connection.
    :param query: Query to use for selecting x matrix data
    :param cols: Column names for the x matrix data
    :return:
    """
    data = pandas.DataFrame(run_query(connection, query), columns=cols)
    return run_for_ratio_range(data, RandomForestClassifier())


def plot_results(ratios, ratio_scores):
    """ Plots the results of the prediction according to train/test split ratios.

    :param ratios: Ratios used
    :param ratio_scores: Scores per ratio
    :param title: Title of the graph
    :return: NA
    """
    plt.plot(ratios[0], ratio_scores[0], "r", label="Income Data")
    plt.plot(ratios[1], ratio_scores[1], "b", label="Demographic Data")
    plt.ylim([0, 1])
    plt.xlim([0, 1])
    plt.title("Comparison of Datasets")
    plt.legend()
    plt.ylabel("Mean Accuracy")
    plt.xlabel("Ratio of Test Data")
    plt.show()


def run(connection):
    """ Standard analysis function used by the program.

    :param connection: A database connection.
    :return: NA
    """
    ratios = list()
    scores = list()

    if not connection:
        connection = dbmanager.init_connection()

    inc_ratios, inc_scores = analysis(connection, SQL_INCOME, INC_COLNAMES)
    ratios.append(inc_ratios)
    scores.append(inc_scores)

    div_ratios, div_scores = analysis(connection, SQL_DIVERSITY, DIV_COLNAMES)
    ratios.append(div_ratios)
    scores.append(div_scores)
    plot_results(ratios, scores)


if __name__ == '__main__':
    run(None)
