from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'videos', views.VideoList, basename='video')
router.register(r'creators', views.CreatorList, basename='creator')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/analysis/', views.analyse_video, name='analyse_video'),
    path('api/plot/', views.plot, name='plot'),

]
