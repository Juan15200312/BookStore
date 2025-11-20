from django.shortcuts import render
from rest_framework import viewsets

from users.serializers import UserSerializer


# Create your views here.
class UserViewSets(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
