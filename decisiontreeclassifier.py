# -*- coding: utf-8 -*-
"""DecisionTreeClassifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l9gkXf_ZIZ_T2-YlStcRqA6-acbOm9Lp
"""

from google.colab import drive
drive.mount('/content/gdrive')

import numpy as np
import pandas as pd
traindata = pd.read_csv('/content/gdrive/My Drive/ai_colab/train.txt', header=None, sep=" ")
testdata = pd.read_csv('/content/gdrive/My Drive/ai_colab/test.txt', header=None, sep=" ")

def extract_qid(qid_str):
    return qid_str[4:]

def extract_val(feat):
    return feat.split(':')[1]

def df_transform(df):
    df[1] = df[1].apply(extract_qid)
    df[df.columns[2:-1]] = df[df.columns[2:-1]].applymap(extract_val)
    df = df.drop(138, axis=1)
    return df

train_df = df_transform(traindata)
train_df.head()

test_df = df_transform(testdata)
test_df.head()

X_test = test_df[test_df.columns[2:]]
y_test = test_df[0]

import sklearn
from sklearn.tree import DecisionTreeClassifier
X = train_df[train_df.columns[2:]]
y = train_df[0]

reg = DecisionTreeClassifier().fit(X, y)

preds = reg.predict(X_test)

preds_df = pd.DataFrame({'qid': test_df[1], 'truth' :test_df[0], 'predicted' : preds })
preds_df.sort_values(by = "predicted", ascending=False).head()

truth_by_pred = preds_df.sort_values(by = "predicted").truth.tolist()
truth_by_pred

import math
def dcg(relevances, p):
    """Discounted cumulative gain at rank (DCG)"""
    relevances = np.asarray(relevances)[:p]
    n_relevances = len(relevances)
    if n_relevances == 0:
        return 0.

    discounts = np.log2(np.arange(n_relevances) + 2)
    return np.sum(relevances / discounts)
 
 
def ndcg(relevances, p):
    """Normalized discounted cumulative gain (NDGC)"""
    best_dcg = dcg(sorted(relevances, reverse=True), p)
    if best_dcg == 0:
        return 0.

    return dcg(relevances, p) / best_dcg

dcg(truth_by_pred, 1)



ndcg(truth_by_pred, 1)