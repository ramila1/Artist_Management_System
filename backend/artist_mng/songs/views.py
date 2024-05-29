from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from rest_framework.permissions import IsAuthenticated
from users.permission import IsAdminOrArtist
from django.shortcuts import get_object_or_404

class CreateSongAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrArtist]

    def get(self, request, pk):
        songs = Song.objects.filter(artist__id=pk)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()  
        data['artist'] = request.user.id 

        serializer = SongSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        serializer = SongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        song = get_object_or_404(Song, pk=pk)

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
    permission_classes = [IsAuthenticated, IsAdminOrArtist]

    def get(self, request):
        songs = Song.objects.select_related('artist').all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)


class ListSongsByUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        songs = Song.objects.filter(artist_id=user_id, is_deleted=False)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
