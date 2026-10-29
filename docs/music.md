# Cramrade theme music: "Base Camp" (2026-10-28)

Composed in code by `engine/v2/music.py`. It is fully original, so there are no licences or copyright claims.
Files live in `engine/assets/music/`.

| file | what | length | level |
|---|---|---|---|
| `cramrade-theme-base-camp.mp3` | full theme, loops seamlessly | 87 s | -18.6 LUFS |
| `cramrade-bed-base-camp.mp3` | lighter version for under Notch's voice (melody every 4th phrase, no bell); used by engine v2 | 58 s loop | -20.6 LUFS |
| `cramrade-sting.mp3` | logo sting: the climb motif plus the summit bell | 5 s | -17 LUFS |

## Inspiration (cramrade.app)

The site shows snowy pixel mountains, mist, pines and waterfalls in cold blues. A winding amber path climbs from a cozy village to a flag on the summit (exam day).

| site element | in the music |
|---|---|
| the path up the mountain | a rising felt-piano motif: D, E, F#, A |
| the summit flag | one soft bell on D5, now and then |
| the village | warm, low felt-piano chords |
| the cold air and mist | a quiet pad that breathes in and out, plus a faint wind texture and long reverb |

## Why it won't distract students

- 66 bpm. No drums, no vocals, no lyrics.
- One chord every two bars: D major 9, B minor 9, G major 7, A sus.
- The melody plays at most every other phrase, with long rests. The pad and bass fade out halfway through each chord, so about a quarter of the time sits in quiet valleys.
- Soft attacks, rolled off above 7 kHz, narrow dynamics (loudness range of about 4.5 LU). The key and pulse never change.
- In videos the bed sits about 8–9 dB under the voice and dips further while Notch speaks.

To make variations, change `seed`, `melody_every`, `PROG`, `CLIMB` or `BPM` in music.py and run `python engine/v2/music.py OUTDIR`.
