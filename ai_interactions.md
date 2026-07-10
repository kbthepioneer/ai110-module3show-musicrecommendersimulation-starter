# AI Interactions Log

---

## Agentic Workflow (Challenge 1 — Advanced Song Features)

**What task did you give the agent?**

I asked Claude to help me expand the music dataset by adding 5 new attributes to `data/songs.csv` and update the scoring logic in `src/recommender.py` to account for the new features. The new attributes were: `popularity` (0-100), `release_decade`, `detailed_mood`, `language`, and `tempo_feel`.

**Prompts used:**

- "I want to add 5 new song attributes to my CSV: popularity (0-100), release_decade, detailed_mood, language, and tempo_feel. Can you fill in these values for all 20 songs and give me the complete updated CSV?"
- "Now update score_song() in recommender.py to give bonus points for language match, decade match, and popularity. Keep the existing genre, mood, and energy logic intact."

**What did the agent generate or change?**

- Updated `data/songs.csv` with 5 new columns across all 20 songs
- Updated `Song` dataclass in `recommender.py` to include the new fields
- Updated `load_songs()` to parse `popularity` as int and `release_decade` as int
- Updated `score_song()` to award +0.5 for language match, +0.5 for decade match, and +0.5 popularity bonus for songs with popularity >= 85
- Updated `UserProfile` dataclass to include `preferred_language`, `preferred_decade`, and `target_popularity`

**What did you verify or fix manually?**

- Verified that all 20 songs had realistic values for the new fields (e.g., Frank Sinatra correctly assigned to the 1960s decade, Tupac to the 1990s)
- Confirmed that the new scoring bonus points were small enough (0.5 each) to not overwhelm the core genre/mood/energy weights
- Ran `python -m pytest tests/` and fixed the `make_small_recommender()` function in `tests/test_recommender.py` which was missing the new required Song fields

---

## Agentic Workflow (Challenge 2 — Multiple Scoring Modes)

**What task did you give the agent?**

I asked Claude to implement a Strategy-style pattern for scoring modes so users could switch between Balanced, Genre-First, Mood-First, and Energy-Focused ranking strategies.

**Prompts used:**

- "Add a scoring mode parameter to my recommender. I want four modes: Balanced (current weights), Genre-First (genre weight = 4.0), Mood-First (mood weight = 4.0), and Energy-Focused (energy weight = 3.0). Create a separate function called score_song_with_mode() and recommend_with_mode() that uses it."
- "Update src/main.py to run all four modes for the Hip-Hop Head profile and display the results using tabulate tables."

**What did the agent generate or change?**

- Added `score_song_with_mode(user_prefs, song, mode)` to `recommender.py`
- Added `recommend_with_mode(user_prefs, songs, k, mode)` to `recommender.py`
- Updated `src/main.py` to loop through all 4 modes and print comparison tables

**What did you verify or fix manually?**

- Verified that Genre-First mode still returned hip-hop songs at the top but with different score distributions
- Confirmed that Energy-Focused mode surfaced Calvin Harris (EDM, high energy) in position 5 for the Hip-Hop Head profile, showing that energy alone can bridge genre gaps
- Checked that the math was valid for each mode by manually calculating one score per mode

---

## Agentic Workflow (Challenge 3 — Diversity Penalty)

**What task did you give the agent?**

I asked Claude to implement a diversity penalty that prevents the same artist from appearing more than once in the top K recommendations.

**Prompts used:**

- "Add a recommend_with_diversity() function that filters out repeat artists from the top results. After scoring and sorting all songs, loop through them and skip any song whose artist is already in a seen_artists set."

**What did the agent generate or change?**

- Added `recommend_with_diversity(user_prefs, songs, k)` to `recommender.py`
- Updated `src/main.py` to show a diversity-on example for the Hip-Hop Head profile

**What did you verify or fix manually?**

- Verified that Nipsey Hussle only appeared once in the diversity results even though he has two songs in the catalog ("Who Detached Us" and "I Do This")
- Noted that with only 5 hip-hop artists in the dataset, the diversity penalty doesn't change results dramatically — a larger catalog would show a bigger difference

---

## Agentic Workflow (Challenge 4 — Visual Summary Table)

**What task did you give the agent?**

I asked Claude to replace the plain text CLI output with formatted tables using the `tabulate` library.

**Prompts used:**

- "Replace the print_recommendations() function in src/main.py with a print_table() function that uses tabulate with the rounded_outline format. The table should include columns for rank, title, artist, genre, mood, score, and why."

**What did the agent generate or change?**

- Installed `tabulate` via pip
- Replaced `print_recommendations()` with `print_table()` using `tabulate(..., tablefmt="rounded_outline")`
- Applied the table format to all 6 profiles, all 4 scoring modes, the diversity output, and the weight experiment

**What did you verify or fix manually?**

- Confirmed all columns displayed correctly by running `python -m src.main`
- Verified that the "Why" column showed the full reasons string for each recommendation

---

## Design Pattern (Challenge 2 — Strategy Pattern)

**Which design pattern did you use?**

The **Strategy Pattern** — a behavioral design pattern where different algorithms (scoring strategies) can be selected at runtime without changing the code that uses them.

**How did AI help you brainstorm or implement it?**

I asked Claude to suggest a clean way to support multiple scoring modes without duplicating the entire scoring function. Claude suggested parameterizing the weights inside a single `score_song_with_mode()` function using a `mode` string argument, which acts as a lightweight Strategy pattern. Rather than creating separate classes for each strategy (which would be more complex), the mode parameter selects different weight configurations at runtime — keeping the code modular and easy to extend.

**How does the pattern appear in your final code?**

In `src/recommender.py`, the `score_song_with_mode(user_prefs, song, mode)` function reads the `mode` parameter and sets `genre_weight`, `mood_weight`, and `energy_weight` accordingly before running the same scoring logic. The `recommend_with_mode()` function passes the mode down to `score_song_with_mode()` for every song in the catalog. This means adding a new mode (e.g., "Valence-First") only requires adding one new `elif` block — no restructuring needed.