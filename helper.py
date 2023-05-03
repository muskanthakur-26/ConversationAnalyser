import streamlit as st
from urlextract import URLExtract
import pandas as pd
import numpy as np
import squarify 
import matplotlib.pyplot as plt
from collections import Counter
import emoji
import seaborn as sns
extract=URLExtract()

def fetch_stats(person,df):
  st.title("Top Statistics")
  col1,col2,col3,col4=st.columns(4)
  if person != "Overall":
    df=df[df['user']==person]
  words=[]
  for msg in df['message']:
    words.extend(msg.split())
  link=[]
  for msg in df['message']:
    link.extend(extract.find_urls(msg))
  with col1:
    st.subheader("Total Messages")
    st.subheader(df.shape[0])
  with col2:
    st.subheader("Total Word")
    st.subheader(len(words))
  with col3:
    st.subheader("Media Shared")
    st.subheader(df[df['message']=='<Media omitted>\n'].shape[0])
  with col4:
    st.subheader("Links Shared")
    st.subheader(len(link))
    
def most_busy(df):
  x=df['user'].value_counts().head()
  df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
  return x,df

def CountFrequency(my_list):
   
    # Creating an empty dictionary
    d=dict()
    for item in my_list:
        if (item in d):
            d[item] += 1
        else:
            d[item] = 1
    
    return d
            
def visual(person,df):
  if person != "Overall":
    df=df[df['user']==person]

  wrd_list=[]
  for msg in df['message']:
    for i in msg.split():
      wrd_list.append(i)
  
  print(wrd_list)
  d=dict()
  d=CountFrequency(wrd_list)
  ke=[]
  val=[]
  for key in list(d.keys()):
    ke.append(key), val.append(d[key])
  new_df=pd.DataFrame({'word_l':ke,'value':val})
  
  # circles = circ.circlify(new_df, show_enclosure=True)
  # pp(circles)
  # # fig = px.scatter(new_df, x='value', y='word')
  # # fig.show()
  plt.switch_backend('TkAgg')
  squarify.plot(sizes=new_df['value'], label=new_df['word_l'], alpha=.8 )
  plt.axis('off')
  plt.show()

def most_common(person,df):
  
  if person != "Overall":
    df=df[df['user']==person]
    
  temp=df[df['user']!='group notification']
  temp=temp[temp['message']!='<Media omitted>\n']
  
  f=open("stop_words.txt",'r')
  stop=f.read()
  words=[]
  for msg in temp['message']:
    for i in msg.lower().split():
      if i not in stop:
        words.append(i)
        
  new_df=pd.DataFrame(Counter(words).most_common(26))
  
  fig,ax=plt.subplots()
  ax.barh(new_df[0],new_df[1])
  st.title("Most 26 Common Words")
  plt.xticks(rotation="vertical")
  # st.dataframe(new_df)
  st.pyplot(fig)
  
def emoji_com(person,df):
  
  if person != "Overall":
    df=df[df['user']==person] 
    
  emojis=[]
  for msg in df['message']:
    emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])
    
  emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
  col1,col2=st.columns(2)
  with col1:
    st.dataframe(emoji_df)
  with col2:
    fig,ax=plt.subplots()
    ax.pie(emoji_df[1].head(19),labels=emoji_df[0].head(19),autopct="%0.2f")
    st.pyplot(fig)
  
def month_time(person,df):
  if person != "Overall":
    df=df[df['user']==person] 
    
  tm_df=df.groupby(['year','month_num','month']).count()['message'].reset_index()
  
  time=[]
  
  for i in range(tm_df.shape[0]):
    time.append(tm_df['month'][i]+"-"+str(tm_df['year'][i]))
   
  tm_df['time']=time
  
  col1,col2=st.columns(2)
  with col1:
    st.dataframe(tm_df)
  with col2:
    fig,ax=plt.subplots()
    ax.plot(tm_df['time'],tm_df['message'],color="red")
    plt.xticks(rotation="vertical")
    st.pyplot(fig)
    
def daily_time(person,df):
  if person != "Overall":
    df=df[df['user']==person] 
    
  daily_df=df.groupby(['only_date']).count()['message'].reset_index()
  
  col1,col2=st.columns(2)
  with col1:
    st.dataframe(daily_df)
  with col2:
    fig,ax=plt.subplots()
    plt.figure(figsize=(25,25))
    ax.plot(daily_df['only_date'],daily_df['message'],color="red")
    plt.xticks(rotation="vertical")
    st.pyplot(fig)

def days(person,df):
  if person != "Overall":
    df=df[df['user']==person] 
    
  day_df=df.groupby(['day_name']).count()['message'].reset_index()
  
  col1,col2=st.columns(2)
  with col1:
    st.dataframe(day_df)
  with col2:
    fig,ax=plt.subplots()
    plt.figure(figsize=(25,25))
    ax.barh(day_df['day_name'],day_df['message'],color="red")
    plt.xticks(rotation="vertical")
    st.pyplot(fig)
    
def months(person,df):
  if person != "Overall":
    df=df[df['user']==person] 
    
  mon_df=df.groupby(['month']).count()['message'].reset_index()
  
  col1,col2=st.columns(2)
  with col1:
    st.dataframe(mon_df)
  with col2:
    fig,ax=plt.subplots()
    plt.figure(figsize=(25,25))
    ax.barh(mon_df['month'],mon_df['message'],color="red")
    plt.xticks(rotation="vertical")
    st.pyplot(fig)
    
def heat(person,df):
  if person != "Overall":
    df=df[df['user']==person] 
    
  user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
  fig,ax=plt.subplots()
  ax=sns.heatmap(user_heatmap)
  st.pyplot(fig)
  