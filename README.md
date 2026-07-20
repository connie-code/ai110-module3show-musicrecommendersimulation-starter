# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Real-world recommenders like Spotify and YouTube learn taste from massive behavioral data, blending collaborative filtering (finding patterns across millions of users — "people like you also liked this") with content-based filtering (matching the actual attributes of songs, like tempo and mood) and deep-learning ranking models that weigh hundreds of signals. My music recommender version is a content-based recommender. It represents each song by its attributes (genre, mood, energy, and acousticness) and a user by their explicit taste profile using a weighted sum of four features. It prioritizes mood most heavily (weight 3), since mood best predicts whether a listener enjoys a song right now, followed by genre and energy (weight 2 each) — with energy scored by closeness to the user's target rather than raw loudness — and finally acoustic preference (weight 1). The songs with the highest scores are recommended and because the scoring is a simple explicit rule, the system can explain exactly why it picked each one.

---

## How The System Works
Explain the mucis recommender design in plain language.
Some prompts to answer:
- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

Each `Song` is stored with its identity (`id`, `title`, `artist`) and the attributes the recommender scores on (`genre` and `mood` and `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`).The scoring will focus on genre, mood, energy, and acousticness. The `UserProfile` captures a listener's explicit taste: their `favorite_genre`, their `favorite_mood`, a `target_energy` (the energy level they're in the mood for), and `likes_acoustic` (whether they prefer an acoustic or a more produced sound). How the `Recommender` recommends songs is by comparing each song to the profile and adding up points using a weighted sum on a 100-point scheme, where every feature produces a value between 0 and 1 that is then multiplied by its weight: a mood match (35 points), a genre match (25 points), an energy closeness score that is highest when the song's energy is close to `target_energy` and falls off as it drifts away in either direction (30 points), and an acoustic-alignment check (10 points), for a final score from 0 to 100. Genre is scored with soft points rather than a hard filter, meaning a genre mismatch simply forgoes those points instead of removing the song, so a strong song that just misses the exact genre can still rank well; this matters because the catalog is genre-sparse and a hard filter would starve the results. Mood is weighted highest because it best predicts whether a listener enjoys a song right now, and energy is scored by closeness, which respects the user's intended vibe. Energy is weighted a little lower than mood because mood and energy are correlated in this catalog (chill songs run low-energy, intense songs run high), so keeping energy below mood avoids double-counting the same "vibe" and lets genre and acousticness still influence the ranking.

### Algorithm Recipe

For each song in the catalog, compute a score out of 100 and a list of reasons:

1. **Mood (35 points).** If the song's `mood` equals the user's `favorite_mood`, add 35 points and record the reason "mood match". Otherwise add 0.
2. **Genre (25 points, soft).** If the song's `genre` equals the user's `favorite_genre`, add 25 points and record "genre match". Otherwise add 0 — the song is *not* removed, it just forgoes these points.
3. **Energy closeness (30 points).** Compute `closeness = 1 - abs(song.energy - user.target_energy)` (clamped to 0), then add `30 * closeness`. The closer the song's energy is to `target_energy`, the more points; record "energy fit" when closeness is high.
4. **Acoustic alignment (10 points).** Treat the song as acoustic when `acousticness > 0.5`. If that matches the user's `likes_acoustic` preference, add 10 points and record "acoustic match". Otherwise add 0.
5. **Total.** Sum the four parts for a final score from 0 to 100.

After scoring every song, **sort by score descending** and return the top `k` number. Because each score is just the sum of these four clear rules, the recorded reasons can be joined into a plain-language explanation of exactly why each song was picked. Finally, the recommender scores every song in the catalog, sorts them from highest to lowest, and returns the top amount and because each score is just the sum of a few clear rules, it can also explain exactly why a song was picked.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

============================================================
  USER PROFILE — Happy Pop
============================================================
  Favorite genre : pop
  Favorite mood  : happy
  Target energy  : 0.75
  Prefers sound  : produced

============================================================
  TOP RECOMMENDATIONS
============================================================

  1. Sunrise City  —  Neon Echo
     Score:  97.9 / 100
       • mood match (+35.0)
       • genre match (+25.0)
       • energy fit (+27.9)
       • produced match (+10.0)

  2. Rooftop Lights  —  Indigo Parade
     Score:  74.7 / 100
       • mood match (+35.0)
       • energy fit (+29.7)
       • produced match (+10.0)

  3. Gym Hero  —  Max Pulse
     Score:  59.6 / 100
       • genre match (+25.0)
       • energy fit (+24.6)
       • produced match (+10.0)

  4. Night Drive Loop  —  Neon Echo
     Score:  40.0 / 100
       • energy fit (+30.0)
       • produced match (+10.0)

  5. Concrete Bars  —  Kairo Vane
     Score:  37.0 / 100
       • energy fit (+27.0)
       • produced match (+10.0)

============================================================

============================================================
  USER PROFILE — Sad but Hyper (conflicting)
============================================================
  Favorite genre : pop
  Favorite mood  : sad
  Target energy  : 0.95
  Prefers sound  : produced

============================================================
  TOP RECOMMENDATIONS
============================================================

  1. Gym Hero  —  Max Pulse
     Score:  64.4 / 100
       • genre match (+25.0)
       • energy fit (+29.4)
       • produced match (+10.0)

  2. Sunrise City  —  Neon Echo
     Score:  61.1 / 100
       • genre match (+25.0)
       • energy fit (+26.1)
       • produced match (+10.0)

  3. Iron Verdict  —  Ashen Crown
     Score:  39.7 / 100
       • energy fit (+29.7)
       • produced match (+10.0)

  4. Storm Runner  —  Voltline
     Score:  38.8 / 100
       • energy fit (+28.8)
       • produced match (+10.0)

  5. Pulse Chamber  —  Null Sector
     Score:  37.9 / 100
       • energy fit (+27.9)
       • produced match (+10.0)

============================================================

============================================================
  USER PROFILE — Impossible Energy (out of range)
============================================================
  Favorite genre : rock
  Favorite mood  : intense
  Target energy  : 5.00
  Prefers sound  : produced

============================================================
  TOP RECOMMENDATIONS
============================================================

  1. Storm Runner  —  Voltline
     Score:  70.0 / 100
       • mood match (+35.0)
       • genre match (+25.0)
       • energy fit (+0.0)
       • produced match (+10.0)

  2. Gym Hero  —  Max Pulse
     Score:  45.0 / 100
       • mood match (+35.0)
       • energy fit (+0.0)
       • produced match (+10.0)

  3. Sunrise City  —  Neon Echo
     Score:  10.0 / 100
       • energy fit (+0.0)
       • produced match (+10.0)

  4. Night Drive Loop  —  Neon Echo
     Score:  10.0 / 100
       • energy fit (+0.0)
       • produced match (+10.0)

  5. Rooftop Lights  —  Indigo Parade
     Score:  10.0 / 100
       • energy fit (+0.0)
       • produced match (+10.0)

============================================================

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

Some limitations of the recommender is the tiny catalog of songs and it favors mood over genre. 
---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

I learned that recommenders turn users preferences into data which are then used into an algorithm score to make predictions. The recommender has to decide on a couple of items and choose which prefence has more power over another in the scoring. Predictions may lean towards one way that might give predictions that are something a user might not actually like because of a attribute weighting amount. 

