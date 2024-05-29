from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users.serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from users.permission import IsAdmin, IsArtist, IsAdminOrArtist
from rest_framework.permissions import IsAuthenticated

class CreateArtist(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        artists = CustomUser.objects.filter(is_artist=True, is_deleted=False)
        serializer = CustomUserSerializer(artists, many=True)
        return Response(serializer.data)

    def post(self, request):
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

    def delete(self, request, pk=None):
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







