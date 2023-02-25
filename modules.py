import pandas as pd
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji
import nltk
nltk.download('vader_lexicon')
nltk.download('stopwords')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

extractor = URLExtract()

def get_stats(selected_user,df):

    if selected_user != 'Overall':
       df =  df[df['user'] == selected_user]
        
    num_msg =  df.shape[0]
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    urls = []
    for msg in df['message']:
        urls.extend(extractor.find_urls(msg))

    #most_active =  df['user'].value_counts().head()
    



    return num_msg,len(words),media,len(urls)

def most_busy_users(df):
    X = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return X,df

def Create_WordCloud(selected_user,df):
    
    if selected_user != 'Overall':
       df =  df[df['user'] == selected_user]
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):

    f = open('C:/Users/Rohan/WhatApp-Analyzer/stop_hinglish.txt','r')
    stop_words =  f.read()

    if selected_user != 'Overall':
       df =  df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    temp_df = pd.DataFrame(Counter(words).most_common(20))

    return temp_df

def most_common_emojis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend(emoji.distinct_emoji_list(message))

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    

    return df['month'].value_counts()

def analyze_sentiment(selected_user,df):

    f = open('C:/Users/Rohan/WhatApp-Analyzer/stop_hinglish.txt','r')
    stop_words =  f.read()

    if selected_user != 'Overall':
       df =  df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    stop_words_nltk = set(stopwords.words('english'))

    filtered_words = [word for word in words if word not in stop_words_nltk]

    sentiments = SentimentIntensityAnalyzer()

    sentiment_scores = {"pos": 0, "neg": 0, "neu": 0}
    for word in filtered_words:
        scores = sentiments.polarity_scores(word)
        if scores["compound"] > 0:
            sentiment_scores["pos"] += 1
        elif scores["compound"] < 0:
            sentiment_scores["neg"] += 1
        else:
            sentiment_scores["neu"] += 1

    

    # Calculate the final sentiment for the list of words
    if sentiment_scores["pos"] > sentiment_scores["neg"]:
        return str("Overall Sentiment: Positive")
    elif sentiment_scores["pos"] < sentiment_scores["neg"]:
        return str("Overall Sentiment: Negative")
    else:
        return("Overall Sentiment: Neutral")
        
        








   

