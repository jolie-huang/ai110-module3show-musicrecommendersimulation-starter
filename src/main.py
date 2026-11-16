"""
Command line runner for the Music Recommender Simulation.

Loads the song catalog, scores it against each taste profile below, and
prints the top recommendations with the reasons behind every score.
"""

from src.recommender import load_songs, recommend_songs

# Named taste profiles. Keys match what score_song reads.
PROFILES = {
    "Default: pop / happy": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "likes_acoustic": False,
    },
    "Late-night study listener: lofi / chill": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.40,
        "likes_acoustic": True,
    },
}

WIDTH = 60


def describe(prefs: dict) -> str:
    acoustic = "likes acoustic" if prefs.get("likes_acoustic") else "prefers non-acoustic"
    return (
        f"genre={prefs['genre']}, mood={prefs['mood']}, "
        f"energy={prefs['energy']:.2f}, {acoustic}"
    )


def print_recommendations(name: str, prefs: dict, songs: list, k: int = 5) -> None:
    print("=" * WIDTH)
    print(f"Profile: {name}")
    print(f"         {describe(prefs)}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k=k), start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / 1.00   [{song['genre']}, {song['mood']}]")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
