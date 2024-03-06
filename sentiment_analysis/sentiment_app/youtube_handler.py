import os

from dotenv import load_dotenv
from googleapiclient.discovery import build


def get_video_comments(video_id, youtube):
    nextPageToken = None
    comments = []
    while True:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100,  # Maximum number of comments per page
            pageToken=nextPageToken
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
    print(len(comments))
    return comments


def get_video_info(youtube_url):
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    video_id = youtube_url.split('=')[-1]
    comments = get_video_comments(video_id, youtube)
    for comment in comments:
        print(comment)


