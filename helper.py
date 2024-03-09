import pandas as pd
import re
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter 

def transformer(data,time_format):
    if time_format=='12 Hour':
            pattern = '\\d{2}/\\d{2}/\\d{4},\\s\\d{1,2}:\\d{2}\\s[a-z][a-z]\\s-\\s'
            dates=re.findall(pattern,data)
            rep=lambda x: x.replace('\\u202f', ' ')
            dates=[i for i in map(rep,dates)]
            dates=pd.to_datetime(dates, format='%d/%m/%Y, %I:%M %p - ')
    else:
            pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
            dates = re.findall(pattern, data)    
    msg=re.split(pattern,data)[1:]
    df=pd.DataFrame({'msg':msg,'date':dates})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M - ')
    df['year']=df['date'].dt.year
    df['hour']=df['date'].dt.hour
    df['hour_range'] = df['hour'].apply(lambda x: str(x)+'-'+str(int(x)+1))
    df['month']=df['date'].dt.month_name()
    df['dow']=df['date'].dt.day_name()
    df['user'], df['message'] = zip(*df['msg'].apply(lambda x: (x.split(': ')[0][0:15], x.split(': ')[1].strip()) if len(x.split(':')) > 1 else ('group_notification',x )))
    df.drop('msg',axis=1,inplace=True)
    return df
wc=WordCloud(height=1000,width=1000,background_color='white')
extract=URLExtract()

def filter_df(selected_usr,df):
    if selected_usr=='Overall':
       return  df
    else:
     return  df[df.user==selected_usr]

def stats(df):
    
    msgs=df.shape[0]
    words=[]
    for msg in df['message']:
        words.extend(msg.split(' '))
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    
    return msgs,len(words),num_media_messages,len(links)

def contribution(df):
    total=df.shape[0]
    x=df['user'].value_counts() 
    df1=pd.DataFrame({'name':x.index,'Contribution':x.values})
    df1['cont_per']=df1['Contribution']/(total/100)
    return df1

def most_common_words(df):

    words_l=words_f(df)
    most_common_df = pd.DataFrame(Counter(words_l).most_common(20))
    return most_common_df

def im_wc(df):
    
    word_l=words_f(df)
    im=wc.generate(' '.join(word_l))
    return im

def words_f(df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    words_list = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words_list.append(word)
    return words_list

def monthly_timeline(df):
    
    df=df.sort_values(by='date')
    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def week_activity_map(df):
    x=df['dow'].value_counts() 
    df1=pd.DataFrame({'day':x.index,'Messages':x.values})
    return df1

def month_activity_map(df):
     x=df['month'].value_counts() 
     df1=pd.DataFrame({'month':x.index,'Messages':x.values})
     return df1

def activity_heatmap(df):
    user_heatmap = df.pivot_table(index='dow', columns='hour_range', values='message', aggfunc='count').fillna(0)

    return user_heatmap