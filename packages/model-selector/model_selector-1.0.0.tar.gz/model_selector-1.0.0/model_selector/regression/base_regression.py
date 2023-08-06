import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.impute import SimpleImputer


def fix_missing_data(dataset):
    inputter = SimpleImputer(missing_values=np.nan, strategy='mean')
    inputter.fit(dataset[:])
    dataset[:] = inputter.transform(dataset[:])
    return dataset


class Base:

    def __init__(self, file_path):
        self.file_path = file_path
        self.x = []
        self.y = []
        self.x_train = []
        self.x_test = []
        self.y_train = []
        self.y_test = []
        self.y_pred = []

    def import_dataset(self):
        dataset = pd.read_csv(self.file_path)
        dataset_fixed = fix_missing_data(dataset)
        self.x = dataset_fixed.iloc[:, :-1].values
        self.y = dataset_fixed.iloc[:, -1].values
        return self

    def split_dataset(self, test_size=0.2):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=test_size,
                                                                                random_state=0)
        return self

    def train_model(self):
        self.regressor.fit(self.x_train, self.y_train)

    def evaluate_metrics(self, model_name):
        metrics = {"Model Name": f"{model_name}",
                   "Mean Squared Error": mean_squared_error(self.y_test, self.y_pred),
                   "Mean Absolute Error": mean_absolute_error(self.y_test, self.y_pred),
                   "R2 Score": round(r2_score(self.y_test, self.y_pred), 4),
                   }
        return metrics
