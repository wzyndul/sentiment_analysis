import os

from dotenv import load_dotenv
from googleapiclient.discovery import build


def get_video_comments(video_id, youtube):
    channel_data = {}

    video_response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()
    channel_id = video_response['items'][0]['snippet']['channelId']
    channel_name = video_response['items'][0]['snippet']['channelTitle']
    published_time = video_response['items'][0]['snippet']['publishedAt']
    vido_title = video_response['items'][0]['snippet']['title']

    channel_response = youtube.channels().list(
        part="snippet",
        id=channel_id
    ).execute()
    channel_picture_url = channel_response['items'][0]['snippet']['thumbnails']['default']['url']

    channel_data['channel_id'] = channel_id
    channel_data['channel_name'] = channel_name
    channel_data['published_time'] = published_time
    channel_data['vido_title'] = vido_title
    channel_data['channel_picture_url'] = channel_picture_url
    channel_data['video_id'] = video_id

    nextPageToken = None
    comments = {}
    while True:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            pageToken=nextPageToken
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_time = item['snippet']['topLevelComment']['snippet']['publishedAt']
            comment_id = item['snippet']['topLevelComment']['id']
            comments[comment_id] = {'comment': comment, 'comment_time': comment_time}

        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
    return comments, channel_data


def get_comments(youtube_url):
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_id = youtube_url.split('v=')[1]

    comments, channel_name = get_video_comments(video_id, youtube)
    return comments, channel_name
