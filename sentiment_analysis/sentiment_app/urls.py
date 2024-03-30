# sentiment_analysis_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('analyse/', views.analysis_view, name='analysis_view'),

]