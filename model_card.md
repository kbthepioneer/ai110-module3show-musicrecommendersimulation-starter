# 🎧 Model Card: VibeMatch 1.0

## 1. Model Name
**VibeMatch 1.0**

---

## 2. Intended Use
VibeMatch 1.0 is designed to simulate how a basic music recommendation system works. It is built for classroom exploration and learning purposes — not for production use. Given a user's favorite genre, mood, energy level, and acoustic preference, it recommends the top 5 most relevant songs from a 20-song catalog. It assumes the user has a single fixed taste profile and does not adapt over time.

---

## 3. How the Model Works
The system compares each song in the catalog against the user's taste profile and assigns a score. A genre match earns the most points (2.0) because genre is usually the strongest indicator of whether someone will enjoy a song. A mood match adds 1.0 point. Energy similarity adds up to 1.5 points — the closer the song's energy is to what the user wants, the more points it earns. Finally, if the user likes acoustic music and the song is highly acoustic, it gets a small bonus of 0.5 points. All songs are then ranked from highest to lowest score and the top results are returned with plain-language explanations.

---

## 4. Data
The catalog contains 20 songs personally selected to reflect a wide range of genres and moods. Genres represented include hip-hop, soul, banda, norteno, country, edm, r&b, jazz, and gospel hip-hop. Moods include happy, intense, moody, relaxed, chill, and focused. Each song has numerical attributes for energy, tempo, valence, danceability, and acousticness on a 0.0 to 1.0 scale. The dataset does not include lyrics, language, or listener behavior data, which are important features in real-world systems.

---

## 5. Strengths
The system works well for users with a strong genre preference — hip-hop fans consistently get Nipsey Hussle, Tupac, Gang Starr, and Schoolboy Q at the top of their list, which matches real musical intuition. The acoustic bonus effectively surfaces Willie Nelson and Sam Cooke for users who prefer organic sounds. Energy similarity acts as a good tiebreaker between songs of the same genre, distinguishing between high-energy and low-energy tracks within the same style.

---

## 6. Limitations and Bias
The biggest limitation is that genre matching is all-or-nothing — banda and norteno are treated as completely separate genres even though they share musical DNA. This means a banda fan might miss great norteno tracks. The catalog also skews toward hip-hop (5 songs out of 20), which means hip-hop users have more options and consistently get stronger recommendations than users of underrepresented genres like jazz or folk. The system has no diversity penalty, so the same artist (like Nipsey Hussle) can appear multiple times in the top 5. Finally, the system cannot learn from user behavior — it gives the same recommendations every time regardless of what the user has already heard.

---

## 7. Evaluation
Six distinct user profiles were tested: Hip-Hop Head, Chill Vibes, Fiesta Mode, Country Soul, EDM Party, and R&B Nights. Each profile produced distinct and mostly intuitive results. The most surprising finding was that Willie Nelson's "On The Road Again" achieved a perfect score of 5.00 for the Country Soul profile — the only song in the catalog to do so. The EDM Party profile unexpectedly surfaced hip-hop songs in positions 3-5 due to high energy similarity, which showed that energy alone can bridge genre gaps in unexpected ways.

---

## 8. Future Work
- Add a diversity penalty so the same artist cannot appear more than once in the top 5
- Group similar genres together (banda + norteno, hip-hop + rap) so users don't miss closely related music
- Add tempo matching as an additional scoring factor
- Allow users to input multiple favorite genres and moods instead of just one
- Incorporate a "recently played" filter so the system stops recommending songs the user has already heard

---

## 9. Personal Reflection
Building VibeMatch 1.0 showed me that recommendation systems are essentially just math applied to taste. What surprised me most was how much a simple weighted scoring system can feel like real intelligence — when the Hip-Hop Head profile surfaced Nipsey Hussle, Tupac, and Gang Starr in the top 4, it felt genuinely accurate, not random. At the same time, seeing Willie Nelson score 5.00 while Kanye West barely appeared in any top 5 made me realize how much the dataset composition matters. Real platforms like Spotify have millions of songs, so the filter bubble problem is less obvious — but with only 20 songs, the bias is impossible to ignore. This project changed how I think about every "For You" playlist I see — there is always a scoring function behind it, and that function always has blind spots.