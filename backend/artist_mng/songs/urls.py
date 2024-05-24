from django.urls import path
from .views import CreateSongAPIView, ListSongsAPIView,ListSongsByUserAPIView

urlpatterns = [
    path('songs/', ListSongsAPIView.as_view(), name='list_songs'),
    path('song/<int:pk>/', CreateSongAPIView.as_view(), name='song_detail'),
    path('song/create/', CreateSongAPIView.as_view(), name='create_song'),
    # path('restore/<int:pk>/', RestoreSongAPIView.as_view(), name='restore_song')
    path('songs/user/<int:user_id>/', ListSongsByUserAPIView.as_view(), name='list-songs-by-user')
]

