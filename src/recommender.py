import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
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
    popularity: int
    release_decade: int
    detailed_mood: str
    language: str
    tempo_feel: str


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    preferred_language: str = "english"
    preferred_decade: int = 0  # 0 means no preference
    target_popularity: int = 0  # 0 means no preference


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score and rank all songs for a user, return top k."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
            "preferred_language": user.preferred_language,
            "preferred_decade": user.preferred_decade,
            "target_popularity": user.target_popularity,
        }
        song_dicts = [vars(s) for s in self.songs]
        results = recommend_songs(user_prefs, song_dicts, k)
        ids = [r[0]["id"] for r in results]
        return [s for s in self.songs if s.id in ids]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for why a song was recommended."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
            "preferred_language": user.preferred_language,
            "preferred_decade": user.preferred_decade,
            "target_popularity": user.target_popularity,
        }
        _, reasons = score_song(user_prefs, vars(song))
        return " | ".join(reasons) if reasons else "No strong matches found."


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["popularity"] = int(row["popularity"])
            row["release_decade"] = int(row["release_decade"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song against user preferences.
    Returns (score, reasons) where reasons explains each point awarded.

    Algorithm Recipe:
    - Genre match: +2.0 points
    - Mood match: +1.0 point
    - Energy similarity: up to +1.5 points
    - Acoustic bonus: +0.5 if user likes acoustic and acousticness > 0.7
    - Language match: +0.5 points
    - Decade match: +0.5 points
    - Popularity bonus: +0.5 if popularity >= 85
    """
    score = 0.0
    reasons = []

    # Genre match
    if song["genre"].lower() == user_prefs["favorite_genre"].lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match
    if song["mood"].lower() == user_prefs["favorite_mood"].lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity
    energy_gap = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = round(1.5 * (1 - energy_gap), 2)
    if energy_score > 0:
        score += energy_score
        reasons.append(f"energy similarity (+{energy_score})")

    # Acoustic bonus
    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.7:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    # Language match
    if user_prefs.get("preferred_language") and \
       song.get("language", "").lower() == user_prefs["preferred_language"].lower():
        score += 0.5
        reasons.append("language match (+0.5)")

    # Decade match
    if user_prefs.get("preferred_decade") and \
       song.get("release_decade") == user_prefs["preferred_decade"]:
        score += 0.5
        reasons.append(f"decade match {song['release_decade']}s (+0.5)")

    # Popularity bonus
    if song.get("popularity", 0) >= 85:
        score += 0.5
        reasons.append(f"popularity bonus (+0.5)")

    return round(score, 2), reasons


def score_song_with_mode(user_prefs: Dict, song: Dict, mode: str = "Balanced") -> Tuple[float, List[str]]:
    """Score a song using a specific scoring mode strategy."""
    score = 0.0
    reasons = []

    # Set weights based on mode — Challenge 2
    if mode == "Genre-First":
        genre_weight, mood_weight, energy_weight = 4.0, 0.5, 0.5
    elif mode == "Mood-First":
        genre_weight, mood_weight, energy_weight = 0.5, 4.0, 0.5
    elif mode == "Energy-Focused":
        genre_weight, mood_weight, energy_weight = 0.5, 0.5, 3.0
    else:  # Balanced
        genre_weight, mood_weight, energy_weight = 2.0, 1.0, 1.5

    if song["genre"].lower() == user_prefs["favorite_genre"].lower():
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight})")

    if song["mood"].lower() == user_prefs["favorite_mood"].lower():
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight})")

    energy_gap = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = round(energy_weight * (1 - energy_gap), 2)
    if energy_score > 0:
        score += energy_score
        reasons.append(f"energy similarity (+{energy_score})")

    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.7:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    if user_prefs.get("preferred_language") and \
       song.get("language", "").lower() == user_prefs["preferred_language"].lower():
        score += 0.5
        reasons.append("language match (+0.5)")

    if user_prefs.get("preferred_decade") and \
       song.get("release_decade") == user_prefs["preferred_decade"]:
        score += 0.5
        reasons.append(f"decade match {song['release_decade']}s (+0.5)")

    if song.get("popularity", 0) >= 85:
        score += 0.5
        reasons.append("popularity bonus (+0.5)")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score all songs and return the top k recommendations sorted highest to lowest."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return scored[:k]


def recommend_with_mode(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "Balanced") -> List[Tuple[Dict, float, List[str]]]:
    """Recommend songs using a specific scoring mode — Challenge 2."""
    scored = []
    for song in songs:
        score, reasons = score_song_with_mode(user_prefs, song, mode)
        scored.append((song, score, reasons))
    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return scored[:k]


def recommend_with_diversity(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Recommend songs with diversity penalty — no repeat artists — Challenge 3."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    scored = sorted(scored, key=lambda x: x[1], reverse=True)

    seen_artists = set()
    results = []
    for song, score, reasons in scored:
        artist = song["artist"]
        if artist not in seen_artists:
            results.append((song, score, reasons))
            seen_artists.add(artist)
        if len(results) == k:
            break
    return results