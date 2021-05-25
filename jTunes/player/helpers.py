from player.models import *

from django.contrib.postgres.search import *
from django.apps import apps


def get_models():
    """
    Return all models in project.
    >>> get_models()
    ['Item', 'Genre', 'Artist', 'PlayableItem', 'Song', 'Album', 'Playlist', 'Order', 'AlbumToSong', 'PlaylistTo', 'PlaylistToSong', 'PlaylistToPlaylist', 'PlaylistToAlbum', 'LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session']
    """
    return [model.__name__ for model in apps.get_models()]  # https://docs.djangoproject.com/en/3.2/ref/applications/


def get_model(name: str):
    """
    Return model object with input name.

    >>> get_model('Song')
    <class 'player.models.Song'>
    >>> get_model('song')
    <class 'player.models.Song'>
    >>> get_model('not a model')
    Traceback (most recent call last):
        ...
    LookupError: App 'player' doesn't have a 'not a model' model.
    """
    return apps.get_model(model_name=name, app_label='player')


def get_fields(model_name: str):
    """
    Get fields of input model.

    >>> get_fields('Item')
    ['genre', 'artist', 'playableitem', 'id', 'name']
    >>> get_fields('item')
    ['genre', 'artist', 'playableitem', 'id', 'name']
    >>> get_fields('not a model')
    Traceback (most recent call last):
        ...
    LookupError: App 'player' doesn't have a 'not a model' model.
    """
    return [field.name for field in get_model(model_name)._meta.get_fields()]  # https://docs.djangoproject.com/en/3.2/ref/applications/


def get_model_instance_obj(model_name: str, name: str):
    """
    get object of an instance of a model

    >>> get_model_instance_obj('song','evaporate')
    <QuerySet [<Song: Song object (3)>]>
    >>> get_model_instance_obj('artist', 'not an artist')
    <QuerySet []>
    """
    return get_model(model_name).objects.annotate(search=SearchVector('name'), ).filter(search=name)  # https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#searchvector


def get_model_instance_txt(model_name: str, name: str):
    """
    get array of text pairs showing field name and field value for each object with the given name

    broken atm
    TODO: fix
    """
    return [[[field, getattr(inst, field)] for field in get_fields(model_name)] for inst in get_model_instance_obj(model_name, name)]


def edit_model_instance(model_instance, feature: str, value, verbose: bool = True):
    """
    Model relations must be edited manually.

    >>> edit_model_instance(Song.objects.all()[0], 'name', 'evaporate', False).name
    'evaporate'
    >>> edit_model_instance(Song.objects.all()[0], 'artists', '')
    Model relations must be edited manually
        ...
    TypeError: Direct assignment to the forward side of a many-to-many set is prohibited. Use artists.set() instead.
    """
    if verbose:
        print('Model relations must be edited manually')

    setattr(model_instance, feature, value)
    model_instance.save()

    return model_instance


def new_genre(name: str, verbose: bool = True):
    """
    name is required and must be unique

    >>> new_genre('t Trance').name
    't Trance'
    >>> new_genre('t Trance').name
    Error: genre  t Trance  already exists
        ...
    AttributeError: 'NoneType' object has no attribute 'name'
    """

    if len(get_model_instance_obj('genre', name)) == 0:
        g = Genre(name=name)
        g.save()
        return g
    elif verbose:
        print("Error: genre ", name, " already exists")
    return None


def new_artist(name: str, genres: [Genre] = None):
    """
    name is required

    >>> new_artist('t Rameses B', [Genre.objects.get(name='t Trance')]).name
    't Rameses B'
    """

    a = Artist(name=name)
    a.save()

    if genres:
        for genre in genres:
            a.genres.add(genre)

    a.save()
    return a


def new_song(name: str, path: str, artists: [Artist] = None, remix_of: Song = None, composers: [Artist] = None,
             year: int = None, song_genres: [Genre] = None, length: int = None, tempo: int = None, key: str = None,
             decibels: int = None, lufs: int = None, arousal: float = None, valence: float = None):
    """
    name and path are required

    >>> new_song(name='t Lost', artists=[Artist.objects.get(name='t Rameses B')], arousal=0.7, valence=0.5).name
    Traceback (most recent call last):
        ...
    TypeError: new_song() missing 1 required positional argument: 'path'
    >>> new_song(name='t Lost', path='H:/Music', artists=[Artist.objects.get(name='t Rameses B')], arousal=0.7, valence=0.5).name
    't Lost'
    """

    s = Song(name=name, path=path, remix_of=remix_of, year=year, length=length, tempo=tempo, key=key, decibels=decibels,
             lufs=lufs, arousal=arousal, valence=valence)
    s.save()

    if song_genres:
        for genre in song_genres:
            s.song_genres.add(genre)

    if artists:
        for artist in artists:
            s.artists.add(artist)

    if composers:
        for composer in composers:
            s.composers.add(composer)

    s.save()
    return s


def new_albumtosong(album: Album, song: Song, track_num: int = None):
    """
    album and song are required
    TODO: something is broken here, fix it


    >>> new_albumtosong(Album.objects.get(name='t Evaporate'),Song.objects.get(name='t Evaporate')).album
    't Evaporate'
    >>> AlbumToSong.objects.get(album=Album.objects.get(name='Evaporate'),song=Song.objects.get(name='Evaporate'))[-1].delete()
    (2, {'player.AlbumToSong': 1, 'player.Order': 1})
    """
    return AlbumToSong(track_num=track_num, album=album, song=song)


def new_album(name: str, album_artists: [Artist] = None, songs_and_track_nums: [[Song, int]] = None):
    """
    name is required
    songs_and_track_nums is an array of [Song, track_num] pairs. track_num can be None.

    >>> new_album(name='t Drift Away', album_artists=[Album.objects.get(name='t Rameses B')]).name
    't Drift Away'
    """

    al = Album(name=name)
    al.save()

    if album_artists:
        for artist in album_artists:
            al.album_artists.add(artist)

    if songs_and_track_nums:
        for [song, track_num] in songs_and_track_nums:
            new_albumtosong(album=al, song=song, track_num=track_num)

    al.save()
    return al


def new_playlisttosong(playlist: Playlist, song: Song, track_num: int = None):
    """
    playlist and song are required

    >>> new_playlisttosong(Playlist.objects.get(name='t Playlist'),Song.objects.get(name='t Evaporate')).playlist
    't Playlist'
    """
    return PlaylistToSong(track_num=track_num, playlist=playlist, song=song)


def new_playlisttoalbum(playlist: Playlist, album: Album, track_num: int = None):
    """
    playlist and album are required

    >>> new_playlisttoalbum(Playlist.objects.get(name='t Playlist'),Album.objects.get(name='t Evaporate')).playlist
    't playlist'
    """
    return PlaylistToAlbum(track_num=track_num, playlist=playlist, album=album)


def new_playlisttoplaylist(playlist: Playlist, member_playlist: Playlist, track_num: int = None, verbose: bool = True):
    """
    playlist and member_playlist are required and cannot be the same

    >>> new_playlisttoplaylist(Playlist.objects.get(name='t Playlist'),Playlist.objects.get(name='t Play Liszt')).playlist
    't playlist'
    """

    if playlist != member_playlist:
        return PlaylistToPlaylist(track_num=track_num, playlist=playlist, member_playlist=member_playlist)
    elif verbose:
        print("playlist cannot equal member_playlist")
    return None


def new_playlist(name: str, items_and_track_nums: [[str, int]]):
    """
    name is required
    items_and_track_nums is an array of [object, track_num] pairs.
    object must be Song, Album, or Playlist. track_num can be None.

    >>> new_playlist('t Play Liszt').name
    't Play Liszt'
    >>> new_playlist('t Playlist', [[Song.objects.get(name='t Lost'),1], [Album.objects.get(name='t Drift Away'), None], [Playlist.objects.get(name='t Play Liszt'), None]]).name
    't Playlist'
    """
    p = Playlist(name=name)
    p.save()

    if items_and_track_nums:
        for [item, track_num] in items_and_track_nums:
            if item.__class__ == Song:
                new_playlisttosong(p, item, track_num)
            if item.__class__ == Album:
                new_playlisttoalbum(p, item, track_num)
            if item.__class__ == Playlist:
                new_playlisttoplaylist(p, item, track_num)

    p.save()
    return p


def generate_playlist(name: str, params: [[str, object, object]]):
    """
    params is an array of [field name, value, range].
    Example: ['arousal', 0.5, 0.1] will get all songs with an arousal value within 0.1 of 0.5.
    The range element is optional, as in: ['artists', Artist.objects.get(name='Rameses B'), None], which will return all
    songs listing Rameses B as an artist.
    """
    songs = []
    for [field, value, val_range] in params:
        if isinstance(value, int) or isinstance(value, float):
            value = float(value)
            if val_range is None:
                val_range = 0.00000000001
            if isinstance(val_range, int) or isinstance(val_range, float):
                for song in Song.objects.all():
                    if value - val_range <= getattr(song, field) <= value + val_range:
                        songs.append(song)
        else:
            for song in Song.objects.all():
                if getattr(song, field) == value:
                    songs.append(song)

    return new_playlist(name, [[song, None] for song in songs])


if __name__ == "__main__":
    import doctest

    ### uncomment if your database is empty
    # pop = new_genre('t pop')
    # orch = new_genre('t orchestral')
    #
    # tri = new_artist('t Trivecta')
    # cold = new_artist('t Coldplay', [pop])
    # hill = new_artist('t Hillsong')
    # shock = new_artist('t Shockline')
    # thom = new_artist('t Thomas Bergersen', [orch])
    #
    # eva = new_song(name='t Evaporate', path="H:/Music/[Trance] - Trivecta - Evaporate (feat. Aloma Steele) [Monstercat Release].mp3",
    #                artists=[tri], arousal=-0.4, valence=1)
    # sky = new_song(name='t A Sky Full of Stars', path="H:/Music/A Sky Full Of Stars.mp3", artists=[cold], arousal=-0.5, valence=0.8, song_genres=[pop])
    # al1 = new_song(name='t Alive', path="H:/Music/Alive(0).mp3", artists=[hill], arousal=0.1, valence=0.8)
    # al2 = new_song(name='t Alive', path="H:/Music/Alive.mp3", artists=[shock], arousal=-0.5, valence=-0.5)
    # always = new_song(name='t Always Mine', path="H:/Music/Always Mine.mp3", artists=[thom], arousal=0.3, valence=0.8, song_genres=[orch])
    # b4 = new_song(name='t Before Time', path="H:/Music/Before Time.mp3", artists=[thom], arousal=0.3, valence=0.6, song_genres=[orch])
    #
    # sky_al = new_album(name='t A Sky Full of Stars', album_artists=[cold], songs_and_track_nums=[[sky, 1]])
    # sun = new_album(name='t Sun', album_artists=[thom], songs_and_track_nums=[[always, 11], [b4, 1]])

    doctest.testmod()

    # pop.delete()
    # orch.delete()
    # tri.delete()
    # cold.delete()
    # hill.delete()
    # shock.delete()
    # thom.delete()
    # eva.delete()
    # sky.delete()
    # al1.delete()
    # al2.delete()
    # always.delete()
    # b4.delete()
    # sky_al.delete()
    # sun.delete()

