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

## Video formula (25-32 s, 60-85 spoken words)

| beat | time | what |
|---|---|---|
| Hook | 0-3 s | a relatable moment or a number: "You read your notes four times...", "Exam in 20 days?", "Study group tonight?" |
| Mechanism | 3-16 s | the study + the exact number, drawn as a pixel scene (bars, timeline, crowd, calendar) |
| What to do | 16-24 s | the technique in one plain sentence |
| Cramrade | 24-29 s | the feature, on a real screenshot with a blinking highlight box on the exact part |
| CTA | last 3 s | Notch: "Comment PLAN, and I'll send you the link." End card: "Comment PLAN" + cramrade.app |

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
