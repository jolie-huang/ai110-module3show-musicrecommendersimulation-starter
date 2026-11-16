# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.


- Music apps like Spotify guess what you'll like by looking at what other people play and skip, and also at the songs themselves. My version only looks at the songs and what one listener says they like, because with 10 songs and one user there's no crowd to learn from.
- Every song has its title, artist, genre, mood, energy, tempo, valence, danceability and acousticness. The score only looks at four of those: genre, mood, energy and acousticness. I left tempo out because it mostly moves with energy, so it would just count the same thing twice. Valence and danceability are loaded too, but I'm saving them for later experiments.
- The user profile stores a favorite genre, a favorite mood, a target energy level between 0 and 1, and a yes/no for whether they like acoustic music.
- A song gets scored by getting a score out of 1.0, built from:
- Energy (40%): I reward being close to what the user wants. If they want 0.8, a song at 0.82 gets nearly full credit and one at 0.35 gets much less.
- Acousticness (20%): If the user likes acoustic music the target is high, and if not it's low.
- Mood (25%): a flat rate if the song's mood matches exactly.
- Genre (15%): a smaller flat rate for an exact genre match.
- I made mood count for more than genre on purpose since mood is the feel you actually hear, while genre is more broad.
- The way a song gets picked is that every song in the catalog gets scored, then they're sorted from highest to lowest, with ties broken alphabetically so you get the same results every time. The top five become the recommendations, and each one comes with a short reason, like "energy 0.82 vs target 0.80" or "mood matches: happy".

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

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

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



