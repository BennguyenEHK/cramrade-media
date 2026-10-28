# Video reference research (2026-10-27)

Why: Minh rejected the first 5 videos (text-only pixel slides + square-wave chiptune). We looked at what
faceless study and self-improvement shorts that actually get views do, on YouTube Shorts, TikTok and
Instagram Reels, to decide what our videos should look like. Views and likes were read on the day.

## What we watched

| reference | platform | numbers | format |
|---|---|---|---|
| @goharsguide "A Clever Way to Study for Exams" | YouTube Shorts | 106M and 37M views (two uploads), 4.1M likes | Faceless: hands, paper and a pencil on a desk. First-person story voiceover ("Your teacher announces… I tried this weird technique… highest 97, lowest 5"). Huge single-word captions ("EXAM", "ON"). A new shot every 1–2 s. ~29 s. |
| @recode_mind_ (821K followers, 250 posts) | Instagram Reels | 78K–2.3M views per reel; top comments 1K–6K likes | One glowing yellow character in a black, white-line-art room. Voiceover with one word on screen at a time, synced to the voice. The character changes pose or action every 2–3 s; the set stays the same. Ends on a challenge ("do this for 7 days"), so people comment "remind me". |
| @animeexplain_ "You're Studying Wrong!" | TikTok | 49.5K likes | Character narrator + voiceover + big word-by-word captions on a paper-texture background; illustration changes every 2–3 s. |
| "idiots with bad study habits unite" | YouTube Shorts | 11M views | Relatable meme: drawn scene + one caption ("the smart kid teaching everyone 5 min before the exam") + trending sound. |
| "I Don't Like To Study", "POV: last 5 minutes in the exam", "The night before an exam" | YouTube Shorts | 10–17M views each | Relatable animated memes about exam stress. |
| "STOP burnout with these 4 tips (read comments)" | YouTube Shorts | 5.9M views | Contrast format: "students who do X" vs "students who follow me and use:". Pushes people into the comments. |
| @studywithsoybean spaced repetition | TikTok | 196K likes | Aesthetic hands-and-planner footage + sped-up trending song + text. |
| Pixel art searches ("pixel art study", "pixel animation facts") | TikTok, YouTube | | Almost all pixel shorts are about *making* pixel art. Pixel-style study explainers basically don't exist: an open lane, but unproven. |
| Stick-figure study explainers | YouTube | mostly under 2K views | Lots of supply, little demand. Skip. |

Side note: StudyFetch (a competitor) runs several persona TikTok accounts (@studyfetchpatty, @studyfetchbrunette).

## What the winners share (and our first videos lacked)

1. **A voice.** Every high performer has a voiceover or a trending sound. Ours had neither: text plus beeps. This is the biggest gap.
2. **Captions one word (or 2–3) at a time, synced to the voice,** big, bold, white with a dark outline, centred. Not paragraphs of text that fade in.
3. **Something moves or changes every 1–3 seconds:** a new pose, prop, zoom or cut. Ours held one slide for 4–5 s.
4. **A character people follow,** shown acting out the idea, in one consistent set. Viewers recognise the series.
5. **A story or a stake in the first 2 s:** "Your teacher announces…", "Do this for 7 days", "students who…". Not a statistic on a slide.
6. **A comment trigger at the end:** a challenge, "remind me", "read comments". Ours had "Comment PLAN", which fits; it should come from the character.
7. **20–35 s,** looping cleanly back to the start.

## What this means for Cramrade

Closest proven match to our brand: the **@recode_mind_ format**: dark scene, everything in white line-art, one coloured
character, word-synced captions, voiceover. It already follows our "nothing else is coloured" rule. Our own
version is **Notch in a dark line-art study room**, drawn in our pixel style, glowing blue with the amber marker.
We copy the structure, not their character or art.

Proposed engine v2:
- **Voice:** Kokoro (open-source, Apache-2.0, runs offline in the cloud from GitHub-hosted model files; tested:
  ~2 s per sentence). Voices to choose from: af_heart (warm female), am_michael (calm male), am_puck (younger male).
- **Captions:** word-by-word, timed from the voice, centred in the safe zone.
- **Scenes:** a small set of pixel/line-art backgrounds (desk at night, library, exam hall, calendar wall) +
  Notch poses (reading, thinking, panicking, celebrating, pointing, sleeping) + props (book, phone, clock,
  calendar with an amber exam day). Shot change every 2–3 s, with small camera moves (slow push-in, shake on punchlines).
- **Music:** soft lo-fi bed under the voice (quiet), not chiptune lead melodies. Sound effects only on key moments.
- **Formats to rotate:** (a) Notch explains one study technique as a mini story, (b) relatable exam-stress
  meme with one caption, (c) "students who… vs students who…", (d) 7-day challenge with a comment trigger,
  (e) app feature shown as Notch using Cramrade.
