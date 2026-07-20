import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read the CSV into a list of dicts, keeping text columns as strings and parsing `id` to int and audio features to float."""
    # Columns that should be numeric; everything else stays a string.
    int_fields = {"id"}
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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song out of 100 (mood 35 + genre 25 + energy-closeness 30 + acoustic 10), returning (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # 1. Mood match (35 points) — exact match on the categorical mood.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 35.0
        reasons.append("mood match (+35.0)")

    # 2. Genre match (25 points, soft) — a miss simply forgoes the points.
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 25.0
        reasons.append("genre match (+25.0)")

    # 3. Energy closeness (30 points) — highest when the song's energy is near
    #    target_energy, falling off in either direction. closeness in [0, 1].
    closeness = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    closeness = max(0.0, closeness)
    energy_points = 30.0 * closeness
    score += energy_points
    reasons.append(f"energy fit (+{energy_points:.1f})")

    # 4. Acoustic alignment (10 points) — reward when the song's acoustic-ness
    #    agrees with the user's stated preference.
    song_is_acoustic = song["acousticness"] > 0.5
    if song_is_acoustic == user_prefs["likes_acoustic"]:
        score += 10.0
        label = "acoustic match" if user_prefs["likes_acoustic"] else "produced match"
        reasons.append(f"{label} (+10.0)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song with score_song(), sort by score descending, and return the top `k` as (song, score, explanation) tuples."""
    # 1. Score every song, building (song, score, explanation) tuples.
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    # 2. Sort by score (highest first) and keep only the top k.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
