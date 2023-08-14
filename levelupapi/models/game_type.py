from django.db import models


class GameType(models.Model):
    """GameType model class"""
    type = models.CharField(max_length=50)
