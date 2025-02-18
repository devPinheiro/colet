from rest_framework import serializers
from .models import User, Property, Match

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
