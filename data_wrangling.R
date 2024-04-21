
# Import libraries
library(tidyverse)
library(lubridate)
library(tidytext)
library(wordcloud)
library(tm)
library(styler)
library(knitr)
library(gridExtra)

tracks <- read.csv("https://raw.githubusercontent.com/BullDF/billboard-songs-analysis-with-spotify/main/data/tracks.csv")
track_artists <- read.csv("https://raw.githubusercontent.com/BullDF/billboard-songs-analysis-with-spotify/main/data/track_artists.csv")
artists <- read.csv("https://raw.githubusercontent.com/BullDF/billboard-songs-analysis-with-spotify/main/data/artists.csv")

# Data wrangling
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

tracks_tokenized <- tracks |>
  unnest_tokens(word, name)

no_stopwords <- tracks_tokenized |>
  filter(!(word %in% stopwords("english"))) |>
  filter(!grepl("[[:digit:]]+", word))

tracks_tokenized_top_20 <- tracks_tokenized |>
  group_by(word) |>
  summarize(word_freq = n()) |>
  arrange(desc(word_freq)) |>
  head(20)

no_stopwords_top_20 <- no_stopwords |>
  group_by(word) |>
  summarize(word_freq = n()) |>
  arrange(desc(word_freq)) |>
  head(20)

tracks_with_artists <- merge(
  x = track_artists,
  y = artists,
  by.x = "artist_id",
  by.y = "id",
  all.x = TRUE,
  all.y = FALSE
) |>
  rename(artist_name = name)
