from django.shortcuts import render


def main_view(request):
    return render(request, 'main.html')


def analysis_view(request):
    platform = None
    if request.method == 'POST':
        if 'twitter_username' in request.POST:
            twitter_username = request.POST.get('twitter_username')
            platform = 'Twitter'
        elif 'youtube_link' in request.POST:
            youtube_link = request.POST.get('youtube_link')
            print(youtube_link)
            platform = 'YouTube'
        context = {
            'platform': platform,
            'username': twitter_username if platform == 'Twitter' else None,
            'link': youtube_link if platform == 'YouTube' else None,
        }
        print(context)

        return render(request, 'analysis.html', context)
