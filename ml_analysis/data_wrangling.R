
library(tidyverse)

tracks <- read.csv("../data/tracks.csv")
track_artists <- read.csv("../data/track_artists.csv")
artists <- read.csv("../data/artists.csv")
billboard_songs <- read.csv("../data/billboard_hot_songs.csv")

tracks <- tracks |>
  mutate(
    acousticness = acousticness * 100,
    danceability = danceability * 100,
    energy = energy * 100,
    instrumentalness = instrumentalness * 100,
    liveness = liveness * 100,
    mode = ifelse(mode == "Mode.MAJOR", "major", "minor"),
    speechiness = speechiness * 100,
    valence = valence * 100,
    duration = as.period(seconds_to_period(round(duration_ms / 1000)))
  ) |>
  select(-duration_ms)