import pandas as pd
from model_evaluator.regression.models import MultipleLinear, Polynomial, RandomForest, DecisionTree
import errno
import os


def perform_regression(regression, test_size):
    regression.import_dataset().split_dataset(test_size=test_size).train_model()
    regression.predict_test()
    metrics = regression.evaluate_metrics(regression.__str__())
    return metrics


def evaluate_regression(filename, test_size=0.2, polynomial_degree=4):
    file_exists = os.path.exists(filename)
    if file_exists:
        multiple_linear = MultipleLinear(filename)
        polynomial = Polynomial(filename, polynomial_degree=polynomial_degree)
        random_forest = RandomForest(filename)
        decision_tree = DecisionTree(filename)

        result = [perform_regression(multiple_linear, test_size=test_size),
                  perform_regression(polynomial, test_size=test_size),
                  perform_regression(random_forest, test_size=test_size),
                  perform_regression(decision_tree, test_size=test_size)]

        df = pd.DataFrame(result)
        return df
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), filename)
