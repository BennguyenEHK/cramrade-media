# Cramrade pixel style: instructions for marketing agents

Read this before making any Cramrade image, video frame, thumbnail or post. Since 2026-10-27 the app uses the "Arcade Night" pixel theme, so everything we publish is pixel art too. For product facts and claims, `cramrade-marketing-knowledge.md` still applies; this file only covers the look.

## The one rule

Pixel style, but easy to read. A stranger scrolling past must read the headline in under two seconds. If you have to choose between "more pixel" and "easier to read", choose easier to read.

## Files to use (in `marketing/social/`)

- **Logo (exactly the app's pixel logo):** a round ring on a 12 × 12 pixel grid. Three quarters are blue, the last quarter is a faint "track" of the same ring, and a 2 × 2 amber exam square sits at the top. Files:
  - `pixel-mark-color.svg` for light backgrounds
  - `pixel-mark-dark-bg.svg` for dark backgrounds
  - `pixel-mark-white.svg` for the blue background
  - `pixel-mark-black.svg` when only one colour is allowed
- **Profile pictures:** `avatar-blue.png` is the one to use everywhere. Also `avatar-light.png`, `profile-dark-1080.png`, `profile-light-1080.png` and `youtube-profile-800.png`.
- **Ready-made images:** `instagram-post-1080x1350.png`, `tiktok-story-cover-1080x1920.png` and `youtube-banner-2560x1440.png`. Copy their layout for new posts.
- **Older versions:** deleted on 2026-10-28. If you find an old Cramrade image anywhere (a smooth ring, or a pixel ring with an open gap and no faint track), don't use it.
- **Source of truth:** the logo and Notch are drawn by the app's own code, in `apps/app/src/components/brand/mark-pixels.ts` and `notch-pixels.ts`. If the app's logo ever changes, the images must be made again from that code.

Never redraw, stretch, rotate, recolour or add effects to the logo. Scale it only by whole steps (2×, 3×, 4×…) so the pixels stay square and sharp.

## Colours

The dark background is the default:

- Background: `#0E1124` (deep: `#090B18`, cards: `#171C38`)
- Text: `#F1F2FA`; quieter text: `#A3ABD1`
- Blue: `#7592FF` on dark; `#2F5BFF` on light and as the avatar background
- Amber: `#FFB13B` on dark; `#F5A524` on light

Rules:
- Amber means exam day. Use it for one thing per image: the exam block, or the words "exam day". Never use it for long text.
- Green and red appear only for right and wrong answers.
- No other colours, no gradients, no glow, no drop-shadow blur.

## Font: Monocraft, the app's own pixel font (since 2026-10-27)

- **Monocraft Bold:** headlines, the "Cramrade" name next to the logo, and the link.
- **Monocraft (regular):** everything else.
- **Font files:**
  - The free font files (SIL Open Font Licence) are in the repo at `apps/app/assets/fonts/Monocraft.ttf` and `Monocraft-Bold.ttf`, with the licence next to them. Install both on your computer to use them in Jitter, CapCut or Canva.
  - Monocraft is not on Google Fonts.
- **Don't use the earlier fonts** (Pixelify Sans, Jersey 10 or DotGothic16) for new work.
- **Minimum sizes on a 1080 px wide image:**
  - headline 76 px, body text 38 px, link 50 px;
  - leave line spacing at about 1.35 for body text.

  Monocraft is wide, so these sizes are smaller than for most fonts but read just as large. Smaller than this turns to mush on phones.
- **Short lines:** a headline is at most about 8 words over 2–4 lines, and body text at most 2–3 lines.
- Use sentence case. No ALL CAPS words, because pixel capitals are hard to read in a row.

## Building blocks

- **Pixel timeline (our signature):** square blocks for study days that get closer together and brighter towards one bigger amber block, exam day. It shows "planned backwards from exam day" without words.
- **Notch:** the app's pixel tutor mascot, built from the logo. The ring is its body, with a face inside, the amber exam square as its antenna, small arms and feet.
  - It has four poses, exactly as in the app: `hello` (waving), `point`, `think` (with an amber question mark) and `cheer`.
  - Use one pose per image, at most once, in a corner or next to the link.
  - Never invent new poses, faces or colours.
- **Background texture:** a faint grid of small square dots, barely visible. If you can clearly see it, it's too strong.
- **Edges:** square corners everywhere. Pixel "stepped" frames are fine for cards; rounded corners are not.

## Layout

- Lots of empty dark space. One message per image.
- Logo and name at the top left, then the headline, then the timeline, then one or two lines of text, then the link (`cramrade.app`) and Notch.
- Left-aligned text.
- **Keep clear of platform buttons:**
  - TikTok and Reels: nothing important in the top 220 px or the bottom 420 px.
  - YouTube banner: everything important inside the middle 1546 × 423 px.
- **Profile pictures:** the logo alone, centred, at most about 60 % of the width, so the circle crop never cuts it.

## Video and screen recordings

- Show the real app. Its Notch pages and map are already pixel style.
- Captions in Monocraft Bold, white `#F1F2FA` on a solid `#0E1124` box, at least 40 px on 1080 px video.
- Motion: snap in whole-pixel steps, no blur, no smooth zooms on pixel art (it smears). Keep it to one animation per moment.

## Checklist before you publish

1. Can you read the headline at thumbnail size (about 200 px wide)?
2. Is amber used for exactly one thing?
3. Is everything set in Monocraft (Bold for the headline and the name)?
4. Are the logo pixels sharp and square (no blur from scaling)?
5. Is everything important clear of the platform's buttons?
6. Are the claims allowed by `cramrade-marketing-knowledge.md` (18+, no prices, no "AI study plan")?
