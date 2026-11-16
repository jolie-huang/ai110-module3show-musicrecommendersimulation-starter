# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a small music recommender that runs in the terminal. You give it a taste profile (favorite genre, favorite mood, target energy, and whether you like acoustic sounds), and it scores every song in an 18-song catalog and prints your top 5, with a "why" showing where each point came from.
The score is a simple weighted sum: how close the song's energy is to your target (the biggest piece), how close its acousticness is to what you like, plus bonuses if its mood and genre match yours exactly. I tested it on three normal profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and four tricky ones, like conflicting preferences and a genre that isn't in the catalog. It works well when your taste matches the catalog, but it struggles with contradictory or unmatched tastes, and it never tells you when it's unsure.
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

## System Evaluation: Profile Outputs

Run with `python -m src.main`. Top 5 results per profile (terminal output, 18-song catalog).

### High-Energy Pop

Works as intended: exact genre+mood match wins clearly.

```text
Profile: High-Energy Pop
         genre=pop, mood=happy, energy=0.90, prefers non-acoustic
============================================================

#1  Sunrise City by Neon Echo
    Score: 0.96 / 1.00   [pop, happy]
    Why:
      - energy 0.82 vs target 0.90 (+0.37)
      - acousticness 0.18 vs target 0.20 (+0.20)
      - mood matches: happy (+0.25)
      - genre matches: pop (+0.15)

#2  Rooftop Lights by Indigo Parade
    Score: 0.76 / 1.00   [indie pop, happy]
    Why:
      - energy 0.76 vs target 0.90 (+0.34)
      - acousticness 0.35 vs target 0.20 (+0.17)
      - mood matches: happy (+0.25)

#3  Gym Hero by Max Pulse
    Score: 0.71 / 1.00   [pop, intense]
    Why:
      - energy 0.93 vs target 0.90 (+0.39)
      - acousticness 0.05 vs target 0.20 (+0.17)
      - genre matches: pop (+0.15)

#4  Storm Runner by Voltline
    Score: 0.58 / 1.00   [rock, intense]
    Why:
      - energy 0.91 vs target 0.90 (+0.40)
      - acousticness 0.10 vs target 0.20 (+0.18)

#5  Neon Overdrive by Pulse Theory
    Score: 0.54 / 1.00   [edm, euphoric]
    Why:
      - energy 0.96 vs target 0.90 (+0.38)
      - acousticness 0.03 vs target 0.20 (+0.17)
```

### Chill Lofi

Works as intended: two lofi/chill songs tie near the top.

```text
Profile: Chill Lofi
         genre=lofi, mood=chill, energy=0.40, likes acoustic
============================================================

#1  Midnight Coding by LoRoom
    Score: 0.97 / 1.00   [lofi, chill]
    Why:
      - energy 0.42 vs target 0.40 (+0.39)
      - acousticness 0.71 vs target 0.80 (+0.18)
      - mood matches: chill (+0.25)
      - genre matches: lofi (+0.15)

#2  Library Rain by Paper Lanterns
    Score: 0.97 / 1.00   [lofi, chill]
    Why:
      - energy 0.35 vs target 0.40 (+0.38)
      - acousticness 0.86 vs target 0.80 (+0.19)
      - mood matches: chill (+0.25)
      - genre matches: lofi (+0.15)

#3  Spacewalk Thoughts by Orbit Bloom
    Score: 0.78 / 1.00   [ambient, chill]
    Why:
      - energy 0.28 vs target 0.40 (+0.35)
      - acousticness 0.92 vs target 0.80 (+0.18)
      - mood matches: chill (+0.25)

#4  Focus Flow by LoRoom
    Score: 0.75 / 1.00   [lofi, focused]
    Why:
      - energy 0.40 vs target 0.40 (+0.40)
      - acousticness 0.78 vs target 0.80 (+0.20)
      - genre matches: lofi (+0.15)

#5  Coffee Shop Stories by Slow Stereo
    Score: 0.57 / 1.00   [jazz, relaxed]
    Why:
      - energy 0.37 vs target 0.40 (+0.39)
      - acousticness 0.89 vs target 0.80 (+0.18)
```

### Deep Intense Rock

Works as intended. Gym Hero (pop) ranks #2 on mood + energy alone.

```text
Profile: Deep Intense Rock
         genre=rock, mood=intense, energy=0.92, prefers non-acoustic
============================================================

#1  Storm Runner by Voltline
    Score: 0.98 / 1.00   [rock, intense]
    Why:
      - energy 0.91 vs target 0.92 (+0.40)
      - acousticness 0.10 vs target 0.20 (+0.18)
      - mood matches: intense (+0.25)
      - genre matches: rock (+0.15)

#2  Gym Hero by Max Pulse
    Score: 0.82 / 1.00   [pop, intense]
    Why:
      - energy 0.93 vs target 0.92 (+0.40)
      - acousticness 0.05 vs target 0.20 (+0.17)
      - mood matches: intense (+0.25)

#3  Sunrise City by Neon Echo
    Score: 0.56 / 1.00   [pop, happy]
    Why:
      - energy 0.82 vs target 0.92 (+0.36)
      - acousticness 0.18 vs target 0.20 (+0.20)

#4  Neon Overdrive by Pulse Theory
    Score: 0.55 / 1.00   [edm, euphoric]
    Why:
      - energy 0.96 vs target 0.92 (+0.38)
      - acousticness 0.03 vs target 0.20 (+0.17)

#5  Iron Reign by Black Anvil
    Score: 0.55 / 1.00   [metal, angry]
    Why:
      - energy 0.97 vs target 0.92 (+0.38)
      - acousticness 0.04 vs target 0.20 (+0.17)
```

### Adversarial: conflicting (energy 0.9 + sad mood)

**Edge case:** `sad` mood doesn't exist in the catalog, so the mood bonus never fires. Energy 0.9 and acoustic 0.8 pull in opposite directions, so the winner is a low-energy folk song that only wins on the genre bonus (0.48 vs 0.46). Scores are all low and bunched together.

```text
Profile: Adversarial: conflicting (energy 0.9 + sad mood)
         genre=folk, mood=sad, energy=0.90, likes acoustic
============================================================

#1  Autumn Letters by Willow and Wren
    Score: 0.48 / 1.00   [folk, melancholy]
    Why:
      - energy 0.30 vs target 0.90 (+0.16)
      - acousticness 0.93 vs target 0.80 (+0.17)
      - genre matches: folk (+0.15)

#2  Storm Runner by Voltline
    Score: 0.46 / 1.00   [rock, intense]
    Why:
      - energy 0.91 vs target 0.90 (+0.40)
      - acousticness 0.10 vs target 0.80 (+0.06)

#3  Rooftop Lights by Indigo Parade
    Score: 0.45 / 1.00   [indie pop, happy]
    Why:
      - energy 0.76 vs target 0.90 (+0.34)
      - acousticness 0.35 vs target 0.80 (+0.11)

#4  Dust Road Home by Tall Pines
    Score: 0.45 / 1.00   [country, nostalgic]
    Why:
      - energy 0.55 vs target 0.90 (+0.26)
      - acousticness 0.74 vs target 0.80 (+0.19)

#5  Sunrise City by Neon Echo
    Score: 0.44 / 1.00   [pop, happy]
    Why:
      - energy 0.82 vs target 0.90 (+0.37)
      - acousticness 0.18 vs target 0.80 (+0.08)
```

### Adversarial: genre/mood not in catalog

**Edge case:** neither genre nor mood exists in the catalog, so results come from energy and acousticness alone; max score is ~0.56 with no signal that the profile was unmatched.

```text
Profile: Adversarial: genre/mood not in catalog
         genre=k-pop, mood=dreamy, energy=0.50, prefers non-acoustic
============================================================

#1  Velvet Hours by Silk Avenue
    Score: 0.56 / 1.00   [r&b, romantic]
    Why:
      - energy 0.52 vs target 0.50 (+0.39)
      - acousticness 0.35 vs target 0.20 (+0.17)

#2  Island Breeze by Sol Tide
    Score: 0.52 / 1.00   [reggae, uplifting]
    Why:
      - energy 0.58 vs target 0.50 (+0.37)
      - acousticness 0.45 vs target 0.20 (+0.15)

#3  Night Drive Loop by Neon Echo
    Score: 0.50 / 1.00   [synthwave, moody]
    Why:
      - energy 0.75 vs target 0.50 (+0.30)
      - acousticness 0.22 vs target 0.20 (+0.20)

#4  Concrete Crown by Verse Theory
    Score: 0.47 / 1.00   [hip hop, confident]
    Why:
      - energy 0.78 vs target 0.50 (+0.29)
      - acousticness 0.12 vs target 0.20 (+0.18)

#5  Dust Road Home by Tall Pines
    Score: 0.47 / 1.00   [country, nostalgic]
    Why:
      - energy 0.55 vs target 0.50 (+0.38)
      - acousticness 0.74 vs target 0.20 (+0.09)
```

### Adversarial: acoustic fan wants max energy

**Edge case:** the label bonuses (0.40) beat a huge energy mismatch, so a 0.18-energy classical song wins over everything near energy 1.0. The acoustic preference is also ignored by the runners-up (metal, EDM).

```text
Profile: Adversarial: acoustic fan wants max energy
         genre=classical, mood=peaceful, energy=1.00, likes acoustic
============================================================

#1  Quiet Hours by Elena Marsh
    Score: 0.64 / 1.00   [classical, peaceful]
    Why:
      - energy 0.18 vs target 1.00 (+0.07)
      - acousticness 0.96 vs target 0.80 (+0.17)
      - mood matches: peaceful (+0.25)
      - genre matches: classical (+0.15)

#2  Iron Reign by Black Anvil
    Score: 0.44 / 1.00   [metal, angry]
    Why:
      - energy 0.97 vs target 1.00 (+0.39)
      - acousticness 0.04 vs target 0.80 (+0.05)

#3  Neon Overdrive by Pulse Theory
    Score: 0.43 / 1.00   [edm, euphoric]
    Why:
      - energy 0.96 vs target 1.00 (+0.38)
      - acousticness 0.03 vs target 0.80 (+0.05)

#4  Storm Runner by Voltline
    Score: 0.42 / 1.00   [rock, intense]
    Why:
      - energy 0.91 vs target 1.00 (+0.36)
      - acousticness 0.10 vs target 0.80 (+0.06)

#5  Gym Hero by Max Pulse
    Score: 0.42 / 1.00   [pop, intense]
    Why:
      - energy 0.93 vs target 1.00 (+0.37)
      - acousticness 0.05 vs target 0.80 (+0.05)
```

### Adversarial: out-of-range energy (-1.0)

**Edge case:** energy -1.0 is invalid but not rejected. `closeness` goes negative, producing negative scores (-0.02, -0.04). The score is documented as [0, 1] but isn't clamped or validated.

```text
Profile: Adversarial: out-of-range energy (-1.0)
         genre=ambient, mood=chill, energy=-1.00, prefers non-acoustic
============================================================

#1  Spacewalk Thoughts by Orbit Bloom
    Score: 0.34 / 1.00   [ambient, chill]
    Why:
      - energy 0.28 vs target -1.00 (+-0.11)
      - acousticness 0.92 vs target 0.20 (+0.06)
      - mood matches: chill (+0.25)
      - genre matches: ambient (+0.15)

#2  Midnight Coding by LoRoom
    Score: 0.18 / 1.00   [lofi, chill]
    Why:
      - energy 0.42 vs target -1.00 (+-0.17)
      - acousticness 0.71 vs target 0.20 (+0.10)
      - mood matches: chill (+0.25)

#3  Library Rain by Paper Lanterns
    Score: 0.18 / 1.00   [lofi, chill]
    Why:
      - energy 0.35 vs target -1.00 (+-0.14)
      - acousticness 0.86 vs target 0.20 (+0.07)
      - mood matches: chill (+0.25)

#4  Quiet Hours by Elena Marsh
    Score: -0.02 / 1.00   [classical, peaceful]
    Why:
      - energy 0.18 vs target -1.00 (+-0.07)
      - acousticness 0.96 vs target 0.20 (+0.05)

#5  Velvet Hours by Silk Avenue
    Score: -0.04 / 1.00   [r&b, romantic]
    Why:
      - energy 0.52 vs target -1.00 (+-0.21)
      - acousticness 0.35 vs target 0.20 (+0.17)
```

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

- Tiny catalog. There are only 18 songs, and most genres and moods have just one, so there's often nothing to choose between.
- Exact-match labels. "Sad" gets no credit for "melancholy," and "k-pop" matches nothing, so those listeners get weak results.
- It never says when it's unsure. Conflicting or unmatched tastes still get five confident-looking songs.
- Energy rules. It's the heaviest weight, so loud listeners mostly get the same loud songs, and it can drown out their other preferences.
- Quirks and bad inputs. The "dislikes acoustic" target is 0.2, not 0, which slightly penalizes very non-acoustic songs. An energy of -1.0 isn't rejected and gives negative scores.
- Ignores a lot. No lyrics, language, tempo, or listening history, and it doesn't learn from skips or likes.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

- I learned that a recommender turns data into predictions by doing pretty simple math: it measures how close each song is to your settings, adds bonus points for matching labels, and sorts the list. For listeners who fit the catalog, that felt a lot like real recommendations. But the "smartness" came from a few weights I picked, and changing them (like doubling energy) reshuffled results for some people more than others.
- Bias can sneak in through those choices. With only 18 songs and exact-match genre and mood labels, listeners whose taste isn't in the catalog, like "sad" or k-pop fans, get weak matches and no warning. Whoever picks the data and the weights decides whose taste gets served well, and in a bigger system that can quietly leave people out.