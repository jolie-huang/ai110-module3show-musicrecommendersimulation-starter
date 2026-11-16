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

- This is a small, classroom-sized music recommender. You give it a taste profile (a favorite genre, a favorite mood, a target energy level, and whether you like acoustic sounds) and it hands back your top 5 songs from an 18-song catalog, each with a score and a short "why" explaining the points.
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

- The catalog is a small CSV with 18 songs. Each song has a title, artist, genre, mood, and numbers for energy, tempo, valence, danceability and acousticness. Only four of those affect the score: genre, mood, energy and acousticness. The other three get loaded but never used.
- There are 15 genres, and most have just one song: pop, indie pop, lofi, rock, metal, edm, hip hop, r&b, jazz, classical, folk, country, reggae, ambient and synthwave. Lofi is the biggest with 3.
- There are 14 moods, also mostly one song each. Chill is the most common (3), then happy and intense (2 each). The rest, like angry, romantic, nostalgic and melancholy, show up once.
- Energy is pretty evenly split: about 8 loud songs, 7 quiet ones, and only 3 in the middle.
- I didn't change the catalog. All my experiments were on the profiles and the weights.
- What's missing: There's no "sad" mood (the closest is "melancholy"). K-pop, latin, blues and punk aren't in there either, so profiles asking for those get no label match. With one song per genre, there's nothing to choose between inside a genre. Nothing about lyrics, language, vocals, decade or popularity. Few mid-energy songs, so listeners who want something in the middle have thin choices. It's a small, made-up sample, so it reflects whoever put it together, not what people really listen to.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

- It works best when your genre and mood are actually in the catalog and your preferences don't fight each other. My three normal profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) all got a clear, sensible #1, with scores around 0.97 for the lofi and rock picks and a big drop after that.
- Energy closeness works. Loud-song fans get loud songs and quiet-song fans get quiet ones, so the pop and lofi lists have nothing in common. Matching labels break ties well. If two songs are equally close on energy, the one with your mood and genre wins. That's why Storm Runner beats Gym Hero for the rock fan. The "Why" lines make it easy to check. You can see exactly where each point came from, which is how I spotted the problems.
- Chill Lofi gave me two lofi/chill songs, then ambient, then lofi/focused, then jazz, which is the order I'd pick myself. High-Energy Pop put Sunrise City first and Rooftop Lights (indie pop, happy) ahead of the louder non-pop songs.

---

## 6. Limitations and Bias

**Weakness: exact-match labels in a tiny catalog leave some listeners unserved.** The catalog has only 18 songs across 15 genres, so most genres and moods appear exactly once, and the code awards the mood (0.25) and genre (0.15) bonuses only when the strings match exactly. A user who asks for "sad" gets no mood bonus at all, even though "melancholy" (Autumn Letters) is the same feeling, so their results are decided almost entirely by the energy gap and acousticness. In the conflicting-profile test (folk, sad, energy 0.9), the top five scored between 0.44 and 0.48 and included loud rock and pop songs, with no signal that the request went unmatched. When I doubled the energy weight, that profile's list became all high-energy songs, so listeners whose energy preference conflicts with their genre or mood are effectively ignored. Users whose taste lines up with a well-covered label such as lofi/chill (the only genre-and-mood pair with two songs) get scores around 0.97, which creates a filter bubble that favors a few mainstream-labelled tastes over everyone else.


## 7. Evaluation

### Profiles tested
I ran seven listener profiles against the 18-song catalog. Full top-5 outputs are in the README. Results below use the original weights (energy 0.40, mood 0.25, acoustic 0.20, genre 0.15).

- **A. High-Energy Pop:** pop, happy, energy 0.9, no acoustic
- **B. Chill Lofi:** lofi, chill, energy 0.4, likes acoustic
- **C. Deep Intense Rock:** rock, intense, energy 0.92, no acoustic
- **D. Conflicting:** folk, sad, energy 0.9, likes acoustic (wants quiet-sounding music that is also loud)
- **E. Unknown tastes:** k-pop, dreamy, energy 0.5 (neither label exists in the catalog)
- **F. Acoustic but maximum energy:** classical, peaceful, energy 1.0, likes acoustic
- **G. Invalid energy:** ambient, chill, energy -1.0

A, B and C are normal listeners. D to G are deliberate traps to see whether the scoring breaks.

### Why does "Gym Hero" keep showing up for "Happy Pop" fans?
Gym Hero is a workout track. It is labelled pop but its mood is "intense", not "happy". The recommender doesn't listen to music. It adds up points: how close the song's energy is to what you asked for, how close its acoustic level is, and bonuses for a matching mood and a matching genre. Gym Hero is very loud (energy 0.93), almost exactly what a "high-energy pop" fan asks for (0.9), and it is pop. So it collects nearly full points for energy and acoustic level, plus the genre bonus. It only misses the mood bonus. With just 18 songs, there aren't many pop songs to choose from, so a loud pop song with the wrong mood still beats everything else. That is a fair guess on paper, but a person who wants happy music would probably skip it. The recommender can't tell that "pumping iron" and "feel-good" are different vibes beyond that one mood label.

### What surprised me
- The standard profiles (A, B, C) behaved the way I'd expect: the song matching both genre and mood came first by a wide margin.
- Deep Intense Rock put a happy pop song (Sunrise City) above a metal track (Iron Reign). The reason is that a non-acoustic listener's target is 0.2, not 0, so a song that is *too* non-acoustic loses a few points. A real rock fan would not expect that.
- With the conflicting profile (D), the winner was a quiet folk song that doesn't match the requested energy at all. It won only on the genre bonus, by 0.02. The scores were all so close that the order is almost arbitrary.
- The invalid profile (G) produced negative scores, so the "0 to 1" score isn't actually guaranteed.
- When I doubled the energy weight and halved genre as an experiment, the three normal profiles barely changed. The conflicting and acoustic-but-loud profiles shifted a lot, which shows those listeners are decided by whichever feature has the biggest weight.

### Pair-by-pair comparisons
**A. High-Energy Pop vs B. Chill Lofi:** no songs in common. A wants loud, bright songs (Sunrise City, Rooftop Lights); B wants quiet, acoustic ones (Midnight Coding, Library Rain). That is the right split, since the two profiles are opposites on energy and acoustic level.

**A vs C. Deep Intense Rock:** both want loud, non-acoustic songs, so the same pool shows up (Gym Hero, Storm Runner, Sunrise City, Neon Overdrive), just in a different order. Pop/happy puts Sunrise City first; rock/intense puts Storm Runner first and moves Gym Hero up to #2 because it matches "intense". The labels reorder the list, which is exactly what they should do.

**A vs D. Conflicting:** both ask for energy 0.9, but D also likes acoustic. Loud, synthetic songs like Gym Hero and Neon Overdrive drop out of D's list because they aren't acoustic, and a quiet folk song takes #1. D's list is a muddled compromise, while A's is clean, because A's wishes don't contradict each other.

**A vs E. Unknown tastes:** no overlap. E asks for middling energy (0.5) and has no genre or mood match, so no song gets a bonus. The top song scores 0.56, compared with 0.96 for A's top song. The low scores are the system's only hint that it didn't understand the request.

**A vs F. Acoustic but maximum energy:** both want very high energy, so Gym Hero, Storm Runner and Neon Overdrive appear in both. F's scores are much lower (about 0.43 vs 0.7) because those songs aren't acoustic, which F wants. The classical song comes first for F purely on label matches.

**A vs G. Invalid energy:** no overlap. G's target energy is below zero, so the quietest songs win. The output is sensible in direction (quiet songs for a "least energy" request) but the scores are meaningless.

**B vs C:** no overlap. Quiet, acoustic lofi versus loud rock: they are at opposite ends of the energy scale, so completely different lists is the correct result.

**B vs D:** no overlap. D wants energy 0.9, B wants 0.4. D's only quiet song is the folk track that wins on genre, which has nothing in common with B's lofi.

**B vs E:** no overlap. B has two songs that match everything and scores 0.97. E has no matches and tops out at 0.56. The gap shows how much listeners with unmatched tastes lose.

**B vs F:** no overlap, even though both like acoustic music. B is quiet and F is loud, and energy carries the most weight. F's acoustic preference only helps one song (Quiet Hours), which is also quiet and so doesn't fit the energy request.

**B vs G:** these two share three songs (Spacewalk Thoughts, Midnight Coding, Library Rain), because G also wants the lowest possible energy and a chill mood. G's scores are far lower (0.34 down to negative) because G doesn't like acoustic music and these songs are very acoustic. Same songs, different scores.

**C vs D:** share Storm Runner and Sunrise City, since both ask for high energy. D's acoustic preference pushes it away from C's loud non-acoustic metal, and a quiet folk song wins instead.

**C vs E:** no overlap. C has a perfect label match (Storm Runner, 0.98); E has none. Again the difference is whether the catalog contains the listener's genre and mood.

**C vs F:** both draw from the same loud pool (Storm Runner, Gym Hero, Neon Overdrive, Iron Reign). C's list is close to perfect because the labels match; F's loud songs score about 0.43 because F wants acoustic sound they don't have. Same songs, different fit.

**C vs G:** no overlap. C is loud and G is at the opposite extreme. This is the correct direction.

**D vs E:** share Dust Road Home. Neither profile gets a mood bonus ("sad" and "dreamy" don't exist), so the results are mostly energy and acousticness. D asks for loud and gets loud; E asks for mid-range and gets mid-range songs (r&b, reggae). Different energy gives different lists, which makes sense.

**D vs F:** share Storm Runner. Both like acoustic music at high energy, and in both cases the top song is the quiet one that matches a label (Autumn Letters, Quiet Hours), followed by loud non-acoustic songs. This shows that the contradiction is handled the same way: label bonuses win over the sound the listener asked for.

**D vs G:** no overlap. D wants loud and G wants silent, so the lists have nothing in common.

**E vs F:** no overlap. E's middling energy picks mid-tempo songs; F's maximum energy picks metal and EDM. Reasonable.

**E vs G:** share Velvet Hours, which has middling energy and low acoustic. For E it ranks #1; for G it is last place at -0.04. Same song, but E's target is close to it and G's isn't.

**F vs G:** no overlap. They sit at opposite energy extremes (1.0 and -1.0). Each gets one label-matched winner (Quiet Hours for F, Spacewalk Thoughts for G) and the rest of the list is decided by the numbers alone.

### Overall verdict
The recommender is valid for listeners whose genre and mood exist in the catalog and whose wishes agree with each other (A, B, C). For listeners with unmatched labels (E), contradictory wishes (D, F) or invalid values (G), it still returns five songs and never says that it is unsure.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

- More features: use the stuff I already load but ignore (tempo, valence, danceability), and add a bigger catalog so each genre has more than one song. Also treat similar labels as close (rock near metal, "sad" near "melancholy") instead of exact-match only.
- Better explanations: keep the "Why" lines, but add a plain warning like "no song matched your genre or mood, so these are just energy matches." Right now the system sounds equally confident when it has nothing.
- More variety: the top 5 for loud profiles are mostly the same loud songs. I'd penalize near-duplicates so the list mixes in different genres and moods.
- Complex tastes: let people pick more than one genre or mood, and a range of energy instead of one number. Also catch conflicting or invalid inputs (like energy -1.0) and fix the "dislikes acoustic" target so it isn't set to 0.2.

---

## 9. Personal Reflection

**Biggest learning moment.** I expected the interesting failures to come from weird inputs, but the most useful one came from a normal profile. For Deep Intense Rock, a happy pop song (Sunrise City) ranked above a metal track (Iron Reign). Tracing the points showed why: my "dislikes acoustic" target was 0.2, not 0, so a song that was *too* non-acoustic lost a few points. Nothing was broken in the code. The rule just meant something different from what I intended. That taught me that a recommender's mistakes usually come from small choices about what to measure and how to weigh it, and the only way to find them is to read the score breakdown for a specific song.

**How AI helped, and when I had to double-check it.** The AI tool was fast at the mechanical parts: writing the profiles, running them, and laying out the score breakdowns. It also made the weight experiment easy to try. But I had to check its work in a few places. When I doubled energy and halved genre, the weights summed to 1.325, which would have pushed scores above the 1.00 maximum, so the math had to be normalized and checked with an assertion. In my own model card draft, a claim that lofi/chill had "3 songs" was wrong (it has two; chill has three), and I only caught it by counting the CSV. And the AI's profile suggestions were its own guesses about what would break the system, so I confirmed each one by running it and reading the output instead of trusting the description.

**Why simple math still feels like recommendations.** For people whose taste matches the catalog, the results felt right. Chill Lofi returned two near-perfect lofi tracks, then ambient, then jazz, and that looks like understanding. In reality it is just three numbers and two exact-match labels added together. The "Why" lines made it feel even more convincing, because a recommendation with a reason attached sounds smart. The illusion breaks on listeners who don't fit, since the system still returns five confident-looking songs. That made me realize real apps probably hide a lot of this same uncertainty.

**What I'd try next.**
- Grow the catalog well beyond 18 songs, so genres and moods have more than one example.
- Replace exact-match genre and mood with similarity (rock close to metal, "sad" close to "melancholy").
- Fix the acoustic target so non-acoustic listeners aren't penalized, and validate inputs so a bad energy value is rejected.
- Show a "low confidence" warning when no song matches the listener's labels.
- Add variety to the top 5, so lists aren't filled with near-identical loud songs.

