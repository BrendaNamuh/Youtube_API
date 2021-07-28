import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation
from itertools import count
from matplotlib import animation

'''

- most liked channel
- least viewed video you liked
- most viewed video you like
- Animated bar chart representing likes given over time to 10 channels.

'''


# Converts string to date object
def string_toDateTime(date_string):
    return datetime.date(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:10]))


today = datetime.date.today()

df = pd.read_csv('Liked_videos_detailed.csv')

df.columns = ['Title', 'Channel', 'Duration', 'Views', 'Likes', 'Dislikes', 'Date']

# Convert all dates to date objects
df['Date'] = df['Date'].apply(lambda x: string_toDateTime(x))


# Returns data from the last "day_range" days
def filter_byDate(df, day_range):
    # No date filter
    if day_range is None:
        return df
    else:
        delta = datetime.timedelta(days=day_range)
        min_day = today - delta
        df_filtered_bydate = df[df['Date'] >= min_day]
        return df_filtered_bydate


# Returns most liked channel, within day range
def most_liked_channel(df, day_range):
    df_filtered_bydate = filter_byDate(df, day_range)
    result = df_filtered_bydate.Channel.value_counts().idxmax()
    nmbr_likes = max(df_filtered_bydate.Channel.value_counts())
    print("In the last {} days you have liked {} videos.\n"
          "The most liked channel is {} with {} likes!".format(day_range, df_filtered_bydate.shape[0], result,
                                                               nmbr_likes))

    return df_filtered_bydate.Channel.value_counts().idxmax()


# Returns least viewed video, liked within day range
def least_viewed(df, day_range):
    data = filter_byDate(df, day_range)
    min_vid = data.Views.idxmin()
    title = df['Title'][min_vid]
    views = df['Views'][min_vid]
    print('The video you liked with the least views is "{}"\nwith {} views!\n'.format(title, views))
    return df['Title'][min_vid]


# Returns most viewed video, liked within day range
def most_viewed(df, day_range):
    data = filter_byDate(df, day_range)
    max_vid = data.Views.idxmax()
    title = df['Title'][max_vid]
    views = df['Views'][max_vid]
    print('The video you liked with the most views is "{}"\nwith {} views!'.format(title, views))
    return df['Title'][max_vid]


# Return name
def topten_likedChannels(df):
    df = df.Channel.value_counts()
    topten = df[:10].index
    return topten.tolist()


# Used to animate chart
def animate(i):
    # Display date of incoming like
    axes.text(4.5, 35, df.Date.iloc[i], style='italic',
              bbox={'facecolor': 'pink', 'alpha': 0.5, 'pad': 10})

    # Channel of incoming like
    curr_channel = df.Channel.iloc[i]

    # Update y axis
    likes[(topChannels.index(curr_channel))] += 1

    # Construct plot
    plt.bar(topChannels, likes)


if __name__ == '__main__':
    # -------------- Prepare data for plot

    # 10 most liked channels
    topChannels = topten_likedChannels(df)

    # Filter df to only include top ten liked channels
    df = df.loc[df.Channel.isin(topChannels)]

    # Sort by date
    df = df.sort_values(by='Date')

    # Restrict to channel and date attribute
    df = df[['Channel', 'Date']]

    # Initialize y axis of plot
    likes = [0] * len(topChannels)

    #--------------- Set up figure and plot

    # Initiate chart figure
    fig = plt.figure(figsize=(12, 5))

    # Add an Axes to the figure as part of a subplot arrangement.
    axes = fig.add_subplot()
    axes.set_ylim(0, 50)
    axes.set_xlim(0, 10)

    fig.autofmt_xdate()
    ani = FuncAnimation(fig=fig, func=animate, interval=1, repeat=False)

    plt.show()

