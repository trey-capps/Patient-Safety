#Load Packages
import pandas as pd
import datatable as dt

#Read in Dexcom G6 dataset
g6_df = dt.fread('dexcomG6.csv').to_pandas()
g6_index = g6_df['MDR_REPORT_KEY'].copy() #Extract Index
#g6_index.to_csv('Index/g6index.csv')

#Read in Dexcom G5 dataset
g5_df = dt.fread('dexcomG5.csv').to_pandas()
g5_index = g5_df['MDR_REPORT_KEY'].copy() #Extract Index
#g5_index.to_csv('Index/g5index.csv')

#Read in Dexcom G4 dataset
g4_df = dt.fread('dexcomG4.csv').to_pandas()
g4_index = g4_df['MDR_REPORT_KEY'].copy() #Extract Index
#g4_index.to_csv('Index/g4index.csv')

#Create DataFrame with all Dexcom related Report keys
all_index = pd.concat([g6_index, g5_index, g4_index]).to_frame()

#Load in text data
txt_21 = dt.fread('foitext.txt').to_pandas()
txt_20 = dt.fread('foitext2020.txt').to_pandas()
txt_19 = dt.fread('foitext2019.txt').to_pandas()
txt_18 = dt.fread('foitext2018.txt').to_pandas()
txt_17 = dt.fread('foitext2017.txt').to_pandas()
txt_16 = dt.fread('foitext2016.txt').to_pandas()

#Combine files
txt_all = pd.concat([txt_21, txt_20, txt_19, txt_18, txt_17, txt_16])

#Filter text reports based on Dexcom specific cases
txt_index = pd.merge(all_index, txt_all, on = 'MDR_REPORT_KEY')

#Export the text
txt_index.to_csv('dexcom_txt_all.csv')