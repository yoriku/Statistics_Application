from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneOut, StratifiedKFold
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, f1_score, matthews_corrcoef
import numpy as np
import pandas as pd

def normalize(X_train, X_test):
    mu = np.mean(X_train, axis=0)
    sd = np.std(X_train, ddof=0, axis=0)
    X_train = (X_train - mu) / sd
    X_test = (X_test - mu) / sd
    return X_train, X_test


def set_model(class_weight):
    if(class_weight == 1):
        return LogisticRegression(class_weight="balanced")
    else:
        return LogisticRegression()
    
def mode_loo(X, y, class_weight):
    loo = LeaveOneOut()
    pred = []
    test = []
    
    for train_index, test_index in loo.split(X):
        
        model = set_model(class_weight)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        X_train, X_test = normalize(X_train, X_test)
        # fit model
        model.fit(X_train, y_train)
        # predict test data
        pred.append(model.predict(X_test)[0])
        test.append(y_test[0])
    return pred, test

def mode_hold(X, y, class_weight):
    SK = StratifiedKFold()
    pred = []
    test = []
    
    for train_index, test_index in SK.split(X, y):
        
        model = set_model(class_weight)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        X_train, X_test = normalize(X_train, X_test)
        # fit model
        model.fit(X_train, y_train)
        # predict test data
        pred.append(model.predict(X_test))
        test.append(y_test)
    return np.array(pred).flatten(), np.array(test).flatten()

def calc_metric(test, pred, label):
    cm = confusion_matrix(test, pred, labels=label)
    accu = accuracy_score(test, pred)
    if len(np.unique(test)) == 2:
        recall = recall_score(test, pred)
        precision = precision_score(test, pred)
        f = f1_score(test, pred)
        mcc = matthews_corrcoef(test, pred)
        header = ["Accuracy", "Recall", "Precision", "F-measure", "matthews CC"]
        index = [accu, recall, precision, f, mcc]
    else:
        micro_recall = recall_score(test, pred, average="micro")
        macro_recall = recall_score(test, pred, average="macro")
        micro_precision = precision_score(test, pred, average="micro")
        macro_precision = precision_score(test, pred, average="macro")
        micro_f = f1_score(test, pred, average="micro")
        macro_f = f1_score(test, pred, average="macro")
        header = ["Accuracy", "Micro Recall", "Macro Recall", "Micro Precision", "Macro Precision", "Micro F-measure", "Macro F-measure"]
        index = [accu, micro_recall, macro_recall, micro_precision, macro_precision, micro_f, macro_f]
    return cm, index, header

