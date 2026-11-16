# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of the recommender as a judge that gives every song a grade from 0 to 1 for one particular listener, then hands back the five highest grades.

**What it knows about a song:** its genre, its mood, how energetic it is, and how acoustic it sounds (warm and organic versus electronic). The catalog also stores tempo, valence and danceability, but the grade doesn't use them yet. Tempo mostly repeats what energy already says, so counting it would just double the same idea.

**What it knows about the listener:** a favorite genre, a favorite mood, how energetic they want the music to be, and whether they like acoustic music.

**How the grade is built:** the grade is made of four pieces.
- **Energy (up to 0.40 points).** I don't reward "more energy" or "less energy". I reward being *close* to what the listener wants. If they want medium-calm music, a song that is a little calmer or a little livelier scores nearly as well as a perfect match, and a very intense song scores much lower.
- **Acousticness (up to 0.20).** The same "closeness" idea. Listeners who like acoustic music get songs with a warm, natural sound; everyone else is steered toward more electronic ones.
- **Mood (0.25).** A flat bonus if the song's mood is exactly the listener's favorite.
- **Genre (0.15).** A smaller flat bonus for an exact genre match.

Mood counts for more than genre on purpose. Mood is the feel you actually hear, while genre is a broad label. "Pop" covers both a joyful song and a workout anthem, and a happy listener probably wants the first one.

**From grades to recommendations:** every song in the catalog gets a grade, the songs are sorted from highest to lowest (ties go alphabetically so results are the same every time), and the top five are shown. Each one comes with a short list of reasons, such as "energy 0.82 vs target 0.80" or "mood matches: happy", so you can see exactly why it was picked.

**What changed from the starter:** the starter had no scoring at all, only empty placeholders. I wrote the data loading, the grading rule, the ranking step, and a command-line output that prints each song's score and reasons.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
