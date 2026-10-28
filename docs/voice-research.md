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
