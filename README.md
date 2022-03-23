# Patient-Safety
DATA

Can be downloaded at this link: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm
Extract cases relating to Dexcom G4, G5, and G6 continuous glucose monitors.


CODE

TS.R - This file contains the time series analysis including STL decomposition, ARIMA model selection and forecasting. 

text_export.py - This file used foitext.txt for years 2016-2021. (Note: for the sake of storage, I will not upload these files) This file will subset all of the text reports relating to Dexcom CGM. The output dataset is dexcom_txt_all.csv.

text_cleaning.py - This file uses dexcom_txt_all.csv and subsets data to only contain original reports (no update reports). The output dataset is dexcom_txt_clean.csv.

preprocess_model.py - This file uses dexcom_txt_clean.csv. This file will preprocess the data and extract topics. The output file is topics_dataframe.csv.

Topic_TS.py - This file uses topics_dataframe.csv. This file is used to create the time series plots for topics.


PRESENTATION


FINAL REPORT

