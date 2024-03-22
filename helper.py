from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import re
def fetch_starts(selected_user, df):
    extract = URLExtract()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of message
    num_messages = df.shape[0]

    # fetch the total number of words

    words = []
    for message in df['messages']:
        if message != '<Media omitted>\n':  # Filter out media omitted messages
            words.extend(message.split())

    # fetch number of media
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['messages']:
        if message != '<Media omitted>\n':  # Filter out media omitted messages
            links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def remove_stop_words(message, stop_words):
    if message == '<Media omitted>\n':
        return ''
    y = []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)

def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove media omitted messages
    df = df[df['messages'] != '<Media omitted>\n']

    # Remove stop words
    df['messages'] = df['messages'].apply(lambda x: remove_stop_words(x, stop_words))

    wc = WordCloud(width=500, height=500, max_font_size=100, background_color='white')
    temp = df[['messages']].copy()

    # Generate word cloud
    df_wc = wc.generate(temp['messages'].str.cat(sep=""))
    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove media omitted messages
    df = df[df['messages'] != '<Media omitted>\n']

    words = []
    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.Dat


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x, df

def remove_stop_words(message, stop_words):
    y = []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)


def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out "<Media omitted>" messages
    df = df[df['messages'] != '<Media omitted>\n']

    # Remove stop words
    df['messages'] = df['messages'].apply(lambda x: remove_stop_words(x, stop_words))

    # Concatenate messages
    messages = df['messages'].str.cat(sep=" ")

    wc = WordCloud(width=500, height=500, max_font_size=100, background_color='white')

    # Generate word cloud
    df_wc = wc.generate(messages)

    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove stop words and count common words
    words = []
    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    if words:  # Check if there are words
        most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])
        return most_common_df
    else:
        # Return an empty DataFrame if no common words found
        return pd.DataFrame(columns=['Word', 'Count'])

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name' , columns= 'period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap







# def most_common_words(selected_user, df):
#     with open('stop_hinglish.txt', 'r') as f:
#         stop_words = f.read().splitlines()
#
#     if selected_user == 'Overall':
#         temp = df[df['user'] != 'group_notification']
#         temp = temp[temp['messages'] != '<Media omitted>\n']
#     else:
#         temp = df[df['user'] == selected_user]
#
#     words = []
#
#     # Iterate through each message
#     for message in temp['messages']:
#         # Split the message into words
#         for word in message.lower().split():
#             # Check if the word is not in the stop words list
#             if word not in stop_words:
#                 words.append(word)
#
#     # Create a DataFrame with the 20 most common words
#     most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])
#
#     return most_common_df
