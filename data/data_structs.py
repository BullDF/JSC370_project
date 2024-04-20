from dataclasses import dataclass
from typing import List
from enum import Enum


class Mode(Enum):
    MAJOR = 1
    MINOR = 0


@dataclass
class Artist:
    id: str
    name: str


@dataclass
class AudioFeatures:
    acousticness: float
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    liveness: float
    loudness: float
    mode: Mode
    speechiness: float
    valence: float

    def get_features(self) -> List:
        return [self.acousticness,
                self.danceability,
                self.duration_ms,
                self.energy,
                self.instrumentalness,
                self.liveness,
                self.loudness,
                self.mode,
                self.speechiness,
                self.valence]


@dataclass
class Track:
    id: str
    name: str
    year: int
    artists: List[Artist]
    audio_features: AudioFeatures
    popularity: int
