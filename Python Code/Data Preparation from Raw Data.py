# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to 
import pandas as pd
import sys
# scipy
import scipy
# matplotlib
import matplotlib
# pandas
import pandas as pd
# scikit-learn
import sklearn
from pandas import read_csv
from sklearn.ensemble import ExtraTreesClassifier
import numpy as np 

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(StockSamapleData = None):
      
    # Check Null Value
    
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
    
    mis_val_table_columns = missing_values_table(StockSamapleData)
    print(StockSamapleData)
    
    StockSamapleData=StockSamapleData.dropna(axis=1, how='all')
    StockSamapleData.shape
    mis_val_table_columns = missing_values_table(StockSamapleData)
    #------------------------------------------------
    
    '''
    # Current ratio calculation
    '''
    
    StockSamapleData['curr_ratio'] = StockSamapleData.apply(
            lambda row: row['tot_curr_asset']/row['tot_curr_liab'] if (np.isnan(row['curr_ratio']) and (row['tot_liab']!= 0)) else row['curr_ratio'],
            axis=1)
    
    '''
    # 'tot_curr_asset
    
    '''
    Avg = (StockSamapleData['tot_curr_asset']).sum() / len(StockSamapleData['tot_curr_asset'])
    
    StockSamapleData['asset_turn'] = StockSamapleData.apply(
            lambda row: row['tot_revnu']/Avg if (np.isnan(row['asset_turn']) and (row['tot_curr_asset']!= 0)) else row['asset_turn'],
            axis=1)
    
    '''
    # 'gross_profit'
    '''
    
    StockSamapleData['gross_profit'] = StockSamapleData.apply(lambda row: row['tot_revnu']-row['cost_good_sold']
    if (np.isnan(row['gross_profit']) and (row['tot_revnu']!= 0)) else row['gross_profit'],axis=1)
    
    '''
    # gross_margin
    '''
    StockSamapleData['gross_margin'] = StockSamapleData.apply(lambda row: row['gross_profit']/row['tot_revnu'] 
    if (np.isnan(row['gross_margin']) and (row['tot_revnu']!= 0)) else row['gross_margin'],axis=1)
    
    
    
    '''
    # Debt_to_Equity_Ratio
    '''
    
    StockSamapleData['Debt_to_Equity_Ratio'] = np.nan    # It creates new column ['Debt_to_Equity_Ratio'] 
    
    StockSamapleData['Debt_to_Equity_Ratio'] = StockSamapleData.apply(lambda row: row['tot_liab']/row['tot_debt_tot_equity'] 
    if (np.isnan(row['Debt_to_Equity_Ratio']) and (row['tot_debt_tot_equity']!= 0)) else row['Debt_to_Equity_Ratio'],axis=1)
    
    
    '''
    # Debt_to_Assets_Ratio
    '''
    StockSamapleData['Debt_to_Assets_Ratio'] = np.nan # It creates new column ['Debt_to_Assets_Ratio']
    
    StockSamapleData['Debt_to_Assets_Ratio'] = StockSamapleData.apply(lambda row: row['tot_revnu']/row['tot_curr_asset']
    if (np.isnan(row['Debt_to_Assets_Ratio']) and (row['tot_curr_asset']!= 0)) else row['Debt_to_Assets_Ratio'],axis=1)
    
    
    '''
    # Total_Debt_to_Capital_Ratio
    '''
    StockSamapleData['Total_Debt_to_Capital_Ratio'] = np.nan # It creates new column ['Total_Debt_to_Capital_Ratio']
    
    StockSamapleData['Total_Debt_to_Capital_Ratio'] = StockSamapleData.apply(lambda row: row['tot_debt']/row['tot_invst_cap']
    if (np.isnan(row['Total_Debt_to_Capital_Ratio']) and (row['tot_invst_cap']!= 0)) else row['Total_Debt_to_Capital_Ratio'],axis=1)
    
    '''
    #ebit_margin
    '''
    
    StockSamapleData['ebit_margin'] = StockSamapleData.apply(lambda row: row['ebit']/row['tot_revnu'] 
    if (np.isnan(row['ebit_margin']) and (row['tot_revnu']!= 0)) else row['ebit_margin'],axis=1)
    
    
    '''
    # ebitda_margin
    '''
    StockSamapleData['ebitda_margin'] = StockSamapleData.apply(lambda row: row['ebitda']/row['tot_revnu'] 
    if (np.isnan(row['ebitda_margin']) and (row['tot_revnu']!= 0)) else row['ebitda'],axis=1)
    
    '''
    #oper_profit_margin
    '''
    
    StockSamapleData['oper_profit_margin'] = StockSamapleData.apply(lambda row: row['oper_income']/row['tot_revnu'] 
    if (np.isnan(row['oper_profit_margin']) and (row['tot_revnu']!= 0)) else row['oper_profit_margin'],axis=1)
    
    '''
    # Cost_of_Revenues
    '''
    StockSamapleData['Cost_of_Revenues']  = np.nan # new column create
    StockSamapleData['Cost_of_Revenues'] = StockSamapleData.apply(lambda row: row['gross_profit'] + row['cost_good_sold'] 
    if (np.isnan(row['Cost_of_Revenues'])) else row['Cost_of_Revenues'],axis=1)
    
    '''
    # Stock wise median imputation
    ''' 
    StockSamapleData.shape
    StockSamapleData.dtypes
    list(StockSamapleData)
    
    # Segregate the char numeric 
    target= StockSamapleData[['ClassInd']]
    Char_data=StockSamapleData[['fund_id','QDate','Quarter','ActionTaken','SectorWeightage','StockWeightage','Aging','Cap_Size','IsNonOwner','Year','Cap_SizeID','Fund Name','Stock Name','industry','Sector','sub_industry','Sector_ID','ActivePassive','fund_type','Investor Style','AUM','Turnover','Region']]
    Numeric=StockSamapleData[['stock_id', 'stock_price','sharevalue','asset_turn','book_val_per_share','curr_ratio','day_sale_rcv','ebit_margin','ebitda_margin','free_cash_flow','free_cash_flow_per_share','gross_margin','invty_turn','lterm_debt_cap','oper_cash_flow_per_share','oper_profit_margin','pretax_profit_margin','profit_margin','rcv_turn','ret_asset','ret_equity','ret_invst','ret_tang_equity','tot_debt_tot_equity','tot_share_holder_equity','income_aft_tax','pre_tax_income','tot_liab','tot_liab_share_holder_equity','tang_stock_holder_equity','tot_comm_equity','cash_flow_invst_activity','incr_decr_cash','cash_flow_oper_activity','cash_flow_fin_activity','tot_deprec_amort_cash_flow','tot_change_asset_liab','dilution_factor','tot_provsn_income_tax','basic_net_eps','diluted_net_eps','avg_b_shares','avg_d_shares','comm_stock_net','net_change_prop_plant_equip','retain_earn_accum_deficit','tot_revnu','tot_oper_exp','net_prop_plant_equip','ebit','net_comm_equity_issued_repurch','ebitda','tot_non_oper_income_exp','addtl_paid_in_cap','debt_issue_retire_net_tot','cash_sterm_invst','acct_pay','stock_based_compsn','tot_curr_asset','tot_curr_liab','rcv_tot','tot_sell_gen_admin_exp','non_oper_int_exp','cost_good_sold','tot_lterm_debt','other_non_curr_liab','gross_profit','oper_income','cap_expense','eps_amt_diff_surp','eps_mean_est','eps_pct_diff_surp','sales_amt_diff_surp','sales_mean_est','sales_pct_diff_surp','tot_invst_cap','tot_debt','Debt_to_Equity_Ratio','Debt_to_Assets_Ratio','Total_Debt_to_Capital_Ratio','Cost_of_Revenues']]
    Numeric.dtypes
    mis_val_table_columns = missing_values_table(Numeric)
    # delete 70% null column
    for c in Numeric:
        if 100*Numeric[c].isnull().sum()/len(Numeric) >= 70:
            Numeric.drop(c, axis=1, inplace=True)
    
    Numeric.shape
    
    mis_val_table_columns1 = missing_values_table(Numeric)
    
    #Numeric["sharevalue"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    #Numeric["invty_turn"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    #Numeric["day_sale_rcv"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    #Numeric["rcv_turn"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["stock_based_compsn"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["tot_provsn_income_tax"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["rcv_tot"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["other_non_curr_liab"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["Cost_of_Revenues"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["cost_good_sold"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["tot_lterm_debt"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["acct_pay"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["retain_earn_accum_deficit"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["non_oper_int_exp"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["addtl_paid_in_cap"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["curr_ratio"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["tot_curr_liab"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["net_prop_plant_equip"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["stock_price"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["Debt_to_Assets_Ratio"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["gross_profit"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["tot_curr_asset"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["tot_sell_gen_admin_exp"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["sales_pct_diff_surp"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["sales_mean_est"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["sales_amt_diff_surp"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["lterm_debt_cap"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["net_comm_equity_issued_repurch"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["eps_pct_diff_surp"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["eps_mean_est"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["eps_amt_diff_surp"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["tot_change_asset_liab"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["tot_debt_tot_equity"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["tot_debt"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["Debt_to_Equity_Ratio"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["Total_Debt_to_Capital_Ratio"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["cap_expense"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["net_change_prop_plant_equip"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    Numeric["gross_margin"] =Numeric.groupby("stock_id").transform(lambda x: x.fillna(x.median()))
    
    mis_val_table_columns = missing_values_table(Numeric)
    
    '''
    ##-------------------------------- Normalize float_Df_1_Not_Nul data -----------------------------------------------
    '''
    st_id=Numeric[['stock_id']]
    df=Numeric[['stock_price','asset_turn','book_val_per_share','curr_ratio','ebit_margin','ebitda_margin','free_cash_flow','free_cash_flow_per_share','gross_margin','lterm_debt_cap','oper_cash_flow_per_share','oper_profit_margin','pretax_profit_margin','profit_margin','ret_asset','ret_equity','ret_invst','ret_tang_equity','tot_debt_tot_equity','tot_share_holder_equity','income_aft_tax','pre_tax_income','tot_liab','tot_liab_share_holder_equity','tang_stock_holder_equity','tot_comm_equity','cash_flow_invst_activity','incr_decr_cash','cash_flow_oper_activity','cash_flow_fin_activity','tot_deprec_amort_cash_flow','tot_change_asset_liab','dilution_factor','tot_provsn_income_tax','basic_net_eps','diluted_net_eps','avg_b_shares','avg_d_shares','comm_stock_net','net_change_prop_plant_equip','retain_earn_accum_deficit','tot_revnu','tot_oper_exp','net_prop_plant_equip','ebit','net_comm_equity_issued_repurch','ebitda','tot_non_oper_income_exp','addtl_paid_in_cap','debt_issue_retire_net_tot','cash_sterm_invst','acct_pay','stock_based_compsn','tot_curr_asset','tot_curr_liab','rcv_tot','tot_sell_gen_admin_exp','non_oper_int_exp','cost_good_sold','tot_lterm_debt','other_non_curr_liab','gross_profit','oper_income','cap_expense','eps_amt_diff_surp','eps_mean_est','eps_pct_diff_surp','sales_amt_diff_surp','sales_mean_est','sales_pct_diff_surp','tot_invst_cap','tot_debt','Debt_to_Equity_Ratio','Debt_to_Assets_Ratio','Total_Debt_to_Capital_Ratio','Cost_of_Revenues']]
    def norm(df):
        result = df.copy()
        for feature_name in df.columns:
            max_value = df[feature_name].max()
            min_value = df[feature_name].min()
            result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
        return result
    Normalised_Data=norm(df)
    print("Normalised col::",list(Normalised_Data.columns.values))
    
    
    
    final_Df=pd.concat([st_id,Char_data,df,target],axis=1)

    # Execution logic goes here
    #print('Input pandas.DataFrame #1:\r\n\r\n{0}'.format(dataframe1))

    # If a zip file is connected to the third input port is connected,
    # it is unzipped under ".\Script Bundle". This directory is added
    # to sys.path. Therefore, if your zip file contains a Python file
    # mymodule.py you can import it using:
    # import mymodule
    
    # Return value must be of a sequence of pandas.DataFrame
    return final_Df,
