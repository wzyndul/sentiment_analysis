import base64

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404

from rest_framework import  viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from api.models import Video, Creator
from api.plot_handler import sentiment_plot

from api.serializers import CreatorSerializer, VideoSerializer
from api.youtube_data_processing import video_sentiment_preprocess
from api.youtube_handler import get_yt_data


class CreatorList(viewsets.ReadOnlyModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        return Creator.objects.filter(Q(channel_name__icontains=search_query)).order_by('channel_name')


class VideoList(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(
            self):  # TODO exampel query http://localhost:8000/api/videos/?channel_id=UCLKKvlo0yK8OgWvjCiZQ3sA&search=ROOT%20RIDERS
        search_query = self.request.query_params.get('search', '')
        channel_id = self.request.query_params.get('channel_id', None)
        queryset = Video.objects.filter(Q(title__icontains=search_query)).order_by('-time_published')
        if channel_id is not None:
            queryset = queryset.filter(channel__channel_id=channel_id)
        return queryset

@api_view(['GET'])
def plot(request):
    creator_id = request.query_params.get('creator_id', None)
    all_videos = Video.objects.all().order_by('time_published')
    if creator_id is not None:
        all_videos = all_videos.filter(channel__channel_id=creator_id)
    else:
        return Response({'error': 'No creator_id provided'}, status=status.HTTP_400_BAD_REQUEST)
    if len(all_videos) == 0:
        return Response({'error': 'No videos found for this creator'}, status=status.HTTP_404_NOT_FOUND)

    sentiments_over_time = {video.time_published: video.rating for video in all_videos}
    graphic = sentiment_plot(sentiments_over_time)
    return Response({'plot': graphic})
    
@api_view(['POST'])
def analyse_video(request):
    video_url = request.data.get('youtube_url')
    if video_url is None or not video_url.startswith('https://www.youtube.com/watch?v='):
        return Response({"error": "Invalid URL"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        comments, channel_data = get_yt_data(video_url)
        sentiments_over_time, stats = video_sentiment_preprocess(comments)
        if len(sentiments_over_time) == 0:
            return Response({"error": "No comments found"}, status=status.HTTP_404_NOT_FOUND)
        graphic = sentiment_plot(sentiments_over_time)
    except Exception:  # TODO zlapac konkretny wyjatek z youtube_handler
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        creator, created = Creator.objects.get_or_create(
            channel_id=channel_data['channel_id'],
            defaults={
                'channel_name': channel_data['channel_name'],
                'picture_url': channel_data['channel_picture_url']
            }
        )
    except ValidationError:
        return Response({"error": "Invalid data for Creator"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        video, created = Video.objects.update_or_create(
            video_id=channel_data['video_id'],
            defaults={
                'channel': creator,
                'url': video_url,
                'title': channel_data['vido_title'],
                'plot': graphic,
                'time_published': channel_data['published_time'],
                'num_comments': stats['num_comments'],
                'positive': stats['positive'],
                'negative': stats['negative'],
                'rating': stats['rating'],
                'image_url': channel_data['video_thumbnail_url']
            }
        )
    except ValidationError:
        return Response({"error": "Invalid data for Video"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'stats': stats, 'plot': graphic})

