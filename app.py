install requirements.txt
import streamlit as st
import helper as hp
import matplotlib.pyplot as plt
import seaborn as sns
st.title('Whatsapp chat analyzer')

t_format=st.sidebar.selectbox('Time Format',['12 Hour','24 Hour'])
file=st.sidebar.file_uploader('upload a txt file')
if file is not None:
    file=file.getvalue()
    data=file.decode(encoding='utf-8')
    df=hp.transformer(data,t_format)
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox('show analysis wrt',user_list)
    df=hp.filter_df(selected_user, df)
    if st.sidebar.button('Show analysis'):
       col1,col2,col3,col4=st.columns(4)
       no_msg,no_word,no_media,no_urls=hp.stats(df)
       with col1:
           st.header('Total Messages')
           st.text(no_msg)
       with col2:
            st.header('Total Words')
            st.text(no_word)
       with col3:
          st.header('Total Media')
          st.text(no_media)
       with col4:
          st.header('URLs')
          st.text(no_urls)
       
       if selected_user=='Overall':
          st.header('Contribution of Users')
          contri_df=hp.contribution(df)
          fig,ax=plt.subplots()
          col5,col6=st.columns(2)
          with col5:
              ax.bar(contri_df['name'],contri_df['Contribution'])
              plt.xticks(rotation='vertical')
              st.pyplot(fig)
          with col6:
              st.dataframe(contri_df)
      
       st.header('Most used words')
       im=hp.im_wc(df)
       fig,ax=plt.subplots()
       plt.figure()
       ax.imshow(im)
       st.pyplot(fig)
       
       mcw_df=hp.most_common_words(df)
       fig,ax=plt.subplots()
       ax.barh(mcw_df[0],mcw_df[1])
       st.pyplot(fig)
       
       st.header('timeline')
       timeline=hp.monthly_timeline(df)
       fig,ax=plt.subplots()
       ax.plot(timeline['time'],timeline['message'])
       plt.xticks(rotation='vertical')
       st.pyplot(fig)
       
       st.header('weekly activity')
       week_df=hp.week_activity_map(df)
       fig,ax=plt.subplots()
       ax.bar(week_df['day'],week_df['Messages'])
       plt.xticks(rotation='vertical')
       st.pyplot(fig)
       
       st.header('Monthly activity')
       month_df=hp.month_activity_map(df)
       fig,ax=plt.subplots()
       ax.bar(month_df['month'],month_df['Messages'])
       plt.xticks(rotation='vertical')
       st.pyplot(fig)
       
       st.header('activity heatmap')
       heatmap=hp.activity_heatmap(df)
       fig,ax=plt.subplots()
       ax=sns.heatmap(heatmap)
       st.pyplot(fig)
       
else:
    st.text('Upload a valid file')









    
    
    
    
    
    
    

