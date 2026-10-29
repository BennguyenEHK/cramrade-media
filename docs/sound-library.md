# Outside sounds that are safe for the pipeline (researched 2026-10-28)

**Decision (2026-10-28):** Minh picked **Minimalist Winter (MoodStrides, Pixabay)** as Cramrade's main theme.
- Prepared versions are in his local `marketing/audio/`:
  - `cramrade-theme-minimalist-winter-loop.mp3`: -17.6 LUFS, seamless 4 s crossfade loop;
  - `cramrade-bed-minimalist-winter.mp3`: -19.6 LUFS.
- **Do not commit these files here.** This repo is public, and the Pixabay licence forbids standalone redistribution.
- To use it in the auto pipeline, it must come from private storage first (a private repo, or a fetch at render time). Until then, the engine falls back to the Base Camp bed.

**Rule:** the auto pipeline only uses tracks that are CC0 or Pixabay-licensed **without** the "Content ID Registered" label.
Labelled tracks get auto-claimed on YouTube, TikTok and Instagram, and nobody is there to dispute the claim.
The default bed is still `engine/assets/music/cramrade-bed-base-camp.mp3`, which is ours and carries zero claim risk.

| track | creator | licence | credit | use |
|---|---|---|---|---|
| First Light Particles | Yoiyami | CC0, https://opengameart.org/node/182244 | optional | focus music, longer videos |
| Minimalist Winter | MoodStrides | Pixabay, no Content ID, https://pixabay.com/music/solo-piano-minimalist-winter-504109/ | none | video bed |
| Frozen Felt Piano | MoodStrides | Pixabay, no Content ID, https://pixabay.com/music/lofi-frozen-felt-piano-504111/ | none | video bed |
| Grey Sky Walk | MoodStrides | Pixabay, no Content ID, https://pixabay.com/music/solo-piano-grey-sky-walk-504107/ | none | hopeful video bed |
| Icy Solitude Piano Music | adiiswanto | Pixabay, no Content ID, https://pixabay.com/music/solo-piano-icy-solitude-piano-music-470725/ | none | focus music |
| Winter Wind | wipics | CC0, https://opengameart.org/node/114089 | none | outro |
| wind whoosh loop | SketchMan3 | CC0, https://opengameart.org/content/wind-whoosh-loop | none | room tone and cut whoosh, kept very low |

**Avoid (Content ID Registered):**
- White Clouds
- Evening Snowfall
- Soft Felt Piano [Moon Rise]
- Winter Morning
- Light Room
- Study Music (The_Mountain)
- Blue Stasis
- Fading (noemazeek)
- Ashveil

Before adding any new Pixabay track, open its page and check for the label.

**Other sources not to use, and why:**
- YouTube Audio Library: cleared for YouTube only.
- Incompetech: CC-BY, so every caption would need a credit.
- Mixkit: most of its piano tracks have drums, and its Restricted licence forbids monetised use.
