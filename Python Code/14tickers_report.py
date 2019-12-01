# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 20:18:04 2019

@author: datacore
"""

# import the necessary packages

import os, os.path

#import csv
import pandas as pd
import numpy as np


import glob
import xlwt
import csv

root_folder = "D:\\Stock_Prediction\\Non_Owner\\Report Analysis"


Finaloutput = root_folder+"/FinalOutput"
if not os.path.exists(Finaloutput):
    os.makedirs(Finaloutput) 


#Read both the sheets from the excel sheet
#Rootfolder = "D:/stock"

##############################################################################

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:51:21 2019

@author: datacore
"""
######################################## Sector - 3 #####################################
from azureml import Workspace
ws = Workspace(
    workspace_id='f50627ea613f47f4a4483609841ee3d9',
    authorization_token='snpj9iPtGLowpzpTjV2OzL6/oLX2FGnDkvwDQk0Xg5ckw9RO3ceC47hDyxbVYjx6s7/BRheZxY8JfCePrFsjQQ==',
    endpoint='https://studioapi.azureml.net'
)
experiment = ws.experiments['f50627ea613f47f4a4483609841ee3d9.f-id.1f5d1ef9da8945199655064a96d51090']
ds = experiment.get_intermediate_dataset(
    node_id='79e355a2-aeb2-4aa3-b067-14ba444d25bb-995',
    port_name='Results dataset',
    data_type_id='GenericCSV'
)
frame = ds.to_dataframe()

df1 = frame.rename(columns={'Scored Probabilities': 'ScoredProbabilities', 'Scored Labels': 'ScoredLabels'})
'''
data1 = df1[(df1['ClassInd'] == 5) & (df1['ScoredLabels'] == 4)]



# =============================================================================

data1.loc[(data1.ScoredProbabilities>=0.10), 'ScoredLabels'] = 5
data1.loc[(data1.ScoredProbabilities<0.10), 'ScoredLabels'] = 4

test = df1[~((df1['ClassInd'] == 5) & (df1['ScoredLabels'] == 4))]
frames = [test, data1]
result = pd.concat(frames)

#result = pd.read_csv('D:\\Stock_Prediction\\Non_Owner\\2018Q_Final_NonOwner_Sectorwise_Report\\result before report\\2018Q2\\Non-Owner_Prediction_Sec_10.csv')

group1 = result.ScoredLabels.value_counts()
print(group1)
'''

df2 = pd.read_csv(root_folder+"\\Master Sheet New.csv")

stk_list = [241,2869,564, 1062, 1609, 3622, 49316,2897,1526,2344,4917,3307,116835,117164]

data1 = df1[df1['stock_id'].isin(stk_list)]
'''
data1['Match'] = ''


for i in range(0, len(data1.index)):
if (data1.ClassInd.values[i]==4 and data1.ScoredLabels.values[i]==4):
data1.Match.values[i] = 'TP'
elif (data1.ClassInd.values[i]==4 and data1.ScoredLabels.values[i]==5) :
data1.Match.values[i] = 'FP'
elif (data1.ClassInd.values[i]==5 and data1.ScoredLabels.values[i]==4):
data1.Match.values[i] = 'FN'
else:
data1.Match.values[i] = 'TN'

data1 = data1[data1['Match'] !='TN']

'''

header_list = list(data1.columns)

data1 = data1.drop(['Cap_Size','ActivePassive','fund_type','Investor Style','AUM','Turnover','Region','ScoredProbabilities'], axis=1)
data1.ClassInd.replace((4, 5), ("Buy", "NA"), inplace=True)
data1.ScoredLabels.replace((4, 5), ("Buy", "NA"), inplace=True)
#data1.ClassInd.replace(("Increasing", "Decreasing"), ("Buy", "NA"), inplace=True)
#data1.ScoredLabels.replace(("Increasing", "Decreasing"), ("Buy", "NA"), inplace=True)

results = pd.merge(data1,

df2[['fund_id', 'fund_house_name']],

on='fund_id')

results = pd.merge(results,

df2[['stock_id', 'ticker']],

on='stock_id')


header_list = list(results.columns)

results = results[['stock_id','ticker','fund_id','fund_house_name','ClassInd','ScoredLabels']]

results.sort_values(by=['stock_id','fund_id',])

group2 = results.ScoredLabels.value_counts()
print(group2)

#finalpath=os.path.join(Finaloutput,"RLH.csv")
#finalpath=os.path.join(Finaloutput,"EARN+CASH+VRTX+TRTX+HLI.csv")
#finalpath=os.path.join(Finaloutput,"GTS.csv")
#finalpath=os.path.join(Finaloutput,"TBI+ADT.csv")
#finalpath=os.path.join(Finaloutput,"APTS+REXR.csv")
finalpath=os.path.join(Finaloutput,"GTS.csv")

results.to_csv(finalpath, sep=',' , index=False)