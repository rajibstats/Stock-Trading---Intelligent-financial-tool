# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 12:34:02 2018

@author: datacore
"""

# plot feature importance manually
from numpy import loadtxt
from xgboost import XGBClassifier
from matplotlib import pyplot
# load data
dataset = loadtxt('stockdata.csv', delimiter=",")
print(dataset)
# split data into X and y
X = dataset[:,0:89]
y = dataset[:,90]
# fit model no training data
model = XGBClassifier()
model.fit(X, y)
# feature importance
print(model.feature_importances_)
# plot
pyplot.bar(range(len(model.feature_importances_)), model.feature_importances_)
pyplot.show()