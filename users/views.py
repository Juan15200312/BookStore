from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer


# Create your views here.
class UserViewSets(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()


class Login(TokenObtainPairView):
    pass


class Logout(GenericAPIView):
    pass