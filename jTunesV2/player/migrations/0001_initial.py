# Generated by Django 3.2.3 on 2021-05-28 03:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_num', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.item')),
            ],
            bases=('player.item',),
        ),
        migrations.CreateModel(
            name='PlayableItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.item')),
            ],
            bases=('player.item',),
        ),
        migrations.CreateModel(
            name='PlaylistTo',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.order')),
            ],
            bases=('player.order',),
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('playableitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.playableitem')),
                ('num_items', models.PositiveIntegerField(default=0)),
            ],
            bases=('player.playableitem',),
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('playableitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.playableitem')),
                ('num_items', models.PositiveIntegerField(default=0)),
            ],
            bases=('player.playableitem',),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.item')),
                ('genres', models.ManyToManyField(blank=True, to='player.Genre')),
            ],
            bases=('player.item',),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('playableitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.playableitem')),
                ('path', models.FilePathField(blank=True, default='H:/Music', path='H:/Music')),
                ('year', models.IntegerField(blank=True, null=True)),
                ('length', models.DurationField(blank=True, default=None, null=True, verbose_name='song length')),
                ('tempo', models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2048)], verbose_name='tempo (bpm)')),
                ('key', models.CharField(blank=True, choices=[('A      maj', 'A      maj'), ('A     min', 'A     min'), ('A#/Bb maj', 'A#/Bb maj'), ('A#/Bb min', 'A#/Bb min'), ('B      maj', 'B      maj'), ('B      min', 'B      min'), ('C      maj', 'C      maj'), ('C      min', 'C      min'), ('C#/Db maj', 'C#/Db maj'), ('C#/Db min', 'C#/Db min'), ('D      maj', 'D      maj'), ('D      min', 'D      min'), ('D#/Eb maj', 'D#/Eb maj'), ('D#/Eb min', 'D#/Eb min'), ('E      maj', 'E      maj'), ('E      min', 'E      min'), ('F      maj', 'F      maj'), ('F      min', 'F      min'), ('F#/Gb maj', 'F#/Gb maj'), ('F#/Gb min', 'F#/Gb min'), ('G      maj', 'G      maj'), ('G      min', 'G      min'), ('G#/Ab maj', 'G#/Ab maj'), ('G#/Ab min', 'G#/Ab min')], default=None, max_length=10, null=True)),
                ('decibels', models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='song loudness in Db')),
                ('lufs', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(-15), django.core.validators.MaxValueValidator(0)], verbose_name='song loudness in LUFS')),
                ('arousal', models.DecimalField(blank=True, decimal_places=20, default=None, max_digits=21, null=True)),
                ('valence', models.DecimalField(blank=True, decimal_places=20, default=None, max_digits=21, null=True)),
                ('artists', models.ManyToManyField(blank=True, related_name='artist', to='player.Artist')),
                ('composers', models.ManyToManyField(blank=True, related_name='composer', to='player.Artist')),
                ('remix_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player.song')),
                ('song_genres', models.ManyToManyField(blank=True, to='player.Genre')),
            ],
            bases=('player.playableitem',),
        ),
        migrations.CreateModel(
            name='PlaylistToSong',
            fields=[
                ('playlistto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.playlistto')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.song')),
            ],
            bases=('player.playlistto',),
        ),
        migrations.CreateModel(
            name='PlaylistToPlaylist',
            fields=[
                ('playlistto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.playlistto')),
                ('member_playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.playlist')),
            ],
            bases=('player.playlistto',),
        ),
        migrations.CreateModel(
            name='PlaylistToAlbum',
            fields=[
                ('playlistto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.playlistto')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.album')),
            ],
            bases=('player.playlistto',),
        ),
        migrations.AddField(
            model_name='playlistto',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.playlist'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='albums',
            field=models.ManyToManyField(blank=True, through='player.PlaylistToAlbum', to='player.Album'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='playlists',
            field=models.ManyToManyField(blank=True, related_name='_player_playlist_playlists_+', through='player.PlaylistToPlaylist', to='player.Playlist'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(blank=True, through='player.PlaylistToSong', to='player.Song'),
        ),
        migrations.CreateModel(
            name='AlbumToSong',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='player.order')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.album')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.song')),
            ],
            bases=('player.order',),
        ),
        migrations.AddField(
            model_name='album',
            name='album_artists',
            field=models.ManyToManyField(blank=True, to='player.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='songs',
            field=models.ManyToManyField(through='player.AlbumToSong', to='player.Song'),
        ),
    ]
