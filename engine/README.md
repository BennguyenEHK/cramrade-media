# Engine: script JSON → 1080×1920 pixel video

```
pip install -r engine/requirements.txt --break-system-packages   # pillow, numpy (+ ffmpeg fallback)
python engine/render.py scripts/2026-W44/01-forgetting-curve.json videos/2026-W44/01-forgetting-curve.mp4 --sheet runs/2026-W44/01.png
python engine/render.py SCRIPT.json --check        # validate only, prints every problem
python engine/capture.py                           # refresh app screenshots (falls back to the stored ones)
python engine/queue.py check queue/2026-W44.json   # validate a week's post queue
python engine/queue.py today [YYYY-MM-DD]          # print the posts due that day (Chicago time)
```

Everything is drawn in code (Pillow + numpy), so there are no stock assets, no licences to track and no
outside services. Font: Monocraft (OFL, `assets/fonts`). Music: square-wave chiptune made per video from
`seed`, with blips on text and a chime on reveals. Look and colour rules: `docs/style-guide.md`.

## Script format

```json
{"id": "2026-W45-03", "seed": 2, "scenes": [ {...}, {...}, {"type": "end"} ]}
```

- `seed` changes the music (tempo and chords). Use a different seed each day.
- Total length must be **12–45 s**. The last scene must be `end`.
- Every scene can take `"dur": seconds` to override its default length.
- Text is given as a **list of lines**. You do the line breaks. `--check` rejects lines that are too long.

| kind of text | max characters per line |
|---|---|
| headline (`hook`, `statement` lines) | 14 |
| title (scene titles, quiz question) | 18 |
| body (captions, sources, takeaways, list items) | 28 |

Notch (the mascot) poses: `hello`, `point`, `think`, `cheer`. Leave `notch` out to hide it.

| type | fields | default length |
|---|---|---|
| `hook` | `lines` (1–5), `highlight_line` (index, amber box), `source` (body lines, small grey), `notch` | 4.2 s |
| `statement` | `lines` (1–5), `highlight_line`, `caption` (body lines), `notch` | 4.0 s |
| `bars` | `title`, `bars` [[label, value], …] (2–6), `unit`, `max`, `takeaway` (2 body lines, the second is highlighted) | 5.0 s |
| `sawtooth` | `title`, `caption`, `notch`, `axis_label` (memory curve that each review resets) | 4.4 s |
| `timeline` | `title`, `caption`, `end_label` (review dots bunching towards exam day) | 4.4 s |
| `app` | `title`, `screen` (a key in `assets/screens/screens.json`), `highlight` (bool), `caption` | 4.0 s |
| `list` | `title`, `items` (each a string or a list of lines, up to 4), `notch` | 5.0 s |
| `quiz` | `question` (title lines), `options` (2–4, each ≤ 24 chars), `answer` (index), `reveal_at` (s), `caption` | 5.0 s |
| `end` | `cta` (default `PLAN`), `note` (default `Beta, for students 18+`) | 4.0 s |

### App screens available (`assets/screens/screens.json`)

| key | what it shows | highlight box |
|---|---|---|
| `plan-card` | a planned question card | the "From your notes, line 14" source line |
| `quote-check` | a question being dropped | "Quote not in your notes. Dropped." |
| `podium` | group quiz podium with sample players | the podium |

They come from the **public** homepage and `/pieces` page, which show sample data only.
`capture.py` refreshes them when the cloud environment can reach cramrade.app; otherwise the stored copies are used.
Never add screenshots from a signed-in account.

## Checks before a video goes out

1. `render.py --check` passes.
2. The contact sheet (one still per scene) reads well at phone size: nothing in the top 220 px or bottom 420 px.
3. Every claim passes `docs/knowledge.md` section 5 ("Never claim").
