import os

from dotenv import load_dotenv
from googleapiclient.discovery import build


def get_video_data(video_id, youtube):
    try:
        video_response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()
    except Exception:
        return None

    return video_response


def get_channel_data(channel_id, youtube):
    try:
        channel_response = youtube.channels().list(
            part="snippet",
            id=channel_id
        ).execute()
    except Exception:
        return None

    return channel_response


def get_comments_data(video_id, youtube):
    comments = {}
    nextPageToken = None
    while True:
        try:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                pageToken=nextPageToken
            ).execute()
        except Exception:
            return None

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_time = item['snippet']['topLevelComment']['snippet']['publishedAt']
            comment_id = item['snippet']['topLevelComment']['id']
            comments[comment_id] = {'comment': comment, 'comment_time': comment_time}

        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break

    return comments


def get_yt_data(youtube_url):
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_id = youtube_url.split('v=')[1]

    channel_video_data = {}

    video_response = get_video_data(video_id, youtube)
    if video_response is None:
        return None, None

    channel_id = video_response['items'][0]['snippet']['channelId']
    channel_name = video_response['items'][0]['snippet']['channelTitle']
    published_time = video_response['items'][0]['snippet']['publishedAt']
    vido_title = video_response['items'][0]['snippet']['title']
    video_thumbnail_url = video_response['items'][0]['snippet']['thumbnails']['default']['url']

    channel_response = get_channel_data(channel_id, youtube)
    if channel_response is None:
        return None, None

    channel_picture_url = channel_response['items'][0]['snippet']['thumbnails']['default']['url']

    channel_video_data['channel_id'] = channel_id
    channel_video_data['channel_name'] = channel_name
    channel_video_data['published_time'] = published_time
    channel_video_data['vido_title'] = vido_title
    channel_video_data['channel_picture_url'] = channel_picture_url
    channel_video_data['video_id'] = video_id
    channel_video_data['video_thumbnail_url'] = video_thumbnail_url

    comments = get_comments_data(video_id, youtube)
    if comments is None:
        return None, None

    return comments, channel_video_data
