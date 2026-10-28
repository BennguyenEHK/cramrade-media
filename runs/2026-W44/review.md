# Review: 2026-W44, items 02-05

Reviewed 2026-10-27 against docs/knowledge.md (sections 2 and 5) and docs/style-guide.md. Item 01 (10-28) skipped, already booked.
Checked: script JSON, contact sheet, full-res frames of the app scenes, caption, titles, hashtags, cited sources.

Sources checked:
- Roediger & Karpicke 2006 (full text): Exp 1 restudy vs test, recall 81/75% at 5 min, 54/68% at 2 days, 42/56% at 1 week. Exp 2 at 1 week: SSSS 40%, SSST 56%, STTT 61%; SSSS students predicted the best recall. Supports "testing beat rereading a week later" and "rereading feels easier but fades faster".
- Dunlosky et al. 2013 (abstract): high utility = practice testing, distributed practice only. Interleaving = moderate. Highlighting, rereading = low. Sleep is not one of the 10 techniques.
- Diekelmann & Born 2010, Nat Rev Neurosci 11:114 (doi 10.1038/nrn2762): sleep after learning supports consolidation of declarative memories. Supports "sleep the night before" (sleep after studying).

Shared visual bug (02 scene 4, 04 scene 4): the `plan-card` highlight box clips the bottom of "matrix of the mitochondria." (source box top y=328 minus 10-15 px pad lands on that line's baseline). Cut-off text, so FIX.

---

## 02 quiz-yourself (2026-10-29): FIX

- Research claims: supported (see above). Caption matches the video.
- Scene 4 (`app`, plan-card): add `"highlight": false` to stop the box clipping "matrix of the mitochondria.".
  (Alternative, not in this file: change `plan-card` highlight in engine/assets/screens/screens.json to `[52, 340, 452, 372]`, which clears the line and fixes 04 too.)
- Optional, slight overstatement in scene 3: `"lines":["Pulling it","out of memory","helps it","stick."]` instead of "is what makes it stick."

## 03 four-habits (2026-10-30): FIX

- The hook cites only Dunlosky 2013 for all 4 habits, but Dunlosky doesn't cover sleep and rates interleaving moderate, not top. Cite both sources on screen:
  scene 1 `"source":["Dunlosky et al. 2013;","Diekelmann & Born 2010"]` (21 and 22 chars).
- The caption is accurate ("the two techniques Dunlosky et al. (2013) rated most useful" = practice testing and spacing, the only two rated high). Timeline and caption match section 2 (gaps shrink towards exam day). Layout reads fine.

## 04 quote-check (2026-10-31): FIX

- Claims match section 2 (quotes exact lines, word-for-word check, dropped and not patched). No sources needed. Tone fine.
- Scene 4 (`app`, plan-card): add `"highlight": false` (same clipping as 02).

## 05 building-it (2026-11-01): FIX

- Scene 3 caption "No account needed." is wrong: the host needs an account, and only guests joining by code or link don't (they tick 18+). Replace with:
  `"caption":["Friends join with a code.","Guests need no account."]` (25 and 23 chars).
- Everything else is fine: honest beta tone, the podium is sample data, the queue caption ("quiz each other live with a join code") is accurate.

---

Not blocking: text inside the app screenshots (e.g. "From your notes, line 14") renders at about 20 px on 1080 px, under the 40 px caption minimum. The captions below carry the message, so I left it as is. All text sits clear of the top 220 px and bottom 420 px. No section 5 breaches in any caption, title or hashtag.
