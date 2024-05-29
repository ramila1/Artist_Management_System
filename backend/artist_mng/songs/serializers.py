from rest_framework import serializers
from .models import Song
from users.models import CustomUser  # Adjust import as per your project structure

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']

class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'title', 'release_date', 'duration', 'language', 'lyrics', 'artist']
        read_only_fields = ['id']

    def create(self, validated_data):
        artist_data = {
            'id': self.context['request'].user.id,
            'first_name': self.context['request'].user.first_name,
            'last_name': self.context['request'].user.last_name,
            'email': self.context['request'].user.email,
        }

        song_instance = Song.objects.create(artist_id=self.context['request'].user.id, **validated_data)
        return song_instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.language = validated_data.get('language', instance.language)
        instance.lyrics = validated_data.get('lyrics', instance.lyrics)
        instance.save()
        return instance
