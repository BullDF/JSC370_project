import pandas as pd
import numpy as np


def read_data(num_rows=5000) -> pd.DataFrame:
    df = pd.read_csv('billboard_hot_songs.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df = df.loc[:, ['song', 'artist', 'year']]

    rng = np.random.default_rng(370)
    sample = rng.choice(len(df), num_rows, replace=False)
    df = df.iloc[sample]

    assert len(df) == num_rows

    return df


def initialize_csv() -> None:
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

    tracks.to_csv('tracks.csv', index=False)
    track_artists.to_csv('track_artists.csv', index=False)
    artists.to_csv('artists.csv', index=False)

if __name__ == '__main__':
    initialize_csv()