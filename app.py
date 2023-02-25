import streamlit as st
import PreProcessor
import modules
import matplotlib.pyplot as plt



st.sidebar.title("WhatsApp Chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = PreProcessor.process(data)
    st.dataframe(df)
    

    user_list = df['user'].unique().tolist()

    
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)


    if st.sidebar.button("Show analysis"):
        st.title("Top Statistics:")
        col1, col2, col3, col4 = st.columns(4)

        Num_msg,num_words,num_media,num_links = modules.get_stats(selected_user,df)

        with col1:
            st.header("Total Messages")
            st.title(Num_msg)

        with col2:
            st.header("Total words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Total Links Shared")
            st.title(num_links)

        #Monthly Timeline
        st.title("Monthly Timeline:")
        timeline = modules.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity based on day
        st.title('Activity Map:')
        col9, col10 = st.columns(2)

        with col9:
            st.title('Most Busy Days:')
            busy_day = modules.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col10:
            st.title('Most Busy Month:')
            busy_month = modules.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.barh(busy_month.index,busy_month.values)
            st.pyplot(fig)


        

        if selected_user == "Overall":
            st.title("Most Active Users:")
            x,new_df = modules.most_busy_users(df)
            fig, ax = plt.subplots()
       
            col5, col6 = st.columns(2)

            with col5:
                fig, ax = plt.subplots()
                ax.bar(x.index,x.values)
                st.pyplot(fig)

            with col6:
                st.dataframe(new_df)

        #wordcloud
    
        st.title("Wordcloud:")
        df_wc = modules.Create_WordCloud(selected_user,df)
        fig, ax= plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most Common Words
        st.title("Top 20 Words:")
        col7, col8 = st.columns(2)
        
        with col7:
                
                top_words = modules.most_common_words(selected_user,df)
                st.dataframe(top_words)
        with col8:
                fig, ax = plt.subplots()

                ax.barh(top_words[0].head(),top_words[1].head())
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        #Top emojis
        st.title("Top 10 Emojis:")
        top_emojis = modules.most_common_emojis(selected_user,df)
        st.dataframe(top_emojis.head(10))

        #sentiment analysis
        st.title("Sentiment Analysis:")
        sentiment = modules.analyze_sentiment(selected_user,df)
        
        st.title(sentiment)

        








