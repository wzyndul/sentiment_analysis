from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'videos', views.VideoList, basename='video')
router.register(r'creators', views.CreatorList, basename='creator')

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('analyse/', views.analysis_view, name='analysis_view'),
    path('creators/', views.creators_view, name='creators_view'),
    path('channel/<str:channel_id>/', views.channel_view, name='channel_view'),
    path('video/<str:video_id>/', views.video_view, name='video_view'),
    path('api/', include(router.urls)),
    path('api/analysis/', views.analyse_video, name='analyse_video'),

]
