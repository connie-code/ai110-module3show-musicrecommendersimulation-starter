"""
Command-line runner: builds listener profiles and prints their top recommendations.
Uses load_songs / score_song / recommend_songs from recommender.py.
"""

from src.recommender import (
    load_songs,
    recommend_songs,
    UserProfile,
    Recommender,
    Song,
)


# Baseline listener: cheerful, upbeat, produced pop at a moderate-high energy.
happy_pop_listener = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.75,
    likes_acoustic=False,
    target_valence=0.85,          # wants cheerful, upbeat songs
    target_danceability=0.75,     # groove-forward
    target_tempo_bpm=120.0,       # classic pop tempo
    target_instrumentalness=0.0,  # wants vocals
    target_speechiness=0.1,       # sung, not rapped/spoken
)


# ---- Adversarial / edge-case profiles: probe the scorer for odd results -----

# Conflicting taste: "sad" mood but very high energy pull opposite ways, so no
# song matches both and the top pick satisfies neither intent cleanly.
sad_but_hyper = UserProfile(
    favorite_genre="pop",
    favorite_mood="sad",
    target_energy=0.95,
    likes_acoustic=False,
)

# Out-of-range target (should be 0..1): at 5.0 energy closeness clamps to 0 for
# every song, silently zeroing the whole energy dimension.
impossible_energy = UserProfile(
    favorite_genre="rock",
    favorite_mood="intense",
    target_energy=5.0,
    likes_acoustic=False,
)


# Distinct listener personas as plain preference dicts (genre/mood values exist
# in data/songs.csv). Handy for quickly swapping tastes when experimenting.
USER_PROFILES = {
    "Happy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.75,
        "likes_acoustic": False,
        "target_valence": 0.85,
        "target_danceability": 0.75,
        "target_tempo_bpm": 120.0,
        "target_instrumentalness": 0.0,
        "target_speechiness": 0.1,
    },
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "intense",
        "target_energy": 0.93,
        "likes_acoustic": False,
        "target_valence": 0.7,
        "target_danceability": 0.8,
        "target_tempo_bpm": 140.0,
        "target_instrumentalness": 0.0,
        "target_speechiness": 0.1,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
        "target_valence": 0.5,
        "target_danceability": 0.5,
        "target_tempo_bpm": 80.0,
        "target_instrumentalness": 0.7,   # often vocal-free beats
        "target_speechiness": 0.05,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "target_valence": 0.4,
        "target_danceability": 0.45,
        "target_tempo_bpm": 150.0,
        "target_instrumentalness": 0.1,
        "target_speechiness": 0.1,
    },
}


def profile_to_prefs(profile: UserProfile) -> dict:
    """Convert a UserProfile into the dict shape recommend_songs() expects."""
    return {
        "favorite_genre": profile.favorite_genre,
        "favorite_mood": profile.favorite_mood,
        "target_energy": profile.target_energy,
        "likes_acoustic": profile.likes_acoustic,
        "target_valence": profile.target_valence,
        "target_danceability": profile.target_danceability,
        "target_tempo_bpm": profile.target_tempo_bpm,
        "target_instrumentalness": profile.target_instrumentalness,
        "target_speechiness": profile.target_speechiness,
    }


def run_profile(name: str, profile: UserProfile, songs: list, k: int = 5) -> None:
    """Score `songs` for one profile and print the profile + top-k results."""
    user_prefs = profile_to_prefs(profile)
    recommendations = recommend_songs(user_prefs, songs, k=k)

    width = 60
    acoustic_pref = "acoustic" if user_prefs["likes_acoustic"] else "produced"
    print()
    print("=" * width)
    print(f"  USER PROFILE — {name}")
    print("=" * width)
    print(f"  Favorite genre : {user_prefs['favorite_genre']}")
    print(f"  Favorite mood  : {user_prefs['favorite_mood']}")
    print(f"  Target energy  : {user_prefs['target_energy']:.2f}")
    print(f"  Target valence : {profile.target_valence:.2f}")
    print(f"  Target dance   : {profile.target_danceability:.2f}")
    print(f"  Target tempo   : {profile.target_tempo_bpm:.0f} bpm")
    print(f"  Instrumental   : {profile.target_instrumentalness:.2f}")
    print(f"  Speechiness    : {profile.target_speechiness:.2f}")
    print(f"  Prefers sound  : {acoustic_pref}")

    print()
    print("=" * width)
    print("  TOP RECOMMENDATIONS")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  {rank}. {song['title']}  —  {song['artist']}")
        print(f"     Score: {score:5.1f} / 100")
        # One reason per line so the scoring breakdown is easy to scan.
        for reason in explanation.split(", "):
            print(f"       • {reason}")

    print()
    print("=" * width)


def run_oop_demo(profile: UserProfile, song_dicts: list, k: int = 3) -> None:
    """Run the class-based API (Recommender) and print its top-k.
    Turns song dicts into Song objects so both APIs share the same scoring.
    """
    songs = [Song(**song_dict) for song_dict in song_dicts]
    recommender = Recommender(songs)
    top = recommender.recommend(profile, k=k)

    width = 60
    print()
    print("=" * width)
    print("  OOP API DEMO — Recommender class (Happy Pop)")
    print("=" * width)
    for rank, song in enumerate(top, start=1):
        print()
        print(f"  {rank}. {song.title}  —  {song.artist}")
        print(f"       {recommender.explain_recommendation(profile, song)}")
    print()
    print("=" * width)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Baseline "normal" listener.
    run_profile("Happy Pop", happy_pop_listener, songs, k=5)

    # Adversarial / edge-case profiles — watch for results that don't match
    # what a human would expect from the stated preferences.
    run_profile("Sad but Hyper (conflicting)", sad_but_hyper, songs, k=5)
    run_profile("Impossible Energy (out of range)", impossible_energy, songs, k=5)

    # Same taste, class-based API — should agree with the functional Happy Pop
    # results above, since both now call score_song().
    run_oop_demo(happy_pop_listener, songs, k=5)


if __name__ == "__main__":
    main()
