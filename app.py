import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

#
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show  analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        #
        num_messages, words, num_media_messages, num_links = helper.fetch_starts(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messsges")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity map
        st.title("Activity map")
        col1, col2 = st.columns(2)
        fig,ax = plt.subplots()


        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        st.header("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest users in the group
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common used words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        ax.barh(most_common_df['Word'], most_common_df['Count'])

        #st.dataframe(most_common_df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df['Word'],most_common_df['Count'])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # # emoji anamlysis
        #
        emoji_df = helper.emoji_helper(selected_user,df)
        # st.title("Emoji Analysis")
        #
        # col1, col2 = st.columns(2)
        #
        #
        # with col1:
        #     st.dataframe(emoji_df)
        #
        # with col2:
        #     fig,ax = plt.subplots()
        #     ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%0.2f")
        #     st.pyplot(fig)

        # Check the structure of emoji_df
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        # Ensure emoji_df has the expected columns and structure
        if emoji_df is not None and not emoji_df.empty:
            if 0 in emoji_df.columns and 1 in emoji_df.columns:
                # If emoji_df has the expected structure, proceed with creating the pie chart
                with col2:
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                    st.pyplot(fig)
            else:
                # If emoji_df does not have the expected structure, display an error message
                st.error("Unexpected structure of emoji DataFrame. Please check the data.")
        else:
            # If emoji_df is empty or None, display a message indicating no data
            st.warning("No data available for emoji analysis.")



