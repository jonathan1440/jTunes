# Generated by Django 3.1.6 on 2021-03-18 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='song_genre',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='player.genre'),
        ),
    ]