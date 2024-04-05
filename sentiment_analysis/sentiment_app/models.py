from django.db import models


class Video(models.Model):
    channel_id = models.ForeignKey('Creator', on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=100)
    url = models.URLField()
    title = models.CharField(max_length=100)
    time_published = models.DateTimeField()
    num_comments = models.IntegerField()
    positive = models.IntegerField()
    negative = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return self.title


class Creator(models.Model):
    channel_id = models.CharField(max_length=100)
    channel_name = models.CharField(max_length=100)
    picture_url = models.URLField()

    def __str__(self):
        return self.channel_name
