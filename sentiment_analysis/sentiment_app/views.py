from django.contrib import messages
from django.shortcuts import render

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
            comments = get_comments(video_url)

            positive = 0
            for comment in comments:
                result = predict_sentiment(comment)
                if result == 1:
                    positive += 1
            negative = len(comments) - positive
            num_comments = len(comments)
            rating = f"{positive / len(comments) * 100} %"

            return render(request, 'analysis.html', context={'url': video_url, 'num_comments': num_comments, 'positive': positive, 'negative': negative, 'rating': rating})
