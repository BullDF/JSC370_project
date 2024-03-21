# Billboard Hot Songs Analysis with Spotify

-- by Johnny Meng

Welcome to my JSC370 project on analyzing songs with the Spotify API 🎵. This project borrowed [this dataset on the hot 100 songs on Billboard](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs) from Kaggle as an entry point. From this, I randomly sampled 5000 songs for the analysis. Then the Spotify API was used to extract these 5000 songs from Spotify along with their audio features and popularity. Click to read more about the [Spotify web API](https://developer.spotify.com/documentation/web-api).

To use the Spotify API, I wrote a program importing the [Spotipy Python package](https://spotipy.readthedocs.io/en/2.22.1/?highlight=start#). The Python program can be found in the [`spot.py`](https://github.com/BullDF/JSC370_project/blob/main/spot.py) file in this repository. **To use this file, a file named `config.py` needs to be created that contains a `CLIENT_ID` and a `CLIENT_SECRET`, which can be obtained from the [Spotify web API](https://developer.spotify.com/documentation/web-api) website.**

The data exploration report can be found in [`report.pdf`](https://github.com/BullDF/JSC370_project/blob/main/report.pdf). More statistical inferences and models are to be done in the future.