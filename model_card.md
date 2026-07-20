# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Playlist Generator

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

The recommender is designed to recommend songs that would best fit your music interest like genre, mood, danceability, energy, etc. It would make some assumptions based on your profile, a user might like these other set of songs as well. This application is intended for class exploration as of now since our song dataset is very limited to a few as of now. 

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

We can think of the app as a matchmaker for your ears. You describe your taste (your favorite genre and mood, and the kind of vibe you want [how energetic, cheerful, danceable, fast, and vocal-heavy) and the app grades every song out of 100 based on how well it fits. Songs that match your genre or mood get bonus points, and the closer a song's vibe is to what you asked for, the more points it earns. It then ranks them and hands you the top matches, along with a quick note on why each one made the cut. The starter version only checked four basics; I taught it to notice five more qualities (like danceability and tempo) so it "hears" each song more fully and made every choice easy to explain.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog is small and handpicked (for now it's just 19 songs) meant for classroom exploration rather than real world use. It covers a wide spread of styles, with about 16 genres (pop, lofi, rock, jazz, hip hop, classical, metal, reggae, r&b, and more) and 15 moods (happy, chill, intense, romantic, nostalgic, angry, and others), and every song comes tagged with details like energy, tempo, cheerfulness, danceability, and how acoustic or instrumental it is. I kept the original starter songs and added a handful more to widen the variety of genres and moods. That said, plenty of musical taste is still missing: most genres have only one song, so there isn't much depth in any single style; global and regional sounds aren't represented; and the data says nothing about lyrics, language, an artist's popularity, or a song's era, which are all things that shape what people actually love.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for listeners with a clear, consistent taste like someone who knows what they want. When a user's preferences all point the same direction, the scoring lines up neatly with what a person would expect: the "Happy Pop" listener's top pick was a bright, danceable pop song scoring nearly a perfect 100, and the "Chill Lofi" listener surfaced calm, low-energy, instrumental tracks. What it captures well is the overall vibe of a song, since it looks at several qualities at once (energy, cheerfulness, danceability, tempo, and more), a song only rises to the top when it matches on many fronts, not just one lucky detail. It also earns trust by explaining itself like every recommendation comes with the reasons it scored well, so when the picks match your gut feeling, you can see exactly why.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The system also struggles in a few telling ways. Genre and mood are matched word for word, so it is close but not exact tastes get shortchanged. The catalog is lopsided too, with several songs for pop and lofi but only one for most other genres, so fans of common styles are simply luckier. The scoring can also overfit to a single strong preference, and when someone's tastes conflict (like wanting "sad" but very high energy), it happily picks a song that matches neither. Finally, the app's default settings quietly assume a vocal, upbeat, mid-tempo pop listener, which means instrumental styles like classical, ambient, and lofi tend to get pushed down for anyone who doesn't spell out their preferences, unintentionally favoring mainstream-pop taste over everything else.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I have tested if the recommender behaved as expected.I built a few different listener profiles and compared what came back: a "Happy Pop" fan, a "Chill Lofi" fan, and then two deliberately tricky ones I made to try to break it. Since every recommendation prints out the reasons behind its score, I mainly looked at whether the top picks made sense and whether the explanations matched why I thought a song should rank high. The normal profiles behaved about how I expected, but the tricky ones were where it got interesting. The one that surprised me most was a "sad but high-energy" user with conflicting tastes because instead of admitting nothing really fit, the app confidently recommended upbeat songs that weren't sad at all. Another test used an impossible energy value (way outside the normal range), and I noticed it silently zeroed out that whole part of the score instead of flagging it. I also ran test where I doubled the importance of energy and halved genre, just to see how much the rankings shifted, which helped me understand how sensitive the results are to the weights I chose.



---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

If I kept working on this, the first thing I'd fix is the diversity of the top results. Right now the top picks can be similar, so I'd like to make sure the list mixes in a few different genres or moods instead of five near-identical songs. I would want there to be something a bit unexpected to discover. The second thing I would add is smarter matching for genres and moods, so that closely related tastes (like "pop" and "indie pop," or "happy" and "uplifting") get partial credit instead of being treated as total mismatches. That change would help the app handle more realistic, complex tastes and stop quietly ignoring listeners whose exact words don't line up with the catalog.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Designing and workng on this music recommender showed me that small human choices/preferences could be used to turn into numbers/calculations and those choices quietly shape everything it suggests. What surprised me most was how confidently it gave answers even when nothing actually fit, which made me realize a recommendation isn't the same as a good recommendation. Now when I use apps like Spotify, I wonder what assumptions are hiding behind my "For You" playlist.



