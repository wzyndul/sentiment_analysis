from rest_framework import serializers
from .models import Video, Creator


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_id', 'channel', 'url', 'image_url', 'title', 'time_published', 'num_comments', 'positive',
                  'negative', 'rating']


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ['channel_id', 'channel_name', 'picture_url']
