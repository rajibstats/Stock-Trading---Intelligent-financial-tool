# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:51:21 2019

@author: datacore
"""
########################################  Sector - 3 #####################################
from azureml import Workspace
ws = Workspace(
    workspace_id='f50627ea613f47f4a4483609841ee3d9',
    authorization_token='snpj9iPtGLowpzpTjV2OzL6/oLX2FGnDkvwDQk0Xg5ckw9RO3ceC47hDyxbVYjx6s7/BRheZxY8JfCePrFsjQQ==',
    endpoint='https://studioapi.azureml.net'
)
experiment = ws.experiments['f50627ea613f47f4a4483609841ee3d9.f-id.6fb695833d844cfdb5abe82d230b5628']
ds = experiment.get_intermediate_dataset(
    node_id='3702f2f4-45be-4a43-9411-0e20b07f6d21-493',
    port_name='Results dataset',
    data_type_id='GenericCSV'
)
dataframe_Sec3 = ds.to_dataframe()


import pandas as pd
df1 = dataframe_Sec3.rename(columns={'Scored Probabilities': 'ScoredProbabilities', 'Scored Labels': 'ScoredLabels'})
data1 = df1[(df1['ClassInd'] == 5) & (df1['ScoredLabels'] == 4)]

# =============================================================================

data1.loc[(data1.ScoredProbabilities>=0.19), 'ScoredLabels'] = 5
data1.loc[(data1.ScoredProbabilities<0.19), 'ScoredLabels'] = 4

test = df1[~((df1['ClassInd'] == 5) & (df1['ScoredLabels'] == 4))]
frames = [test, data1]
result = pd.concat(frames)


group2 = result.ScoredLabels.value_counts()
print(group2)

result.to_csv('D:\\Stock_Prediction\\Non_Owner\\2018Q3_all sector output\\Non-Owner_Prediction_2018Q3_Sec_7.csv', sep=',', encoding='utf-8', index=False)

