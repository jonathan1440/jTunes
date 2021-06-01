from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Song, Artist, Album, Playlist, Genre
import player.helpers as helpers


""" INDEX VIEW """


def index(request):
    template = loader.get_template('jTunes/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


""" LIST ___ VIEWS """


def list_albums(request):
    template = loader.get_template('jTunes/lists/album_list.html')
    context = {
        'albums': [[album.name, album.id]for album in Album.objects.all()]
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


""" ADD ___ VIEWS """


def add_album(request):
    template = loader.get_template('jTunes/add/add_album.html')
    context = {}
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


""" VIEW ___ VIEWS """


def view_album(request, album_id):
    template = loader.get_template('jTunes/view/view_album.html')
    album = get_object_or_404(Album, id=album_id)
    context = {
        'song': album,
        'artists': ', '.join([artist.name for artist in album.album_artists.all()]),
        'songs': ', '.join([song.name for song in album.songs.all()]),
    }

    return HttpResponse(template.render(context, request))


def view_artist(request, artist_id):
    template = loader.get_template('jTunes/view/view_artist.html')
    context = {
        'artist': get_object_or_404(Artist, id=artist_id)
    }
    return HttpResponse(template.render(context, request))


def view_genre(request, genre_id):
    template = loader.get_template('jTunes/view/view_genre.html')
    context = {
        'genre': get_object_or_404(Genre, id=genre_id)
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
        'items': ', '.join(items)
    }
    return HttpResponse(template.render(context, request))


def view_song(request, song_id):
    template = loader.get_template('jTunes/view/song_view.html')
    song = get_object_or_404(Song, id=song_id)
    context = {
        'song': song,
        'artists': ', '.join([artist.name for artist in song.artists.all()]),
        'arousal': round(song.arousal * 10, 0),
        'valence': round(song.valence * 10, 0),
    }

    return HttpResponse(template.render(context, request))


""" EDIT ___ VIEWS """


def edit_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    album.name = request.POST['name']

    album.save()

    new_artists = [artist.strip() for artist in request.Post['artists'].split(',')]
    old_artists = [artist for artist in album.album_artists.all()]
    # add any newly added artists
    for artist in new_artists:
        if artist not in old_artists:
            a = Artist.objects.annotate(search=SearchVector('name'), ).filter(search=artist)
            if artist not in [rtist.name for rtist in a]:
                a = [helpers.new_artist(name=artist)]
            album.album_artists.add(a[0])
    # remove any newly removed artists
    for artist in old_artists:
        if artist not in new_artists:
            a = Song.artists.annotate(search=SearchVector('name'), ).filter(search=artist)
            if artist in [rtist.name for rtist in a]:
                a[0].album_artists.remove(artist)

    album.save()

    new_songs = [song.strip() for song in request.POST['songs'].split(',')]
    old_songs = [song for song in album.songs.all()]
    # add any newly added artists
    for song in new_songs:
        if song not in old_songs:
            a = album.objects.annotate(search=SearchVector('name'), ).filter(search=song)
            if song not in [rtist.name for rtist in a]:
                a = [Song(name=song)]
            helpers.new_albumtosong(album, a[0])
    # remove any newly removed artists
    for song in old_songs:
        if song not in new_songs:
            a = album.album_artists.annotate(search=SearchVector('name'), ).filter(search=song)
            if song in [rtist.name for rtist in a]:
                a[0].songs.remove(song)

    album.save()

    return HttpResponseRedirect(reverse('jTunes:view album', args=(album.id,)))


def edit_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    artist.name = request.POST['name']

    artist.save()

    return HttpResponseRedirect(reverse('jTunes:view artist', args=(artist.id,)))


def edit_genre(request, genre_id):
    return HttpResponse('edit genre %s' % genre_id)


def edit_playlist(request, playlist_id):
    return HttpResponse('Editing playlist ')


def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    song.name = request.POST['name']
    song.arousal = int(request.POST['arousal']) / 10
    song.valence = int(request.POST['valence']) / 10
    song.path = request.POST['path']

    song.save()

    new_artists = [artist.strip() for artist in request.POST['artists'].split(',')]
    old_artists = [artist.name for artist in song.artists.all()]
    # add any newly added artists
    for artist in new_artists:
        if artist not in old_artists:
            a = Artist.objects.annotate(search=SearchVector('name'), ).filter(search=artist)
            if artist not in [rtist.name for rtist in a]:
                a = [helpers.new_artist(name=artist)]
            song.artists.add(a[0])
    # remove any newly removed artists
    for artist in old_artists:
        if artist not in new_artists:
            a = song.artists.annotate(search=SearchVector('name'), ).filter(search=artist)
            if artist in a:
                a[0].artists.remove(id=artist.id)

    song.save()

    return HttpResponseRedirect(reverse('jTunes:view song', args=(song.id,)))


""" NEW ___ VIEWS """


def new_album(request):
    artists = [artist.strip() for artist in request.POST['artists'].split(',')]
    songs = [[song.strip(), None] for song in request.POST['songs'].split(',')]
    album = helpers.new_album(name=request.POST['name'], album_artists=artists, songs_and_track_nums=songs)

    return HttpResponseRedirect(reverse('jTunes:view album', args=(album.id,)))


def new_artist(request):
    artist = helpers.new_artist(name=request.POST['name'])

    return HttpResponseRedirect(reverse('jTunes:view artist', args=(artist.id,)))


def new_genre(request):
    genre = helpers.new_genre(name=request.POST['name'])

    return HttpResponseRedirect(reverse('jTunes:view genre', args=(genre.id,)))


def new_playlist(request):
    items = []
    for item in [i.strip for i in request.POST['items'].split(',')]:
        if item in [song.name for song in Song.objects.all()]:
            items.append(Song.objects.get(name=item))
        elif item in [album.name for album in Album.objects.all()]:
            items.append(Album.objects.get(name=item))
        elif item in [playlist.name for playlist in Playlist.objects.all()]:
            items.append(Playlist.objects.get(name=item))
    playlist = helpers.new_playlist(name=request.POST['name'], items_and_track_nums=[[item, None] for item in items])
    return HttpResponseRedirect(reverse('jTunes:view playlist', args=(playlist.id,)))


def new_song(request):
    artists = [artist.strip() for artist in request.Post['artists'].split(',')]
    song = helpers.new_song(name=request.POST['name'], artists=artists)

    return HttpResponseRedirect(reverse('jTunes:view song', args=(song.id,)))


""" DELETE ___ VIEWS """


def delete_album(request, album_id):
    Album.objects.get(id=album_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list albums'))


def delete_artist(request, artist_id):
    Artist.objects.get(id=artist_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list artists'))


def delete_genre(request, genre_id):
    Genre.objects.get(id=genre_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list genres'))


def delete_playlist(request, playlist_id):
    Playlist.objects.get(id=playlist_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list playlists'))


def delete_song(request, song_id):
    Song.objects.get(id=song_id).delete()

    return HttpResponseRedirect(reverse('jTunes:list songs'))


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
