# cramrade-media

Short faceless pixel videos for Cramrade (https://cramrade.app), made and posted by scheduled Claude runs.

| path | what |
|---|---|
| `RUNBOOK.md` | the weekly run (Sunday): research, write, render, review, queue up to 7 videos |
| `PUBLISH.md` | the daily run: books that day's video at 19:00 Chicago on TikTok, Instagram and YouTube via Buffer |
| `engine/` | the renderer (script JSON → 1080×1920 mp4), screenshot capture, queue helper. See `engine/README.md` |
| `scripts/<week>/` | one JSON script per video |
| `videos/<week>/` | the rendered mp4s; Buffer fetches them from their raw GitHub URL |
| `queue/<week>.json` | captions, titles, hashtags, sources and the posting date for each video |
| `runs/<week>/` | contact sheets, research notes and the review for that week |
| `docs/` | product facts and never-claim rules, style guide, learnings |

Delete a post before it goes out: open Buffer and delete it there, or set its queue item's `status` to `"hold"`.

Everything here is public. Never commit keys, passwords or user data.
