from django.test import TestCase
from player.helpers import *


def create_test_database():
    objs = {}
    objs['popu'] = new_genre('t pop')
    objs['orch'] = new_genre('t orchestral')

    objs['tri'] = new_artist('t Trivecta')
    objs['cold'] = new_artist('t Coldplay', [objs['popu']])
    objs['hill'] = new_artist('t Hillsong')
    objs['shock'] = new_artist('t Shockline')
    objs['thom'] = new_artist('t Thomas Bergersen', [objs['orch']])

    objs['eva'] = new_song(name='t Evaporate',
                           path="H:/Music/[Trance] - Trivecta - Evaporate (feat. Aloma Steele) [Monstercat Release].mp3",
                           artists=[objs['tri']], arousal=-0.4, valence=1)
    objs['sky'] = new_song(name='t A Sky Full of Stars', path="H:/Music/A Sky Full Of Stars.mp3", artists=[objs['cold']], arousal=-0.5,
                   valence=0.8, song_genres=[objs['popu']])
    objs['al1'] = new_song(name='t Alive', path="H:/Music/Alive(0).mp3", artists=[objs['hill']], arousal=0.1, valence=0.8)
    objs['al2'] = new_song(name='t Alive', path="H:/Music/Alive.mp3", artists=[objs['shock']], arousal=-0.5, valence=-0.5)
    objs['always'] = new_song(name='t Always Mine', path="H:/Music/Always Mine.mp3", artists=[objs['thom']], arousal=0.3, valence=0.8,
                      song_genres=[objs['orch']])
    objs['b4'] = new_song(name='t Before Time', path="H:/Music/Before Time.mp3", artists=[objs['thom']], arousal=0.3, valence=0.6,
                  song_genres=[objs['orch']])

    objs['sky_al'] = new_album(name='t A Sky Full of Stars', album_artists=[objs['cold']], songs_and_track_nums=[[objs['sky'], 1]])
    objs['sun'] = new_album(name='t Sun', album_artists=[objs['thom']], songs_and_track_nums=[[objs['always'], 11], [objs['b4'], 1]])

    objs['liszt'] = new_playlist(name='t Play Liszt', items_and_track_nums=[[objs['tri'], None], [objs['sun'], None]])

    return objs


def delete_test_db(db_dict):
    for item in db_dict:
        item.delete()
