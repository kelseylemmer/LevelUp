"""View module for handling requests about event"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game
from django.contrib.auth.models import User


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """

        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all event

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests for creating a new event

        Returns:
            Response -- JSON serialized event record
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        new_event = Event()
        new_event.title = request.data["title"]
        new_event.date_time = request.data["date_time"]
        new_event.organizer = organizer
        new_event.game = game
        new_event.location = request.data["location"]
        new_event.save()

        serialized = EventSerializer(new_event, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a event

        Returns:
            Response -- Empty body with 204 status code
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.get(pk=pk)
        event.title = request.data["title"]
        event.date_time = request.data["date_time"]
        event.organizer = organizer
        event.game = game
        event.location = request.data["location"]
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EventOrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer
    """

    class Meta:
        model = Gamer
        fields = ('id', 'full_name')


class EventGameSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer
    """

    class Meta:
        model = Game
        fields = ('id', 'title')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for event
    """

    organizer = EventOrganizerSerializer(many=False)
    game = EventGameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'title', 'date_time', 'organizer', 'game', 'location')
