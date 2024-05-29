from django.urls import path
from ._views import  ListUsers,ListArtists,Login,ListAdmin,CurrentArtist,ListAdmin, ArtistDetail
from rest_framework_simplejwt.views import TokenBlacklistView
from users.views.create import CreateArtist

urlpatterns = [
    path('artists/', CreateArtist.as_view(), name='create-artist'),
    path('artists/<int:pk>/', ArtistDetail.as_view(), name='artist-detail'),
    path('only/artists/', ListArtists.as_view(), name='list-artists'),
    path('users/', ListUsers.as_view(), name='list-users'),
    path('login/',Login.as_view(),name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('admin_list/',ListAdmin.as_view(),name="Adminlist"),
    path('artists/me/', CurrentArtist.as_view(), name='current-artist'),
    path('only/admin/',ListAdmin.as_view(),name='only_admin')
]



