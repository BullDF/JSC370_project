import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import CLIENT_ID, CLIENT_SECRET

from typing import List
from nltk import word_tokenize

client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=client_credentials_manager)

GENRES = ['rap', 'hip', 'classic', 'soul', 'country', 'pop', 'rock', 'other']

def get_genre(genres: List[str]) -> str:
    global g
    for genre in genres:
        genre = word_tokenize(genre.lower())
        for w in genre:
            if w in GENRES:
                return w
    return 'other'


def search_artists(artist_ids: List[str]) -> List[str]:
    artists = sp.artists(artist_ids)['artists']
    genres = []
    for artist in artists:
        genres.append(get_genre(artist['genres']))
    return genres


def main() -> None:
    artists = pd.read_csv('artists.csv')
    # genres = []
    # for i in range(0, len(artists), 50):
    #     genres.extend(search_artists(list(artists[i:i + 50]['id'])))
    # genres = pd.Series(genres, name='genre')
    # genres.to_csv('genre.csv', index=False)

    genres = pd.read_csv('genre.csv')
    artists_with_genres = pd.concat([artists, genres], axis=1)
    artists_with_genres.to_csv('artists_with_genres.csv', index=False)

if __name__ == '__main__':
    main()

