import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn_genetic import GAFeatureSelectionCV
from sklearn_genetic import GASearchCV
from sklearn_genetic.space import Categorical, Integer, Continuous
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn_genetic.mlflow_log import MLflowConfig
import numpy as np
from sklearn.datasets import make_classification


X, y = make_classification(n_samples=200, n_features=1000, n_informative=50, n_redundant=20)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

clf = DecisionTreeClassifier()
cv = StratifiedKFold(n_splits=3, shuffle=True)

evolved_estimator = GAFeatureSelectionCV(
    estimator=clf,
    cv=cv,
    scoring="accuracy",
    n_jobs=-1,
    verbose=True,
    keep_top_k=2,
    elitism=True,
    max_features=300,
    generations=500,
    population_size=300
)

evolved_estimator.fit(X, y)
print(sum(evolved_estimator.best_features_))
print(evolved_estimator.best_features_)
