from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer, CustomTokenObtainPairSerializer


# Create your views here.
class UserViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                return Response({'error': 'La cuenta esta desactivada'}, status=status.HTTP_403_FORBIDDEN)

            user_serializer = UserSerializer(user)
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({
                'token_access': access,
                'token_refresh': str(refresh),
                'user': user_serializer.data,
                'message': 'Inicio de sesión exitoso'
            }, status= status.HTTP_200_OK)
        return Response({'error': 'Usuario o contraseña incorrecto'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):

    def post(self, request, *args, **kwargs):
        token_refresh = request.data.get('refresh', None)

        if token_refresh:
            try:
                token = RefreshToken(token_refresh)
                if int(token['user_id']) == request.user.id:
                    token.blacklist()
                    return Response({'message': 'Sesión cerrada correctamente'}, status=status.HTTP_200_OK)
                return Response({'error': 'El token no pertenece al usuario'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({'error': 'Token invalido o expirado'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Token requerido'}, status=status.HTTP_400_BAD_REQUEST)
