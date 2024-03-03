from django.shortcuts import render


def main_view(request):
    return render(request, 'main.html')


def analysis_view(request):
    # Add your logic for analyzing YouTube comments here
    return render(request, 'analysis.html')

