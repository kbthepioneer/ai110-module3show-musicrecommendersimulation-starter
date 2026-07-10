# 🎵 Music Recommender Simulation

## Project Summary

This project simulates how a music streaming platform like Spotify decides what to recommend next. I built a content-based recommender that scores songs against a user's taste profile using attributes like genre, mood, energy, and acousticness. The system ranks all 20 songs in the catalog and returns the top matches with explanations for why each song was recommended.

---

## How The System Works

Each `Song` in the system has the following features:
- **genre** — musical style (hip-hop, soul, banda, edm, etc.)
- **mood** — emotional tone (happy, intense, moody, relaxed, chill, focused)
- **energy** — how hype or calm the song feels (0.0 to 1.0)
- **tempo_bpm** — beats per minute
- **valence** — musical positivity (0.0 to 1.0)
- **danceability** — how suitable for dancing (0.0 to 1.0)
- **acousticness** — how acoustic vs electronic the song is (0.0 to 1.0)

Each `UserProfile` stores:
- **favorite_genre** — the genre they prefer most
- **favorite_mood** — the mood they want from music
- **target_energy** — their preferred energy level (0.0 to 1.0)
- **likes_acoustic** — whether they prefer acoustic sounds

**Algorithm Recipe (how scores are calculated):**
- Genre match: **+2.0 points**
- Mood match: **+1.0 point**
- Energy similarity: **up to +1.5 points** (closer to target = more points)
- Acoustic bonus: **+0.5 points** if user likes acoustic and song acousticness > 0.7

Songs are ranked from highest to lowest score and the top K results are returned with explanations.

---

## Getting Started

### Setup

1. Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the recommender:

```bash
python -m src.main
```

### Running Tests

```bash
python -m pytest tests/
```

---

## Sample Recommendation Output

```
Loaded songs: 20

==================================================
Profile 1: Hip-Hop Head
==================================================
1. Man of the Year by Schoolboy Q
   Score: 4.50
   Why: genre match (+2.0), mood match (+1.0), energy similarity (+1.5)

2. I Do This by Nipsey Hussle ft. Young Thug and Mozzy
   Score: 4.46
   Why: genre match (+2.0), mood match (+1.0), energy similarity (+1.46)

3. To Live and Die in LA by Tupac
   Score: 4.43
   Why: genre match (+2.0), mood match (+1.0), energy similarity (+1.43)

4. Full Clip by Gang Starr
   Score: 4.40
   Why: genre match (+2.0), mood match (+1.0), energy similarity (+1.4)

5. Who Detached Us by Nipsey Hussle ft. Steve Jobs
   Score: 2.98
   Why: genre match (+2.0), energy similarity (+0.98)

==================================================
Profile 4: Country Soul
==================================================
1. On The Road Again by Willie Nelson
   Score: 5.00
   Why: genre match (+2.0), mood match (+1.0), energy similarity (+1.5), acoustic bonus (+0.5)

2. Sitting on the Dock of the Bay by Otis Redding
   Score: 2.97
   Why: mood match (+1.0), energy similarity (+1.47), acoustic bonus (+0.5)
```

---

## Experiments You Tried

- **Genre weight dominance:** Genre match (+2.0) is the strongest signal. Songs with a matching genre almost always appear in the top 3, even if mood or energy don't align perfectly.
- **Acoustic bonus:** Adding the acoustic bonus helped surface Willie Nelson and Sam Cooke for users who prefer acoustic sounds, which felt accurate.
- **Energy similarity:** Songs with energy very close to the user's target score near the maximum +1.5, while songs far away drop significantly. This makes energy a meaningful tiebreaker.
- **Diverse profiles:** Testing 6 different profiles showed that hip-hop, soul, banda, country, edm, and r&b users all get reasonable and distinct recommendations.

---

## Limitations and Risks

- The catalog is only 20 songs — a real system needs thousands to avoid repetition
- Genre matching is binary (match or no match), so norteno and banda are treated as completely different even though they are musically similar
- The system has no memory — it cannot learn from what a user skips or replays
- Songs without a genre or mood match rely entirely on energy similarity, which can produce unexpected results
- The dataset skews toward hip-hop (5 songs), which may over-represent that genre in results

---

## Reflection

See [Model Card](model_card.md) for full details.

Building this recommender taught me that even a simple algorithm can produce surprisingly accurate results when the features are chosen carefully. Genre and mood together act as strong filters, while energy similarity adds nuance. At the same time, the system revealed how easy it is to create a filter bubble — a user who loves hip-hop will almost always see hip-hop in their top 5, regardless of what else is in the catalog. Real platforms like Spotify solve this by mixing collaborative filtering (what similar users liked) with content-based filtering, adding diversity penalties, and learning from listening behavior over time.