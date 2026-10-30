# cramrade-media

Short faceless videos with Notch for Cramrade (https://cramrade.app), made by a scheduled Claude run, reviewed by Minh by email, then posted by a second scheduled run.

| path | what |
|---|---|
| `RUNBOOK.md` | the weekly run (Sunday): research, write, voice, music, render, review, queue up to 7 videos, email Minh for approval |
| `PUBLISH.md` | the daily run: books that day's video at 19:00 Chicago on TikTok, Instagram and YouTube via Buffer, only if Minh approved it |
| `engine/v2/` | engine v2: `notch_v2.py` (render), `voice.py` (Notch voice + word timings), `score.py` (music); `engine/scan_text.py` (no-18+ check), `engine/queue.py` |
| `docs/content-plan.md` | the approved "Notch explains" format the weekly run follows |
| `samples/<week>/` | voice, word timings and shots JSON per video |
| `scripts/<week>/` | one JSON script per video |
| `videos/<week>/` | the rendered mp4s; Buffer fetches them from their raw GitHub URL |
| `queue/<week>.json` | captions, titles, hashtags, sources and the posting date for each video |
| `runs/<week>/` | contact sheets, research notes and the review for that week |
| `docs/` | product facts and never-claim rules, style guide, learnings |

Delete a post before it goes out: open Buffer and delete it there, or set its queue item's `status` to `"hold"`.

Everything here is public. Never commit keys, passwords or user data.
