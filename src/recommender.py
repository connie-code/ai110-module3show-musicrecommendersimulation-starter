import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """A song and its audio-feature attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    instrumentalness: float = 0.0
    speechiness: float = 0.0

@dataclass
class UserProfile:
    """A listener's taste; the four required fields plus optional numeric-feature targets (neutral defaults keep old profiles working)."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5          # musical positivity / cheerfulness
    target_danceability: float = 0.5     # how groove/dance oriented
    target_tempo_bpm: float = 120.0      # preferred speed, in BPM
    target_instrumentalness: float = 0.0 # 1.0 = wants no vocals
    target_speechiness: float = 0.1      # spoken-word / rap content

class Recommender:
    """OOP wrapper over the functional scorer so both APIs share one source of truth."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Songs for `user` (best first) via recommend_songs(), mapped back to Song objects."""
        user_prefs = asdict(user)
        song_dicts = [asdict(song) for song in self.songs]
        ranked = recommend_songs(user_prefs, song_dicts, k=k)

        by_id = {song.id: song for song in self.songs}
        return [by_id[song_dict["id"]] for song_dict, _score, _explanation in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the human-readable scoring breakdown for one song."""
        _score, reasons = score_song(asdict(user), asdict(song))
        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Read the CSV into dicts, parsing `id` to int and audio features to float (other columns stay strings)."""
    int_fields = {"id"}  # numeric columns; everything else stays a string
    float_fields = {
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "instrumentalness",
        "speechiness",
    }

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

# Per-feature point budget; sums to 100 so scores stay on a 0..100 scale (tweak to reweight).
FEATURE_WEIGHTS = {
    "mood": 20.0,
    "genre": 13.0,
    "energy": 14.0,
    "valence": 11.0,
    "danceability": 11.0,
    "tempo": 10.0,
    "instrumentalness": 8.0,
    "speechiness": 7.0,
    "acoustic": 6.0,
}

# BPM gap at which tempo closeness hits 0 (tempo isn't 0..1, so it needs its own scale).
TEMPO_TOLERANCE_BPM = 80.0


def _closeness(value: float, target: float, scale: float = 1.0) -> float:
    """Return 1.0 when value == target, decaying linearly to 0 at `scale` away."""
    return max(0.0, 1.0 - abs(value - target) / scale)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song out of 100 — exact-match on mood/genre, closeness on six audio features, boolean acoustic — returning (score, reasons)."""
    score = 0.0
    reasons: List[str] = []
    w = FEATURE_WEIGHTS

    # Categorical: exact-match awards.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    if song["genre"] == user_prefs["favorite_genre"]:
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    # Numeric: points scale with closeness to the user's target. (weight, song col, pref key, default, scale)
    numeric_features = [
        ("energy", "energy", "target_energy", 0.5, 1.0),
        ("valence", "valence", "target_valence", 0.5, 1.0),
        ("danceability", "danceability", "target_danceability", 0.5, 1.0),
        ("tempo", "tempo_bpm", "target_tempo_bpm", 120.0, TEMPO_TOLERANCE_BPM),
        ("instrumentalness", "instrumentalness", "target_instrumentalness", 0.0, 1.0),
        ("speechiness", "speechiness", "target_speechiness", 0.1, 1.0),
    ]
    for weight_key, song_col, pref_key, default_target, scale in numeric_features:
        target = user_prefs.get(pref_key, default_target)
        points = w[weight_key] * _closeness(song[song_col], target, scale)
        score += points
        reasons.append(f"{weight_key} fit (+{points:.1f})")

    # Acoustic: reward when the song's acoustic/produced nature matches the preference.
    song_is_acoustic = song["acousticness"] > 0.5
    if song_is_acoustic == user_prefs["likes_acoustic"]:
        score += w["acoustic"]
        label = "acoustic match" if user_prefs["likes_acoustic"] else "produced match"
        reasons.append(f"{label} (+{w['acoustic']:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top `k` as (song, score, explanation) tuples, highest score first."""
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
