# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 10:00:30 2018

@author: datacore
"""

from sqlalchemy import create_engine
import pickle
import sqlite3
from sklearn import preprocessing
import sys
print('Python: {}'.format(sys.version))
# scipy
import scipy
print('scipy: {}'.format(scipy.__version__))
# numpy
import numpy
print('numpy: {}'.format(numpy.__version__))
# matplotlib
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
# pandas
import pandas as pd
print('pandas: {}'.format(pd.__version__))
# scikit-learn
import sklearn
print('sklearn: {}'.format(sklearn.__version__))
import os


#% of missing values in each column:
def missing_values_table(df):
        mis_val = df.isnull().sum()
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")
        return mis_val_table_ren_columns




#To get the current working directory use

cwd = os.getcwd()


''' This is one time job to read large csv and insert into SQLLITE db
'''
#https://pythondata.com/working-large-csv-files-python/
# Raw input column lists
ArrangeCollist = ['fund_id',
'stock_id',
'QDate',
'Quarter',
'sharevalue',
'ActionTaken',
'ClassInd',
'stock_price',
'SectorWeightage',
'StockWeightage',
'Aging',
'Cap_Size',
'IsOwner',
'Year',
'Cap_SizeID',
'Fund Name',
'Stock Name',
'industry',
'Sector',
'Sector_ID',
'ActivePassive',
'fund_type',
'Investor Style',
'AUM',
'Turnover',
'Region',
'asset_turn',
'book_val_per_share',
'comb_ratio',
'curr_ratio',
'day_sale_rcv',
'ebit_margin',
'ebitda_margin',
'exp_ratio',
'free_cash_flow',
'free_cash_flow_per_share',
'gross_margin',
'invty_turn',
'loan_loss_reserve',
'loss_ratio',
'lterm_debt_cap',
'non_perform_asset_tot_loan',
'oper_cash_flow_per_share',
'oper_profit_margin',
'pretax_profit_margin',
'profit_margin',
'rcv_turn',
'ret_asset',
'ret_equity',
'ret_invst',
'ret_tang_equity',
'tot_debt_tot_equity',
'tot_share_holder_equity',
'income_aft_tax',
'pre_tax_income',
'tot_liab',
'tot_liab_share_holder_equity',
'tang_stock_holder_equity',
'tot_comm_equity',
'cash_flow_invst_activity',
'incr_decr_cash',
'cash_flow_oper_activity',
'cash_flow_fin_activity',
'tot_deprec_amort_cash_flow',
'tot_change_asset_liab',
'dilution_factor',
'tot_provsn_income_tax',
'basic_net_eps',
'diluted_net_eps',
'avg_b_shares',
'avg_d_shares',
'comm_stock_net',
'net_change_prop_plant_equip',
'retain_earn_accum_deficit',
'tot_revnu',
'tot_oper_exp',
'net_prop_plant_equip',
'ebit',
'net_comm_equity_issued_repurch',
'ebitda',
'tot_non_oper_income_exp',
'addtl_paid_in_cap',
'debt_issue_retire_net_tot',
'cash_sterm_invst',
'acct_pay',
'stock_based_compsn',
'tot_curr_asset',
'tot_curr_liab',
'rcv_tot',
'tot_sell_gen_admin_exp',
'non_oper_int_exp',
'cost_good_sold',
'tot_lterm_debt',
'other_non_curr_liab',
'gross_profit',
'oper_income',
'cap_expense',
'eps_amt_diff_surp',
'eps_mean_est',
'eps_pct_diff_surp',
'sales_amt_diff_surp',
'sales_mean_est',
'sales_pct_diff_surp',
'tot_invst_cap',
'tot_debt']

os.getcwd()
#file = "E:/GG-12-6/Advanced Analytics/2018Q2-000.csv"

#Just check first n rows (here 22) from large csv file
#print(pd.read_csv(file,usecols=range(0, 104), nrows=22))
# https://plot.ly/python/big-data-analytics-with-pandas-and-sqlite/
#Pandas and SQLite in Python


csv_database = create_engine('sqlite:///csv_database.db')
file = "D:/Stock_Prediction/Non_Owner/data/data(others)/NonOwner2018Q3_SC_other.csv"
chunksize = 100000
i = 0
j = 1
for df in pd.read_csv(file, chunksize=chunksize,header=None , skiprows=1 , names=ArrangeCollist, error_bad_lines=False, index_col=False, dtype='unicode',iterator=True):
      df = df.rename(columns={c: c.replace(' ', '') for c in df.columns}) 
      df.index += j
      i+=1
      df.to_sql('stockTbl', csv_database, if_exists='append')
      j = df.index[-1] + 1     

# Move DB to another folder

# One time job 
conn = sqlite3.connect("C:/Users/datacore/csv_database.db")
cur = conn.cursor()
cur.execute("SELECT DISTINCT(Sector_ID) from stockTbl;")


cur.execute("SELECT * FROM stockTbl WHERE Sector_ID = 7")

myresult = cur.fetchall()

for x in myresult:
  print(x)
  
  
sector_list = [row[0] for row in cur.fetchall()] # to avoid [('testing',), ('testing',)]
cur.close()
conn.close()
#results = cur.fetchall()
with open("DistinctSector.txt", "wb") as fp:   #Pickling
     pickle.dump(sector_list, fp)
'''
E N D Of One Time Job
'''



'''
conn = sqlite3.connect("E:/GG-12-6/Media-Intelligence/SqlLiteDB/csv_database.db")

T H IS ARE FOR TSETING 
cur = conn.cursor()
cur.execute("select * from 'stockTbl' limit 5;")

results = cur.fetchall()
print(results)

cur.execute("select Sector_ID, count(*) from stockTbl group by Sector_ID ;")

cur.execute("SELECT DISTINCT Sector_ID from stockTbl;")

results = cur.fetchall()

import pickle
 l = [1,2,3,4]
with open("test.txt", "wb") as fp:   #Pickling
     pickle.dump(l, fp)
with open("test.txt", "rb") as fp:   # Unpickling
     b = pickle.load(fp)

print(results)


cur.close()
'''

# Start from here once time job is done
# Load already stored DistinctSector list from the file & store it results list

with open("DistinctSector.txt", "rb") as fp:   # Unpickling
     sector_list = pickle.load(fp)

# remove non-numeric list entries as sector code must be numeric
SectorCode = [ x for x in sector_list if x.isdigit()]
# Sort list as '1', '2' , '3' as string 
SectorCode.sort(key=int)

''' Where to store the Report file 
following example shows Reporting file will be stored as Run Date wise
'E:\\GG-12-6\\Advanced Analytics\\IntroActMissingValuePattern\\MissingPattern_2018-11-01'
'''

Drive = "E:"   #Enter your drive name 

RootFolder = Drive+"\\GG-12-6\\Advanced Analytics\\IntroActMissingValuePattern"

from datetime import date
today = str(date.today())
ReportFolderName  = RootFolder+"\\MissingPattern_" +today 

if not os.path.exists(ReportFolderName):
   os.makedirs(ReportFolderName) 

# End of Where to store the Report file 


conn = sqlite3.connect("E:/GG-12-6/Media-Intelligence/SqlLiteDB/csv_database.db")

# Find Sectorwise Action Taken count 
df = pd.read_sql_query('SELECT Sector, ActionTaken, COUNT(*) as `num_complaints`'
                       'FROM stockTbl '
                       'GROUP BY Sector, ActionTaken', conn)



sql = """
              SELECT * from stockTbl
               
              WHERE
                Sector_ID = "7"
        """
    
StockSamapleData = pd.read_sql_query(sql, conn)
StockSamapleData.to_csv("D:/Stock_Prediction/Non_Owner/data/data(others)/Sector7-Example2.csv", index=False)




for i in range (len(SectorCode)):
    #print(SectorCode[i])
    SectorKode = SectorCode[i]
    print ("Sector- " + SectorKode + " processing.")
    #https://www.programcreek.com/python/example/101334/pandas.read_sql_query
    sql = """
              SELECT * from stockTbl
               
              WHERE
                Sector_ID = {}
        """.format(SectorCode[i])
    
    StockSamapleData = pd.read_sql_query(sql, conn)
    #break
    #df13= StockSamapleData.head(10)

    conn.close()

    '''
    Find Sectorwise null pattern
    '''
    
    
    #Drop column if they only contain missing values
    StockSamapleData=StockSamapleData.dropna(axis=1, how='all')
    #df133= StockSamapleData.head(10)
    # Find Number of column 
    cols = StockSamapleData.columns.tolist()
    
    '''
    #Count distinct ,  if Single value - dropped that column
    StockSamapleData.groupby('IsOwner').size()  
    StockSamapleData.groupby('industry').size() 
    StockSamapleData.groupby('Sector').size() 
    StockSamapleData.groupby('Sector_ID').size() 
    StockSamapleData.groupby('Region').size() # # Some region having id = 999
    StockSamapleData.groupby('Investor Style').size() # # Some region having id = 999
    StockSamapleData.groupby('Cap_Size').size() 
    StockSamapleData.groupby('AUM').size() 
    StockSamapleData.groupby('ActivePassive').size() 
    
    StockSamapleData.groupby(['Sector','Cap_Size']).size() 
    '''
    
    
    '''
    Need to understand the relation betwwen Sector , Industry and Region 
    '''
    
    
    # Now drop Year column (not required)
    colToBeDropped = [#'AUM',
                      'IsOwner',
                      'FundName' , 
                      'StockName',
                      # 'industry',
                      'Sector',
                      'ActionTaken']
    
    
    
    StockSamapleData.drop(colToBeDropped, inplace=True, axis=1)
    df1333= StockSamapleData.head(10)
    '''
    Convert Aging column (no of days) to Year (AgeingYR)
    
    
    '''
    # Convert Aging column to numeric
    StockSamapleData[['Aging']] = StockSamapleData[['Aging']].astype(int)
    
    StockSamapleData['AgeingYR'] = round((StockSamapleData.Aging/365),0)
    
    
    StockSamapleData.groupby('AgeingYR').size()  
    # Check Min and Max of AgeingYR 
    min(StockSamapleData.AgeingYR)
    max(StockSamapleData.AgeingYR)
    
    # Based on min and  max group the AgeingYR to Age-Bin
    #0-3 = 0 , 3-5 = 1 . 5-7 = 2 , > 7 = 3
    #bins = [0, 3,5,7]
    #StockSamapleData['Age-Bin'] = numpy.searchsorted(bins, StockSamapleData['AgeingYR'].values)
    
    
    
    
    
    # Based on min and  max group the AgeingYR to Age-Bin
    StockSamapleData['Age-Bin'] = pd.cut(StockSamapleData['AgeingYR'], [0, 3,5,7], labels=['0-3', '3-5', '5-7'])
    
    # Check count of each category
    StockSamapleData.groupby('Age-Bin').size()  
    
    
    '''
    #Lebel the Age-Bin with nummeric
    #'Age-Bin' - ['0-3', '3-5', '5-25'] to numeric 0 ,1 ,2
    #and then drop 'Age-Bin' column
    
    '''
    # Create a label encoder object 
    #from sklearn import preprocessing
    number = preprocessing.LabelEncoder()
    
    StockSamapleData['AgeCat'] = number.fit_transform(StockSamapleData['Age-Bin'].astype('str'))
    # Check count of each category
    StockSamapleData.groupby('AgeCat').size()  
    df13333= StockSamapleData.head(10)
    #Create a label encoder object for industry 
    StockSamapleData['industryId'] = number.fit_transform(StockSamapleData['industry'].astype('str'))
    
    StockSamapleData.head(3)
    # Check count of each category
    StockSamapleData.groupby('industry').size()  
    
import copy 
df_sectorid=[]
dict_of_df = {}
data_dict = []
CSV_dict = []
for industryid, df_industryid in StockSamapleData.groupby('industry'):

    #key_name = 'df_new_'+str(sectorid)  
    # Example df_Sector1_clean
    key_name = 'df_Industry'+str(industryid)+'_clean'  

    dict_of_df[key_name] = copy.deepcopy(df_industryid)

    to_change = StockSamapleData['industry']> industryid
    dict_of_df[key_name].loc[to_change, 'new_col'] = industryid
    globals()[key_name]=dict_of_df[key_name]
    #Drop  columns with a high (70%)percentage of  missing(NaN) values 
    globals()[key_name] = globals()[key_name].dropna(axis=1, thresh=int(0.7*len( globals()[key_name])))
    




    # Create a list CSV_dict having dataframe name and number of column 
    # like ['df_Sector_1_clean', 95]
    
    data_dict = []
    data_dict.append(key_name)
    data_dict.append(len(globals()[key_name].columns))
    data_dict.append(len(globals()[key_name].index))
    CSV_dict.append(data_dict)

col_names = ["DataFrameName","No_Of_Column", "No_Of_Rows"]

#Creating data frame with the specified columns
DataFrameSummary = pd.DataFrame.from_records(CSV_dict, columns=col_names)

ListofDataFramewithSameColumn = DataFrameSummary.groupby('No_Of_Column')['DataFrameName'].apply(list)

StockSamapleData.to_csv("E:/GG-12-6/Advanced Analytics/Sector7-Example2.csv", index=False)
# DONE -------------------------------------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Drop ['Age-Bin','AgeingYR','Aging'] column and keep only AgeCat column
    colToBeDropped = ['Age-Bin','AgeingYR','Aging']
    StockSamapleData.drop(colToBeDropped, inplace=True, axis=1)
    # Find Number of column after dropping a
    cols = list(df_IndustrySoftware_clean.columns.values)
    
    ReArrangeCollist = ['fund_id',
     'stock_id',
     'QDate',
     'Quarter',
      'Year',
      'AgeCat',
      'industry',
     'Cap_SizeID',
     'Sector_ID',
     'ActivePassive',
     'fund_type',
     'Investor Style',
     'AUM',
     'Turnover',
     'Region',
     'SectorWeightage',
     'StockWeightage',
     'sharevalue',
     'stock_price',
     'asset_turn',
     'book_val_per_share',
     'comb_ratio',
     'curr_ratio',
     'day_sale_rcv',
     'ebit_margin',
     'ebitda_margin',
     'exp_ratio',
     'free_cash_flow',
     'free_cash_flow_per_share',
     'gross_margin',
     'invty_turn',
     'loan_loss_reserve',
     'loss_ratio',
     'lterm_debt_cap',
     'non_perform_asset_tot_loan',
     'oper_cash_flow_per_share',
     'oper_profit_margin',
     'pretax_profit_margin',
     'profit_margin',
     'rcv_turn',
     'ret_asset',
     'ret_equity',
     'ret_invst',
     'ret_tang_equity',
     'tot_debt_tot_equity',
     'tot_share_holder_equity',
     'income_aft_tax',
     'pre_tax_income',
     'tot_liab',
     'tot_liab_share_holder_equity',
     'tang_stock_holder_equity',
     'tot_comm_equity',
     'cash_flow_invst_activity',
     'incr_decr_cash',
     'cash_flow_oper_activity',
     'cash_flow_fin_activity',
     'tot_deprec_amort_cash_flow',
     'tot_change_asset_liab',
     'dilution_factor',
     'tot_provsn_income_tax',
     'basic_net_eps',
     'diluted_net_eps',
     'avg_b_shares',
     'avg_d_shares',
     'comm_stock_net',
     'net_change_prop_plant_equip',
     'retain_earn_accum_deficit',
     'tot_revnu',
     'tot_oper_exp',
     'net_prop_plant_equip',
     'ebit',
     'net_comm_equity_issued_repurch',
     'ebitda',
     'tot_non_oper_income_exp',
     'addtl_paid_in_cap',
     'debt_issue_retire_net_tot',
     'cash_sterm_invst',
     'acct_pay',
     'stock_based_compsn',
     'tot_curr_asset',
     'tot_curr_liab',
     'rcv_tot',
     'tot_sell_gen_admin_exp',
     'non_oper_int_exp',
     'cost_good_sold',
     'tot_lterm_debt',
     'other_non_curr_liab',
     'gross_profit',
     'oper_income',
     'cap_expense',
     'eps_amt_diff_surp',
     'eps_mean_est',
     'eps_pct_diff_surp',
     'sales_amt_diff_surp',
     'sales_mean_est',
     'sales_pct_diff_surp',
     'tot_invst_cap',
     'tot_debt',
      'ClassInd']
    
    
    StockSamapleData = StockSamapleData.reindex(columns=ReArrangeCollist)
    cols = list(StockSamapleData.columns.values)
    
    
    StockSamapleData.shape[0] #gives number of row count
    StockSamapleData.shape[1] #gives number of col count
    '''
    #Drop column if they only contain missing values
    '''
    StockSamapleData=StockSamapleData.dropna(axis=1, how='all')
    
    #% of missing values in each column:
    mis_val_table_columns = missing_values_table(StockSamapleData)
    
    # Get column list 
    cols=list(StockSamapleData.columns.values)
    # Take only numeric and related column
    ColList = cols[16:91]
    
    #Find % of NULL (missing value) for each column from ColList.
    # 0% - No missing , 100 - All missing
    #AllNullColumns=StockSamapleData.groupby(['Sector_ID','stock_id'])[ColList].apply(lambda x: x.isnull().sum()/len(x)*100)
    AllNullColumns=StockSamapleData.groupby(['stock_id'])[ColList].apply(lambda x: x.isnull().sum()/len(x)*100)
    #AllNullColumns=StockSamapleData.groupby('stock_id' )[ColList].apply(lambda x: x.isnull().sum()/len(x)*100)
    
    # Repalce all 0 with nan 
    FromRawData = AllNullColumns.replace(0, numpy.nan)
    
    #Drop column if they only contain nan (i,e 0)
    FromRawData1=FromRawData.dropna(axis=1, how='all')
    
    NumofColumn= FromRawData1.shape[1] #gives number of col count
    
    FromRawData1['Kount'] = FromRawData1.count(axis=1)
    
    FromRawData1['TotalFeatures'] = NumofColumn - 1
    
    FromRawData1['AllMissingPercentage'] = round((FromRawData1.Kount/FromRawData1.TotalFeatures),2)
    
    
    Final_filename = "Sector_" +SectorKode+ "-MissedCol.csv"
    finalpath=os.path.join(ReportFolderName,Final_filename)
    #wtite to csv for further data exploration and pattern of missing data
    FromRawData1.to_csv(finalpath, sep=',' , index=True) 



'''
df = FromRawData1.groupby(['stock_id'])['AllMissingPercentage'].max().reset_index()

#criteria_1 = (df['AllMissingPercentage'] == 0,20) 
#TopMissionPattern = df[criteria_1]
cols=list(df.columns.values)
Maximum = df['AllMissingPercentage'] > 0.19
TopMissionPattern = df[Maximum]
TopMissionPattern.to_csv('TopMissionPattern.csv', sep=',' , index=True) 
'''

StockSamapleData.shape[0] #gives number of row count
#StockSamapleData['COUNTER'] =1

#group_data = StockSamapleData.groupby(['Sector_ID','ClassInd'])['COUNTER'].sum() #sum function

#print(group_data)

Classditribution=StockSamapleData.groupby(['Sector_ID', 'ClassInd']).size() \
  .sort_values(ascending=False) \
  .reset_index(name='count') \
  .drop_duplicates(subset='ClassInd')


Classditribution['TotalRows'] = StockSamapleData.shape[0]

#Classditribution.dtypes
#Classditribution['ClassPercentage'] = round((Classditribution.count / Classditribution.TotalRows),2)



















# https://www.pythonsheets.com/notes/python-sqlalchemy.html
from sqlalchemy import inspect  
inspector = inspect(csv_database)

csv_database = "E:/GG-12-6/Media-Intelligence/SqlLiteDB/csv_database.db"


inspector = inspect(csv_database)

# Get table information
print(inspector.get_table_names())

# Get column information
print(inspector.get_columns('stockTbl'))


#http://www.sqlitetutorial.net/sqlite-where/
import sqlite3

conn = sqlite3.connect("csv_database.db")
cur = conn.cursor()
cur.execute("select * from 'stockTbl' limit 5;")
results = cur.fetchall()
print(results)

df1 = pd.read_sql_query("select * from stockTbl Where Sector_ID =1;", conn)

df13= df1.head(3)


cur.close()
conn.close()

















df = pd.read_sql_query('SELECT * FROM table', csv_database)


# https://www.pythonsheets.com/notes/python-sqlalchemy.html
from sqlalchemy import inspect  
inspector = inspect(csv_database)

# Get table information
print(inspector.get_table_names())

# Get column information
print(inspector.get_columns('stockTbl'))


#https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
import sqlalchemy as db

print('db: {}'.format(db.__version__))

connection.close()
#engine = db.create_engine('sqlite:///census.sqlite')
connection = csv_database.connect()
metadata = db.MetaData()
stocktbl = db.Table('stockTbl', metadata, autoload=True, autoload_with=csv_database)
# Print the column names
print(stocktbl.columns.keys())


