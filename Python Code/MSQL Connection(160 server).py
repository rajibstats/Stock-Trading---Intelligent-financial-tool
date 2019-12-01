# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 17:14:08 2018

@author: datacore
"""
import pypyodbc
connection = pypyodbc.connect('Driver={SQL Server};'
'Server=52.168.37.160;'
'Database=IntroActML;'
'uid=sa;pwd=bd@m1n#Intr0@ct')
cur=connection.cursor()

cur.execute("SELECT * FROM IntroActML.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
result_tbl = cur.fetchall()
print("TABLES IN DATABASE::\n")
for i in range(len(result_tbl)):
print(result_tbl[i])
