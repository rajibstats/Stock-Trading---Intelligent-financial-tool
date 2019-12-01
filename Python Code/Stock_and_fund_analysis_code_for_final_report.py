# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 18:21:07 2018

@author: datacore
"""



# import the necessary packages

import os, os.path

#import csv
import pandas as pd
import numpy  as np

import glob
import xlwt
import csv
root_folder = "D:/sruti/newfolder"
CompanyAnalysis = root_folder+"/CompanyAnalysis"
if not os.path.exists(CompanyAnalysis):
    os.makedirs(CompanyAnalysis) 
    

Finaloutput = root_folder+"/FinalOutput"
if not os.path.exists(Finaloutput):
    os.makedirs(Finaloutput) 
    

#Read both the sheets from the excel sheet
Rootfolder = "D:/sruti/newfolder"
xls = pd.ExcelFile(Rootfolder+"\\Owner_2016Q4_All_output.xlsx")
df1 = pd.read_excel(xls, 'Owner_2016Q4_All_output')
df2 = pd.read_excel(xls, 'MasterSheet')



df1 = df1.rename(columns={'Investor Style': 'Investor_Style', 'Scored Labels': 'ScoredLabels'})

df1 = df1.sort_values(by=[ 'fund_id'],ascending=[True])
#Methods to get the value of different columns in the master sheet with respect to value
def FundName(FundId):
    for i in range(0, len(df2['Fund_ID'].index)):
       Fundname = df2[df2['Fund_ID']==FundId]['fund_house_name'].iloc[0]
       return(Fundname)
     

def FundType(FundTypeID):
   for i in range(0, len(df2['FundTypeID'].index)):
       FundType = df2[df2['FundTypeID']==FundTypeID]['FundType'].iloc[0]
       return(FundType)


def InvestorDescription(InvestorID):
   for i in range(0, len(df2['InvestorID'].index)):
       InvestorDescription = df2[df2['InvestorID']==InvestorID]['InvestorDescription'].iloc[0]
       return(InvestorDescription)

def AUM(AUMID):
   for i in range(0, len(df2['AUMID'].index)):
       AUM = df2[df2['AUMID']==AUMID]['AUM'].iloc[0]
       return(AUM)

def Turnover(TurnoverID):
   for i in range(0, len(df2['TurnoverID'].index)):
       Turnover = df2[df2['TurnoverID']==TurnoverID]['Turnover'].iloc[0]
       return(Turnover)

def Region(RegionID):
   for i in range(0, len(df2['RegionID'].index)):
       Region = df2[df2['RegionID']==RegionID]['Region'].iloc[0]
       return(Region)
       
def Ticker(id):
   for i in range(0, len(df2['id'].index)):
       Ticker = df2[df2['id']==id]['ticker'].iloc[0]
       return(Ticker)     
def Maxof4(i):
       maxval = df1[["Scored Probabilities for Class \"Decreasing\"", "Scored Probabilities for Class \"Hold\"","Scored Probabilities for Class \"Increasing\"","Scored Probabilities for Class \"Remove\""]].max(axis=1).iloc[i]
       return(maxval)
def conflevel(maxval):
    if(maxval>=0 and maxval<0.5):
        confval = "Low"
    elif(maxval>=0.5 and maxval<0.7):
        confval = "Medium"
    elif(maxval>=0.7):
        confval = "High"
    return (confval)



index=np.arange(len(df1.index))   
#creates a new dataframe
Column_Names = ['fund_id','Fundname','fund_type','Type','Investor_Style','Style','AUMID','AUM','TurnoverID','Turnover','RegionID','Region','ActionTaken','ScoredLabels','Result','Resultfalse','Truepositive','Increment','Decrement','Hold','Remove','Incrementtotal','Decrementtotal','Holdtotal','Removetotal','Incrementfalse','Decrementfalse','Holdfalse','Removefalse','Incrementpredict','Decrementpredict','HoldPredict','Removepredict','Incrementfalsenegative','Decrementfalsenegative','Holdfalsenegative','Removefalsenegative','MaxConfidence','Confidencelevel']
df3 = pd.DataFrame(str(np.nan),index,columns= Column_Names)
df3['fund_id']=df1['fund_id']
df3['fund_type'] = df1['fund_type']
df3['Investor_Style']= df1['Investor_Style']
df3['AUMID'] = df1['AUM']
df3['TurnoverID'] = df1['Turnover']
df3['RegionID'] = df1['Region']
df3['ActionTaken'] = df1['ActionTaken']
df3['ScoredLabels'] = df1['ScoredLabels']

#df3['Fundname'] = df3['Fundname'].astype(str)
for i in range(0, len(df1.index)):    
    df3.Fundname.values[i]= FundName(df1.fund_id.values[i])
    # df3.Fundname.values[i]= ("A".astype(float))    
    df3.Type.values[i] = FundType(df1.fund_type.values[i])    
    df3.Style.values[i] = InvestorDescription(df1.Investor_Style.values[i])
    df3.AUM.values[i] = AUM(df1.AUM.values[i])    
    df3.Turnover.values[i] = Turnover(df1.Turnover.values[i])    
    df3.Region.values[i] = Region(df1.Region.values[i])   
    df3.MaxConfidence.values[i] = Maxof4(i)
    df3.Confidencelevel.values[i]= conflevel(df3.MaxConfidence.values[i])
    
'''
Fund Analysis_1Q2018_ML_ALL_ML_Studio
1. Step 1  - Divide the data frame to 4 different file(Increment, Decrement, Hold, Remove)
2. Step 2 - Add condition where Action taken = Scored labels (Truepositive)
3. Step 3 - Add condition where Action taken !=Scored labels(False positive)
4. Step 4 - Original will be the total action taken value
5. Step5 - Prediction will be the total scored labels value
6. Step 6 - If Scored labels != Action Taken (False Negative)


'''
for i in range(0, len(df3.index)): 
    if df3.ActionTaken.values[i] =='Increasing':
           df3.Incrementtotal.values[i] = 1
    elif df3.ActionTaken.values[i] =='Decreasing':
           df3.Decrementtotal.values[i] = 1
    elif df3.ActionTaken.values[i] =='Hold':
           df3.Holdtotal.values[i] = 1
    elif df3.ActionTaken.values[i] =='Remove':
           df3.Removetotal.values[i] = 1    
           
    if df3.ScoredLabels.values[i] =='Increasing':
           df3.Incrementpredict.values[i] = 1
    elif df3.ScoredLabels.values[i] =='Decreasing':
           df3.Decrementpredict.values[i] = 1
    elif df3.ScoredLabels.values[i] =='Hold':
           df3.HoldPredict.values[i] = 1
    elif df3.ScoredLabels.values[i] =='Remove':
           df3.Removepredict.values[i] = 1    
           
           
    if  df3.ActionTaken.values[i] == df3.ScoredLabels.values[i]:
        df3.Result.values[i] = 1
        if df3.ActionTaken.values[i] =='Increasing':
           df3.Increment.values[i] = 1
        elif df3.ActionTaken.values[i] =='Decreasing':
           df3.Decrement.values[i] = 1
        elif df3.ActionTaken.values[i] =='Hold':
           df3.Hold.values[i] = 1
        elif df3.ActionTaken.values[i] =='Remove':
           df3.Remove.values[i] = 1
        
    else:
        df3.Result.values[i] = 0
        if df3.ActionTaken.values[i] =='Increasing':
           df3.Incrementfalse.values[i] = 1
        elif df3.ActionTaken.values[i] =='Decreasing':
           df3.Decrementfalse.values[i] = 1
        elif df3.ActionTaken.values[i] =='Hold':
           df3.Holdfalse.values[i] = 1
        elif df3.ActionTaken.values[i] =='Remove':
           df3.Removefalse.values[i] = 1
           
    if  df3.ScoredLabels.values[i] == df3.ActionTaken.values[i]:
        df3.Resultfalse.values[i] = 1
    else:
        df3.Resultfalse.values[i] = 0
        if df3.ScoredLabels.values[i] =='Increasing':
           df3.Incrementfalsenegative.values[i] = 1
        elif df3.ScoredLabels.values[i] =='Decreasing':
           df3.Decrementfalsenegative.values[i] = 1
        elif df3.ScoredLabels.values[i] =='Hold':
           df3.Holdfalsenegative.values[i] = 1
        elif df3.ScoredLabels.values[i] =='Remove':
           df3.Removefalsenegative.values[i] = 1
#For making different worksheets as per the requirment
           
df3Increment =  df3.groupby(['fund_id','Increment']).size().reset_index(name='ResultIncre')
df3Decrement =  df3.groupby(['fund_id','Decrement']).size().reset_index(name='ResultDecre')
df3Hold =  df3.groupby(['fund_id','Hold']).size().reset_index(name='ResultHold')
df3Remove =  df3.groupby(['fund_id','Remove']).size().reset_index(name='ResultRemove')

df3Incrementtotal =  df3.groupby(['fund_id','Incrementtotal']).size().reset_index(name='ResultIncre')
df3Decrementtotal =  df3.groupby(['fund_id','Decrementtotal']).size().reset_index(name='ResultDecre')
df3Holdtotal =  df3.groupby(['fund_id','Holdtotal']).size().reset_index(name='ResultHold')
df3Removetotal =  df3.groupby(['fund_id','Removetotal']).size().reset_index(name='ResultRemove')


df3Incrementpredict =  df3.groupby(['fund_id','Incrementpredict']).size().reset_index(name='ResultIncre')
df3Decrementpredict =  df3.groupby(['fund_id','Decrementpredict']).size().reset_index(name='ResultDecre')
df3HoldPredict =  df3.groupby(['fund_id','HoldPredict']).size().reset_index(name='ResultHold')
df3Removepredict =  df3.groupby(['fund_id','Removepredict']).size().reset_index(name='ResultRemove')


df3Incrementfalse =  df3.groupby(['fund_id','Incrementfalse']).size().reset_index(name='ResultIncre')
df3Decrementfalse =  df3.groupby(['fund_id','Decrementfalse']).size().reset_index(name='ResultDecre')
df3Holdfalse =  df3.groupby(['fund_id','Holdfalse']).size().reset_index(name='ResultHold')
df3Removefalse =  df3.groupby(['fund_id','Removefalse']).size().reset_index(name='ResultRemove')

df3Incrementfalsenegative =  df3.groupby(['fund_id','Incrementfalsenegative']).size().reset_index(name='ResultIncre')
df3Decrementfalsenegative =  df3.groupby(['fund_id','Decrementfalsenegative']).size().reset_index(name='ResultDecre')
df3Holdfalsenegative =  df3.groupby(['fund_id','Holdfalsenegative']).size().reset_index(name='ResultHold')
df3Removefalsenegative =  df3.groupby(['fund_id','Removefalsenegative']).size().reset_index(name='ResultRemove')

df3result = df3.groupby(['fund_id','Result']).size().reset_index(name='Result1')
df3results = df3.groupby(['fund_id','Result']).size().reset_index(name='Result1')
df3result1 = df3.groupby(['fund_id','Resultfalse']).size().reset_index(name='Result2')

df3result['Truepositive'] = str(np.nan)
df3results['Falsepositive'] = str(np.nan)

for i in range(0, len(df3result.index)): 
    if(df3result.Result.values[i] == 1):
        df3result.Truepositive.values[i] = df3result.Result1.values[i]
                
for i in range(0, len(df3results.index)): 
    if(df3results.Result.values[i] == 0):
        df3results.Falsepositive.values[i] = df3results.Result1.values[i]
           

df3result1['Falsenegative'] = str(np.nan)       

for i in range(0, len(df3result1.index)): 
    if(df3result1.Resultfalse.values[i] == 0):
        df3result1.Falsenegative.values[i] = df3result1.Result2.values[i]
                
df3result = df3result.sort_values(['Result'], ascending=[False])
df3result = df3result.drop_duplicates(['fund_id'],keep='first')
df3result = df3result.drop(['Result','Result1'], axis=1)

df3results = df3results.sort_values(['Result'], ascending=[True])
df3results = df3results.drop_duplicates(['fund_id'],keep='first')
df3results = df3results.drop(['Result','Result1'], axis=1)
df3result = df3result.replace('nan', 0)
df3results = df3results.replace('nan', 0)

#
##-------------------------------------------------------------------------------
#
#data_dict = []
#CSV_dict =[]
#j=0
#for i in range(0, len(df3result.index)):
#    j=j+1
#    if j == 1:
#       v_fund_id       = df3result.fund_id.values[i] 
#       v_true_positive = df3result.Truepositive.values[i] 
#       continue
#    if j== 2:
#       v_false_positive = df3result.Falsepositive.values[i]
#       
#       df3result_dict = []
#       df3result_dict.append(v_fund_id)
#       df3result_dict.append(v_true_positive)
#       df3result_dict.append(v_false_positive)
#       CSV_dict.append(df3result_dict)
#       j=0
#       continue
#col_names = ["fund_id","Truepositive", 'Falsepositive']
#
##Creating data frame with the specified columns
#TempDf = pd.DataFrame.from_records(CSV_dict, columns=col_names)
#columns = ['Truepositive','Falsepositive']
#df3result.drop(columns, inplace=True, axis=1)
#Temp1df = df3result.drop_duplicates(subset=['fund_id'], keep='first')
#
#df3resultfinal = pd.merge(Temp1df, TempDf, on="fund_id")
#
##-------------------------------------------------------------------------------
df3result1 = df3result1.sort_values(['fund_id','Resultfalse'], ascending=[True,True])
df3result1 = df3result1.drop_duplicates(['fund_id'],keep='first')
df3result1 = df3result1.drop(['Resultfalse','Result2'], axis=1)
df3result1 = df3result1.replace('nan', 0)
#---------------------------------------------------------------------------
df3Increment['Truepositive'] = str(np.nan)

for i in range(0, len(df3Increment.index)): 
    if(df3Increment.Increment.values[i] == 1):
        df3Increment.Truepositive.values[i] = df3Increment.ResultIncre.values[i]
        
df3Increment = df3Increment.drop_duplicates(['fund_id',],keep='first')

df3Increment = df3Increment.drop(['Increment','ResultIncre'], axis=1)

#-----------------------------------------------------------------------------

df3Decrement['Truepositive'] = str(np.nan)

for i in range(0, len(df3Decrement.index)): 
    if(df3Decrement.Decrement.values[i] == 1):
        df3Decrement.Truepositive.values[i] = df3Decrement.ResultDecre.values[i]
        
df3Decrement = df3Decrement.drop_duplicates(['fund_id',],keep='first')

df3Decrement = df3Decrement.drop(['Decrement','ResultDecre'], axis=1)
#----------------------------------------)---------------------------

df3Hold['Truepositive'] = str(np.nan)

for i in range(0, len(df3Hold.index)): 
    if(df3Hold.Hold.values[i] == 1):
        df3Hold.Truepositive.values[i] = df3Hold.ResultHold.values[i]
        
df3Hold = df3Hold.drop_duplicates(['fund_id',],keep='first')

df3Hold = df3Hold.drop(['Hold','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df3Remove['Truepositive'] = str(np.nan)

for i in range(0, len(df3Remove.index)): 
    if(df3Remove.Remove.values[i] == 1):
        df3Remove.Truepositive.values[i] = df3Remove.ResultRemove.values[i]
        
df3Remove = df3Remove.drop_duplicates(['fund_id',],keep='first')

df3Remove = df3Remove.drop(['Remove','ResultRemove'], axis=1)

#-------------------------------------------------------------------------

df3Incrementtotal['Originals'] = str(np.nan)

for i in range(0, len(df3Incrementtotal.index)): 
    if(df3Incrementtotal.Incrementtotal.values[i] == 1):
        df3Incrementtotal.Originals.values[i] = df3Incrementtotal.ResultIncre.values[i]
    
df3Incrementtotal = df3Incrementtotal.drop_duplicates(['fund_id',],keep='first')

df3Incrementtotal = df3Incrementtotal.drop(['Incrementtotal','ResultIncre'], axis=1)


#-------------------------------------------------------------------------

df3Decrementtotal['Originals'] = str(np.nan)

for i in range(0, len(df3Decrementtotal.index)): 
    if(df3Decrementtotal.Decrementtotal.values[i] == 1):
        df3Decrementtotal.Originals.values[i] = df3Decrementtotal.ResultDecre.values[i]
        
df3Decrementtotal = df3Decrementtotal.drop_duplicates(['fund_id',],keep='first')

df3Decrementtotal = df3Decrementtotal.drop(['Decrementtotal','ResultDecre'], axis=1)

#-------------------------------------------------------------------------

df3Holdtotal['Originals'] = str(np.nan)

for i in range(0, len(df3Holdtotal.index)): 
    if(df3Holdtotal.Holdtotal.values[i] == 1):
        df3Holdtotal.Originals.values[i] = df3Holdtotal.ResultHold.values[i]
        
df3Holdtotal = df3Holdtotal.drop_duplicates(['fund_id',],keep='first')

df3Holdtotal = df3Holdtotal.drop(['Holdtotal','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df3Removetotal['Originals'] = str(np.nan)

for i in range(0, len(df3Removetotal.index)): 
    if(df3Removetotal.Removetotal.values[i] == 1):
        df3Removetotal.Originals.values[i] = df3Removetotal.ResultRemove.values[i]
        
df3Removetotal = df3Removetotal.drop_duplicates(['fund_id',],keep='first')

df3Removetotal = df3Removetotal.drop(['Removetotal','ResultRemove'], axis=1)

#-------------------------------------------------------------------------

df3Incrementpredict['Prediction'] = str(np.nan)

for i in range(0, len(df3Incrementpredict.index)): 
    if(df3Incrementpredict.Incrementpredict.values[i] == 1):
        df3Incrementpredict.Prediction.values[i] = df3Incrementpredict.ResultIncre.values[i]
        
df3Incrementpredict = df3Incrementpredict.drop_duplicates(['fund_id',],keep='first')

df3Incrementpredict = df3Incrementpredict.drop(['Incrementpredict','ResultIncre'], axis=1)


#-------------------------------------------------------------------------

df3Decrementpredict['Prediction'] = str(np.nan)

for i in range(0, len(df3Decrementpredict.index)): 
    if(df3Decrementpredict.Decrementpredict.values[i] == 1):
        df3Decrementpredict.Prediction.values[i] = df3Decrementpredict.ResultDecre.values[i]
        
df3Decrementpredict = df3Decrementpredict.drop_duplicates(['fund_id',],keep='first')

df3Decrementpredict = df3Decrementpredict.drop(['Decrementpredict','ResultDecre'], axis=1)

#-------------------------------------------------------------------------

df3HoldPredict['Prediction'] = str(np.nan)

for i in range(0, len(df3HoldPredict.index)): 
    if(df3HoldPredict.HoldPredict.values[i] == 1):
        df3HoldPredict.Prediction.values[i] = df3HoldPredict.ResultHold.values[i]
        
df3HoldPredict = df3HoldPredict.drop_duplicates(['fund_id',],keep='first')

df3HoldPredict = df3HoldPredict.drop(['HoldPredict','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df3Removepredict['Prediction'] = str(np.nan)

for i in range(0, len(df3Removepredict.index)): 
    if(df3Removepredict.Removepredict.values[i] == 1):
        df3Removepredict.Prediction.values[i] = df3Removepredict.ResultRemove.values[i]
        
df3Removepredict = df3Removepredict.drop_duplicates(['fund_id',],keep='first')

df3Removepredict = df3Removepredict.drop(['Removepredict','ResultRemove'], axis=1)


#-------------------------------------------------------------------------

df3Incrementfalse['FalsePositive'] = str(np.nan)

for i in range(0, len(df3Incrementfalse.index)): 
    if(df3Incrementfalse.Incrementfalse.values[i] == 1):
        df3Incrementfalse.FalsePositive.values[i] = df3Incrementfalse.ResultIncre.values[i]
        
df3Incrementfalse = df3Incrementfalse.drop_duplicates(['fund_id',],keep='first')

df3Incrementfalse = df3Incrementfalse.drop(['Incrementfalse','ResultIncre'], axis=1)

#-----------------------------------------------------------------------------

df3Decrementfalse['FalsePositive'] = str(np.nan)

for i in range(0, len(df3Decrementfalse.index)): 
    if(df3Decrementfalse.Decrementfalse.values[i] == 1):
        df3Decrementfalse.FalsePositive.values[i] = df3Decrementfalse.ResultDecre.values[i]
        
df3Decrementfalse = df3Decrementfalse.drop_duplicates(['fund_id',],keep='first')

df3Decrementfalse = df3Decrementfalse.drop(['Decrementfalse','ResultDecre'], axis=1)

#-------------------------------------------------------------------
df3Holdfalse['FalsePositive'] = str(np.nan)

for i in range(0, len(df3Holdfalse.index)): 
    if(df3Holdfalse.Holdfalse.values[i] == 1):
        df3Holdfalse.FalsePositive.values[i] = df3Holdfalse.ResultHold.values[i]
        
df3Holdfalse = df3Holdfalse.drop_duplicates(['fund_id',],keep='first')

df3Holdfalse = df3Holdfalse.drop(['Holdfalse','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df3Removefalse['FalsePositive'] = str(np.nan)

for i in range(0, len(df3Removefalse.index)): 
    if(df3Removefalse.Removefalse.values[i] == 1):
        df3Removefalse.FalsePositive.values[i] = df3Removefalse.ResultRemove.values[i]
        
df3Removefalse = df3Removefalse.drop_duplicates(['fund_id',],keep='first')

df3Removefalse = df3Removefalse.drop(['Removefalse','ResultRemove'], axis=1)
#-------------------------------------------------------------------------

df3Incrementfalsenegative['FalseNegative'] = str(np.nan)

for i in range(0, len(df3Incrementfalsenegative.index)): 
    if(df3Incrementfalsenegative.Incrementfalsenegative.values[i] == 1):
        df3Incrementfalsenegative.FalseNegative.values[i] = df3Incrementfalsenegative.ResultIncre.values[i]
        
df3Incrementfalsenegative = df3Incrementfalsenegative.drop_duplicates(['fund_id',],keep='first')

df3Incrementfalsenegative = df3Incrementfalsenegative.drop(['Incrementfalsenegative','ResultIncre'], axis=1)

#-----------------------------------------------------------------------------

df3Decrementfalsenegative['FalseNegative'] = str(np.nan)

for i in range(0, len(df3Decrementfalsenegative.index)): 
    if(df3Decrementfalsenegative.Decrementfalsenegative.values[i] == 1):
        df3Decrementfalsenegative.FalseNegative.values[i] = df3Decrementfalsenegative.ResultDecre.values[i]
        
df3Decrementfalsenegative = df3Decrementfalsenegative.drop_duplicates(['fund_id',],keep='first')

df3Decrementfalsenegative = df3Decrementfalsenegative.drop(['Decrementfalsenegative','ResultDecre'], axis=1)

#-------------------------------------------------------------------
df3Holdfalsenegative['FalseNegative'] = str(np.nan)

for i in range(0, len(df3Holdfalsenegative.index)): 
    if(df3Holdfalsenegative.Holdfalsenegative.values[i] == 1):
        df3Holdfalsenegative.FalseNegative.values[i] = df3Holdfalsenegative.ResultHold.values[i]
        
df3Holdfalsenegative = df3Holdfalsenegative.drop_duplicates(['fund_id',],keep='first')

df3Holdfalsenegative = df3Holdfalsenegative.drop(['Holdfalsenegative','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df3Removefalsenegative['FalseNegative'] = str(np.nan)

for i in range(0, len(df3Removefalsenegative.index)): 
    if(df3Removefalsenegative.Removefalsenegative.values[i] == 1):
        df3Removefalsenegative.FalseNegative.values[i] = df3Removefalsenegative.ResultRemove.values[i]
        
df3Removefalsenegative = df3Removefalsenegative.drop_duplicates(['fund_id',],keep='first')

df3Removefalsenegative = df3Removefalsenegative.drop(['Removefalsenegative','ResultRemove'], axis=1)

#-------------------------------------------------------------------------
df3Increfinal = []


#df3Increfinal = [df3Increment,df3Incrementfalse,df3Incrementpredict,df3Incrementtotal]
df3Increfinal = pd.merge(df3Increment, df3Incrementfalse, on=['fund_id'])
df3Increfinal = pd.merge(df3Increfinal, df3Incrementpredict, on=['fund_id'])
df3Increfinal = pd.merge(df3Increfinal, df3Incrementtotal, on=['fund_id'])
df3Increfinal = pd.merge(df3Increfinal, df3Incrementfalsenegative, on=['fund_id'])


#---------------------------------------------------------------------------

df3Decrefinal = []

#df3Decrefinal = [df3Decrement,df3Decrementfalse,df3Decrementpredict,df3Decrementtotal]
df3Decrefinal = pd.merge(df3Decrement, df3Decrementfalse, on=['fund_id'])
df3Decrefinal = pd.merge(df3Decrefinal, df3Decrementpredict, on=['fund_id'])
df3Decrefinal = pd.merge(df3Decrefinal, df3Decrementtotal, on=['fund_id'])
df3Decrefinal = pd.merge(df3Decrefinal, df3Decrementfalsenegative, on=['fund_id'])
#-----------------------------------------------------------------------------

df3Holdfinal = []

#df3Holdfinal = [df3Hold,df3Holdfalse,df3HoldPredict,df3Holdtotal]
df3Holdfinal = pd.merge(df3Hold, df3Holdfalse, on=['fund_id'])
df3Holdfinal = pd.merge(df3Holdfinal, df3HoldPredict, on=['fund_id'])
df3Holdfinal = pd.merge(df3Holdfinal, df3Holdtotal, on=['fund_id'])
df3Holdfinal = pd.merge(df3Holdfinal, df3Holdfalsenegative, on=['fund_id'])
#-----------------------------------------------------------------------------
df3Removefinal = []

#df3Removefinal = [df3Remove,df3Removefalse,df3RemovePredict,df3Removetotal]
df3Removefinal = pd.merge(df3Remove, df3Removefalse, on=['fund_id'])
df3Removefinal = pd.merge(df3Removefinal, df3Removepredict, on=['fund_id'])
df3Removefinal = pd.merge(df3Removefinal, df3Removetotal, on=['fund_id'])
df3Removefinal = pd.merge(df3Removefinal, df3Removefalsenegative, on=['fund_id'])

#-----------------------------------------------------------------------------

df5 = df1.groupby(['fund_id','ActionTaken']).size().reset_index(name='Originals')
df5sum = pd.Series.to_frame(df5.groupby(['fund_id'])["Originals"].apply(lambda x : x.astype(int).sum()))

df5sum['fund_id'] = df5sum.index

df7 = df1.groupby(['fund_id','ScoredLabels']).size().reset_index(name='Predictions')
df7sum = pd.Series.to_frame(df7.groupby(['fund_id'])['Predictions'].sum())
df7sum['fund_id'] = df7sum.index
df6 = df3.drop_duplicates(['fund_id',],keep='first')

df6.drop(['fund_type','Investor_Style','AUMID','TurnoverID','RegionID','ActionTaken','ScoredLabels','Result','Truepositive','Increment','Decrement','Hold','Remove','Incrementtotal','Decrementtotal','Holdtotal','Removetotal','Incrementfalse','Decrementfalse','Holdfalse','Removefalse','Incrementpredict','Decrementpredict','HoldPredict','Removepredict','Incrementfalsenegative','Decrementfalsenegative','Holdfalsenegative','Removefalsenegative'], axis=1, inplace=True)
df = pd.merge(df5sum, df7sum, on=['fund_id'])


Increment = df3Increfinal.join(df6.set_index('fund_id'), on='fund_id')


Increment['Recall']= str(np.nan)
Increment['PRECISION']= str(np.nan)
Increment['F1Score']= str(np.nan)


for i in range(0, len(Increment.index)):
    if(Increment.Truepositive.values[i]!='nan' and Increment.Prediction.values[i]!='nan'):
        Increment.PRECISION.values[i] = (int(Increment.Truepositive.values[i])/int(Increment.Prediction.values[i]))
    else:
        Increment.PRECISION.values[i] = 0

    if(Increment.Truepositive.values[i]!='nan' and Increment.Originals.values[i]!='nan'):
        Increment.Recall.values[i] = (int(Increment.Truepositive.values[i])/int(Increment.Originals.values[i]))
    else:
        Increment.Recall.values[i] = 0
    if(Increment.PRECISION.values[i]!=0 and Increment.Recall.values[i]!=0):
        Increment.F1Score.values[i] = (2*(Increment.PRECISION.values[i]*(Increment.Recall.values[i]))/((Increment.PRECISION.values[i])+(Increment.Recall.values[i])))

header_list = list(Increment.columns)
max_rows = 5

Increment1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)

Increment1.fund_id.values[0] = i+1
Increment = Increment.replace('nan', 0)


Increment[['Originals']] = Increment[['Originals']].astype(int)
Increment1.Originals.values[0] = (Increment.Originals).sum()
Increment1.Prediction.values[0] = Increment['Prediction'].sum()
Increment1.Truepositive.values[0] = Increment['Truepositive'].sum()
Increment1.FalsePositive.values[0] = Increment['FalsePositive'].sum()
Increment1.FalseNegative.values[0] = Increment['FalseNegative'].sum()
Increment1.Recall.values[0] = (Increment1.Truepositive.values[0]/Increment1.Originals.values[0])
Increment1.PRECISION.values[0] = (Increment1.Truepositive.values[0]/Increment1.Prediction.values[0])
Increment1.F1Score.values[0] = (2*(Increment1.PRECISION.values[0]*(Increment1.Recall.values[0]))/((Increment1.PRECISION.values[0])+(Increment1.Recall.values[0])))
Increment1.MaxConfidence.values[0] = np.std(Increment['MaxConfidence'])
Increment = Increment[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Increment1 = Increment1[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Increment = Increment.append(Increment1)
       
Decrement = df3Decrefinal.join(df6.set_index('fund_id'), on='fund_id')

Decrement['Recall']= str(np.nan)
Decrement['PRECISION']= str(np.nan)
Decrement['F1Score']= str(np.nan)
for i in range(0, len(Decrement.index)):
    if(Decrement.Truepositive.values[i]!='nan' and Decrement.Prediction.values[i]!='nan'):
        Decrement.PRECISION.values[i] = (int(Decrement.Truepositive.values[i])/int(Decrement.Prediction.values[i]))
    else:
        Decrement.PRECISION.values[i] = 0

    if(Decrement.Truepositive.values[i]!='nan' and Decrement.Originals.values[i]!='nan'):
        Decrement.Recall.values[i] = (int(Decrement.Truepositive.values[i])/int(Decrement.Originals.values[i]))
    else:
        Decrement.Recall.values[i] = 0
    if(Decrement.PRECISION.values[i]!=0 and Decrement.Recall.values[i]!=0):
        Decrement.F1Score.values[i] = (2*(Decrement.PRECISION.values[i]*(Decrement.Recall.values[i]))/((Decrement.PRECISION.values[i])+(Decrement.Recall.values[i])))
        
Decrement1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)

Decrement1.fund_id.values[0] = i+1
Decrement = Decrement.replace('nan', 0)


Decrement[['Originals']] = Decrement[['Originals']].astype(int)
Decrement1.Originals.values[0] = (Decrement.Originals).sum()
Decrement1.Prediction.values[0] = Decrement['Prediction'].sum()
Decrement1.Truepositive.values[0] = Decrement['Truepositive'].sum()
Decrement1.FalsePositive.values[0] = Decrement['FalsePositive'].sum()
Decrement1.FalseNegative.values[0] = Decrement['FalseNegative'].sum()
Decrement1.Recall.values[0] = (Decrement1.Truepositive.values[0]/Decrement1.Originals.values[0])
Decrement1.PRECISION.values[0] = (Decrement1.Truepositive.values[0]/Decrement1.Prediction.values[0])
Decrement1.F1Score.values[0] = (2*(Decrement1.PRECISION.values[0]*(Decrement1.Recall.values[0]))/((Decrement1.PRECISION.values[0])+(Decrement1.Recall.values[0])))
Decrement1.MaxConfidence.values[0] = np.std(Decrement['MaxConfidence'])
Decrement = Decrement[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Decrement1 = Decrement1[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Decrement = Decrement.append(Decrement1)

Hold = df3Holdfinal.join(df6.set_index('fund_id'), on='fund_id')

Hold['Recall']= str(np.nan)
Hold['PRECISION']= str(np.nan)
Hold['F1Score']= str(np.nan)
for i in range(0, len(Hold.index)):
    if(Hold.Truepositive.values[i]!='nan' and Hold.Prediction.values[i]!='nan'):
        Hold.PRECISION.values[i] = (int(Hold.Truepositive.values[i])/int(Hold.Prediction.values[i]))
    else:
        Hold.PRECISION.values[i] = 0

    if(Hold.Truepositive.values[i]!='nan' and Hold.Originals.values[i]!='nan'):
        Hold.Recall.values[i] = (int(Hold.Truepositive.values[i])/int(Hold.Originals.values[i]))
    else:
        Hold.Recall.values[i] = 0
    if(Hold.PRECISION.values[i]!=0 and Hold.Recall.values[i]!=0):
        Hold.F1Score.values[i] = (2*(Hold.PRECISION.values[i]*(Hold.Recall.values[i]))/((Hold.PRECISION.values[i])+(Hold.Recall.values[i])))
Hold1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)

Hold1.fund_id.values[0] = i+1
Hold = Hold.replace('nan', 0)


Hold[['Originals']] = Hold[['Originals']].astype(int)
Hold1.Originals.values[0] = (Hold.Originals).sum()
Hold1.Prediction.values[0] = Hold['Prediction'].sum()
Hold1.Truepositive.values[0] = Hold['Truepositive'].sum()
Hold1.FalsePositive.values[0] = Hold['FalsePositive'].sum()
Hold1.FalseNegative.values[0] = Hold['FalseNegative'].sum()
Hold1.Recall.values[0] = (Hold1.Truepositive.values[0]/Hold1.Originals.values[0])
Hold1.PRECISION.values[0] = (Hold1.Truepositive.values[0]/Hold1.Prediction.values[0])
Hold1.F1Score.values[0] = (2*(Hold1.PRECISION.values[0]*(Hold1.Recall.values[0]))/((Hold1.PRECISION.values[0])+(Hold1.Recall.values[0])))
Hold1.MaxConfidence.values[0] = np.std(Hold['MaxConfidence'])
Hold = Hold[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Hold1 = Hold1[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Hold = Hold.append(Hold1) 

Remove = df3Removefinal.join(df6.set_index('fund_id'), on='fund_id')


Remove['Recall']= str(np.nan)
Remove['PRECISION']= str(np.nan)
Remove['F1Score']= str(np.nan)
for i in range(0, len(Remove.index)):
    if(Remove.Truepositive.values[i]!='nan' and Remove.Prediction.values[i]!='nan'):
        Remove.PRECISION.values[i] = (int(Remove.Truepositive.values[i])/int(Remove.Prediction.values[i]))
    else:
        Remove.PRECISION.values[i] = 0

    if(Remove.Truepositive.values[i]!='nan' and Remove.Originals.values[i]!='nan'):
        Remove.Recall.values[i] = (int(Remove.Truepositive.values[i])/int(Remove.Originals.values[i]))
    else:
        Remove.Recall.values[i] = 0
    if(Remove.PRECISION.values[i]!=0 and Remove.Recall.values[i]!=0):
        Remove.F1Score.values[i] = (2*(Remove.PRECISION.values[i]*(Remove.Recall.values[i]))/((Remove.PRECISION.values[i])+(Remove.Recall.values[i])))
Remove1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)

Remove1.fund_id.values[0] = i+1
Remove = Remove.replace('nan', 0)


Remove[['Originals']] = Remove[['Originals']].astype(int)
Remove1.Originals.values[0] = (Remove.Originals).sum()
Remove1.Prediction.values[0] = Remove['Prediction'].sum()
Remove1.Truepositive.values[0] = Remove['Truepositive'].sum()
Remove1.FalsePositive.values[0] = Remove['FalsePositive'].sum()
Remove1.FalseNegative.values[0] = Remove['FalseNegative'].sum()
Remove1.Recall.values[0] = (Remove1.Truepositive.values[0]/Remove1.Originals.values[0])
Remove1.PRECISION.values[0] = (Remove1.Truepositive.values[0]/Remove1.Prediction.values[0])
Remove1.F1Score.values[0] = (2*(Remove1.PRECISION.values[0]*(Remove1.Recall.values[0]))/((Remove1.PRECISION.values[0])+(Remove1.Recall.values[0])))
Remove1.MaxConfidence.values[0] = np.std(Remove['MaxConfidence'])
Remove = Remove[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Remove1 = Remove1[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Remove = Remove.append(Remove1)

Speechcomp = df.join(df6.set_index('fund_id'), on='fund_id')


Speechcomp = Speechcomp[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Predictions','MaxConfidence','Confidencelevel']]

Speechcomp = Speechcomp.join(df3result.set_index('fund_id'), on='fund_id')
Speechcomp = Speechcomp.join(df3results.set_index('fund_id'), on='fund_id')
Speechcomp = Speechcomp.join(df3result1.set_index('fund_id'), on='fund_id')
#Speechcomp = pd.merge(Speechcomp, df3result, on=['fund_id'])
#Speechcomp = pd.merge(Speechcomp, df3results, on=['fund_id'])
#Speechcomp = pd.merge(Speechcomp, df3result1, on=['fund_id'])


Speechcomp['Recall']= str(np.nan)
Speechcomp['PRECISION']= str(np.nan)
Speechcomp['F1Score']= str(np.nan)
for i in range(0, len(Speechcomp.index)):
    if(Speechcomp.Truepositive.values[i]!='nan' and Speechcomp.Predictions.values[i]!='nan'):
        Speechcomp.PRECISION.values[i] = (int(Speechcomp.Truepositive.values[i])/int(Speechcomp.Predictions.values[i]))
    else:
        Speechcomp.PRECISION.values[i] = 0

    if(Speechcomp.Truepositive.values[i]!='nan' and Speechcomp.Originals.values[i]!='nan'):
        Speechcomp.Recall.values[i] = (int(Speechcomp.Truepositive.values[i])/int(Speechcomp.Originals.values[i]))
    else:
        Speechcomp.Recall.values[i] = 0
    if(Speechcomp.PRECISION.values[i]!=0 and Speechcomp.Recall.values[i]!=0):
        Speechcomp.F1Score.values[i] = (2*(Speechcomp.PRECISION.values[i]*(Speechcomp.Recall.values[i]))/((Speechcomp.PRECISION.values[i])+(Speechcomp.Recall.values[i])))
header_list = list(Speechcomp.columns)
Speechcomp1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)

Speechcomp1.fund_id.values[0] = i+1
Speechcomp = Speechcomp.replace('nan', 0)

Speechcomp[['Originals']] = Speechcomp[['Originals']].astype(int)
Speechcomp1.Originals.values[0] = (Speechcomp.Originals).sum()
Speechcomp1.Predictions.values[0] = Speechcomp['Predictions'].sum()
Speechcomp1.Truepositive.values[0] = Speechcomp['Truepositive'].sum()
Speechcomp1.Falsepositive.values[0] = Speechcomp['Falsepositive'].sum()
Speechcomp1.Falsenegative.values[0] = Speechcomp['Falsenegative'].sum()


Speechcomp1.Truepositive.values[0] = np.ones(1000000, dtype=np.int64)
Speechcomp1.Originals.values[0] = np.ones(1000000, dtype=np.int64)
Speechcomp1.Predictions.values[0] = np.ones(1000000, dtype=np.int64)

Speechcomp1.Recall.values[0] = (Speechcomp1.Truepositive.values[0]/Speechcomp1.Originals.values[0])
Speechcomp1.PRECISION.values[0] = (Speechcomp1.Truepositive.values[0]/Speechcomp1.Predictions.values[0])
Speechcomp1.F1Score.values[0] = (2*(Speechcomp1.PRECISION.values[0]*(Speechcomp1.Recall.values[0]))/((Speechcomp1.PRECISION.values[0])+(Speechcomp1.Recall.values[0])))

Speechcomp1.MaxConfidence.values[0] = np.std(Speechcomp['MaxConfidence'])
Speechcomp = Speechcomp[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Predictions','Truepositive','Falsepositive','Falsenegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Speechcomp1 = Speechcomp1[['fund_id','Fundname','Type','Style','AUM','Turnover','Region','Originals','Predictions','Truepositive','Falsepositive','Falsenegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Speechcomp = Speechcomp.append(Speechcomp1)

finalpath=os.path.join(root_folder,"All.csv")

Speechcomp.to_csv(finalpath, sep=',' , index=False) 


finalpath=os.path.join(root_folder,"Increment.csv")

Increment.to_csv(finalpath, sep=',' , index=False) 

finalpath=os.path.join(root_folder,"Decrement.csv")

Decrement.to_csv(finalpath, sep=',' , index=False) 

finalpath=os.path.join(root_folder,"Hold.csv")

Hold.to_csv(finalpath, sep=',' , index=False) 

finalpath=os.path.join(root_folder,"Remove.csv")

Remove.to_csv(finalpath, sep=',' , index=False) 

allFiles = glob.glob(root_folder + "/*.csv")
outputno = 1
wb = xlwt.Workbook()
for file_ in allFiles:
    
    
    fpath = file_.split("\\", 1)
    fname = fpath[1].split(".", 1) ## fname[0] should be our worksheet name
  
    
    with open(file_) as f:
        ws = wb.add_sheet(fname[0])
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                ws.write(r, c, col)
    outputno = outputno+1
wb.save(Finaloutput+"\\"'Fund Analysis_2Q2018_ML_Studio.csv')
    

#-----------------------------------------------------------------------

index=np.arange(len(df1.index))   
 #creates a new dataframe
Column_Names = ['stock_id','Ticker','Cap_Size','Sector','ActionTaken','ScoredLabels','Result','Resultfalse','Truepositive','Increment','Decrement','Hold','Remove','Incrementtotal','Decrementtotal','Holdtotal','Removetotal','Incrementfalse','Decrementfalse','Holdfalse','Removefalse','Incrementpredict','Decrementpredict','HoldPredict','Removepredict','Incrementfalsenegative','Decrementfalsenegative','Holdfalsenegative','Removefalsenegative','MaxConfidence','Confidencelevel']
df4 = pd.DataFrame(str(np.nan),index,columns= Column_Names)


#df3['Fundname'] = df3['Fundname'].astype(str)

'''
CompanyAnalysis_2Q2018_ALL_ML_Studio
1. Step 1  - Divide the data frame to 4 different file(Increment, Decrement, Hold, Remove)
2. Step 2 - Add condition where Action taken = Scored labels (Truepositive)
3. Step 3 - Add condition where Action taken !=Scored labels(False positive)
4. Step 4 - Original will be the total action taken value
5. Step5 - Prediction will be the total scored labels value
6. Step 6 - If Scored labels != Action Taken (False Negative)


'''

df4['Result'] = str(np.nan)
df4['stock_id'] = df1['stock_id']
df4['Cap_Size'] = df1['Cap_Size']
df4['Sector'] = df1['Sector']
df4['ActionTaken']= df1['ActionTaken']
df4['ScoredLabels'] = df1['ScoredLabels']
for i in range(0, len(df1.index)):    
    df4.Ticker.values[i]= Ticker(df1.stock_id.values[i])
   # df3.Fundname.values[i]= ("A".astype(float))
    df4.MaxConfidence.values[i] = Maxof4(i)
    df4.Confidencelevel.values[i]= conflevel(df4.MaxConfidence.values[i])


for i in range(0, len(df4.index)): 
    if df4.ActionTaken.values[i] =='Increasing':
           df4.Incrementtotal.values[i] = 1
    elif df4.ActionTaken.values[i] =='Decreasing':
           df4.Decrementtotal.values[i] = 1
    elif df4.ActionTaken.values[i] =='Hold':
           df4.Holdtotal.values[i] = 1
    elif df4.ActionTaken.values[i] =='Remove':
           df4.Removetotal.values[i] = 1    
           
    if df4.ScoredLabels.values[i] =='Increasing':
           df4.Incrementpredict.values[i] = 1
    elif df4.ScoredLabels.values[i] =='Decreasing':
           df4.Decrementpredict.values[i] = 1
    elif df4.ScoredLabels.values[i] =='Hold':
           df4.HoldPredict.values[i] = 1
    elif df4.ScoredLabels.values[i] =='Remove':
           df4.Removepredict.values[i] = 1    
           
           
    if  df4.ActionTaken.values[i] == df4.ScoredLabels.values[i]:
        df4.Result.values[i] = 1
        if df4.ActionTaken.values[i] =='Increasing':
           df4.Increment.values[i] = 1
        elif df4.ActionTaken.values[i] =='Decreasing':
           df4.Decrement.values[i] = 1
        elif df4.ActionTaken.values[i] =='Hold':
           df4.Hold.values[i] = 1
        elif df4.ActionTaken.values[i] =='Remove':
           df4.Remove.values[i] = 1
        
    else:
        df4.Result.values[i] = 0
        if df4.ActionTaken.values[i] =='Increasing':
           df4.Incrementfalse.values[i] = 1
        elif df4.ActionTaken.values[i] =='Decreasing':
           df4.Decrementfalse.values[i] = 1
        elif df4.ActionTaken.values[i] =='Hold':
           df4.Holdfalse.values[i] = 1
        elif df4.ActionTaken.values[i] =='Remove':
           df4.Removefalse.values[i] = 1
           
    if  df4.ScoredLabels.values[i] == df4.ActionTaken.values[i]:
        df4.Resultfalse.values[i] = 1
    else:
        df4.Resultfalse.values[i] = 0
        if df4.ScoredLabels.values[i] =='Increasing':
           df4.Incrementfalsenegative.values[i] = 1
        elif df4.ScoredLabels.values[i] =='Decreasing':
           df4.Decrementfalsenegative.values[i] = 1
        elif df4.ScoredLabels.values[i] =='Hold':
           df4.Holdfalsenegative.values[i] = 1
        elif df4.ScoredLabels.values[i] =='Remove':
           df4.Removefalsenegative.values[i] = 1
        
df4Increment =  df4.groupby(['stock_id','Increment']).size().reset_index(name='ResultIncre')
df4Decrement =  df4.groupby(['stock_id','Decrement']).size().reset_index(name='ResultDecre')
df4Hold =  df4.groupby(['stock_id','Hold']).size().reset_index(name='ResultHold')
df4Remove =  df4.groupby(['stock_id','Remove']).size().reset_index(name='ResultRemove')

df4Incrementtotal =  df4.groupby(['stock_id','Incrementtotal']).size().reset_index(name='ResultIncre')
df4Decrementtotal =  df4.groupby(['stock_id','Decrementtotal']).size().reset_index(name='ResultDecre')
df4Holdtotal =  df4.groupby(['stock_id','Holdtotal']).size().reset_index(name='ResultHold')
df4Removetotal =  df4.groupby(['stock_id','Removetotal']).size().reset_index(name='ResultRemove')


df4Incrementpredict =  df4.groupby(['stock_id','Incrementpredict']).size().reset_index(name='ResultIncre')
df4Decrementpredict =  df4.groupby(['stock_id','Decrementpredict']).size().reset_index(name='ResultDecre')
df4HoldPredict =  df4.groupby(['stock_id','HoldPredict']).size().reset_index(name='ResultHold')
df4Removepredict =  df4.groupby(['stock_id','Removepredict']).size().reset_index(name='ResultRemove')


df4Incrementfalse =  df4.groupby(['stock_id','Incrementfalse']).size().reset_index(name='ResultIncre')
df4Decrementfalse =  df4.groupby(['stock_id','Decrementfalse']).size().reset_index(name='ResultDecre')
df4Holdfalse =  df4.groupby(['stock_id','Holdfalse']).size().reset_index(name='ResultHold')
df4Removefalse =  df4.groupby(['stock_id','Removefalse']).size().reset_index(name='ResultRemove')

df4Incrementfalsenegative =  df4.groupby(['stock_id','Incrementfalsenegative']).size().reset_index(name='ResultIncre')
df4Decrementfalsenegative =  df4.groupby(['stock_id','Decrementfalsenegative']).size().reset_index(name='ResultDecre')
df4Holdfalsenegative =  df4.groupby(['stock_id','Holdfalsenegative']).size().reset_index(name='ResultHold')
df4Removefalsenegative =  df4.groupby(['stock_id','Removefalsenegative']).size().reset_index(name='ResultRemove')

df4result = df4.groupby(['stock_id','Result']).size().reset_index(name='Result1')
df4results = df4.groupby(['stock_id','Result']).size().reset_index(name='Result1')
df4result1 = df4.groupby(['stock_id','Resultfalse']).size().reset_index(name='Result2')

df4result['Truepositive'] = str(np.nan)
df4results['Falsepositive'] = str(np.nan)

for i in range(0, len(df4result.index)): 
    if(df4result.Result.values[i] == 1):
        df4result.Truepositive.values[i] = df4result.Result1.values[i]
                
for i in range(0, len(df4results.index)): 
    if(df4results.Result.values[i] == 0):
        df4results.Falsepositive.values[i] = df4results.Result1.values[i]
           

df4result1['Falsenegative'] = str(np.nan)       

for i in range(0, len(df4result1.index)): 
    if(df4result1.Resultfalse.values[i] == 0):
        df4result1.Falsenegative.values[i] = df4result1.Result2.values[i]
                
df4result = df4result.sort_values(['Result'], ascending=[False])
df4result = df4result.drop_duplicates(['stock_id'],keep='first')
df4result = df4result.drop(['Result','Result1'], axis=1)

df4results = df4results.sort_values(['Result'], ascending=[True])
df4results = df4results.drop_duplicates(['stock_id'],keep='first')
df4results = df4results.drop(['Result','Result1'], axis=1)


df4result1 = df4result1.sort_values(['stock_id','Resultfalse'], ascending=[True,True])
df4result1 = df4result1.drop_duplicates(['stock_id'],keep='first')
df4result1 = df4result1.drop(['Resultfalse','Result2'], axis=1)

#---------------------------------------------------------------------------
df4Increment['Truepositive'] = str(np.nan)

for i in range(0, len(df4Increment.index)): 
    if(df4Increment.Increment.values[i] == 1):
        df4Increment.Truepositive.values[i] = df4Increment.ResultIncre.values[i]
        
df4Increment = df4Increment.drop_duplicates(['stock_id',],keep='first')

df4Increment = df4Increment.drop(['Increment','ResultIncre'], axis=1)

#-----------------------------------------------------------------------------

df4Decrement['Truepositive'] = str(np.nan)

for i in range(0, len(df4Decrement.index)): 
    if(df4Decrement.Decrement.values[i] == 1):
        df4Decrement.Truepositive.values[i] = df4Decrement.ResultDecre.values[i]
        
df4Decrement = df4Decrement.drop_duplicates(['stock_id',],keep='first')

df4Decrement = df4Decrement.drop(['Decrement','ResultDecre'], axis=1)
#----------------------------------------)---------------------------

df4Hold['Truepositive'] = str(np.nan)

for i in range(0, len(df4Hold.index)): 
    if(df4Hold.Hold.values[i] == 1):
        df4Hold.Truepositive.values[i] = df4Hold.ResultHold.values[i]
        
df4Hold = df4Hold.drop_duplicates(['stock_id',],keep='first')

df4Hold = df4Hold.drop(['Hold','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df4Remove['Truepositive'] = str(np.nan)

for i in range(0, len(df4Remove.index)): 
    if(df4Remove.Remove.values[i] == 1):
        df4Remove.Truepositive.values[i] = df4Remove.ResultRemove.values[i]
        
df4Remove = df4Remove.drop_duplicates(['stock_id',],keep='first')

df4Remove = df4Remove.drop(['Remove','ResultRemove'], axis=1)

#-------------------------------------------------------------------------

df4Incrementtotal['Originals'] = str(np.nan)

for i in range(0, len(df4Incrementtotal.index)): 
    if(df4Incrementtotal.Incrementtotal.values[i] == 1):
        df4Incrementtotal.Originals.values[i] = df4Incrementtotal.ResultIncre.values[i]
        
df4Incrementtotal = df4Incrementtotal.drop_duplicates(['stock_id',],keep='first')

df4Incrementtotal = df4Incrementtotal.drop(['Incrementtotal','ResultIncre'], axis=1)


#-------------------------------------------------------------------------

df4Decrementtotal['Originals'] = str(np.nan)

for i in range(0, len(df4Decrementtotal.index)): 
    if(df4Decrementtotal.Decrementtotal.values[i] == 1):
        df4Decrementtotal.Originals.values[i] = df4Decrementtotal.ResultDecre.values[i]
        
df4Decrementtotal = df4Decrementtotal.drop_duplicates(['stock_id',],keep='first')

df4Decrementtotal = df4Decrementtotal.drop(['Decrementtotal','ResultDecre'], axis=1)

#-------------------------------------------------------------------------

df4Holdtotal['Originals'] = str(np.nan)

for i in range(0, len(df4Holdtotal.index)): 
    if(df4Holdtotal.Holdtotal.values[i] == 1):
        df4Holdtotal.Originals.values[i] = df4Holdtotal.ResultHold.values[i]
        
df4Holdtotal = df4Holdtotal.drop_duplicates(['stock_id',],keep='first')

df4Holdtotal = df4Holdtotal.drop(['Holdtotal','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df4Removetotal['Originals'] = str(np.nan)

for i in range(0, len(df4Removetotal.index)): 
    if(df4Removetotal.Removetotal.values[i] == 1):
        df4Removetotal.Originals.values[i] = df4Removetotal.ResultRemove.values[i]
        
df4Removetotal = df4Removetotal.drop_duplicates(['stock_id',],keep='first')

df4Removetotal = df4Removetotal.drop(['Removetotal','ResultRemove'], axis=1)

#-------------------------------------------------------------------------

df4Incrementpredict['Prediction'] = str(np.nan)

for i in range(0, len(df4Incrementpredict.index)): 
    if(df4Incrementpredict.Incrementpredict.values[i] == 1):
        df4Incrementpredict.Prediction.values[i] = df4Incrementpredict.ResultIncre.values[i]
        
df4Incrementpredict = df4Incrementpredict.drop_duplicates(['stock_id',],keep='first')

df4Incrementpredict = df4Incrementpredict.drop(['Incrementpredict','ResultIncre'], axis=1)


#-------------------------------------------------------------------------

df4Decrementpredict['Prediction'] = str(np.nan)

for i in range(0, len(df4Decrementpredict.index)): 
    if(df4Decrementpredict.Decrementpredict.values[i] == 1):
        df4Decrementpredict.Prediction.values[i] = df4Decrementpredict.ResultDecre.values[i]
        
df4Decrementpredict = df4Decrementpredict.drop_duplicates(['stock_id',],keep='first')

df4Decrementpredict = df4Decrementpredict.drop(['Decrementpredict','ResultDecre'], axis=1)

#-------------------------------------------------------------------------

df4HoldPredict['Prediction'] = str(np.nan)

for i in range(0, len(df4HoldPredict.index)): 
    if(df4HoldPredict.HoldPredict.values[i] == 1):
        df4HoldPredict.Prediction.values[i] = df4HoldPredict.ResultHold.values[i]
        
df4HoldPredict = df4HoldPredict.drop_duplicates(['stock_id',],keep='first')

df4HoldPredict = df4HoldPredict.drop(['HoldPredict','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df4Removepredict['Prediction'] = str(np.nan)

for i in range(0, len(df4Removepredict.index)): 
    if(df4Removepredict.Removepredict.values[i] == 1):
        df4Removepredict.Prediction.values[i] = df4Removepredict.ResultRemove.values[i]
        
df4Removepredict = df4Removepredict.drop_duplicates(['stock_id',],keep='first')

df4Removepredict = df4Removepredict.drop(['Removepredict','ResultRemove'], axis=1)


#-------------------------------------------------------------------------

df4Incrementfalse['FalsePositive'] = str(np.nan)

for i in range(0, len(df4Incrementfalse.index)): 
    if(df4Incrementfalse.Incrementfalse.values[i] == 1):
        df4Incrementfalse.FalsePositive.values[i] = df4Incrementfalse.ResultIncre.values[i]
        
df4Incrementfalse = df4Incrementfalse.drop_duplicates(['stock_id',],keep='first')

df4Incrementfalse = df4Incrementfalse.drop(['Incrementfalse','ResultIncre'], axis=1)

#-----------------------------------------------------------------------------

df4Decrementfalse['FalsePositive'] = str(np.nan)

for i in range(0, len(df4Decrementfalse.index)): 
    if(df4Decrementfalse.Decrementfalse.values[i] == 1):
        df4Decrementfalse.FalsePositive.values[i] = df4Decrementfalse.ResultDecre.values[i]
        
df4Decrementfalse = df4Decrementfalse.drop_duplicates(['stock_id',],keep='first')

df4Decrementfalse = df4Decrementfalse.drop(['Decrementfalse','ResultDecre'], axis=1)

#-------------------------------------------------------------------
df4Holdfalse['FalsePositive'] = str(np.nan)

for i in range(0, len(df4Holdfalse.index)): 
    if(df4Holdfalse.Holdfalse.values[i] == 1):
        df4Holdfalse.FalsePositive.values[i] = df4Holdfalse.ResultHold.values[i]
        
df4Holdfalse = df4Holdfalse.drop_duplicates(['stock_id',],keep='first')

df4Holdfalse = df4Holdfalse.drop(['Holdfalse','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df4Removefalse['FalsePositive'] = str(np.nan)

for i in range(0, len(df4Removefalse.index)): 
    if(df4Removefalse.Removefalse.values[i] == 1):
        df4Removefalse.FalsePositive.values[i] = df4Removefalse.ResultRemove.values[i]
        
df4Removefalse = df4Removefalse.drop_duplicates(['stock_id',],keep='first')

df4Removefalse = df4Removefalse.drop(['Removefalse','ResultRemove'], axis=1)
#-------------------------------------------------------------------------
df4Incrementfalsenegative['FalseNegative'] = str(np.nan)

for i in range(0, len(df4Incrementfalsenegative.index)): 
    if(df4Incrementfalsenegative.Incrementfalsenegative.values[i] == 1):
        df4Incrementfalsenegative.FalseNegative.values[i] = df4Incrementfalsenegative.ResultIncre.values[i]
        
df4Incrementfalsenegative = df4Incrementfalsenegative.drop_duplicates(['stock_id',],keep='first')

df4Incrementfalsenegative = df4Incrementfalsenegative.drop(['Incrementfalsenegative','ResultIncre'], axis=1)

#-----------------------------------------------------------------------------

df4Decrementfalsenegative['FalseNegative'] = str(np.nan)

for i in range(0, len(df4Decrementfalsenegative.index)): 
    if(df4Decrementfalsenegative.Decrementfalsenegative.values[i] == 1):
        df4Decrementfalsenegative.FalseNegative.values[i] = df4Decrementfalsenegative.ResultDecre.values[i]
        
df4Decrementfalsenegative = df4Decrementfalsenegative.drop_duplicates(['stock_id',],keep='first')

df4Decrementfalsenegative = df4Decrementfalsenegative.drop(['Decrementfalsenegative','ResultDecre'], axis=1)

#-------------------------------------------------------------------
df4Holdfalsenegative['FalseNegative'] = str(np.nan)

for i in range(0, len(df4Holdfalsenegative.index)): 
    if(df4Holdfalsenegative.Holdfalsenegative.values[i] == 1):
        df4Holdfalsenegative.FalseNegative.values[i] = df4Holdfalsenegative.ResultHold.values[i]
        
df4Holdfalsenegative = df4Holdfalsenegative.drop_duplicates(['stock_id',],keep='first')

df4Holdfalsenegative = df4Holdfalsenegative.drop(['Holdfalsenegative','ResultHold'], axis=1)

#-------------------------------------------------------------------------

df4Removefalsenegative['FalseNegative'] = str(np.nan)

for i in range(0, len(df4Removefalsenegative.index)): 
    if(df4Removefalsenegative.Removefalsenegative.values[i] == 1):
        df4Removefalsenegative.FalseNegative.values[i] = df4Removefalsenegative.ResultRemove.values[i]
        
df4Removefalsenegative = df4Removefalsenegative.drop_duplicates(['stock_id',],keep='first')

df4Removefalsenegative = df4Removefalsenegative.drop(['Removefalsenegative','ResultRemove'], axis=1)
#-------------------------------------------------------------------------
df4Increfinal = []

#df4Increfinal = [df4Increment,df4Incrementfalse,df4Incrementpredict,df4Incrementtotal]
df4Increfinal = pd.merge(df4Increment, df4Incrementfalse, on=['stock_id'])
df4Increfinal = pd.merge(df4Increfinal, df4Incrementpredict, on=['stock_id'])
df4Increfinal = pd.merge(df4Increfinal, df4Incrementtotal, on=['stock_id'])
df4Increfinal = pd.merge(df4Increfinal, df4Incrementfalsenegative, on=['stock_id'])
#---------------------------------------------------------------------------

df4Decrefinal = []

#df4Decrefinal = [df4Decrement,df4Decrementfalse,df4Decrementpredict,df4Decrementtotal]
df4Decrefinal = pd.merge(df4Decrement, df4Decrementfalse, on=['stock_id'])
df4Decrefinal = pd.merge(df4Decrefinal, df4Decrementpredict, on=['stock_id'])
df4Decrefinal = pd.merge(df4Decrefinal, df4Decrementtotal, on=['stock_id'])
df4Decrefinal = pd.merge(df4Decrefinal, df4Decrementfalsenegative, on=['stock_id'])
#-----------------------------------------------------------------------------

df4Holdfinal = []

#df4Holdfinal = [df4Hold,df4Holdfalse,df4HoldPredict,df4Holdtotal]
df4Holdfinal = pd.merge(df4Hold, df4Holdfalse, on=['stock_id'])
df4Holdfinal = pd.merge(df4Holdfinal, df4HoldPredict, on=['stock_id'])
df4Holdfinal = pd.merge(df4Holdfinal, df4Holdtotal, on=['stock_id'])
df4Holdfinal = pd.merge(df4Holdfinal, df4Holdfalsenegative, on=['stock_id'])
#-----------------------------------------------------------------------------
df4Removefinal = []

#df4Removefinal = [df4Remove,df4Removefalse,df4RemovePredict,df4Removetotal]
df4Removefinal = pd.merge(df4Remove, df4Removefalse, on=['stock_id'])
df4Removefinal = pd.merge(df4Removefinal, df4Removepredict, on=['stock_id'])
df4Removefinal = pd.merge(df4Removefinal, df4Removetotal, on=['stock_id'])
df4Removefinal = pd.merge(df4Removefinal, df4Removefalsenegative, on=['stock_id'])

#-----------------------------------------------------------------------------

#df4result = df4result.drop_duplicates(['stock_id',],keep='first')

df5stock = df1.groupby(['stock_id','ActionTaken']).size().reset_index(name='Originals')

df5sumstock = pd.Series.to_frame(df5stock.groupby(['stock_id'])["Originals"].apply(lambda x : x.astype(int).sum()))

df5sumstock['stock_id'] = df5sumstock.index

df7stock = df1.groupby(['stock_id','ScoredLabels']).size().reset_index(name='Predictions')
df7sumstock = pd.Series.to_frame(df7stock.groupby(['stock_id'])['Predictions'].sum())
df7sumstock['stock_id'] = df7sumstock.index

df6stock = df4.drop_duplicates(['stock_id',],keep='first')

df6stock.drop(['ActionTaken','ScoredLabels','Result','Truepositive','Increment','Decrement','Hold','Remove','Incrementtotal','Decrementtotal','Holdtotal','Removetotal','Incrementfalse','Decrementfalse','Holdfalse','Removefalse','Incrementpredict','Decrementpredict','HoldPredict','Removepredict'], axis=1, inplace=True)
df = pd.merge(df5sumstock, df7sumstock, on=['stock_id'])

Increment = df4Increfinal.join(df6stock.set_index('stock_id'), on='stock_id')

Increment['Recall']= str(np.nan)
Increment['PRECISION']= str(np.nan)
Increment['F1Score']= str(np.nan)
for i in range(0, len(Increment.index)):
    if(Increment.Truepositive.values[i]!='nan' and Increment.Prediction.values[i]!='nan'):
        Increment.PRECISION.values[i] = (int(Increment.Truepositive.values[i])/int(Increment.Prediction.values[i]))
    else:
        Increment.PRECISION.values[i] = 0

    if(Increment.Truepositive.values[i]!='nan' and Increment.Originals.values[i]!='nan'):
        Increment.Recall.values[i] = (int(Increment.Truepositive.values[i])/int(Increment.Originals.values[i]))
    else:
        Increment.Recall.values[i] = 0
    if(Increment.PRECISION.values[i]!=0 and Increment.Recall.values[i]!=0):
        Increment.F1Score.values[i] = (2*(Increment.PRECISION.values[i]*(Increment.Recall.values[i]))/((Increment.PRECISION.values[i])+(Increment.Recall.values[i])))
    
header_list = list(Increment.columns)
max_rows = 5

Increment1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)

Increment1.stock_id.values[0] = i+1
Increment = Increment.replace('nan', 0)


Increment[['Originals']] = Increment[['Originals']].astype(int)
Increment1.Originals.values[0] = (Increment.Originals).sum()
Increment1.Prediction.values[0] = Increment['Prediction'].sum()
Increment1.Truepositive.values[0] = Increment['Truepositive'].sum()
Increment1.FalsePositive.values[0] = Increment['FalsePositive'].sum()
Increment1.FalseNegative.values[0] = Increment['FalseNegative'].sum()
Increment1.Recall.values[0] = (Increment1.Truepositive.values[0]/Increment1.Originals.values[0])
Increment1.PRECISION.values[0] = (Increment1.Truepositive.values[0]/Increment1.Prediction.values[0])
Increment1.F1Score.values[0] = (2*(Increment1.PRECISION.values[0]*(Increment1.Recall.values[0]))/((Increment1.PRECISION.values[0])+(Increment1.Recall.values[0])))
Increment1.MaxConfidence.values[0] = np.std(Increment['MaxConfidence'])
Increment = Increment[['stock_id','Ticker','Sector','Cap_Size','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Increment1 = Increment1[['stock_id','Ticker','Sector','Cap_Size','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Increment = Increment.append(Increment1)

Decrement = df4Decrefinal.join(df6stock.set_index('stock_id'), on='stock_id')

Decrement['Recall']= str(np.nan)
Decrement['PRECISION']= str(np.nan)
Decrement['F1Score']= str(np.nan)
for i in range(0, len(Decrement.index)):
    if(Decrement.Truepositive.values[i]!='nan' and Decrement.Prediction.values[i]!='nan'):
        Decrement.PRECISION.values[i] = (int(Decrement.Truepositive.values[i])/int(Decrement.Prediction.values[i]))
    else:
        Decrement.PRECISION.values[i] = 0

    if(Decrement.Truepositive.values[i]!='nan' and Decrement.Originals.values[i]!='nan'):
        Decrement.Recall.values[i] = (int(Decrement.Truepositive.values[i])/int(Decrement.Originals.values[i]))
    else:
        Decrement.Recall.values[i] = 0
    if(Decrement.PRECISION.values[i]!=0 and Decrement.Recall.values[i]!=0):
        Decrement.F1Score.values[i] = (2*(Decrement.PRECISION.values[i]*(Decrement.Recall.values[i]))/((Decrement.PRECISION.values[i])+(Decrement.Recall.values[i])))
        
Decrement1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)        
Decrement1.stock_id.values[0] = i+1
Decrement = Decrement.replace('nan', 0)


Decrement[['Originals']] = Decrement[['Originals']].astype(int)
Decrement1.Originals.values[0] = (Decrement.Originals).sum()
Decrement1.Prediction.values[0] = Decrement['Prediction'].sum()
Decrement1.Truepositive.values[0] = Decrement['Truepositive'].sum()
Decrement1.FalsePositive.values[0] = Decrement['FalsePositive'].sum()
Decrement1.FalseNegative.values[0] = Decrement['FalseNegative'].sum()
Decrement1.Recall.values[0] = (Decrement1.Truepositive.values[0]/Decrement1.Originals.values[0])
Decrement1.PRECISION.values[0] = (Decrement1.Truepositive.values[0]/Decrement1.Prediction.values[0])
Decrement1.F1Score.values[0] = (2*(Decrement1.PRECISION.values[0]*(Decrement1.Recall.values[0]))/((Decrement1.PRECISION.values[0])+(Decrement1.Recall.values[0])))
Decrement1.MaxConfidence.values[0] = np.std(Decrement['MaxConfidence'])
Decrement = Decrement[['stock_id','Ticker','Sector','Cap_Size','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Decrement1 = Decrement1[['stock_id','Ticker','Sector','Cap_Size','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Decrement = Decrement.append(Decrement1)

Hold = df4Holdfinal.join(df6stock.set_index('stock_id'), on='stock_id')

Hold['Recall']= str(np.nan)
Hold['PRECISION']= str(np.nan)
Hold['F1Score']= str(np.nan)
for i in range(0, len(Hold.index)):
    if(Hold.Truepositive.values[i]!='nan' and Hold.Prediction.values[i]!='nan'):
        Hold.PRECISION.values[i] = (int(Hold.Truepositive.values[i])/int(Hold.Prediction.values[i]))
    else:
        Hold.PRECISION.values[i] = 0

    if(Hold.Truepositive.values[i]!='nan' and Hold.Originals.values[i]!='nan'):
        Hold.Recall.values[i] = (int(Hold.Truepositive.values[i])/int(Hold.Originals.values[i]))
    else:
        Hold.Recall.values[i] = 0
    if(Hold.PRECISION.values[i]!=0 and Hold.Recall.values[i]!=0):
        Hold.F1Score.values[i] = (2*(Hold.PRECISION.values[i]*(Hold.Recall.values[i]))/((Hold.PRECISION.values[i])+(Hold.Recall.values[i])))
Hold1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)
Hold1.stock_id.values[0] = i+1
Hold = Hold.replace('nan', 0)


Hold[['Originals']] = Hold[['Originals']].astype(int)
Hold1.Originals.values[0] = (Hold.Originals).sum()
Hold1.Prediction.values[0] = Hold['Prediction'].sum()
Hold1.Truepositive.values[0] = Hold['Truepositive'].sum()
Hold1.FalsePositive.values[0] = Hold['FalsePositive'].sum()
Hold1.FalseNegative.values[0] = Hold['FalseNegative'].sum()
Hold1.Recall.values[0] = (Hold1.Truepositive.values[0]/Hold1.Originals.values[0])
Hold1.PRECISION.values[0] = (Hold1.Truepositive.values[0]/Hold1.Prediction.values[0])
Hold1.F1Score.values[0] = (2*(Hold1.PRECISION.values[0]*(Hold1.Recall.values[0]))/((Hold1.PRECISION.values[0])+(Hold1.Recall.values[0])))
Hold1.MaxConfidence.values[0] = np.std(Hold['MaxConfidence'])
Hold = Hold[['stock_id','Ticker','Sector','Cap_Size','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Hold1 = Hold1[['stock_id','Ticker','Sector','Cap_Size','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Hold = Hold.append(Hold1)  


  
Remove = df4Removefinal.join(df6stock.set_index('stock_id'), on='stock_id')

Remove['Recall']= str(np.nan)
Remove['PRECISION']= str(np.nan)
Remove['F1Score']= str(np.nan)
for i in range(0, len(Remove.index)):
    if(Remove.Truepositive.values[i]!='nan' and Remove.Prediction.values[i]!='nan'):
        Remove.PRECISION.values[i] = (int(Remove.Truepositive.values[i])/int(Remove.Prediction.values[i]))
    else:
        Remove.PRECISION.values[i] = 0

    if(Remove.Truepositive.values[i]!='nan' and Remove.Originals.values[i]!='nan'):
        Remove.Recall.values[i] = (int(Remove.Truepositive.values[i])/int(Remove.Originals.values[i]))
    else:
        Remove.Recall.values[i] = 0
    if(Remove.PRECISION.values[i]!=0 and Remove.Recall.values[i]!=0):
        Remove.F1Score.values[i] = (2*(Remove.PRECISION.values[i]*(Remove.Recall.values[i]))/((Remove.PRECISION.values[i])+(Remove.Recall.values[i])))

Remove1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)
Remove1.stock_id.values[0] = i+1
Remove = Remove.replace('nan', 0)


Remove[['Originals']] = Remove[['Originals']].astype(int)
Remove1.Originals.values[0] = (Remove.Originals).sum()
Remove1.Prediction.values[0] = Remove['Prediction'].sum()
Remove1.Truepositive.values[0] = Remove['Truepositive'].sum()
Remove1.FalsePositive.values[0] = Remove['FalsePositive'].sum()
Remove1.FalseNegative.values[0] = Remove['FalseNegative'].sum()
Remove1.Recall.values[0] = (Remove1.Truepositive.values[0]/Remove1.Originals.values[0])
Remove1.PRECISION.values[0] = (Remove1.Truepositive.values[0]/Remove1.Prediction.values[0])
Remove1.F1Score.values[0] = (2*(Remove1.PRECISION.values[0]*(Remove1.Recall.values[0]))/((Remove1.PRECISION.values[0])+(Remove1.Recall.values[0])))
Remove1.MaxConfidence.values[0] = np.std(Remove['MaxConfidence'])
Remove = Remove[['stock_id','Ticker','Sector','Cap_Size','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Remove1 = Remove1[['stock_id','Ticker','Sector','Cap_Size','Originals','Prediction','Truepositive','FalsePositive','FalseNegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Remove = Remove.append(Remove1)
   
Speechcompstock = df.join(df6stock.set_index('stock_id'), on='stock_id')

Speechcompstock = Speechcompstock[['stock_id','Ticker','Sector','Cap_Size','Originals','Predictions','MaxConfidence','Confidencelevel']]

Speechcompstock = pd.merge(Speechcompstock, df4result, on=['stock_id'])
Speechcompstock = pd.merge(Speechcompstock, df4results, on=['stock_id'])
Speechcompstock = pd.merge(Speechcompstock, df4result1, on=['stock_id'])


Speechcompstock['Recall']= str(np.nan)
Speechcompstock['PRECISION']= str(np.nan)
Speechcompstock['F1Score']= str(np.nan)
for i in range(0, len(Speechcompstock.index)):
    if(Speechcompstock.Truepositive.values[i]!='nan' and Speechcompstock.Predictions.values[i]!='nan'):
        Speechcompstock.PRECISION.values[i] = (int(Speechcompstock.Truepositive.values[i])/int(Speechcompstock.Predictions.values[i]))
    else:
        Speechcompstock.PRECISION.values[i] = 0

    if(Speechcompstock.Truepositive.values[i]!='nan' and Speechcompstock.Originals.values[i]!='nan'):
        Speechcompstock.Recall.values[i] = (int(Speechcompstock.Truepositive.values[i])/int(Speechcompstock.Originals.values[i]))
    else:
        Speechcompstock.Recall.values[i] = 0
    if(Speechcompstock.PRECISION.values[i]!=0 and Speechcompstock.Recall.values[i]!=0):
        Speechcompstock.F1Score.values[i] = (2*(Speechcompstock.PRECISION.values[i]*(Speechcompstock.Recall.values[i]))/((Speechcompstock.PRECISION.values[i])+(Speechcompstock.Recall.values[i])))
header_list = list(Speechcompstock.columns)
Speechcompstock1 = pd.DataFrame(str(np.nan),[max_rows],columns= header_list)
Speechcompstock1.stock_id.values[0] = i+1
Speechcompstock = Speechcompstock.replace('nan', 0)


Speechcompstock[['Originals']] = Speechcompstock[['Originals']].astype(int)
Speechcompstock1.Originals.values[0] = (Speechcompstock.Originals).sum()
Speechcompstock1.Predictions.values[0] = Speechcompstock['Predictions'].sum()
Speechcompstock1.Truepositive.values[0] = Speechcompstock['Truepositive'].sum()
Speechcompstock1.Falsepositive.values[0] = Speechcompstock['Falsepositive'].sum()
Speechcompstock1.Falsenegative.values[0] = Speechcompstock['Falsenegative'].sum()
Speechcompstock1.Recall.values[0] = (Speechcompstock1.Truepositive.values[0]/Speechcompstock1.Originals.values[0])
Speechcompstock1.PRECISION.values[0] = (Speechcompstock1.Truepositive.values[0]/Speechcompstock1.Predictions.values[0])
Speechcompstock1.F1Score.values[0] = (2*(Speechcompstock1.PRECISION.values[0]*(Speechcompstock1.Recall.values[0]))/((Speechcompstock1.PRECISION.values[0])+(Speechcompstock1.Recall.values[0])))
Speechcompstock1.MaxConfidence.values[0] = np.std(Speechcompstock['MaxConfidence'])
Speechcompstock = Speechcompstock[['stock_id','Ticker','Sector','Cap_Size','Originals','Predictions','Truepositive','Falsepositive','Falsenegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Speechcompstock1 = Speechcompstock1[['stock_id','Ticker','Sector','Cap_Size','Originals','Predictions','Truepositive','Falsepositive','Falsenegative','Recall','PRECISION','F1Score','MaxConfidence','Confidencelevel']]
Speechcompstock = Speechcompstock.append(Speechcompstock1)
    
finalpath=os.path.join(CompanyAnalysis,"All.csv")

Speechcompstock.to_csv(finalpath, sep=',' , index=False) 


finalpath=os.path.join(CompanyAnalysis,"Increment.csv")

Increment.to_csv(finalpath, sep=',' , index=False) 

finalpath=os.path.join(CompanyAnalysis,"Decrement.csv")

Decrement.to_csv(finalpath, sep=',' , index=False) 

finalpath=os.path.join(CompanyAnalysis,"Hold.csv")

Hold.to_csv(finalpath, sep=',' , index=False) 

finalpath=os.path.join(CompanyAnalysis,"Remove.csv")

Remove.to_csv(finalpath, sep=',' , index=False) 

allFiles = glob.glob(CompanyAnalysis + "/*.csv")
outputno = 1
wb = xlwt.Workbook()
for file_ in allFiles:
    
    
    fpath = file_.split("\\", 1)
    fname = fpath[1].split(".", 1) ## fname[0] should be our worksheet name
  
    
    with open(file_) as f:
        ws = wb.add_sheet(fname[0])
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                ws.write(r, c, col)
    outputno = outputno+1
wb.save(Finaloutput+"\\"'CompanyAnalysis_2Q2018_ML_Studio.csv')
    

