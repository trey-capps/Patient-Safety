# Patient-Safety

## Extract Data

### Cloud Option

#### Download Data to GCP storage bucket

Data will be downloaded straight into a GCP bucket to  avoid saving the data locally. 

This can be done using the GCP Cloud Shell. The data will be downloaded from [here](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm). This data will be a ```.zip``` file which will need to be unzipped using the Cloud Shell as well. 

We have two datasets for the years 2016 to 2021. 

#### Device Data 

Device data contains all the information about the device.

2021 Example:

Ingest the data into a GCP storage bucket...

```curl https://www.accessdata.fda.gov/MAUDE/ftparea/device2021.zip | gsutil cp - gs://maude-device-reports/device2021.zip```


```gsutil cat gs://maude-device-reports/device2021.zip | zcat |  gsutil cp - gs://maude-device-reports/device2021.txt```

#### Narative Data 

Narrative data contains all the text that has been submitted with the device malfunction report. 

2021 Example:

```curl https://www.accessdata.fda.gov/MAUDE/ftparea/foitext2021.zip | gsutil cp - gs://maude-device-reports/foitext2021.zip```


```gsutil cat gs://maude-device-reports/foitext2021.zip | zcat |  gsutil cp - gs://maude-device-reports/foitext2021.txt```

#### Setting Up Jupyter on Cloud Dataproc
Using the Cloud Shell...

Set environment variables
```
REGION=[ADD REGION]
CLUSTER_NAME=[ADD CLUSTER NAME]
BUCKET_NAME=[ADD BUCKET NAME]
```

```
gcloud dataproc clusters create ${CLUSTER_NAME} \
    --bucket=${BUCKET_NAME} \
    --optional-components=JUPYTER \
    --region=${REGION} \
    --enable-component-gateway
```

Ensure you do not leave out ```--enable-component-gateway``` as this will provide authenticated and secure access to JupyterLab

### Local Option

In the home directory run: ```python extract_data.py``` to extract device and text data for 2016 to 2021


## Data Cleaning

```jupyter-dexcom_cleaning.ipynb``` uses Spark SQL to join device and narrative dataset along with concatenating all the years into one dataset. Only the original device reports (not the updated entries) will be used for topic modeling. These are specified as ```TEXT_TYPE_CODE == 'N'```. We can also filter only the Dexcom entries and export the new file.

### Dataproc Cluster
After your Dataproc cluster is setup, you can launch the Jupyter Notebook UI to clean the data through GCP


## Old README
PURPOSE

The purpose of this analysis was to look at patient reports based on Dexcom continuous glucose monitor issues. Time series forecasting and analysis along with topic modeling was used to model topics over time. 


DATA

Can be downloaded at this link: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm
Extract cases relating to Dexcom G4, G5, and G6 continuous glucose monitors.


CODE

TS.R - This file contains the time series analysis including STL decomposition, ARIMA model selection and forecasting. 

text_export.py - This file used foitext.txt for years 2016-2021. (Note: for the sake of storage, I will not upload these files) This file will subset all of the text reports relating to Dexcom CGM. The output dataset is dexcom_txt_all.csv.

text_cleaning.py - This file uses dexcom_txt_all.csv and subsets data to only contain original reports (no update reports). The output dataset is dexcom_txt_clean.csv.

preprocess_model.py - This file uses dexcom_txt_clean.csv. This file will preprocess the data and extract topics. The output file is topics_dataframe.csv.

Topic_TS.py - This file uses topics_dataframe.csv. This file is used to create the time series plots for topics.


PRESENTATION: PatientSafe_Presentation.pptx
FINAL REPORT: PatientSafe_FinalReport.pdf