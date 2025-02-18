from rest_framework import viewsets, permissions
from .models import User, Property, Match
from .serializers import UserSerializer, PropertySerializer, MatchSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related('properties').all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.select_related('user').all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related('user1', 'user2').all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

