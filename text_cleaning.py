#Load Packages
import pandas as pd
import numpy as np
import datatable as dt

'''
Explanation of the report form:

TEXT file contains following 6 fields, delimited by pipe (|), one record per line:

1. MDR Report Key
2. MDR Text Key
3. Text Type Code (D=B5, E=H3, N=H10 from mdr_text table)
4. Patient Sequence Number (from mdr_text table)
5. Date Report (from mdr_text table)
6. Text (B5, or H3 or H10 from mdr_text table)
'''

#Load in Data
txt_all = dt.fread('dexcom_txt_all.csv').to_pandas()
print(txt_all.TEXT_TYPE_CODE.value_counts())

#Drop unneeded data
txt_cases = txt_all[txt_all['TEXT_TYPE_CODE'] == 'D'].copy()
drop_cols = ['DATE_REPORT', 'PATIENT_SEQUENCE_NUMBER', 'C0', 'TEXT_TYPE_CODE']
txt_cases.drop(columns = drop_cols, inplace = True)
txt_cases.reset_index(inplace = True, drop = True)


#Create Model (G#) Column
g4 = pd.read_csv('index/g4index.csv', index_col = 'Unnamed: 0')
g5 = pd.read_csv('index/g5index.csv', index_col = 'Unnamed: 0')
g6 = pd.read_csv('index/g6index.csv', index_col = 'Unnamed: 0')

g4_list = g4['MDR_REPORT_KEY'].to_list()
g5_list = g5['MDR_REPORT_KEY'].to_list()
g6_list = g6['MDR_REPORT_KEY'].to_list()

#Specify Dexcom related reports
txt_cases['G4'] = txt_cases['MDR_REPORT_KEY'].isin(g4_list)
txt_cases['G5'] = txt_cases['MDR_REPORT_KEY'].isin(g5_list)
txt_cases['G6'] = txt_cases['MDR_REPORT_KEY'].isin(g6_list)

#Create Dummy Variable
txt_cases.replace({True: 1, False: 0}, inplace = True)

# Export Dataset
txt_cases.to_csv('dexcom_txt_clean.csv', index = False)