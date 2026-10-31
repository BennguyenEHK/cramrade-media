# Content plan: "Notch explains" (approved by Minh, 2026-10-30)

The weekly run follows this plan. It comes from the reference research (`docs/video-research.md`) and the
launch week Minh approved (`samples/launch/`, `videos/2026-W44/*-v3.mp4`, `queue/2026-W44.json`).

## The idea

Every video = **one study technique, explained precisely by Notch** (a real number and the study it comes
from), then **the Cramrade feature that does it for you**, shown with a real screenshot from
`engine/assets/screens/`. About 70 % teaching, 30 % product. It must never feel like an ad.

Why: the faceless study shorts that win have a voice, word-by-word captions, a change every 1-3 s, a stake
in the first 2 s and a comment trigger. A precise number with a named study is saveable and builds trust
for an AI study app.

## Video formula (22-30 s, 55-75 spoken words) -- updated 2026-10-30 with Minh's short-form tips

| beat | time | what |
|---|---|---|
| Hook | 0-3 s | a relatable moment **plus an open loop** (a bold claim or a curiosity gap) said by 3 s: "You read your notes four times. That feeling is lying to you." / "Exam in 20 days? Most people review on the wrong days." No intro, no logo: Notch is on screen at frame 1 and the voice starts at 0.0 s. |
| Mechanism | 3-14 s | the study + the exact number, drawn as a pixel scene (bars, timeline, crowd, calendar); a cut every 1.5-3 s |
| What to do | 14-21 s | the technique in one plain sentence |
| Cramrade | 21-26 s | the feature, on a real screenshot with a blinking highlight box on the exact part |
| Loop + CTA | last 3-4 s | one short line that calls back the hook ("So don't read it a fifth time."), then "Comment PLAN, and I'll send you the link." End card under 1 s so the replay starts fast. |

### Packaging (every video)

- **Cover frame / on-screen hook**: the shots JSON has a `hook` block: `"hook": {"text": "READ IT 4 TIMES?\nIT'S LYING TO YOU", "amber": ["LYING"], "mark": [x, y, r], "until": 2.6}`.
  The engine draws the hook text near the top (below the apps' top bar) for the first 2.6 s and an amber ring
  (or `[x, y, r, "arrow"]`) on the key thing in the first scene. Frame 1 is what TikTok/Instagram/YouTube show
  as the thumbnail, so it must read on its own: at most 2 lines, about 4 words a line, one amber word, the ring on
  the thing the hook is about. Amber, never red (brand: only blue and amber).
- **Keyword**: pick one search keyword per video (e.g. "active recall", "spaced repetition", "study group").
  Use it once in the TikTok and YouTube titles, twice in the caption, and as one of the hashtags.
- **Captions** stay word-by-word (many watch on mute); art stays in the top two-thirds, captions above the bottom 420 px.
- **Trends**: use trending *topics and angles* (exam season, a study trend the Scout finds). Never trending audio:
  it is copyrighted and cannot go through Buffer; every video keeps its own original score.

## Posting schedule ("golden hours", Chicago time) -- set 2026-10-30

- **5 videos a week: Sun, Mon, Tue, Thu, Fri** (Wednesday is TikTok's weakest day). Consistency for 6-8 weeks
  matters more than any single slot.
- Per platform, in each queue item's `times`: **TikTok 20:00, Instagram 18:00, YouTube 17:00** (`time` stays "19:00"
  as the fallback). Basis: Buffer 2026 data (TikTok strongest 6-11 pm, Instagram peaks ~6 pm, Shorts strong Fri 4 pm
  and weekday evenings 6-11 pm), adapted for students.
- **Season**: mid-Nov to mid-Dec (finals) TikTok 21:00 and lean on exam-week content; Thanksgiving week (and the
  week of Dec 25) 3 videos (Sun, Tue, Thu); winter break (mid-Dec to mid-Jan) 3 a week; back to 5 when spring
  semester starts.
- **Self-tuning**: every week one video tests one changed slot on one platform (e.g. TikTok 21:00 instead of 20:00),
  noted in the queue item as `"slot_test": "tiktok 21:00 vs 20:00"`. The weekly run compares views in
  `docs/learnings.md`; after 4 weeks of data it moves the default to the winner and writes why.

## Pillars (rotate; one technique per video)

1. **Recall over re-reading** -> questions from your own notes, each showing the line it came from (quote check). Screens: `home/question-source.png`, `home/quote-check-card.png`.
2. **Spacing** -> plan built backwards from the exam date; gaps shrink as the date nears; move the date and the plan moves. Screens: `home/plan-calendar.png`, `home/date-not-streak.png`.
3. **Study together, test each other** -> live group quiz from the group's notes, join with a code, podium. Screens: `home/how-it-works.png` (crop to step 4), `podium.png`.
4. **Exam-week triage** -> mock test 2 days before, final review the day before, several exams at once.
5. **Interleaving / mixing topics**, **sleep and memory**, **cramming vs spacing**, **handwriting vs typing** -> only when the feature link is honest (e.g. sessions cover up to 3 topics).
6. **Privacy said plainly** -> files deleted after reading, never reads your calendar. Screen: `home/privacy.png`.

Already done (do not repeat the same hook within 4 weeks): 40 % vs 61 % re-read vs self-test (Roediger &
Karpicke 2006); the spacing gap, 1,350+ people (Cepeda et al. 2008); study group quiz.

## Rules

- docs/knowledge.md section 5 is binding: no "AI study plan" (the plan is plain code), no prices or "free",
  no results claims, no teens/high school, photos of paper notes are "soon".
- **No "18+" anywhere** (video, end card, screenshots, captions, titles). Cramrade is still for 18+ only.
- Site is **invite-only**: captions end "Cramrade is invite-only right now. Comment PLAN and I'll send you
  the waitlist link." Never "sign up now".
- Every number needs 2 sources you opened (paper, university page or reputable outlet) in the queue item.
- Each video gets its own music: `python engine/v2/score.py auto SHOTS.json MUSIC.mp3 --seed N` with a
  different seed per video (palettes rotate: snow, bells, group, ember).
- Captions avoid AI tells: no "it's not X, it's Y", no em dashes, no "Here's the thing".
- Hashtags: 3-5 from #studytips #activerecall #spacedrepetition #examprep #studyhacks #studygroup #college.
