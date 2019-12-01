# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:47:21 2019

@author: datacore
"""
from azureml import Workspace
ws = Workspace(
    workspace_id='f50627ea613f47f4a4483609841ee3d9',
    authorization_token='snpj9iPtGLowpzpTjV2OzL6/oLX2FGnDkvwDQk0Xg5ckw9RO3ceC47hDyxbVYjx6s7/BRheZxY8JfCePrFsjQQ==',
    endpoint='https://studioapi.azureml.net'
)
experiment = ws.experiments['f50627ea613f47f4a4483609841ee3d9.f-id.86c2cd27450c446496db569e74df3612']
ds = experiment.get_intermediate_dataset(
    node_id='5cb437bd-b615-444a-9eb7-5e7f51c22cec-852969',
    port_name='Results dataset',
    data_type_id='GenericCSV'
)
frame = ds.to_dataframe()


