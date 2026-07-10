"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # --- Profile 1: Hip-Hop Head ---
    print("=" * 50)
    print("Profile 1: Hip-Hop Head")
    print("=" * 50)
    print_recommendations(recommend_songs({
        "favorite_genre": "hip-hop",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
    }, songs, k=5))

    # --- Profile 2: Chill Vibes ---
    print("=" * 50)
    print("Profile 2: Chill Vibes")
    print("=" * 50)
    print_recommendations(recommend_songs({
        "favorite_genre": "soul",
        "favorite_mood": "moody",
        "target_energy": 0.40,
        "likes_acoustic": True,
    }, songs, k=5))

    # --- Profile 3: Fiesta Mode ---
    print("=" * 50)
    print("Profile 3: Fiesta Mode")
    print("=" * 50)
    print_recommendations(recommend_songs({
        "favorite_genre": "banda",
        "favorite_mood": "happy",
        "target_energy": 0.75,
        "likes_acoustic": False,
    }, songs, k=5))

    # --- Profile 4: Country Soul ---
    print("=" * 50)
    print("Profile 4: Country Soul")
    print("=" * 50)
    print_recommendations(recommend_songs({
        "favorite_genre": "country",
        "favorite_mood": "relaxed",
        "target_energy": 0.30,
        "likes_acoustic": True,
    }, songs, k=5))

    # --- Profile 5: EDM Party ---
    print("=" * 50)
    print("Profile 5: EDM Party")
    print("=" * 50)
    print_recommendations(recommend_songs({
        "favorite_genre": "edm",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
    }, songs, k=5))

    # --- Profile 6: R&B Nights ---
    print("=" * 50)
    print("Profile 6: R&B Nights")
    print("=" * 50)
    print_recommendations(recommend_songs({
        "favorite_genre": "r&b",
        "favorite_mood": "moody",
        "target_energy": 0.50,
        "likes_acoustic": False,
    }, songs, k=5))


def print_recommendations(recommendations):
    for i, (song, score, reasons) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Why: {', '.join(reasons)}")
        print()


if __name__ == "__main__":
    main()