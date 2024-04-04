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
            pageToken=nextPageToken
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
    return comments


def get_comments(youtube_url):
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_id = youtube_url.split('v=')[1]

    comments = get_video_comments(video_id, youtube)
    return comments



