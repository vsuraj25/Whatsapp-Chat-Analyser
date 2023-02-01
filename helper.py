from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, dataframe):
    
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]

    ## 1.fetching number of messages
    no_of_msg =  dataframe.shape[0]

    ## 2. fetching number of words
    words = []
    for msg in dataframe['message']:
        words.extend(msg.split())
    no_of_words = len(words)

    ## 3. fetching number or media files
    no_of_media_msg = dataframe[dataframe['message'] == '<Media omitted>'].shape[0]

    ## 4. Fetching all links
    url_extractor = URLExtract()
    links = []
    for msg in dataframe['message']:    
        links.extend(url_extractor.find_urls(msg))
    no_of_links = len(links)

    return no_of_msg, no_of_words, no_of_media_msg, no_of_links

## Finding the Busiest Users in the group
def frequent_users(dataframe):
    top_5_user = dataframe['user'].value_counts().head()

    user_freq_df = round((dataframe['user'].value_counts()/dataframe.shape[0])*100,2).reset_index().rename(columns={'index': 'User', 'user': 'Usage Percent'})
    
    return top_5_user, user_freq_df
    
# def create_wordcloud(selected_user, dataframe):
#     if selected_user != 'Overall':
#         dataframe = dataframe[dataframe['user'] == selected_user]

#     wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
#     df_wc = wc.generate(dataframe['message'].str.cat(sep = " "))
#     return df_wc

## Most Frequent Words
def most_common_words(selected_user, dataframe):
    file = open(file = 'stopwords-hinglish.txt', mode = 'r', encoding = 'utf-8')
    stopwords = file.read()
    if selected_user != 'Overall':       
        dataframe = dataframe[dataframe['user'] == selected_user]
    temp = dataframe[dataframe['user'] != 'group_nortification']
    temp = temp[temp['message'] != '<Media omitted>']

    words = []

    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stopwords:
                words.append(word)
    
    common_words_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
    return common_words_df

## Most Used Emojis
def most_used_emoji(selected_user, dataframe):
    if selected_user != 'Overall':       
        dataframe = dataframe[dataframe['user'] == selected_user]
        
    emojis = []
    for message in dataframe['message']:
        emojis.extend([e for e in message if e in list(emoji.get_emoji_unicode_dict('en').values())])
    most_freq_emojis = pd.DataFrame(Counter(emojis).most_common(len(emojis)), columns = ['Emoji', 'Frequency'])
    return most_freq_emojis

## Monthly Timeline
def monthly_timeline(selected_user, dataframe):
    if selected_user != 'Overall':       
        dataframe = dataframe[dataframe['user'] == selected_user]
    
    timeline = dataframe.groupby(['year', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time
    
    return timeline

## Daily Timeline
def daily_timeline(selected_user, dataframe):
    if selected_user != 'Overall':       
        dataframe = dataframe[dataframe['user'] == selected_user]

    daily_timeline = dataframe.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

## Weekly Activity Map  
def weekly_activity_map(selected_user, dataframe):
    if selected_user != 'Overall':       
        dataframe = dataframe[dataframe['user'] == selected_user]
    
    return dataframe['day_name'].value_counts()

## Monthly Activity Map  
def monthly_activity_map(selected_user, dataframe):
    if selected_user != 'Overall':       
        dataframe = dataframe[dataframe['user'] == selected_user]
    
    return dataframe['month'].value_counts()

def activity_heatmap(selected_user, dataframe):
    if selected_user != 'Overall':       
        dataframe = dataframe[dataframe['user'] == selected_user]

    period_df = dataframe.pivot_table(index='day_name', columns='period', values = 'message', aggfunc='count').fillna(0)

    return period_df