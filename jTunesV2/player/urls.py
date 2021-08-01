from django.urls import path

from . import views


app_name = 'jTunes'
urlpatterns = [
    path('', views.index, name='index'),

    path('songs/', views.list_songs, name='list songs'),
    path('songs/new/', views.add_song, name='add song'),
    path('songs/<int:song_id>/', views.view_song, name='view song'),
    path('songs/edit/', views.new_song, name='new song'),
    path('songs/edit/<int:song_id>/', views.edit_song, name='edit song'),
    path('songs/delete/<int:song_id>/', views.delete_song, name='delete song'),

    path('songtoartist/delete/<int:song_id>/<int:artist_id>/', views.delete_songtoartist, name='delete songtoartist'),
    path('songtoartist/new/<int:song_id>/', views.new_songtoartist, name='new songtoartist'),

    path('albums/', views.list_albums, name='list albums'),
    path('albums/new/', views.add_album, name='add album'),
    path('albums/<int:album_id>/', views.view_album, name='view album'),
    path('albums/edit/', views.new_album, name='new album'),
    path('albums/edit/<int:album_id>/', views.edit_album, name='edit album'),
    path('albums/delete/<int:album_id>/', views.delete_album, name='delete album'),

    path('albumtoartist/delete/<int:album_id>/<int:artist_id>/', views.delete_albumtoartist, name='delete albumtoartist'),
    path('albumtoartist/new/<int:album_id>/', views.new_albumtoartist, name='new albumtoartist'),

    path('albumtosong/delete/<int:albumtosong_id>/', views.delete_albumtosong, name='delete albumtosong'),
    path('albumtosong/new/<int:album_id>/', views.new_albumtosong, name='new albumtosong'),

    path('playlists/', views.list_playlists, name='list playlists'),
    path('playlists/new/', views.add_playlist, name='add playlist'),
    path('playlists/<int:playlist_id>/', views.view_playlist, name='view playlist'),
    path('playlists/edit/', views.new_playlist, name='new playlist'),
    path('playlists/edit/<int:playlist_id>/', views.edit_playlist, name='edit playlist'),
    path('playlists/new/generate/', views.generate_playlist, name='generate playlist'),
    path('playlists/new/generating/', views.generating_playlist, name='generating playlist'),
    path('playlists/delete/<int:playlist_id>/', views.delete_playlist, name='delete playlist'),

    path('playlisttoitem/delete/<int:playlist_id>/<str:item_type>/<str:item_id>/',
         views.delete_playlisttoitem, name='delete playlisttoitem'),
    path('playlisttoitem/new/<int:playlist_id>/', views.new_playlisttoitem, name='new playlisttoitem'),

    path('artists/', views.list_artists, name='list artists'),
    path('artists/new/', views.add_artist, name='add artist'),
    path('artists/<int:artist_id>/', views.view_artist, name='view artist'),
    path('artists/edit/', views.new_artist, name='new artist'),
    path('artists/edit/<int:artist_id>/', views.edit_artist, name='edit artist'),
    path('artists/delete/<int:artist_id>/', views.delete_artist, name='delete artist'),

    path('artisttogenre/delete/<int:artist_id>/<int:genre_id>/', views.delete_artisttogenre, name='delete artisttogenre'),
    path('artisttogenre/new/<int:artist_id>/', views.new_artisttogenre, name='new artisttogenre'),

    path('genres/', views.list_genres, name='list genres'),
    path('genres/new/', views.add_genre, name='add genre'),
    path('genres/<int:genre_id>/', views.view_genre, name='view genre'),
    path('genres/edit/', views.new_genre, name='new genre'),
    path('genres/edit/<int:genre_id>/', views.edit_genre, name='edit genre'),
    path('genres/delete/<int:genre_id>/', views.delete_genre, name='delete genre'),
]
