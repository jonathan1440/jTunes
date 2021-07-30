from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Song, Artist, Album, Playlist, Genre, PlaylistToSong, PlaylistToAlbum, PlaylistToPlaylist, \
    AlbumToSong
import player.helpers as helpers

""" INDEX VIEW """


def index(request):
    template = loader.get_template('jTunes/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


""" ADD ___ VIEWS """


def add_album(request):
    template = loader.get_template('jTunes/add/add_album.html')
    context = {
        "album": Album.objects.all()[1]
    }
    return HttpResponse(template.render(context, request))


def add_artist(request):
    template = loader.get_template('jTunes/add/add_artist.html')
    context = {}
    return HttpResponse(template.render(context, request))


def add_genre(request):
    template = loader.get_template('jTunes/add/add_genre.html')
    context = {}
    return HttpResponse(template.render(context, request))


def add_playlist(request):
    template = loader.get_template('jTunes/add/add_playlist.html')
    context = {}
    return HttpResponse(template.render(context, request))


def add_song(request):
    template = loader.get_template('jTunes/add/add_song.html')
    context = {}
    return HttpResponse(template.render(context, request))


""" DELETE ___ VIEWS """


def delete_album(request, album_id):
    Album.objects.get(id=album_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list albums'))


def delete_albumtoartist(request, album_id, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    album = get_object_or_404(Album, id=album_id)
    album.album_artists.remove(artist)

    return HttpResponseRedirect(reverse('jTunes:view album', args=(album_id,)))


def delete_artisttogenre(request, artist_id, genre_id):
    artist = get_object_or_404(Artist, id=artist_id)
    genre = get_object_or_404(Genre, id=genre_id)
    artist.genres.remove(genre)

    return HttpResponseRedirect(reverse('jTunes:view artist', args=(artist_id,)))


def delete_albumtosong(request, albumtosong_id):
    ats = get_object_or_404(AlbumToSong, id=albumtosong_id)
    album_id = ats.album.id
    ats.delete()

    return HttpResponseRedirect(reverse('jTunes:view album', args=(album_id,)))


def delete_artist(request, artist_id):
    Artist.objects.get(id=artist_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list artists'))


def delete_genre(request, genre_id):
    Genre.objects.get(id=genre_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list genres'))


def delete_playlist(request, playlist_id):
    Playlist.objects.get(id=playlist_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list playlists'))


def delete_playlisttoitem(request, playlist_id):

    return HttpResponseRedirect(reverse('jTunes:view playlist', args=(playlist_id,)))


def delete_song(request, song_id):
    Song.objects.get(id=song_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list songs'))


def delete_songtoartist(request, song_id, artist_id):
    song = get_object_or_404(Song, id=song_id)
    artist = get_object_or_404(Artist, id=artist_id)
    song.artists.remove(artist)

    return HttpResponseRedirect(reverse('jTunes:view song', args=(song_id,)))



""" EDIT ___ VIEWS """


def edit_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    album.name = request.POST['name']

    album.save()

    return HttpResponseRedirect(reverse('jTunes:view album', args=(album.id,)))


def edit_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    artist.name = request.POST['name']

    artist.save()

    return HttpResponseRedirect(reverse('jTunes:view artist', args=(artist.id,)))


def edit_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.name = request.POST['name']
    genre.save()
    return HttpResponseRedirect(reverse('jTunes:view genre', args=(genre.id,)))


def edit_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    playlist.name = request.POST['name']
    playlist.save()
    new_items = [i.strip() for i in request.POST['items'].split(',')]
    old_items = [p.name for p in playlist.songs.all()] + [p.name for p in playlist.albums.all()] + [p.name for p in
                                                                                                    playlist.playlists.all()]
    for item in new_items:
        if item in [song.name for song in Song.objects.all()]:
            if item not in [p.name for p in playlist.songs.all()]:
                helpers.new_playlisttosong(playlist, Song.objects.get(name=item))
        elif item in [album.name for album in Album.objects.all()]:
            if item not in [p.name for p in playlist.albums.all()]:
                helpers.new_playlisttoalbum(playlist, Album.objects.get(name=item))
        elif item in [p.name for p in Playlist.objects.all()]:
            if playlist != Playlist.objects.get(name=item):
                if item not in playlist.albums.all():
                    helpers.new_playlisttoplaylist(playlist, Playlist.objects.get(name=item))
    for item in old_items:
        if item not in new_items:
            if item in [song.name for song in Song.objects.all()]:
                PlaylistToSong.objects.get(playlist=playlist, song=item).delete()
            elif item in [album.name for album in Album.objects.all()]:
                PlaylistToAlbum.objects.get(playlist=playlist, album=item).delete()
            elif item in [p.name for p in Playlist.objects.all()]:
                if playlist != Playlist.objects.get(name=item):
                    PlaylistToPlaylist.objects.get(playlist=playlist, member_playlist=item).delete()

    playlist.save()
    return HttpResponseRedirect(reverse('jTunes:view playlist', args=(playlist.id,)))


def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    song.name = request.POST['name']
    song.arousal = int(request.POST['arousal']) / 10
    song.valence = int(request.POST['valence']) / 10
    song.path = request.POST['path']

    song.save()

    return HttpResponseRedirect(reverse('jTunes:view song', args=(song.id,)))


""" GENERATE ___ VIEWS """


def generate_playlist(request):
    template = loader.get_template('jTunes/generate_playlist.html')
    context = {}
    return HttpResponse(template.render(context, request))


def generating_playlist(request):
    use_a = request.POST.get('use arousal', False)
    use_v = request.POST.get('use valence', False)
    min_a = int(request.POST['min arousal value'])
    max_a = int(request.POST['max arousal value'])
    min_v = int(request.POST['min valence value'])
    max_v = int(request.POST['max valence value'])
    songs = []
    for song in Song.objects.all():
        in_a = song.arousal in range(min(min_a, max_a), max(min_a, max_a))
        in_v = song.valence in range(min(min_v, max_v), max(min_v, max_v))
        if use_a and (not use_v) and in_a or \
                use_v and (not use_a) and in_v or \
                use_v and use_a and in_a and in_v or \
                (not use_a) and (not use_v):
            songs.append(song)
    playlist = helpers.new_playlist(name=request.POST['name'], items_and_track_nums=[[song, None] for song in songs])
    print(playlist.id)
    return HttpResponseRedirect(reverse('jTunes:view playlist'), args=(playlist.id,))


""" LIST ___ VIEWS """


def list_albums(request):
    template = loader.get_template('jTunes/lists/album_list.html')
    context = {
        'albums': [[album.name, album.id] for album in Album.objects.all()]
    }
    return HttpResponse(template.render(context, request))


def list_artists(request):
    template = loader.get_template('jTunes/lists/artist_list.html')
    context = {
        'artists': [[artist.name, artist.id] for artist in Artist.objects.all()]
    }
    return HttpResponse(template.render(context, request))


def list_genres(request):
    template = loader.get_template('jTunes/lists/genre_list.html')
    context = {
        'genres': [[genre.name, genre.id] for genre in Genre.objects.all()]
    }
    return HttpResponse(template.render(context, request))


def list_playlists(request):
    template = loader.get_template('jTunes/lists/playlist_list.html')
    context = {
        'playlists': [[playlist.name, playlist.id] for playlist in Playlist.objects.all()]
    }
    return HttpResponse(template.render(context, request))


def list_songs(request):
    template = loader.get_template('jTunes/lists/song_list.html')
    songs = []
    for song in Song.objects.all():
        songs.append([song.name, song.id, ''])
        for artist in song.artists.all():
            songs[-1][2] += artist.name
    context = {
        'songs': songs
    }
    return HttpResponse(template.render(context, request))


""" NEW ___ VIEWS """


def new_album(request):
    # artists = [artist.strip() for artist in request.POST['artists'].split(',')]
    # songs = [[song.strip(), None] for song in request.POST['songs'].split(',')]
    album = helpers.new_album(name=request.POST['name'])  # , album_artists=artists, songs_and_track_nums=songs)

    return HttpResponseRedirect(reverse('jTunes:view album', args=(album.id,)))


def new_albumtoartist(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    artist = request.POST['artist'].strip()

    if artist == 'Artist':
        return HttpResponseRedirect(reverse('jTunes:view album', args=(album_id,)))

    if artist:
        artists = Artist.objects.annotate(search=SearchVector('name'), ).filter(search=artist)
        if artists:
            album.album_artists.add(artists[0])
        else:
            album.album_artists.add(helpers.new_artist(name=artist))

    return HttpResponseRedirect(reverse('jTunes:view album', args=(album_id,)))


def new_artisttogenre(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    genre = request.POST['genre'].strip()

    if genre == 'Genre':
        return HttpResponseRedirect(reverse('jTunes:view artist', args=(artist_id,)))

    if genre:
        genres = Genre.objects.annotate(search=SearchVector('name'), ).filter(search=genre)
        if genres:
            artist.genres.add(genres[0])
        else:
            artist.genres.add(helpers.new_genre(name=genre))

    return HttpResponseRedirect(reverse('jTunes:view artist', args=(artist_id,)))


def new_albumtosong(request, album_id):
    if request.POST['song'] == 'Song' or \
            not (request.POST['song'] and request.POST['artists']):
        return HttpResponseRedirect(reverse('jTunes:view album', args=(album_id,)))

    album = get_object_or_404(Album, id=album_id)
    songs = Song.objects.annotate(search=SearchVector('name'), ).filter(name=request.POST['song'].strip())
    artists = [artist.strip() for artist in request.POST['artists'].split(',')]

    if len(songs) > 0:
        for song in songs:
            if artists is None or artists == ["Artists (comma seperated)"]:
                helpers.new_albumtosong(album, song)
                return HttpResponseRedirect(reverse('jTunes:view album', args=(album_id,)))
            elif artists == [a.name for a in song.artists.all()]:
                helpers.new_albumtosong(album, song)
                return HttpResponseRedirect(reverse('jTunes:view album', args=(album_id,)))

    song = helpers.new_song(name=request.POST['song'].strip(), artists=artists)
    helpers.new_albumtosong(album, song)

    return HttpResponseRedirect(reverse('jTunes:view album', args=(album_id,)))


def new_artist(request):
    artist = helpers.new_artist(name=request.POST['name'])

    return HttpResponseRedirect(reverse('jTunes:view artist', args=(artist.id,)))


def new_genre(request):
    genre = helpers.new_genre(name=request.POST['name'])

    return HttpResponseRedirect(reverse('jTunes:view genre', args=(genre.id,)))


def new_playlist(request):
    items = []
    for item in [i.strip() for i in request.POST['items'].split(',')]:
        if item in [song.name for song in Song.objects.all()]:
            items.append(Song.objects.get(name=item))
        elif item in [album.name for album in Album.objects.all()]:
            items.append(Album.objects.get(name=item))
        elif item in [playlist.name for playlist in Playlist.objects.all()]:
            items.append(Playlist.objects.get(name=item))
    playlist = helpers.new_playlist(name=request.POST['name'], items_and_track_nums=[[item, None] for item in items])

    return HttpResponseRedirect(reverse('jTunes:view playlist', args=(playlist.id,)))


def new_playlisttoitem(request, playlist_id):

    return HttpResponseRedirect(reverse('jTunes:view playlist', args=(playlist_id,)))


def new_song(request):
    song = helpers.new_song(name=request.POST['name'], path=request.POST['path'], artists=[],
                            arousal=int(request.POST['arousal']) / 10, valence=int(request.POST['valence']) / 10)

    return HttpResponseRedirect(reverse('jTunes:view song', args=(song.id,)))


def new_songtoartist(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    artist = request.POST['artist'].strip()

    if artist == 'Artist':
        return HttpResponseRedirect(reverse('jTunes:view song', args=(song_id,)))

    if artist:
        artists = Artist.objects.annotate(search=SearchVector('name'), ).filter(search=artist)
        if artists:
            song.artists.add(artists[0])
        else:
            song.artists.add(helpers.new_artist(name=artist))

    return HttpResponseRedirect(reverse('jTunes:view song', args=(song_id,)))


""" VIEW ___ VIEWS """


def view_album(request, album_id):
    template = loader.get_template('jTunes/view/view_album.html')
    album = get_object_or_404(Album, id=album_id)
    ats_relations = album.albumtosong_set.all()
    context = {
        'album': album,
        'artists': [[artist.name, artist.id] for artist in album.album_artists.all()],
        'songs': [[x.song.name, x.song.id, x.id, ', '.join([artist.name for artist in x.song.artists.all()])] for x in
                  ats_relations],
    }

    return HttpResponse(template.render(context, request))


def view_artist(request, artist_id):
    template = loader.get_template('jTunes/view/view_artist.html')
    artist = get_object_or_404(Artist, id=artist_id)
    context = {
        'artist': artist,
        'genres': [[genre.name, genre.id] for genre in artist.genres.all()]
    }
    return HttpResponse(template.render(context, request))


def view_genre(request, genre_id):
    template = loader.get_template('jTunes/view/view_genre.html')
    genre = get_object_or_404(Genre, id=genre_id)
    context = {
        'genre': genre
    }
    return HttpResponse(template.render(context, request))


def view_playlist(request, playlist_id):
    template = loader.get_template('jTunes/view/view_playlist.html')
    p = get_object_or_404(Playlist, id=playlist_id)
    items = []
    [items.append(song.name) for song in p.songs.all()]
    [items.append(album.name) for album in p.albums.all()]
    [items.append(playlist.name) for playlist in p.playlists.all()]
    context = {
        'playlist': p,
        'items': ', '.join(items),
        'paths': helpers.get_playlist_paths(p),
    }
    return HttpResponse(template.render(context, request))


def view_song(request, song_id):
    template = loader.get_template('jTunes/view/song_view.html')
    song = get_object_or_404(Song, id=song_id)
    context = {
        'song': song,
        'artists': [[artist.name, artist.id] for artist in song.artists.all()],
        'arousal': round(song.arousal * 10, 0),
        'valence': round(song.valence * 10, 0),
    }

    return HttpResponse(template.render(context, request))
