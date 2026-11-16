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

Each song can earn up to 5 points:
- Genre match: +2.0. If the song's genre is the same as the user's favorite, it gets the biggest bonus. Genre is the strongest sign of taste.
- Mood match: +1.0. If the mood lines up (chill, happy, intense, etc.), the song gets a smaller bonus.
- Energy closeness: up to +1.5. Songs get more points the closer their energy is to the user's target. The formula is 1.5 × (1 − |song energy − target energy|). A perfect match gets the full 1.5, and a song at the opposite end of the scale gets close to 0.
- Acousticness closeness: up to +0.5. This only counts if the user has an acoustic preference. It's mostly a tie-breaker, for example to pick between similar lofi tracks.

Biases I expect
- A genre match is worth more than a mood match plus a pretty good energy match.
- "indie pop" doesn't count as "pop", so a pop fan could get Gym Hero (pop, but intense) ranked above Rooftop Lights (indie pop, happy and the right energy), even though Rooftop Lights probably feels like a better fit.
- There are only 18 songs, and most genres and moods appear once. 
- Energy decides most rankings once genre and mood run out, so users with weird energy targets might get odd results.
- The weights are my guesses, not tuned from real listening data, so they reflect my assumptions.


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

Output from `python -m src.main` for the default **pop / happy** profile (each song shows its score and the reasons behind it):

```
Loaded songs: 18

============================================================
Profile: Default: pop / happy
         genre=pop, mood=happy, energy=0.80, prefers non-acoustic
============================================================

#1  Sunrise City by Neon Echo
    Score: 0.99 / 1.00   [pop, happy]
    Why:
      - energy 0.82 vs target 0.80 (+0.39)
      - acousticness 0.18 vs target 0.20 (+0.20)
      - mood matches: happy (+0.25)
      - genre matches: pop (+0.15)

#2  Rooftop Lights by Indigo Parade
    Score: 0.80 / 1.00   [indie pop, happy]
    Why:
      - energy 0.76 vs target 0.80 (+0.38)
      - acousticness 0.35 vs target 0.20 (+0.17)
      - mood matches: happy (+0.25)

#3  Gym Hero by Max Pulse
    Score: 0.67 / 1.00   [pop, intense]
    Why:
      - energy 0.93 vs target 0.80 (+0.35)
      - acousticness 0.05 vs target 0.20 (+0.17)
      - genre matches: pop (+0.15)

#4  Concrete Crown by Verse Theory
    Score: 0.58 / 1.00   [hip hop, confident]
    Why:
      - energy 0.78 vs target 0.80 (+0.39)
      - acousticness 0.12 vs target 0.20 (+0.18)

#5  Night Drive Loop by Neon Echo
    Score: 0.58 / 1.00   [synthwave, moody]
    Why:
      - energy 0.75 vs target 0.80 (+0.38)
      - acousticness 0.22 vs target 0.20 (+0.20)
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



