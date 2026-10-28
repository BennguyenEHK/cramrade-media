# Notch's voice: research and choice (2026-10-27)

**Brief from Minh:** sounds 17–19, energetic, light baritone, like a favourite English teacher. Reliable. Makes students want to keep listening.

## What the research says makes a voice engaging

- **Charisma rises with a higher average pitch and a wider melody range.**
  - For male speakers, perceived charisma correlated with mean pitch (r = 0.61) and with the 80-percentile pitch range (r = 0.62).
  - Voices that often reach the top of their own range (negative skew) rated higher.
  - Source: Niebuhr & Skarnitzl 2019, https://fonetika.ff.cuni.cz/wp-content/uploads/sites/104/2019/08/NieSka19-f0Charisma.pdf
- **Pitch mean, pitch range and loudness variation all go with charisma, across languages.**
  - Source: Biadsy et al. 2008, https://www.cs.columbia.edu/nlp/papers/2008/fadi_al_08b.pdf
- **Faster, enthusiastic instructors hold students longer.**
  - In 6.9M MOOC video sessions (mean pace 156 wpm), engagement rose with speaking rate, up to 2x.
  - The authors read speed as a stand-in for enthusiasm, and recommend cutting dead pauses.
  - Source: Guo, Kim & Rubin 2014, https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf
- **Pitch range for this age:** young adult men typically speak around 85–155 Hz; a light baritone sits in the upper-middle of that.
  - Source: https://en.wikipedia.org/wiki/Voice_frequency

## Targets we measured against

| | target | why |
|---|---|---|
| average pitch | 115–132 Hz | young light baritone, upper-middle male range |
| melody range (80th–10th percentile) | at least 10 semitones | lively, teacherly, not monotone |
| skew | 0 or negative | often lifts to the top of the range |
| pace | 165–190 wpm, short pauses between sentences | energetic but easy to follow |

## How it's made

- Kokoro TTS (Apache-2.0, offline; model files from GitHub releases, so it works in the cloud runs).
- Voice styles blended from built-in male voices.
- Each sentence is generated separately at base speed 0.92, with small changes per sentence: questions a little slower, punchlines a little faster. Short pauses of 0.2–0.35 s go between sentences.
- Finishing chain (ffmpeg):
  - high-pass at 70 Hz;
  - +2 dB warmth at 140 Hz;
  - +2.5 dB presence at 3.5 kHz;
  - −2 dB at 7 kHz;
  - light compression;
  - normalised to −14 LUFS.

| finalist | blend | avg pitch | melody range | pace |
|---|---|---|---|---|
| A energetic tutor | 0.5 am_puck + 0.5 am_fenrir | 130 Hz | 10.4 st | 185 wpm |
| B warm light baritone | 0.5 am_liam + 0.5 am_adam | 125 Hz | 10.4 st | 179 wpm |
| C young and bright | am_liam | 133 Hz | 13.0 st | 174 wpm |
| D confident coach | 0.5 am_fenrir + 0.5 am_michael | 130 Hz | 10.2 st | 176 wpm |

Chosen: _(pending Minh's pick)_

Upgrade path: more expressive engines (Chatterbox, OpenAI "cedar", ElevenLabs) need huggingface.co or a paid API allowed in the cloud network settings.
Disney or celebrity voices (Baymax etc.) are off limits.

## Round 2: wider search around C (2026-10-27)

Minh picked C (am_liam). Searched 966 voices for ones that sound like C but fit the brief better.
- Similarity is the cosine between Resemblyzer speaker embeddings and C.
- "Brief score" combines: melody range, skew, pace distance from 180 wpm, pitch window 120–135 Hz, loudness variation, clarity (HNR).

- **Kokoro, 54 variants of C:**
  - liam blended 15% or 30% with each of the 12 other male voices;
  - liam "exaggerated" away from the average male voice;
  - two speeds each.
  - All stay 0.96–0.995 similar to C.
- **Piper LibriTTS-high, all 904 speakers screened** (model from GitHub release v0.0.2).
  - The best match to C was only 0.76 similar; they are different people (audiobook readers).
  - Speaker 189 was the only one close to C's brief score, and it is the clearest voice tested.

| finalist | recipe | similarity to C | pitch | melody | pace | clarity (HNR) |
|---|---|---|---|---|---|---|
| C reference | am_liam, speed 0.92 | 1.000 | 134 | 12.9 | 174 | 9.6 |
| K1 C plus character | liam + 0.2 × (liam − mean male style), 0.96 | 0.995 | 135 | 13.7 | 178 | 9.3 |
| K2 C plus energy | 0.85 liam + 0.15 fenrir, 0.96 | 0.989 | 135 | 13.1 | 179 | 9.8 |
| K3 C steadier | 0.70 liam + 0.30 fenrir, 0.92 | 0.965 | 136 | 12.9 | 178 | 10.0 |
| K4 C clearer | 0.85 liam + 0.15 eric, 0.96 | 0.990 | 137 | 13.0 | 177 | 10.1 |
| P1 speaker 189 | Piper libritts-high sid 189, length 0.9, noise 0.75 | 0.737 | 133 | 11.9 | 192 | 12.7 |
