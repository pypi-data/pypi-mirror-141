from model_selector.classification.base_classification import Base
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


class LogisticReg(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.classifier = LogisticRegression(random_state=0)

    def __str__(self):
        return "Logistic Regression"


class DecisionTree(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)

    def __str__(self):
        return "Decision Tree"


class KNearestNeighbors(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)

    def __str__(self):
        return "K-Nearest Neighbors"


class KernelSVM(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.classifier = SVC(kernel='rbf', random_state=0)

    def __str__(self):
        return "Kernel SVM"


class NaiveBayes(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.classifier = GaussianNB()

    def __str__(self):
        return "Naive Bayes"


class RandomForest(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)

    def __str__(self):
        return "Random Forest"


class SupportVectorMachine(Base):

    def __init__(self, file_path):
        self.file_path = file_path
        self.classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
        self.classifier = SVC(kernel='linear', random_state=0)

    def __str__(self):
        return "Support Vector Machine"
