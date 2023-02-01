import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    ## Conveting byte stream data into string
    data = bytes_data.decode('utf-8')

    ## Preprocessing data and returning dataframe
    df = preprocessor.preprocess(data)

    ## Getting users list
    users_list = df['user'].unique().tolist()


    ## Removing group nortification, adding overall and sorting the users list
    if 'group_nortification' in users_list:
        users_list.remove('group_nortification')
    users_list.sort()
    users_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show Analysis w.r.t", users_list)

    ## Adding button for showing analysis
    if st.sidebar.button('Show Analysis'):

        num_messages, words, media, links = helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')
        col1, col2, col3, col4, = st.columns(4)

        with col1: 
            st.header('Total Messages')
            st.title(num_messages)
        
        with col2: 
            st.header('Total Words  ')
            st.title(words)

        with col3: 
            st.header('Total Media Files')
            st.title(media)

        with col4: 
            st.header('Total Links  ')
            st.title(links)

        ## Daily Timeline
        st.title('Daily Message Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()

        plt.ylabel('Number of Messages')
        plt.xlabel('Days')
        plt.xticks(rotation = 'vertical')
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color = 'red')
        st.pyplot(fig)

        ## Monthly Timeline
        st.title('Monthly Messages Timeline')
        monthly_timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()

        plt.ylabel('Number of Messages')
        plt.xlabel('Month')
        plt.xticks(rotation = 'vertical')
        ax.plot(monthly_timeline['time'], monthly_timeline['message'], color = 'green')
        st.pyplot(fig)
    
        ## Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day = helper.weekly_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'pink')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most busy month')
            busy_day = helper.monthly_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        ## Activity Heatmap
        st.title("Activity HeatMap")
        heatmap_data = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(heatmap_data)
        st.pyplot(fig)
        
        ## Finding the Busiest Users in the group
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            top_5_users, user_freq = helper.frequent_users(df)
            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(top_5_users.index, top_5_users.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(user_freq)

        ## Wordcloud

        # df_wc = helper.create_wordcloud(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.imshow(df_wc)
        # st.pyplot(fig)

        ## Most common words
        st.title("Most Used Words")
        most_common_words_df = helper.most_common_words(selected_user = selected_user, dataframe=df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_common_words_df)
        with col2:      
            fig,ax = plt.subplots()
            ax.barh(most_common_words_df['Word'], most_common_words_df['Frequency'])
            st.pyplot(fig)

        ## Most common emojis
        st.title("Most Used Emojis")
        most_used_emojis_df = helper.most_used_emoji(selected_user = selected_user, dataframe=df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_used_emojis_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(most_used_emojis_df['Frequency'].head(), labels = most_used_emojis_df['Emoji'].head(), autopct = '%0.2f' )
            st.pyplot(fig)  