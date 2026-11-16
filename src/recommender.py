import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple

# Algorithm Recipe weights (sum to 1.0)
W_ENERGY = 0.40
W_ACOUSTIC = 0.20
W_MOOD = 0.25
W_GENRE = 0.15

ACOUSTIC_TARGET_LIKES = 0.8
ACOUSTIC_TARGET_DISLIKES = 0.2


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

def closeness(value: float, target: float) -> float:
    """1.0 at an exact match, falling linearly with distance from the target."""
    return 1.0 - abs(value - target)


def _profile_to_prefs(user: UserProfile) -> Dict:
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = _profile_to_prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda s: (-score_song(prefs, asdict(s))[0], s.title),
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    Returns (score in [0, 1], list of human-readable reasons).
    """
    reasons: List[str] = []
    score = 0.0

    target_energy = user_prefs["energy"]
    pts = W_ENERGY * closeness(song["energy"], target_energy)
    score += pts
    reasons.append(f"energy {song['energy']:.2f} vs target {target_energy:.2f} (+{pts:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    target_ac = ACOUSTIC_TARGET_LIKES if likes_acoustic else ACOUSTIC_TARGET_DISLIKES
    pts = W_ACOUSTIC * closeness(song["acousticness"], target_ac)
    score += pts
    reasons.append(f"acousticness {song['acousticness']:.2f} vs target {target_ac:.2f} (+{pts:.2f})")

    if song["mood"] == user_prefs.get("mood"):
        score += W_MOOD
        reasons.append(f"mood matches: {song['mood']} (+{W_MOOD:.2f})")

    if song["genre"] == user_prefs.get("genre"):
        score += W_GENRE
        reasons.append(f"genre matches: {song['genre']} (+{W_GENRE:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    scored.sort(key=lambda item: (-item[1], item[0]["title"]))
    return scored[:k]
