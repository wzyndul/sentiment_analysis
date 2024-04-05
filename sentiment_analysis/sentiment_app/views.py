from collections import defaultdict
from datetime import datetime
import matplotlib.dates as mdates
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from matplotlib import pyplot as plt

from sentiment_app.models import Video, Creator
from sentiment_app.plot_handler import sentiment_plot
from sentiment_app.predict import predict_sentiment
from sentiment_app.youtube_data_processing import video_sentiment
from sentiment_app.youtube_handler import get_comments


def main_view(request):
    return render(request, 'main.html')


def analysis_view(request):
    if request.method == 'POST':
        video_url = request.POST.get('youtube_url')
        if video_url is None or not video_url.startswith('https://www.youtube.com/watch?v='):
            return render(request, 'main.html')
        else:
            comments, channel_data = get_comments(video_url)
            sentiments_over_time, stats = video_sentiment(comments)
            graphic = sentiment_plot(sentiments_over_time)

            try:
                creator = Creator.objects.get(channel_id=channel_data['channel_id'])
            except Creator.DoesNotExist:
                try:
                    creator = Creator(channel_id=channel_data['channel_id'],
                                      channel_name=channel_data['channel_name'],
                                      picture_url=channel_data['channel_picture_url'])
                    creator.full_clean()
                    creator.save()

                except ValidationError:
                    return HttpResponseBadRequest(render(request, 'error_page.html', {'error_code': 400}))

            try:
                video = Video.objects.get(video_id=channel_data['video_id'])
                video.channel = creator
                video.url = video_url
                video.title = channel_data['vido_title']
                video.time_published = channel_data['published_time']
                video.num_comments = stats['num_comments']
                video.positive = stats['positive']
                video.negative = stats['negative']
                video.rating = stats['rating']
                video.save()

            except Video.DoesNotExist:
                try:
                    video = Video(video_id=channel_data['video_id'], channel=creator, url=video_url,
                                  title=channel_data['vido_title'], time_published=channel_data['published_time'],
                                  num_comments=stats['num_comments'], positive=stats['positive'],
                                  negative=stats['negative'], rating=stats['rating'])
                    video.full_clean()
                    video.save()
                except ValidationError:
                    return HttpResponseBadRequest(render(request, 'error_page.html', {'error_code': 400}))

            return render(request, 'analysis.html',
                          context={'url': video_url, 'stats': stats, 'plot': graphic})


def creators_view(request):
    search_query = request.GET.get('search', '')
    creators_list = Creator.objects.filter(Q(channel_name__icontains=search_query)).order_by('channel_name')
    paginator = Paginator(creators_list, 5)

    page_number = request.GET.get('page')
    creators = paginator.get_page(page_number)

    return render(request, 'creators.html', {'creators': creators})


def channel_view(request, channel_id):
    creator = get_object_or_404(Creator, channel_id=channel_id)
    search_query = request.GET.get('search', '')
    video_list = creator.video_set.filter(title__icontains=search_query).order_by('-time_published')
    paginator = Paginator(video_list, 20)

    page_number = request.GET.get('page')
    videos = paginator.get_page(page_number)

    return render(request, 'channel.html', {'creator': creator, 'videos': videos})


def video_view(request, video_id):
    video = get_object_or_404(Video, video_id=video_id)
    return render(request, 'video.html', {'video': video})
