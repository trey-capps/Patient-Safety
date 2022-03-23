#Load Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

#Load dataset
txt_all_df = pd.read_csv('dexcom_txt_clean.csv')

#Subset to only G6
txt_df = txt_all_df[txt_all_df['G6'] == 1].copy()

#Create list of report text
text = txt_df['FOI_TEXT'].to_list()

#Remove Regular Expressions
text = [re.sub(r'[^a-zA-Z0-9]', ' ', i) for i in text]


#Lowercase and tokenize the text
for i in range(0, len(text)):
    text[i] = text[i].lower().split()


#Remove and Update Stop Words
stop_words = stopwords.words('english')
stop_words.extend(['b', 'via', 'cgm', 'and', 'the', 'also', 'you', 'your', '2018', '6', '4'])
stop_words.remove('not')

for i in range(0, len(text)):
    for j in range(0, len(text[i])):
        if text[i][j] in stop_words:
            text[i][j] = ''


#Lemmatization
lemmatizer = WordNetLemmatizer()
for i in range(0, len(text)):
    for j in range(0, len(text[i])):
        text[i][j] = lemmatizer.lemmatize(text[i][j])


split_text = text.copy()

#Rejoin preprocessed text
for i in range(0, len(text)):
    text[i] = ' '.join(text[i])

#Remove white space
for i in range(0, len(text)):
    text[i] = re.sub(' +', ' ', text[i])

#Look at first report
print(text[0])

#Export the dataset with new text column
txt_df['clean_text'] = text
txt_df.reset_index(inplace = True)

#TF-IDF
vectorizer = TfidfVectorizer(stop_words = stop_words, lowercase = True)
tfidf_text = vectorizer.fit_transform(txt_df['clean_text'])

#Create dataframe for 
data_dtm_noun = pd.DataFrame(tfidf_text.toarray(), columns=vectorizer.get_feature_names())


#LDA
from sklearn.decomposition import LatentDirichletAllocation
#Specify Model
lda_mod = LatentDirichletAllocation(n_components = 3, max_iter = 10, random_state = 42)
#Fit Model
lda_fit = lda_mod.fit_transform(tfidf_text)
#Get topics and words
words_lda = vectorizer.get_feature_names()
topics_lda = lda_mod.components_
#View words for each topic
for i, topic in enumerate(topics_lda):
    sort_topic = np.argsort(topic)
    topics = np.array(words_lda)[sort_topic]
    print('Topic {0}: '.format(i + 1))
    print(topics)
#Show weights for each report
choose_topic_lda = lda_mod.transform(tfidf_text)
print(choose_topic_lda)


#NMF
from sklearn.decomposition import NMF
#Specify and fit model
NUM_TOPICS = 3
nmf_mod = NMF(NUM_TOPICS)
doc_topic = nmf_mod.fit_transform(tfidf_text)
#Get topics and words
words_nmf = vectorizer.get_feature_names()
topics_nmf = nmf_mod.components_
#View top 10 words for each topic
for i, topic in enumerate(topics_nmf):
    sort_topic = np.argsort(topic)
    topics = [words_nmf[i] for i in topic.argsort()[:-10 - 1:-1]]
    print('Topic {0}: '.format(i + 1))
    print(topics)

#Show weights for 1st report
case_topic_nmf = nmf_mod.transform(tfidf_text)
print(case_topic_nmf[0])

#Export Topics from NMF
topics = pd.DataFrame(data = case_topic_nmf, columns=['Topic {0}'.format(x) for x in range(1, NUM_TOPICS+1)])


#LSA
from sklearn.decomposition import TruncatedSVD
#Specify and fit model
lsa_mod = TruncatedSVD(n_components = 3, random_state = 42)
lsa_fit = lsa_mod.fit_transform(tfidf_text)
#Get topics and words
words_lsa = vectorizer.get_feature_names()
topics_lsa = lsa_mod.components_
#View top 10 words for each topic
for i, topic in enumerate(topics_lsa):
    sort_topic = np.argsort(topic)
    topics = [words_lsa[i] for i in topic.argsort()[:-10 - 1:-1]]
    print('Topic {0}: '.format(i + 1))
    print(topics)

#View first report classification
print(lsa_fit[0])

#Export Final Topic Dataframe
topics_df = pd.concat([txt_df, topics], axis = 1)
topics_df.to_csv('topics_dataframe.csv', index = False)