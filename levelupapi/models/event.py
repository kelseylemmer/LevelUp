from django.db import models


class Event(models.Model):
    """Event model class"""
    title = models.CharField(
        max_length=150)
    date_time = models.DateTimeField()
    organizer = models.ForeignKey(
        "Gamer", on_delete=models.CASCADE, related_name="organized_events")
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="events")
    location = models.CharField(max_length=60)
