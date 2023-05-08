import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
    
st.set_page_config(layout="wide")
st.sidebar.title('Conversation Analyser')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)
    data=bytes_data.decode("utf-8")
    #st.text(data)
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    #print(data)
    #st.write(data)
    unique_users=df['user'].unique().tolist()
    unique_users.remove('group notification')
    unique_users.sort()
    unique_users.insert(0,"Overall")
    selected=st.sidebar.selectbox("Show Analysis wrt",unique_users)
    
    st.sidebar.button("Show Analysis", on_click=helper.fetch_stats,args=(selected,df))
    #most frequent user
    if selected=="Overall":
        st.subheader("Most Busy Users")
        x,new_df=helper.most_busy(df)
        fig,ax=plt.subplots()
        col1,col2=st.columns(2)
        with col1:
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
            
    if st.button('Show Word Count Analysis'):
        helper.visual(selected,df)
        
    if st.button('Show Most Common 26 Words'):
        helper.most_common(selected,df)
    
    if st.button('Show Most Common 19 Emojis'):
        helper.emoji_com(selected,df)
    
    if st.button('Show Monthly  Timeline'):
        helper.month_time(selected,df)
        
    if st.button('Show Daily  Timeline'):
          helper.daily_time(selected,df)
            
    if st.button('Show Month Activity  Timeline'):
          helper.days(selected,df)
          
    if st.button('Show Day Activity  Timeline'):
          helper.months(selected,df)
          
    if st.button('Show Activity Heatmap Timeline'):
          helper.heat(selected,df)
            
            
    
    
