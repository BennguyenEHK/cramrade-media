# Weekly run: make next week's videos (engine v2, "Notch explains")

> **Pause switch:** if a file named `PAUSED` exists at the repo root, do nothing else: your final message is `paused: <first line of PAUSED>` and you stop.

You are the Cramrade weekly video run, started by a scheduled task in a fresh cloud session. Nobody is
watching and nobody will answer questions. Take the most reasonable choice, write it down, carry on.
You make up to 5 short faceless videos with Notch, check them, store them in this repo, queue them with
status `review`, and **email Minh the videos to review**. You do **not** book posts in Buffer: the daily
publish run (`PUBLISH.md`) books each day's video only after Minh has approved it by email.

Cramrade (https://cramrade.app) is a study web app in beta, invite-only (waitlist): it plans reviews
backwards from the exam date and quizzes you only from your own notes. Before writing anything, read:
1. `docs/knowledge.md` fully (section 5 = never claim; binding),
2. `docs/content-plan.md` (the approved format: one technique, explained precisely, then the feature),
3. `docs/video-research.md` (why the format looks like this), `docs/style-guide.md`, `docs/learnings.md`,
4. the approved examples: `samples/launch/*.json` (shots), `queue/2026-W44.json` (captions).

## 0. Set up (5 min)

```bash
date -u +%Y-%m-%dT%H:%M:%SZ        # STARTED_AT
cd <repo> && git pull --ff-only
pip install -r engine/requirements.txt --break-system-packages -q
which tesseract || (apt-get install -y -q tesseract-ocr >/dev/null 2>&1 || true)   # for scan_text.py
```

Work out the **target dates**: the posting days from tomorrow (Chicago time) up to and including the Sunday
that ends next ISO week if today is Sunday, otherwise this ISO week's Sunday. Posting days are **Sun, Mon, Tue,
Thu, Fri** (5 a week), except the seasonal weeks in `docs/content-plan.md` ("Posting schedule"): Thanksgiving
week and winter break use 3 days (Sun, Tue, Thu). Drop dates that already have an item in any `queue/*.json`.
At most 5. WEEK = the ISO week of the first target date (e.g. `2026-W45`). If there are no target dates,
skip to step 7.

Check the tools: Buffer (`mcp__Buffer__get_account`) and Gmail (a send-email tool). If Gmail is missing,
still make the videos, and put "REVIEW EMAIL NOT SENT: Gmail tool missing" in the first line of the final
message (Minh then reviews from the phone notification links).

## 1. Read last week's results (Buffer)

Organization `6ade9794a35a0249267652ea`. Channels: TikTok `6adeb5f32f1f5ed648d24c10`,
Instagram `6adeae0a2f1f5ed648d2098e`, YouTube `6adeb1252f1f5ed648d21ba6`.

- `list_posts` with `status: ["sent"]`, `dueAt` = the last 8 days, `includeMetrics: true`.
- Match each post to its queue item by the video URL or caption. For each video, append one line to
  `docs/learnings.md` under "Results": date, kind, hook line, keyword, and per channel the posting time,
  views or impressions, likes and comments (and the `slot_test`, if any).
- Then update "What works" in at most 5 bullets. With under 2 weeks of data, say "too early".
- Posting slots: with 4+ weeks of results, compare views per channel per time slot; if a tested slot beat the
  default on at least 3 of 4 tests, change the default in `docs/content-plan.md` ("Posting schedule") and say so.
- List errored posts (`status: ["error"]`) in the final message with their error text.

## 2. Research (one helper agent, in parallel with step 3)

Start one **Scout** agent with this brief (fill in the dates):

> Find material for Cramrade's short study videos for <target dates>. Cramrade is a study web app for
> university students. Return a markdown list, written to `runs/<WEEK>/scout.md`:
> (a) 6 study techniques backed by research that a student would find surprising, each with: one
> plain-words sentence, the exact numbers (sample size, effect, what was compared), and **2 sources**
> (the paper or a university/reputable page; give URLs you actually opened). Prefer: retrieval practice,
> spacing, interleaving, sleep and memory, cramming vs spacing, pretesting, elaboration, test anxiety,
> handwriting vs typing. Mark anything contested or small-sample. Avoid the ones listed as "already done"
> in docs/content-plan.md.
> (b) 2 things students are talking about this week (midterms/finals timing, a study trend), with link and date.
> No medical advice. No claims about any product.

While it runs, read `docs/learnings.md` and the last two queue files so you don't repeat a hook.

## 3. Plan the week

One video per target date, each following `docs/content-plan.md`: one technique, the precise number and
its study, what to do, then the Cramrade feature that matches it, on a real screenshot. Rotate the pillars
so no two days in a row use the same feature. If the Scout found a timely trend that fits, use it as the
hook of one video. Kinds for the queue: `fact` (a study number), `tips`, `feature`, `trend`.

Write each script (55-75 spoken words, 22-30 s) in `scripts/<WEEK>/NN-<slug>.txt`:
- Hook in the first sentence (a relatable moment or a number) **and an open loop by second 3** (a bold claim or a
  curiosity gap: "That feeling is lying to you."). Plain words, short sentences, no hype.
- Before the CTA, one short line that calls back the hook (loop ending: "So don't read it a fifth time.").
- Name the study in words a student understands ("In a 2006 study...", "Researchers tested more than 1,350 people").
- One true Cramrade feature from docs/knowledge.md section 2, said plainly.
- End exactly with: "Comment PLAN, and I'll send you the link."
- Pick the video's **keyword** (see `docs/content-plan.md`, Packaging) now; it goes in titles, caption, hashtags.
- At most one ElevenLabs tag such as [excited], before the turn from problem to fix.
- Never "18+", never "AI study plan", never "sign up".

## 4. Voice, scenes, music, render

For each video, `NN` = 01, 02, … in date order; files go in `samples/<WEEK>/` (shots, voice, words) and
`videos/<WEEK>/`:

1. **Voice + word timings:** `python engine/v2/voice.py "$(cat scripts/<WEEK>/NN-<slug>.txt)" samples/<WEEK>/NN-<slug>`.
   It uses ElevenLabs (the real Notch voice) through the environment's network secret for api.elevenlabs.io
   (or an `ELEVENLABS_API_KEY` variable), otherwise the Kokoro fallback voice. If it prints `FALLBACK`, say so in the review email and
   the final message. Run it once per video (ElevenLabs charges per call; never loop on errors).
2. **Shots JSON** `samples/<WEEK>/NN-<slug>.json`, the format of `samples/launch/01-recall.json`:
   `voice`, `words`, `end_t` = last word end + 0.8 s, **`hook`** (cover text + amber mark, see
   `docs/content-plan.md`, Packaging; the first frame is the thumbnail, so check it on the contact sheet), `emphasis` (4-10 key words, "blue"; "exam" "amber"),
   `shots`: cut on sentence boundaries from the words file, a new shot every 1.5-3 s, last shot `end` at
   "Comment PLAN". Use the sets in `engine/v2/notch_v2.py` (`SETS`); write a new set function when the story
   needs a new picture (keep the pixel line-art look, art inside canvas y 55-325, only Notch blue and exam
   amber). The Cramrade beat uses `"set": "screen"` with `"screen": {"file": "home/....png", "hl": [x0,y0,x1,y1]}`
   (crop with `"crop"` when the image is wide). Screens and what they show: `engine/assets/screens/screens.json`.
3. **Music:** `python engine/v2/score.py auto samples/<WEEK>/NN-<slug>.json samples/<WEEK>/NN-<slug>-music.mp3 --seed <NN>`
   (a different track per video; it follows the video's cuts).
4. **Render:** `python engine/v2/notch_v2.py samples/<WEEK>/NN-<slug>.json videos/<WEEK>/NN-<slug>.mp4 --sheet runs/<WEEK>/NN.png --bed samples/<WEEK>/NN-<slug>-music.mp3`.
5. **Look** at the contact sheet yourself (Read the PNG): nothing cut off, the caption never covers Notch or
   the screenshot, the highlight box sits on the right line, the first still (the cover) shows the hook text and
   the amber mark on the right thing. Fix and re-render if not.
6. **Scan:** `python engine/scan_text.py videos/<WEEK>/NN-<slug>.mp4` must end with `0 with forbidden text`
   (no "18+" / "18 and over" anywhere). Loudness: about -14 LUFS (the engine normalises it).
7. **Queue item** in `queue/<WEEK>.json` (format: `queue/2026-W44.json`):
   - `time` `"19:00"` (Chicago, fallback) and **`times`** `{"tiktok": "20:00", "instagram": "18:00", "youtube": "17:00"}`
     (finals season: tiktok `"21:00"`); one item a week carries a `slot_test` (content-plan "Self-tuning").
   - `kind`, `video`, `script` (the shots JSON path), `sources` (2 URLs per number), `keyword`.
   - `caption`: paragraph 1 the idea with the study and number; paragraph 2 how Cramrade fits, ending
     "Cramrade is invite-only right now. Comment PLAN and I'll send you the waitlist link."
   - 3-5 hashtags (one is the keyword); `tiktok_title` ≤ 90 chars and `youtube_title` ≤ 100 chars ending with
     `#Shorts`, each with the keyword once; the caption uses the keyword twice.
   - **`status` `"review"`** (the daily run only books it after Minh approves; see step 6).
   - **No "18+" anywhere** (Minh, 2026-10-30): caption, titles, voiceover, on-screen captions, end card, screenshots.
8. `python engine/queue.py check queue/<WEEK>.json` must print `queue ok`.

## 5. Independent review (one helper agent)

Start a **Reviewer** agent that has not seen your reasoning. Give it the paths, not your opinions:

> You review Cramrade's short videos before they go to the founder. Read `docs/knowledge.md` (section 5
> is binding), `docs/content-plan.md`, then for each item in `queue/<WEEK>.json`: its script, its shots
> JSON, its contact sheet `runs/<WEEK>/NN.png`, its words file and its caption. Open every source URL the
> item cites. Return, per video, PASS, or FIX with exact changes, or DROP with the reason. FIX or DROP when:
> a number is not supported by the cited source; any claim breaks section 5 (no teens, no phone app or
> alarms, no prices or "free", no "AI study plan", no "nothing leaves your device", no results claims, no
> first/only claims); any "18+" / "18 and over" text is visible, spoken or written; a feature is shown that
> is not live; the screenshot does not match what the voice says; text is cut off or unreadable on a phone;
> the caption and the video disagree; the tone is hype or guilt. Write your verdicts to `runs/<WEEK>/review.md`.

Apply the FIXes, re-render, ask the same Reviewer to look again (send it a message). At most 2 rounds. A
video that still fails is removed: delete its mp4 and queue item and leave that date empty.

## 6. Publish to the repo, then send Minh the review email

```bash
git add scripts samples videos queue runs docs engine
git commit -m "Week <WEEK>: <n> videos for review"        # end with the attribution lines from the session
git push
```

Check each video URL answers 200: `curl -sI https://raw.githubusercontent.com/BennguyenEHK/cramrade-media/main/videos/<WEEK>/<file> | head -1`
(the raw URL can take a minute; retry once after 60 s).

Then send **one** email with the Gmail tool, to **bennguyenehk@gmail.com only**, plain text:
- Subject exactly: `[Cramrade] Review week <WEEK>: <n> videos`
- Body, per video, numbered with its NN:
  ```
  NN  <weekday date>  ·  <kind>  ·  <hook sentence>  ·  keyword: <keyword>
      Watch: https://raw.githubusercontent.com/BennguyenEHK/cramrade-media/main/videos/<WEEK>/<file>.mp4
      Stills: https://raw.githubusercontent.com/BennguyenEHK/cramrade-media/main/runs/<WEEK>/NN.png
      Caption: <first sentence of the caption> …
      Sources: <urls>
  ```
  then one line if the voice used the fallback, then:
  ```
  How to answer (reply to this email; the daily run reads your reply at 1 pm on each post day):
    APPROVE ALL            post every video on its day
    APPROVE 01 03 04       post only these
    DROP 02                never post this one
    FIX 05: <what to change>   not posted; tell Claude what to change
  Nothing is posted until you approve it.
  ```

## 7. Clean up

Delete `videos/<week>/` folders whose last queue date is more than 14 days ago, and set those items'
`status` to `"archived"`. Scripts, samples, queue files and runs stay. Commit and push.

## 8. Final message (this is all the founder reads; also sent as a phone notification)

At most 15 lines:
- First line: "<n> videos ready for your review: check your email ([Cramrade] Review week <WEEK>)",
  or what blocked the run.
- One line per video: date, kind, hook.
- Anything dropped and why; whether the voice was ElevenLabs or the fallback.
- Last week's numbers in one line, and the top video.
- Problems: errored posts, a missing Buffer or Gmail connection, a failed push.

Never: book or delete Buffer posts (the daily run books them after approval); email anyone but
bennguyenehk@gmail.com; commit keys, passwords, emails or anything from a signed-in account; claim
something section 5 forbids; put "18+" in any video, caption or title; leave the repo with a failing
`queue.py check`.
