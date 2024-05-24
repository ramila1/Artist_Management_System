from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from users.permission import IsAdmin, IsArtist, IsAdminOrArtist



class CreateArtist(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None, format=None):
        if pk is not None:
            try:
                artist = CustomUser.objects.get(pk=pk, is_deleted=False)
                serializer = CustomUserSerializer(artist)
                return Response(serializer.data)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Artist not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_artist=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if pk is not None:
            try:
                artist = CustomUser.objects.get(pk=pk, is_deleted=False)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Artist not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = CustomUserSerializer(artist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, pk):
        if pk is not None:
            try:
                artist = CustomUser.objects.get(pk=pk, is_deleted=False)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Artist not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = CustomUserSerializer(artist, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, pk=None, format=None):
        if pk is not None:
            try:
                artist = CustomUser.objects.get(pk=pk)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Artist not found'}, status=status.HTTP_404_NOT_FOUND)

            if artist.is_deleted:
                try:
                    artist.hard_delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                artist.soft_delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ListArtists(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrArtist]

    def get(self, request, format=None):
        artists = CustomUser.objects.filter(is_artist=True)
        
        serializer = CustomUserSerializer(artists, many=True)
        return Response(serializer.data)

from rest_framework.permissions import IsAuthenticated

class CurrentArtist(APIView):
    permission_classes = [IsAuthenticated, IsArtist]  

    def get(self, request, format=None):
        artist = request.user
        serializer = CustomUserSerializer(artist)
        return Response(serializer.data)

    
class ListUsers(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, format=None):
        users = CustomUser.objects.filter(is_deleted=False)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
        
class ListAdmin(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def get(self, request, format=None):
        admins = request.user
        serializer = CustomUserSerializer(admins)
        return Response(serializer.data)

    def put(self, request):
        try:
            admin = request.user
            serializer = CustomUserSerializer(admin, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            admin = request.user
            serializer = CustomUserSerializer(admin, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Both email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'Inactive account'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CustomUserSerializer(user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }, status=status.HTTP_200_OK)