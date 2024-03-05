from django.shortcuts import render


def main_view(request):
    return render(request, 'main.html')


def analysis_view(request):
    platform = None
    if request.method == 'POST':
        if 'x_username' in request.POST:
            x_username = request.POST.get('x_username')
            platform = 'X'
        elif 'youtube_link' in request.POST:
            youtube_link = request.POST.get('youtube_link')
            platform = 'Youtube'
        context = {
            'platform': platform,
            'x_username': x_username if platform == 'X' else None,
            'youtube_link': youtube_link if platform == 'Youtube' else None,
        }

    return render(request, 'analysis.html', context)
