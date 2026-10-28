# Cramrade: marketing knowledge base

Public copy for the weekly video run. Source of truth for anyone (human or Claude) making Cramrade content. Built from the codebase, founder notes and live site on 2026-10-25. When this file and the code disagree, the code wins.

## 1. The product in one breath

**Pitch:** A study app that builds your review plan backwards from your real exam date, quizzes you only from your own notes, and lets your study group quiz each other live.

**Homepage headline:** "Your notes, planned backwards from exam day."

**Name:** cram + comrade. "-rade" also sounds like "grade".

**Who it's for (today):** university students and adult learners, **18+ only**. This is enforced in the database. The AI vendors' terms bar under-18s, so no teen marketing.

**Where:** https://cramrade.app. Works in the browser, nothing to install.

**Main competitor named by the team:** NotebookLM. Cramrade is deliberately *not* "chat with your notes". The two things nobody else leads with are the exam-date plan and the group quiz from the group's own notes.

## 2. What's live right now (safe to show and say)

**Exam dates**
- Upload a syllabus and Cramrade finds the exam dates. You press "Confirm" or "Not right", and nothing is saved until you confirm.
- Estimated dates are labelled as estimates.
- You can also add an exam by hand.

**Notes in**
- PDF, Word (.docx), .txt, .md and photos (jpg/png/webp/heic), up to 20 MB each.
- Batch photo upload, the phone browser's camera, and a handwriting pad.
- Files and photos are deleted after the text is read. Only the text stays.

**The plan (this is plain code, not AI)**
- Sessions of 5–7 questions, covering at most 3 topics, with 2 slots kept for new material.
- A topic comes back after a gap of about 20% of the days left (max 14 days), and daily in the final week. It's based on spacing research (Cepeda et al. 2008).
- A topic counts as learned after 3 recalls.
- Mock test (up to 20 questions) 2 days before the exam, and a final review the day before.
- Handles several exams at once: the closer and higher-stakes ones get priority. It skips busy days and warns you when you're behind.
- Change the exam date and the whole plan moves.

**Questions you can trust**
- Every question quotes the exact lines of your notes it came from.
- The app checks that the quote really exists word for word. If it doesn't, the question is dropped, not patched.
- The AI never adds content to your notes.

**Practice modes**
- Flashcards
- Solo quiz
- Live group quiz
- Chain Climb (a two-player co-op game: agree on the answer to climb)

**Live group quiz**
- Hosted from the web. Pick one exam or one note, 1–50 questions, 5–300 seconds per question.
- Friends join with a 6-character code or a link. Guests don't need an account (they tick the 18+ box).
- The server keeps the clock and scores, with a live leaderboard and podium.

**Other live features**
- **Calendar:** one-tap subscribe for Apple and Google Calendar. Cramrade only sends to your calendar and never reads it.
- **Reminders:** an email an hour before each study day's session, with an on/off switch.
- **Coach:** an AI tutor that answers only from your notes and coaches you rather than handing out answers.
- **"Tonight" card** with a skim sheet.
- **Friends:** invite by link or QR code.
- **Light and dark themes.**

**Beta or flagged:**
- Place-aware study nudge
- Lecture recording to text (off by default)

## 3. Best "wow" moments to film (faceless 2D videos)

1. **Syllabus → exam date found → Confirm.** The fastest "how did it know" moment.
2. **Plan appears:** sessions bunching up as exam day approaches, and the whole plan sliding when you change the date.
3. **A question with its source quote:** "From your notes, page 2". This is the trust angle against generic AI.
4. **Group quiz:** share a code, the leaderboard updates live, podium at the end.
5. **Chain Climb:** two players have to agree to climb. A playful, shareable clip.
6. **Calendar:** one tap and the study sessions appear in Google/Apple Calendar.
7. **Photo of paper notes → text → questions.**

## 4. Content angles that are true to the product

- **Exam countdown:** "18 days to my final, here's my plan."
- **Built around the date, not a streak.** Anti-guilt, anti-gamification.
- **Your notes, only your notes.** No made-up AI facts, every question shows where it came from.
- **Cramming vs. spacing,** explained in 15 seconds (the 20%-of-days-left rule is good content on its own).
- **Study group night:** the quiz everyone joins from a link.
- **Privacy, said plainly:** files deleted after reading, never reads your calendar, never scans your device.

## 5. Never claim (any of these would be false or risky)

**Audience and platforms**
- Teens or high schoolers as users. It's 18+ only today.
- A downloadable phone app, App Store/Play listings, or phone push alarms. The native app isn't built. The browser camera, email reminders and calendar are real.

**Features that don't exist**
- Alarms that ring through silent mode.
- Arena/battle game, video chat, voice chat, or cited 5–10 minute lessons. Chain Climb is the only game.
- "Live updates from friends". The app itself says this is coming soon.

**AI wording**
- "AI study plan". The schedule is plain code. Say "plan built from your exam date".
- "AI is always right". The Terms say AI can be wrong.

**Privacy**
- "Nothing leaves your device". Note text is stored on Cramrade's servers (Supabase) and sent to AI providers: Google Gemini, OpenAI, Microsoft Azure for lectures.

**Pricing and results**
- Prices, "free forever", or Pro tiers. No pricing is built yet. Founder's planned direction is Free / Pro (~$6.99/mo) / Max, undecided in code.
- Results like "students improve grades by X%". There's no test data yet.
- "First" or "only" claims about competitors (see the competitor research docs).

## 6. Brand kit

**Logo**
- The countdown ring: a blue arc with an amber square at the top, like a timer with the exam marker.
- Files: `apps/app/assets/brand/mark.svg` (symbol), `lockup.svg` (symbol + "Cramrade"), `mark-small.svg`.
- App icon: `apps/app/assets/images/icon.png` (1024×1024, off-white background).

**Pixel look (since 2026-10-27).** Making an image or video? Follow `marketing/pixel-style-guide.md` (step-by-step instructions for agents). In short, the app moved to the Arcade Night pixel theme, so social images are pixel art too:
- The logo is exactly the app's pixel logo: a round ring on a 12 × 12 grid, three quarters blue with a faint track for the rest, and a 2 × 2 amber exam square on top. Files: `marketing/social/pixel-mark-color.svg` (on light), `pixel-mark-dark-bg.svg` (on dark), `pixel-mark-white.svg` (on blue), `pixel-mark-black.svg` (one colour).
- Notch, the pixel tutor mascot built from the logo (the ring is its body), may appear small in posts, in one of its four app poses.
- The signature element is a pixel timeline: study-day blocks that get closer and brighter towards an amber exam-day block.
- Keep it easy to read: big headlines, short lines, plenty of dark space, one amber highlight per image.
- Older images were deleted on 2026-10-28; only the files in `marketing/social/` are current.

**Social avatars** (pixel, 2026-10-27): `marketing/social/avatar-blue.png` (recommended: white pixel ring on blue, pops in feeds) and `avatar-light.png`.

**Colors**
- Cobalt `#2F5BFF`: action, study
- Amber `#F5A524`: exam day. Use as a fill only, never for text.
- Ink `#1B1F2A`, paper `#EEF0F6`, homepage dark backdrop `#0E1220`
- Green `#22C55E` and red `#EF4444`: right/wrong answers only

The rule is "nothing else is colored", so keep videos to blue + amber + ink/paper.

**Fonts** (Monocraft, the app's own pixel font since 2026-10-27)
- Monocraft Bold for headlines, the "Cramrade" wordmark and links.
- Monocraft for body text.
- Free (SIL OFL) font files: `apps/app/assets/fonts/Monocraft.ttf` and `Monocraft-Bold.ttf`. They are not on Google Fonts; install them to use in Jitter/CapCut.
- Sizes on a 1080 px image: headline 76 px or more, body 38 px or more (Monocraft is wide).
- Don't use the earlier fonts (Pixelify Sans, Jersey 10, DotGothic16) for new work.

**Dark (Arcade Night) colours for social:** background `#0E1124`, text `#F1F2FA`, muted text `#A3ABD1`, blue `#7592FF`, amber `#FFB13B`.

**Voice:** plain words a non-expert can follow. Short sentences, no hype, no jargon.

## 7. Quotable site copy

- "Your notes, planned backwards from exam day."
- "Add the exam date and the notes you already have."
- "Built around the date, not around a streak."
- "Questions from your notes, and only your notes."
- "Got an exam coming up?"
- Button label: "Start a plan"
- Invite text: "Study with me on Cramrade."

## 8. Growth hooks already in the product

- Quiz join links and codes, where guests need no account. This is the main free growth loop.
- Friend invites by link or QR code.
- Calendar subscribe link.
- A demo login exists, useful for showing judges or creators.
- **Missing:** no analytics, waitlist, referral tracking or feedback widget. So we can't yet measure which video brought a signup. Worth adding simple UTM links plus a "how did you hear about us" question.
