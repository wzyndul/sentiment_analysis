from collections import defaultdict
from datetime import datetime
import matplotlib.dates as mdates
from django.contrib import messages
from django.shortcuts import render
from matplotlib import pyplot as plt

from sentiment_app.plot_handler import sentiment_over_time
from sentiment_app.predict import predict_sentiment
from sentiment_app.youtube_handler import get_comments


def main_view(request):
    return render(request, 'main.html')


def analysis_view(request):
    if request.method == 'POST':
        video_url = request.POST.get('youtube_url')
        if video_url is None or not video_url.startswith('https://www.youtube.com/watch?v='):
            return render(request, 'main.html')
        else:
            comments, channel_name = get_comments(video_url)
            # Convert the comments dictionary to a list of tuples and sort it by comment time
            sorted_comments = sorted(comments.items(),
                                     key=lambda item: datetime.strptime(item[1]['comment_time'], "%Y-%m-%dT%H:%M:%S%z"))
            sentiments_over_time = {}
            positive = 0
            all = 0
            for comment_id, comment_data in sorted_comments:
                all += 1
                comment = comment_data['comment']
                comment_time = comment_data['comment_time']
                result = predict_sentiment(comment)
                timestamp = datetime.strptime(comment_time, "%Y-%m-%dT%H:%M:%S%z")
                timestamp = timestamp.replace(minute=0, second=0)
                if result == 1:
                    positive += 1
                sentiment = positive / all
                sentiments_over_time[timestamp] = sentiment

            negative = len(comments) - positive
            num_comments = len(comments)
            rating = f"{positive / len(comments) * 100} %"
            stats = {
                'num_comments': num_comments,
                'positive': positive,
                'negative': negative,
                'rating': rating
            }
            graphic = sentiment_over_time(sentiments_over_time)

            return render(request, 'analysis.html',
                          context={'url': video_url, 'stats': stats, 'plot': graphic})
