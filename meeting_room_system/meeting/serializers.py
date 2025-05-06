
from rest_framework import serializers
from .models import Room, Participant
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Room, Participant
# from .serializers import RoomSerializer, ParticipantSerializer

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'area', 'floor', 'status']

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name']



