from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permission import IsAdmin, IsArtist, IsAdminOrArtist

class CreateSongAPIView(APIView):
    permission_classes = [IsAdminOrArtist]  

    def get(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist:
            return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        if song.is_deleted:
            try:
                song.hard_delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            song.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class ListSongsAPIView(APIView):
    permission_classes = [IsAdminOrArtist]  

    def get(self, request, format=None):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

class ListSongsByUserAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, user_id, format=None):
        try:
            songs = Song.objects.filter(artist_id=user_id, is_deleted=False)
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data)
        except Song.DoesNotExist:
            return Response({'error': 'Songs not found for this user'}, status=status.HTTP_404_NOT_FOUND)
