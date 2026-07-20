"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, UserProfile


# Saved "taste profile": happy pop listener, moderate-high energy, prefers a
# produced (non-acoustic) sound. target_energy raised to 0.75 to match how
# happy-pop actually behaves (0.60 undersold it).
happy_pop_listener = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.75,
    likes_acoustic=False,
)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Same profile as a dict for the functional recommend_songs() path.
    user_prefs = {
        "favorite_genre": happy_pop_listener.favorite_genre,
        "favorite_mood": happy_pop_listener.favorite_mood,
        "target_energy": happy_pop_listener.target_energy,
        "likes_acoustic": happy_pop_listener.likes_acoustic,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # ---- Formatted terminal output -------------------------------------
    width = 60

    # User profile — shown first so the reader knows what the scores are
    # being matched against.
    acoustic_pref = "acoustic" if user_prefs["likes_acoustic"] else "produced"
    print()
    print("=" * width)
    print("  USER PROFILE")
    print("=" * width)
    print(f"  Favorite genre : {user_prefs['favorite_genre']}")
    print(f"  Favorite mood  : {user_prefs['favorite_mood']}")
    print(f"  Target energy  : {user_prefs['target_energy']:.2f}")
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


if __name__ == "__main__":
    main()
