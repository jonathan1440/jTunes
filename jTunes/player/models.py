from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Member(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    container = models.ForeignKey('Playlist', on_delete=models.CASCADE)


class Item(models.Model):
    name = models.CharField(max_length=200)


class Song(Item):
    A = "A"
    Bb = "A#/Bb"
    B = "B"
    C = "C"
    Db = "C#/Db"
    D = "D"
    Eb = "D#/Eb"
    E = "E"
    F = "F"
    Gb = "F#/Gb"
    G = "G"
    Ab = "G#/Ab"
    KEY_CHOICES = (
        (A, A),
        (Bb, Bb),
        (B, B),
        (C, C),
        (Db, Db),
        (D, D),
        (Eb, Eb),
        (E, E),
        (F, F),
        (Gb, Gb),
        (G, G),
        (Ab, Ab)
    )

    ionian = "I"
    dorian = "II"
    phrygian = "III"
    lydian = "IV"
    mixolydian = "V"
    aeolian = "VI"
    locrian = "VII"
    MODE_CHOICES = (
        (ionian, "Ionian (I)"),
        (dorian, "Dorian (II)"),
        (phrygian, "Phrygian (III)"),
        (lydian, "Lydian (IV)"),
        (mixolydian, "Mixolydian (V)"),
        (aeolian, "Aeolian (VI)"),
        (locrian, "Locrian (VII)")
    )

    artist = models.CharField(blank=True, max_length=200)
    composer = models.CharField(blank=True, max_length=200, default=artist)
    year = models.IntegerField(blank=True, null=True)
    genre = models.CharField(blank=True, max_length=200)
    length = models.DurationField(verbose_name="song length", blank=True, null=True, default=None)
    tempo = models.PositiveIntegerField(verbose_name="tempo (bpm)", blank=True, null=True, default=None,
                                        validators=[MinValueValidator(0), MaxValueValidator(2048)])
    key = models.CharField(blank=True, null=True, choices=KEY_CHOICES, default=None)
    mode = models.CharField(blank=True, null=True, choices=MODE_CHOICES, default=None)
    decibels = models.PositiveIntegerField(verbose_name="song loudness in Db", blank=True, null=True, default=0,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])
    lufs = models.IntegerField(verbose_name="song loudness in LUFS", blank=True, null=True, default=0,
                               validators=[MinValueValidator(-15), MaxValueValidator(0)])
    arousal = models.DecimalField(blank=True, null=True, default=None)
    valence = models.DecimalField(blank=True, null=True, default=None)


class Playlist(Item):
    items = models.ManyToManyField(Item, through=Member)
    pass


class Album(Playlist):
    artist = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, through=Member)

