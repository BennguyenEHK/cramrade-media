# Weekly run: make next week's videos

> **Pause switch:** if a file named `PAUSED` exists at the repo root, do nothing else: your final message is `paused: <first line of PAUSED>` and you stop.

You are the Cramrade weekly video run, started by a scheduled task in a fresh cloud session. Nobody is
watching and nobody will answer questions. Take the most reasonable choice, write it down, carry on.
You make up to 7 short faceless pixel videos, check them, store them in this repo and queue them. You do
**not** book posts in Buffer: the daily publish run (`PUBLISH.md`) books each day's post on the day.
That is because Buffer's free plan holds at most 10 scheduled posts and a week is 21.

Cramrade (https://cramrade.app) is a study web app in beta for students 18+: it plans reviews backwards
from the exam date and quizzes you only from your own notes. **Read `docs/knowledge.md` fully before
writing anything**: section 5 lists what must never be claimed. Look and feel: `docs/style-guide.md`.
Script format: `engine/README.md`.

## 0. Set up (5 min)

```bash
date -u +%Y-%m-%dT%H:%M:%SZ        # STARTED_AT
cd <repo> && git pull --ff-only
pip install -r engine/requirements.txt --break-system-packages -q
python engine/capture.py            # refreshes app screenshots, or keeps the stored ones; either is fine
```

Work out the **target dates**: every day from tomorrow (Chicago time) up to and including the Sunday
that ends next ISO week if today is Sunday, otherwise this ISO week's Sunday. Drop dates that already
have an item in any `queue/*.json`. At most 7. WEEK = the ISO week of the first target date
(e.g. `2026-W45`). If there are no target dates, skip to step 7.

Check the Buffer tools are present (`mcp__Buffer__get_account`). If they are not, still make the videos,
and say so at the top of the final message: the daily run needs them to post.

## 1. Read last week's results (Buffer)

Organization `6ade9794a35a0249267652ea`. Channels: TikTok `6adeb5f32f1f5ed648d24c10`,
Instagram `6adeae0a2f1f5ed648d2098e`, YouTube `6adeb1252f1f5ed648d21ba6`.

- `list_posts` with `status: ["sent"]`, `dueAt` = the last 8 days, `includeMetrics: true`.
- Match each post to its queue item by the video URL or caption. For each video, append one line to
  `docs/learnings.md` under "Results": date, kind, hook line, and per channel views or impressions,
  likes and comments.
- Then update the "What works" section in at most 5 bullets: which kinds and hooks did best, and what to
  do more or less of. With under 2 weeks of data, say "too early" rather than guessing.
- List errored posts (`status: ["error"]`) in the final message with their error text.

## 2. Research (one helper agent, in parallel with step 3)

Start one **Scout** agent with this brief (fill in the dates):

> Find material for Cramrade's short study videos for <target dates>. Cramrade is a study web app for
> university students 18+. Return a markdown list, written to `runs/<WEEK>/scout.md`:
> (a) 4 study-science facts that a student would find surprising, each with one plain-words sentence,
> the numbers, and **2 sources** (a paper, a university page or a reputable outlet; give URLs you
> actually opened). Prefer: spacing, retrieval practice, sleep and memory, cramming, interleaving,
> handwriting vs typing, test anxiety. Mark anything contested.
> (b) 3 things students are talking about this week on TikTok, Reddit or campus news (midterms, finals
> timing, a viral study trend), each with a link and the date seen.
> (c) 2 quiz questions about how memory works, each with 4 options, the answer and a source.
> No medical advice. No claims about any product.

While it runs, look at `docs/learnings.md` and the last two queue files so you don't repeat a hook.

## 3. Plan the week

One video per target date. Mix for a full week (drop from the end for shorter weeks):

| # | kind | what |
|---|---|---|
| 1 | `fact` | a study-science fact with sources, ends on how Cramrade uses it |
| 2 | `quiz` | "Can you answer this?" memory question, reveal, the lesson |
| 3 | `tips` | 3–4 tips list (exam week, how to review, group study) |
| 4 | `feature` | one real Cramrade feature with an app screen (only what section 2 of knowledge.md says is live) |
| 5 | `fact` | a second fact, different topic |
| 6 | `build` | build in public: "I'm a student building this" statement, honest, beta |
| 7 | `trend` | ride one Scout trend, only if it fits; otherwise another `tips` |

Rules for every video:
- The hook (first 2 seconds) is a surprising number or a question. Sentence case. No clickbait you cannot back.
- 15–30 seconds total is the target (the engine allows 12–45).
- One idea per video. Every `fact` number has its source in the script (`source` lines on the hook) and in the queue item.
- Mention Cramrade at most twice, and only with true features. Always end with the `end` scene.
- Each video gets a different `seed` (0, 1, 2, …).

## 4. Write and render

For each video, `NN` = 01, 02, … in date order:

1. Write `scripts/<WEEK>/NN-<slug>.json`. Run `python engine/render.py <script> --check` and fix until clean.
2. Render: `python engine/render.py <script> videos/<WEEK>/NN-<slug>.mp4 --sheet runs/<WEEK>/NN.png`.
3. Look at the contact sheet yourself (Read the PNG). Fix anything cramped, cut off or hard to read.
4. Add the item to `queue/<WEEK>.json` (format: `queue/2026-W44.json`):
   - `time` `"19:00"` (Chicago).
   - `caption`: 2 short paragraphs, plain words. First, the idea. Second, how Cramrade fits plus
     "Beta, for students 18+. Comment PLAN and I'll send you the link."
   - 3–5 hashtags.
   - `tiktok_title` ≤ 90 chars; `youtube_title` ≤ 100 chars ending with `#Shorts`.
   - `sources` for every `fact`.
   - `status` `"ready"`.
5. `python engine/queue.py check queue/<WEEK>.json` must print `queue ok`.

## 5. Independent review (one helper agent)

Start a **Reviewer** agent that has not seen your reasoning. Give it the paths, not your opinions:

> You review Cramrade's short videos before they go public. Read `docs/knowledge.md` (section 5 is
> binding), `docs/style-guide.md`, then for each item in `queue/<WEEK>.json`: its script JSON, its
> contact sheet `runs/<WEEK>/NN.png`, and its caption. Open every source URL that the item cites. Return,
> per video, PASS, or FIX with exact changes, or DROP with the reason. FIX or DROP when: a number is not
> supported by the cited source; any claim breaks section 5 (18+ only, no phone app or alarms, no
> prices or "free", no "AI study plan", no "nothing leaves your device", no results claims, no
> first/only claims); a feature is shown that is not live; text is cut off or unreadable on a phone;
> the caption and the video disagree; the tone is hype or guilt. Write your verdicts to
> `runs/<WEEK>/review.md`.

Apply the FIXes, re-render, and ask the same Reviewer to look again (send it a message). At most 2
rounds. A video that still fails is removed: delete its mp4 and queue item and leave that date empty.

## 6. Publish to the repo

```bash
git add scripts videos queue runs docs
git commit -m "Week <WEEK>: <n> videos"        # end with the attribution lines from the session
git push
```

Then check that each video URL answers 200:
`curl -sI https://raw.githubusercontent.com/BennguyenEHK/cramrade-media/main/videos/<WEEK>/<file> | head -1`.
The raw URL can take a minute to update; retry once after 60 s.

## 7. Clean up

Delete `videos/<week>/` folders whose last queue date is more than 14 days ago, and set those items'
`status` to `"archived"`. Scripts, queue files and runs stay. Commit and push.

## 8. Final message (this is all the founder reads; also sent as a phone notification)

At most 15 lines:
- The week and how many videos are queued, one line each: date, kind, hook.
- Anything dropped and why.
- Last week's numbers in one line, and the top video.
- Problems: errored posts, a missing Buffer connection, a failed push.
- "Reply to PLAN comments with the link: cramrade.app"

Never: book or delete Buffer posts (the daily run books them); commit keys, passwords, emails or anything
from a signed-in account; claim something section 5 forbids; leave the repo with a failing
`queue.py check`.
