from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, login, logout
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    UserUpdateSerializer, ChangePasswordSerializer
)

User = get_user_model()

# ==================== JWT LOGIN (RECOMMANDÉ) ====================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

class LoginView(TokenObtainPairView):
    """
    Connexion avec JWT (recommandé pour React)
    """
    serializer_class = CustomTokenObtainPairSerializer


# ==================== SESSION LOGIN (ALTERNATIVE) ====================
class SessionLoginView(APIView):
    """
    Connexion avec session Django (alternative)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return Response({
            'user': UserSerializer(user).data,
            'message': 'Connexion réussie !'
        }, status=status.HTTP_200_OK)


# ==================== INSCRIPTION ====================
class RegisterView(generics.CreateAPIView):
    """
    Inscription d'un nouvel utilisateur
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': UserSerializer(user).data,
            'message': 'Inscription réussie ! Vous pouvez maintenant vous connecter.'
        }, status=status.HTTP_201_CREATED)


# ==================== DÉCONNEXION ====================
class LogoutView(APIView):
    """
    Déconnexion utilisateur
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Déconnexion réussie !'}, status=status.HTTP_200_OK)


# ==================== PROFIL UTILISATEUR ====================
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Récupérer et mettre à jour le profil utilisateur
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ==================== CHANGEMENT DE MOT DE PASSE ====================
class ChangePasswordView(APIView):
    """
    Changer le mot de passe de l'utilisateur
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        # Vérifier l'ancien mot de passe
        if not user.check_password(old_password):
            return Response(
                {'old_password': 'Ancien mot de passe incorrect.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Changer le mot de passe
        user.set_password(new_password)
        user.save()

        return Response(
            {'message': 'Mot de passe changé avec succès.'},
            status=status.HTTP_200_OK
        )
