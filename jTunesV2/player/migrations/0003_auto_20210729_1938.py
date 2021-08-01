# Generated by Django 3.2.3 on 2021-07-29 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_alter_song_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='arousal',
            field=models.DecimalField(blank=True, decimal_places=20, default=0, max_digits=21, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='valence',
            field=models.DecimalField(blank=True, decimal_places=20, default=0, max_digits=21, null=True),
        ),
    ]