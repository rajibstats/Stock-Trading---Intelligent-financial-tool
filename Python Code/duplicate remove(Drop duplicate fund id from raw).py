# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 13:39:27 2018

@author: datacore
"""

import pandas as pd

 

# Read Duplicate Fund id file

Duplicate_FundID = pd.read_csv("D:\\Stock_Prediction\\2018Q3 prediction analysis report\\Remove_Funds_Duplicate.csv")
 
# Read raw data file

Qtr1_raw = pd.read_csv("D:\\sruti\\3ClassPrediction result for 8 Qtr\\Owner_2018Q4_All_output.csv")
 
# Convert duplicate Find id into a list
Duplicate_FundID_List = Duplicate_FundID['id'].tolist()
 
#Drop duplicate fund id from raw
df_removing_duplicate = Qtr1_raw.query('fund_id not in @ Duplicate_FundID_List')
 
# Check the output Qtr1_raw 
df_removing_duplicate.to_csv("D:\\sruti\\MachinePredictionResult\\Owner_2018Q4_All_output.csv", sep=',', encoding='utf-8', index=False)
