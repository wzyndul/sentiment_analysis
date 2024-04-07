from django.db import models

class Creator(models.Model):
    channel_id = models.CharField(max_length=100, primary_key=True)
    channel_name = models.CharField(max_length=100)
    picture_url = models.URLField()

    def __str__(self):
        return self.channel_name


class Video(models.Model):
    video_id = models.CharField(max_length=50, primary_key=True)
    channel = models.ForeignKey(Creator, on_delete=models.CASCADE)
    url = models.URLField()
    image_url = models.URLField()
    title = models.CharField(max_length=100)
    time_published = models.DateTimeField()
    num_comments = models.IntegerField()
    positive = models.IntegerField()
    negative = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return self.title


