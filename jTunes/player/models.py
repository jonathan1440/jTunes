from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.apps import AppConfig


class Item(models.Model):
    name = models.CharField(max_length=200)


class Genre(Item):
    # TODO: make name a unique field
    pass


class Artist(Item):
    genres = models.ManyToManyField(Genre, blank=True)


class PlayableItem(Item):
    pass


class Song(PlayableItem):
    class Keys:
        A = "A      maj"
        Bb = "A#/Bb maj"
        B = "B      maj"
        C = "C      maj"
        Db = "C#/Db maj"
        D = "D      maj"
        Eb = "D#/Eb maj"
        E = "E      maj"
        F = "F      maj"
        Gb = "F#/Gb maj"
        G = "G      maj"
        Ab = "G#/Ab maj"
        Am = "A     min"
        Bbm = "A#/Bb min"
        Bm = "B      min"
        Cm = "C      min"
        Dbm = "C#/Db min"
        Dm = "D      min"
        Ebm = "D#/Eb min"
        Em = "E      min"
        Fm = "F      min"
        Gbm = "F#/Gb min"
        Gm = "G      min"
        Abm = "G#/Ab min"

    KEY_CHOICES = (
        (Keys.A, Keys.A),
        (Keys.Am, Keys.Am),
        (Keys.Bb, Keys.Bb),
        (Keys.Bbm, Keys.Bbm),
        (Keys.B, Keys.B),
        (Keys.Bm, Keys.Bm),
        (Keys.C, Keys.C),
        (Keys.Cm, Keys.Cm),
        (Keys.Db, Keys.Db),
        (Keys.Dbm, Keys.Dbm),
        (Keys.D, Keys.D),
        (Keys.Dm, Keys.Dm),
        (Keys.Eb, Keys.Eb),
        (Keys.Ebm, Keys.Ebm),
        (Keys.E, Keys.E),
        (Keys.Em, Keys.Em),
        (Keys.F, Keys.F),
        (Keys.Fm, Keys.Fm),
        (Keys.Gb, Keys.Gb),
        (Keys.Gbm, Keys.Gbm),
        (Keys.G, Keys.G),
        (Keys.Gm, Keys.Gm),
        (Keys.Ab, Keys.Ab),
        (Keys.Abm, Keys.Abm),
    )

    path = models.FilePathField(path="H:/Music", default="H:/Music")
    artists = models.ManyToManyField(Artist, blank=True, related_name='artist')
    remix_of = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    composers = models.ManyToManyField(Artist, blank=True, related_name='composer')
    year = models.IntegerField(blank=True, null=True)
    song_genres = models.ManyToManyField(Genre, blank=True)
    length = models.DurationField(verbose_name="song length", blank=True, null=True, default=None)
    tempo = models.PositiveIntegerField(verbose_name="tempo (bpm)", blank=True, null=True, default=None,
                                        validators=[MinValueValidator(0), MaxValueValidator(2048)])
    key = models.CharField(blank=True, null=True, choices=KEY_CHOICES, default=None, max_length=10)
    decibels = models.PositiveIntegerField(verbose_name="song loudness in Db", blank=True, null=True, default=0,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])
    lufs = models.IntegerField(verbose_name="song loudness in LUFS", blank=True, null=True, default=0,
                               validators=[MinValueValidator(-15), MaxValueValidator(0)])
    arousal = models.DecimalField(blank=True, null=True, default=None, decimal_places=20, max_digits=21)
    valence = models.DecimalField(blank=True, null=True, default=None, decimal_places=20, max_digits=21)


class Album(PlayableItem):
    num_items = models.PositiveIntegerField(default=0)  # TODO: implement count, set editable=False
    album_artists = models.ManyToManyField(Artist, blank=True)
    songs = models.ManyToManyField(Song, through='AlbumToSong')


class Playlist(PlayableItem):
    num_items = models.PositiveIntegerField(default=0)  # TODO: implement count, set editable=False
    songs = models.ManyToManyField(Song, through='PlaylistToSong', blank=True)
    albums = models.ManyToManyField(Album, through='PlaylistToAlbum', blank=True)
    playlists = models.ManyToManyField('self', through='PlaylistToPlaylist', blank=True)  # TODO: prevent referencing itself


#### 'through' models ####
class Order(models.Model):
    track_num = models.PositiveIntegerField(blank=True, null=True)


class AlbumToSong(Order):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class PlaylistTo(Order):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)


class PlaylistToSong(PlaylistTo):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class PlaylistToPlaylist(PlaylistTo):
    member_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)


class PlaylistToAlbum(PlaylistTo):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
