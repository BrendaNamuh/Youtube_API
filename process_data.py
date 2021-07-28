from datetime import date, timedelta
from googleapiclient.discovery import build
import csv
import numpy as np
import pandas as pd

# Construct ressource object to interact with API
youtube_api = build('youtube', 'v3', developerKey='AIzaSyCQh9TEVHr0Ku1if32h3GzmLC7miNjjjNg', )

# Result of search (is an object). Data is not persistent.
query = youtube_api.videos()


def get_video_info(video_id, req):
    request = query.list(part='snippet,contentDetails,statistics', id=video_id)
    result = request.execute()
    video_info = result['items']

    for category in video_info:
        names = category['snippet']
        stats = category['statistics']
        length = category['contentDetails']
        print(names['title'])

        try:
            like_count = stats['likeCount']
            dislike_count = stats['dislikeCount']

        # Some videos do not share (dis)like count
        except:
            like_count = None
            dislike_count = None

        return [names['title'], names['channelTitle'], length['duration'],
                stats['viewCount'], like_count, dislike_count]


df = pd.DataFrame(columns=('Title', 'Channel', 'Duration', 'ViewCount', 'Likes', 'Dislikes', 'TimeAdded'))

# Return new Likes file with added details from youtube API
with open('Liked videos.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    with open('Liked_videos_detailed.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file)

        for index, line in enumerate(csv_reader):

            if index < 4 or not line: continue  # Skip 4 first lines & empty lines

            # Uses video id to retrieve more information about video from query
            new_row = get_video_info(line[0], query)

            # Returns None if there are no details from video id by API
            if new_row is None: continue

            # Add date from reading file
            new_row.append(line[1][0:11])

            csv_writer.writerow(new_row)
