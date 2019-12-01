# The script MUST contain a function named azureml_main
# which is the entry point for this module.
import sys
sys.path.insert(0, ".\\Script Bundle")    

import os
os.environ['PATH'] = os.path.dirname(".\\Script Bundle\\DLLs\\")+ ';' + os.environ['PATH']

#final_Df.to_csv("data/final_df.csv",sep=',')
import pandas as pd
import numpy as np
from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None):
    dataframe1.ClassInd.replace((4, 5), (1, 0), inplace=True)
    # split data into train and test sets
    
    y1 = dataframe1.loc[dataframe1['QDate'] == '6/30/2018 12:00:00 AM']
    X1 = dataframe1.loc[dataframe1['QDate'] != '6/30/2018 12:00:00 AM']
    
    #drop QDate column
    X2 = X1.drop(['QDate'], axis=1)
    y2 = y1.drop(['QDate'], axis=1)
    
    # split data into X and y
    train_X = X2.iloc[:,2:88]
    train_y = X2.iloc[:,89]
    
    test_X = y2.iloc[:,2:88]
    test_y = y2.iloc[:,89]
    
    '''
    #y = fund641_nonOwner.iloc[:,91
    X = X2.iloc[:,0:89]
    Y = X2.iloc[:,90]
    
    # split data into trainmport accuracy_score
    
    
    and test sets
    seed = 7
    test_size = 0.20
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
    
    '''
    
    y11 = X1.loc[X1['QDate'] == '3/31/2018 12:00:00 AM']
    X11 = X1.loc[X1['QDate'] != '3/31/2018 12:00:00 AM']
    
    #drop QDate column
    X22 = X11.drop(['QDate'], axis=1)
    y22 = y11.drop(['QDate'], axis=1)
    
    # split data into X and y
    train_X1 = X22.iloc[:,2:88]
    train_y1 = X22.iloc[:,89]
    
    test_X1 = y22.iloc[:,2:88]
    test_y1 = y22.iloc[:,89]
    
    
    group1 = train_y1.value_counts()
    print(group1)
    
    group2 = test_y.value_counts()
    print(group2)
    # Execution logic goes here
    #print('Input pandas.DataFrame #1:\r\n\r\n{0}'.format(dataframe1))

    # If a zip file is connected to the third input port is connected,
    # it is unzipped under ".\Script Bundle". This directory is added
    # to sys.path. Therefore, if your zip file contains a Python file
    # mymodule.py you can import it using:
    # import mymodule
    # fit model no training data
    #eval_set = [(train_X1, train_y1), (test_X1, test_y1)]
    #eval_metric = ["auc","error"]
    #scale_pos_weight = 13.24
    model = XGBClassifier(scale_pos_weight=13.24)
    model.fit(train_X1,train_y1)

    print(model)
    
    # make predictions for test data
    y_pred = model.predict(test_X)
    predictions = [round(value) for value in y_pred]
    predictions_df = pd.DataFrame(predictions)
    predictions_df.rename(columns={0:'Prediction_Class'}, inplace=True)
    
    
    probability = model.predict_proba(test_X)
    print(probability)
    probability_df = pd.DataFrame(probability)
    probability_df.rename(columns={0:'Scored_Probabilities_for_Class_NA',1:'Scored_Probabilities_for_Class_Buy'}, inplace=True)
    
    
    pred_prob =pd.concat([probability_df, predictions_df], axis=1)
    
    result1 = pd.concat([y1.reset_index(drop=True), pred_prob], axis=1)
    #result1.to_csv('D:\\Stock_Prediction\\Non_Owner\\Sec3\\Non-Owner_Prediction_Sec_3.csv', sep=',', encoding='utf-8', index=False)
    
    accuracy = accuracy_score(test_y, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    
    #group3 = y_pred['0'].value_counts()
    #print(group3)
    
    from sklearn.metrics import confusion_matrix
    results = confusion_matrix(test_y, predictions)
    print(results)
    
    from sklearn.metrics import confusion_matrix
    tn, fp, fn, tp = confusion_matrix(test_y, model.predict(test_X)).ravel()
    # Error rate : 
    err_rate = (fp + fn) / (tp + tn + fn + fp)
    print("Error rate  : ", err_rate)
    # Accuracy : 
    acc_ = (tp + tn) / (tp + tn + fn + fp)
    print("Accuracy  : ", acc_)
    # Sensitivity : 
    sens_ = tp / (tp + fn)
    print("Sensitivity  : ", sens_)
    # Specificity 
    sp_ = tn / (tn + fp)
    print("Specificity  : ", sens_)
    # False positive rate (FPR)
    FPR = fp / (tn + fp)
    print("False positive rate  : ", FPR)

    # Return value must be of a sequence of pandas.DataFrame
    return result1,
