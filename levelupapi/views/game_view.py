"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType, Gamer
from django.contrib.auth.models import User


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """

        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests for creating a new game

        Returns:
            Response -- JSON serialized game record
        """
        game_type = GameType.objects.get(pk=request.data["game_type"])
        creator = Gamer.objects.get(user=request.auth.user)

        new_game = Game()
        new_game.title = request.data["title"]
        new_game.creator = creator
        new_game.game_type = game_type
        new_game.maker = request.data["maker"]
        new_game.number_of_players = request.data["number_of_players"]
        new_game.skill_level = request.data["skill_level"]

        new_game.save()

        serialized = GameSerializer(new_game, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.game_type = GameType.objects.get(pk=request.data["game_type"])
        game.creator = Gamer.objects.get(user=request.auth.user)
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """

    class Meta:
        model = Game
        fields = ('id', 'title', 'creator', 'game_type', 'events',
                  'maker', 'number_of_players', 'skill_level')
