#Load Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datatable as dt

#Load Datasets
#Topics
topics = pd.read_csv('topics_dataframe.csv')
#Dates
g6 = dt.fread('dexcomG6.csv').to_pandas()
g6_date = g6[['MDR_REPORT_KEY', 'DATE_RECEIVED']].copy()

g6_date.set_index(['MDR_REPORT_KEY'], inplace = True)
topics.set_index(['MDR_REPORT_KEY'], inplace = True)

#Combine topics and dates
joined = g6_date.join(topics)

joined.reset_index(inplace = True)
joined['DATE_RECEIVED'] = pd.to_datetime(joined['DATE_RECEIVED'], format = '%Y-%m-%d')
joined = joined.set_index('DATE_RECEIVED')

#Select Topic for each report
joined['Selected_Topic'] = joined[['Topic {0}'.format(x) for x in range(1, 4)]].idxmax(axis=1)    

t_1 = joined[joined['Selected_Topic'] == 'Topic 1'].copy()
t_2 = joined[joined['Selected_Topic'] == 'Topic 2'].copy()
t_3 = joined[joined['Selected_Topic'] == 'Topic 3'].copy()

def create_ts(df, freq = 'M'):
    '''
    This function will take df and create time series sampled by freq (Month)
    '''
    df['tot'] = 1
    df = df.resample(freq).sum()
    df_tot = df.groupby(df.index)['tot'].agg('sum').to_frame()
    return df_tot

#Create time series datasets
t_1_ts = create_ts(t_1)
t_2_ts = create_ts(t_2)
t_3_ts = create_ts(t_3)

#Create dictionary to store datasets
all_ts = {'Topic 1 - Transmitter' : t_1_ts, 'Topic 2 - Signal' : t_2_ts, 'Topic 3 - Glucose Reading' : t_3_ts}

#Plot combined time series
plt.figure(figsize = (20, 5))
for topic in all_ts:
    plt.plot(all_ts.get(topic), label = topic)

plt.title('Topics of Reports Over Time', size = 20)
plt.xlabel('Time', size = 18)
plt.xticks(size = 15)
plt.ylabel('Total Number of Reports (Per Month)', size = 18)
plt.yticks(size = 15)
plt.legend(prop = {'size': 15})
plt.show()

def plot_series(observed = True, ma = True, WINDOW = 6):
    '''
    This function will plot the observed and WINDOW (month) length moving average.
    '''
    for topic in all_ts:
        plt.figure(figsize = (20, 5))
        
        if observed:
            plt.plot(all_ts.get(topic))
        if ma:
            rolling = all_ts.get(topic).rolling(window = WINDOW).mean()
            plt.plot(rolling, color = 'green', label = '{0} Month Moving Average'.format(WINDOW))
            plt.legend(prop = {'size': 15})
        plt.title(topic, size = 20)
        plt.xlabel('Time', size = 18)
        plt.xticks(size = 15)
        plt.ylabel('Total Number of Reports (Per Month)', size = 18)
        plt.yticks(size = 15)
        plt.show()

#Plot individual series
plot_series()

#Export Topics Dataset
joined.to_csv('chose_topic.csv')