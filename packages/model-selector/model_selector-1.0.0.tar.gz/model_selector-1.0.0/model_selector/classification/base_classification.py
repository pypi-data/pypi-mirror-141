import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler


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

    def feature_scale(self):
        sc = StandardScaler()
        self.x_train = sc.fit_transform(self.x_train)
        self.x_test = sc.transform(self.x_test)
        return self

    def train_model(self):
        self.classifier.fit(self.x_train, self.y_train)

    def confusion_matrix(self, model_name):
        self.y_pred = self.classifier.predict(self.x_test)
        cm = confusion_matrix(self.y_test, self.y_pred)
        # print(cm)
        metrics = {"Model Name": f"{model_name}",
                   # "Precision Score": precision_score(self.y_test, self.y_pred, average=None, zero_division=1),
                   # "Recall Score": recall_score(self.y_test, self.y_pred, average=None, zero_division=1),
                   "Accuracy Score": accuracy_score(self.y_test, self.y_pred),
                   }
        return metrics
