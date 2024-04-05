# sentiment_analysis_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('analyse/', views.analysis_view, name='analysis_view'),
    path('creators/', views.creators_view, name='creators_view'),
    path('channel/<str:channel_id>/', views.channel_view, name='channel_view'),
    path('video/<str:video_id>/', views.video_view, name='video_view'),

]
