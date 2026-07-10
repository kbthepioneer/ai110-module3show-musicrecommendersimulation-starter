from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs, load_songs


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
            popularity=85,
            release_decade=2010,
            detailed_mood="euphoric",
            language="english",
            tempo_feel="fast",
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
            popularity=60,
            release_decade=2020,
            detailed_mood="nostalgic",
            language="english",
            tempo_feel="slow",
        ),
    ]
    return Recommender(songs)


# --- Original starter tests ---

def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- score_song tests ---

def test_score_song_genre_match_adds_points():
    user_prefs = {
        "favorite_genre": "hip-hop",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
    }
    song = {
        "genre": "hip-hop",
        "mood": "chill",
        "energy": 0.85,
        "acousticness": 0.1,
    }
    score, reasons = score_song(user_prefs, song)
    assert score > 0
    assert any("genre match" in r for r in reasons)


def test_score_song_mood_match_adds_points():
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.80,
        "likes_acoustic": False,
    }
    song = {
        "genre": "pop",
        "mood": "intense",
        "energy": 0.80,
        "acousticness": 0.1,
    }
    score, reasons = score_song(user_prefs, song)
    assert any("mood match" in r for r in reasons)


def test_score_song_acoustic_bonus():
    user_prefs = {
        "favorite_genre": "soul",
        "favorite_mood": "moody",
        "target_energy": 0.40,
        "likes_acoustic": True,
    }
    song = {
        "genre": "soul",
        "mood": "moody",
        "energy": 0.40,
        "acousticness": 0.85,
    }
    score, reasons = score_song(user_prefs, song)
    assert any("acoustic bonus" in r for r in reasons)


def test_score_song_no_acoustic_bonus_when_user_dislikes():
    user_prefs = {
        "favorite_genre": "soul",
        "favorite_mood": "moody",
        "target_energy": 0.40,
        "likes_acoustic": False,
    }
    song = {
        "genre": "soul",
        "mood": "moody",
        "energy": 0.40,
        "acousticness": 0.85,
    }
    score, reasons = score_song(user_prefs, song)
    assert not any("acoustic bonus" in r for r in reasons)


def test_score_song_returns_tuple():
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
    }
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "acousticness": 0.1,
    }
    result = score_song(user_prefs, song)
    assert isinstance(result, tuple)
    assert isinstance(result[0], float)
    assert isinstance(result[1], list)


# --- recommend_songs tests ---

def test_recommend_songs_returns_top_k():
    songs = [
        {"id": 1, "genre": "hip-hop", "mood": "intense", "energy": 0.85, "acousticness": 0.1, "title": "Song A", "artist": "Artist A"},
        {"id": 2, "genre": "pop", "mood": "happy", "energy": 0.50, "acousticness": 0.2, "title": "Song B", "artist": "Artist B"},
        {"id": 3, "genre": "soul", "mood": "moody", "energy": 0.40, "acousticness": 0.8, "title": "Song C", "artist": "Artist C"},
    ]
    user_prefs = {
        "favorite_genre": "hip-hop",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
    }
    results = recommend_songs(user_prefs, songs, k=2)
    assert len(results) == 2


def test_recommend_songs_sorted_highest_first():
    songs = [
        {"id": 1, "genre": "hip-hop", "mood": "intense", "energy": 0.85, "acousticness": 0.1, "title": "Song A", "artist": "Artist A"},
        {"id": 2, "genre": "pop", "mood": "happy", "energy": 0.20, "acousticness": 0.2, "title": "Song B", "artist": "Artist B"},
    ]
    user_prefs = {
        "favorite_genre": "hip-hop",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
    }
    results = recommend_songs(user_prefs, songs, k=2)
    assert results[0][1] >= results[1][1]


def test_recommend_songs_reasons_not_empty():
    songs = [
        {"id": 1, "genre": "hip-hop", "mood": "intense", "energy": 0.85, "acousticness": 0.1, "title": "Song A", "artist": "Artist A"},
    ]
    user_prefs = {
        "favorite_genre": "hip-hop",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
    }
    results = recommend_songs(user_prefs, songs, k=1)
    assert len(results[0][2]) > 0


# --- load_songs tests ---

def test_load_songs_returns_list():
    songs = load_songs("data/songs.csv")
    assert isinstance(songs, list)


def test_load_songs_correct_count():
    songs = load_songs("data/songs.csv")
    assert len(songs) == 20


def test_load_songs_numeric_fields():
    songs = load_songs("data/songs.csv")
    for song in songs:
        assert isinstance(song["energy"], float)
        assert isinstance(song["tempo_bpm"], float)
        assert isinstance(song["acousticness"], float)