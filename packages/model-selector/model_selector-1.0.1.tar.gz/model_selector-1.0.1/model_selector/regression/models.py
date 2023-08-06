from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from model_selector.regression.base_regression import Base


class MultipleLinear(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.regressor = LinearRegression()

    def predict_test(self):
        self.y_pred = self.regressor.predict(self.x_test)

    def __str__(self):
        return "Multiple Linear"


class DecisionTree(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.regressor = DecisionTreeRegressor(random_state=0)

    def predict_test(self):
        self.y_pred = self.regressor.predict(self.x_test)

    def __str__(self):
        return "Decision Tree"


class Polynomial(Base):

    def __init__(self, file_path, polynomial_degree=4):
        self.file_path = file_path
        self.regressor = LinearRegression()
        self.poly_reg = PolynomialFeatures(degree=polynomial_degree)

    def train_model(self):
        x_poly = self.poly_reg.fit_transform(self.x_train)
        self.regressor.fit(x_poly, self.y_train)

    def predict_test(self):
        self.y_pred = self.regressor.predict(self.poly_reg.transform(self.x_test))

    def __str__(self):
        return "Polynomial"


class RandomForest(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.regressor = RandomForestRegressor(n_estimators=10, random_state=0)

    def predict_test(self):
        self.y_pred = self.regressor.predict(self.x_test)

    def __str__(self):
        return "Random Forest"


class SupportVector:
    pass
