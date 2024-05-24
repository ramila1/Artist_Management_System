from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'release_date', 'duration', 'lyrics', 'language', 'is_deleted', 'deleted_at')
