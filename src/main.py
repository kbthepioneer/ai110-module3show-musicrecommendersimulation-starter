"""
Command line runner for the Music Recommender Simulation.
Includes Challenge 2 (scoring modes), Challenge 3 (diversity penalty),
and Challenge 4 (visual table using tabulate).
"""

from src.recommender import load_songs, recommend_songs, recommend_with_mode, recommend_with_diversity
from tabulate import tabulate


def print_table(recommendations, title):
    """Challenge 4: Print recommendations as a formatted table."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    table = []
    for i, (song, score, reasons) in enumerate(recommendations, 1):
        table.append([
            i,
            song["title"],
            song["artist"],
            song["genre"],
            song["mood"],
            f"{score:.2f}",
            ", ".join(reasons),
        ])
    print(tabulate(
        table,
        headers=["#", "Title", "Artist", "Genre", "Mood", "Score", "Why"],
        tablefmt="rounded_outline"
    ))


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded songs: {len(songs)}")

    # ─── Standard Profiles ───────────────────────────────────────
    hip_hop = {
        "favorite_genre": "hip-hop",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
        "preferred_language": "english",
        "preferred_decade": 1990,
        "target_popularity": 80,
    }

    chill_vibes = {
        "favorite_genre": "soul",
        "favorite_mood": "moody",
        "target_energy": 0.40,
        "likes_acoustic": True,
        "preferred_language": "english",
        "preferred_decade": 1960,
        "target_popularity": 90,
    }

    fiesta = {
        "favorite_genre": "banda",
        "favorite_mood": "happy",
        "target_energy": 0.75,
        "likes_acoustic": False,
        "preferred_language": "spanish",
        "preferred_decade": 2010,
        "target_popularity": 80,
    }

    country_soul = {
        "favorite_genre": "country",
        "favorite_mood": "relaxed",
        "target_energy": 0.30,
        "likes_acoustic": True,
        "preferred_language": "english",
        "preferred_decade": 1980,
        "target_popularity": 85,
    }

    edm_party = {
        "favorite_genre": "edm",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "preferred_language": "english",
        "preferred_decade": 2010,
        "target_popularity": 80,
    }

    rnb_nights = {
        "favorite_genre": "r&b",
        "favorite_mood": "moody",
        "target_energy": 0.50,
        "likes_acoustic": False,
        "preferred_language": "english",
        "preferred_decade": 2010,
        "target_popularity": 80,
    }

    # ─── Standard Recommendations ────────────────────────────────
    print_table(recommend_songs(hip_hop, songs, k=5), "Profile 1: Hip-Hop Head")
    print_table(recommend_songs(chill_vibes, songs, k=5), "Profile 2: Chill Vibes")
    print_table(recommend_songs(fiesta, songs, k=5), "Profile 3: Fiesta Mode")
    print_table(recommend_songs(country_soul, songs, k=5), "Profile 4: Country Soul")
    print_table(recommend_songs(edm_party, songs, k=5), "Profile 5: EDM Party")
    print_table(recommend_songs(rnb_nights, songs, k=5), "Profile 6: R&B Nights")

    # ─── Challenge 2: Scoring Modes ──────────────────────────────
    print("\n\n🎛️  CHALLENGE 2: SCORING MODES (Hip-Hop Head profile)")
    for mode in ["Balanced", "Genre-First", "Mood-First", "Energy-Focused"]:
        print_table(recommend_with_mode(hip_hop, songs, k=5, mode=mode), f"Mode: {mode}")

    # ─── Challenge 3: Diversity Penalty ──────────────────────────
    print("\n\n🎯  CHALLENGE 3: DIVERSITY PENALTY (no repeat artists)")
    print_table(recommend_with_diversity(hip_hop, songs, k=5), "Hip-Hop Head (Diversity ON)")

    # ─── Phase 4 Step 3: Weight Experiment ───────────────────────
    print("\n\n🧪  EXPERIMENT: Energy-Focused mode vs Balanced (Hip-Hop Head)")
    print_table(recommend_with_mode(hip_hop, songs, k=5, mode="Balanced"), "Balanced Weights")
    print_table(recommend_with_mode(hip_hop, songs, k=5, mode="Energy-Focused"), "Energy-Focused Weights")


if __name__ == "__main__":
    main()