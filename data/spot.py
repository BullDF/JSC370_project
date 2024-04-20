
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import CLIENT_ID, CLIENT_SECRET
from data_structs import *
from utils import read_data
from tqdm import tqdm
import time

client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=client_credentials_manager)


def search_track(name: str, track_artists: str) -> Optional[Track]:
    query = f'{name} artist:{track_artists}'
    search_result = sp.search(query, type='track', limit=1)
    if not search_result['tracks']['items']:
        return None
    track = search_result['tracks']['items'][0]
    if name.lower() in track['name'].lower():
        artists = [Artist(artist['id'], artist['name']) for artist in track['artists']]

        track_audio_features = sp.audio_features(tracks=[track['id']])[0]
        audio_features = AudioFeatures(
            acousticness=track_audio_features['acousticness'],
            danceability=track_audio_features['danceability'],
            duration_ms=track_audio_features['duration_ms'],
            energy=track_audio_features['energy'],
            instrumentalness=track_audio_features['instrumentalness'],
            liveness=track_audio_features['liveness'],
            loudness=track_audio_features['loudness'],
            mode=Mode(track_audio_features['mode']),
            speechiness=track_audio_features['speechiness'],
            valence=track_audio_features['valence']
        )

        return Track(track['id'], track['name'], 0, artists, audio_features, track['popularity'])


def search_on_spotify(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    tracks = pd.DataFrame(columns=['id',
                                   'name',
                                   'year',
                                   'acousticness',
                                   'danceability',
                                   'duration_ms',
                                   'energy',
                                   'instrumentalness',
                                   'liveness',
                                   'loudness',
                                   'mode',
                                   'speechiness',
                                   'valence',
                                   'popularity'])
    track_artists = pd.DataFrame(columns=['track_id', 'artist_id'])
    artists = pd.DataFrame(columns=['id', 'name'])
    unique_tracks = set()
    unique_artists = set()

    for _, row in tqdm(df.iterrows(), desc='Search'):
        t_name = row['song']
        t_artist = row['artist']
        try:
            track = search_track(t_name, t_artist)
        except spotipy.SpotifyException:
            break
        if not track:
            continue
        if track.id not in unique_tracks:
            unique_artists.add(track.id)
            track_info = [track.id, track.name, row['year']]
            track_info.extend(track.audio_features.get_features())
            track_info.append(track.popularity)
            tracks.loc[len(tracks)] = track_info

            for artist in track.artists:
                track_artists.loc[len(track_artists)] = [track.id, artist.id]
                if artist.id not in unique_artists:
                    unique_artists.add(artist.id)
                    artists.loc[len(artists)] = [artist.id, artist.name]

        # To prevent overloading the API
        time.sleep(1)

    return tracks, track_artists, artists


def create_csv() -> None:
    df = read_data()
    tracks, track_artists, artists = search_on_spotify(df)
    tracks.to_csv('tracks.csv', index=False, header=False, mode='a')
    track_artists.to_csv('track_artists.csv', index=False, header=False, mode='a')
    artists.to_csv('artists.csv', index=False, header=False, mode='a')


if __name__ == '__main__':
    create_csv()
