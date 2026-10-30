"""Cramrade video engine: turns a small JSON script into a 1080x1920 pixel-style MP4.

    python engine/render.py SCRIPT.json OUT.mp4            render video + audio
    python engine/render.py SCRIPT.json OUT.mp4 --sheet S.png   also write a contact sheet for review
    python engine/render.py SCRIPT.json --check            validate only (no render)

Style rules come from Cramrade's marketing/pixel-style-guide.md: dark #0E1124 ground, Monocraft,
amber only for exam day, square corners, snap-in motion, nothing important in the top 220 px
or bottom 420 px. Sprites (logo, Notch) are ported from the app's mark-pixels.ts / notch-pixels.ts.
See engine/README.md for the script format.
"""
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def _ffmpeg():
    import shutil
    if os.environ.get('FFMPEG'):
        return os.environ['FFMPEG']
    if shutil.which('ffmpeg'):
        return 'ffmpeg'
    try:
        import imageio_ffmpeg  # pip install imageio-ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise SystemExit('ffmpeg not found: pip install imageio-ffmpeg --break-system-packages')


FFMPEG = _ffmpeg()

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')

W, H, FPS = 1080, 1920, 30
BG = (14, 17, 36)
DEEP = (9, 11, 24)
CARD = (23, 28, 56)
TEXT = (241, 242, 250)
QUIET = (163, 171, 209)
BLUE = (117, 146, 255)
BLUE_SOFT = (34, 44, 97)
AMBER = (255, 177, 59)
LIMB = (142, 164, 255)
DOT = (24, 29, 54)
X0 = 90
SAFE_TOP, SAFE_BOTTOM = 220, H - 420

_fonts = {}


def font(bold, size):
    key = (bold, size)
    if key not in _fonts:
        name = 'Monocraft-Bold.ttf' if bold else 'Monocraft.ttf'
        _fonts[key] = ImageFont.truetype(os.path.join(ASSETS, 'fonts', name), size)
    return _fonts[key]


H96, B72, B60, R48, B48, R40, B40 = (font(True, 96), font(True, 72), font(True, 60), font(False, 48),
                                     font(True, 48), font(False, 40), font(True, 40))


def max_chars(f):
    return int((W - 2 * X0) // f.getlength('M'))


LIMITS = {'headline': max_chars(H96), 'title': max_chars(B72), 'body': max_chars(R48)}


# ---------------- sprites (from the app's own code) ----------------

def _mark_cells():
    G, INNER, OUTER = 12, 3.9, 5.8
    out = []
    for y in range(G):
        for x in range(G):
            dx, dy = x + 0.5 - G / 2, y + 0.5 - G / 2
            d = math.hypot(dx, dy)
            if INNER <= d <= OUTER:
                ang = (math.degrees(math.atan2(dx, -dy)) + 360) % 360
                out.append((x, y, BLUE if ang < 270 else BLUE_SOFT))
    out += [(x, y, AMBER) for x, y in [(5, 0), (6, 0), (5, 1), (6, 1)]]
    return out


_ARMS = {
    'hello': [(2, 12), (2, 13), (2, 14), (17, 8), (17, 7), (17, 6), (17, 5)],
    'point': [(2, 12), (2, 13), (2, 14), (17, 9), (18, 9), (19, 9)],
    'think': [(2, 12), (2, 13), (2, 14), (16, 12), (15, 13), (14, 13), (13, 13), (12, 13), (11, 13)],
    'cheer': [(2, 7), (2, 6), (2, 5), (3, 4), (17, 7), (17, 6), (17, 5), (16, 4)],
}
_FACE = {
    'hello': [(8, 8), (8, 9), (11, 8), (11, 9), (8, 11), (9, 12), (10, 12), (11, 11)],
    'point': [(9, 8), (9, 9), (12, 8), (12, 9), (8, 11), (9, 12), (10, 12), (11, 11)],
    'think': [(8, 7), (8, 8), (11, 7), (11, 8), (9, 11), (10, 11)],
    'cheer': [(6, 9), (7, 8), (8, 9), (11, 9), (12, 8), (13, 9), (8, 11), (9, 11), (10, 11), (11, 11), (9, 12), (10, 12)],
}
NOTCH_POSES = tuple(_ARMS)


def _notch_cells(pose):
    out = []
    for y in range(20):
        for x in range(-1, 21):
            dx, dy = x * 10 + 5 - 100, y * 10 + 5 - 100
            d = math.hypot(dx, dy)
            if d < 52:
                out.append((x, y, CARD))
            elif d <= 72:
                ang = (math.degrees(math.atan2(dx, -dy)) + 360) % 360
                out.append((x, y, BLUE if ang <= 270 else BLUE_SOFT))
    lift = 1 if pose == 'cheer' else 0
    out += [(x, y, AMBER) for x, y in [(9, 3 - lift), (10, 3 - lift), (9, 4 - lift), (10, 4 - lift)]]
    out += [(x, y, LIMB) for x, y in [(7, 17), (8, 17), (11, 17), (12, 17)] + _ARMS[pose]]
    out += [(x, y, TEXT) for x, y in _FACE[pose]]
    if pose == 'think':
        out += [(x, y, AMBER) for x, y in [(16, 1), (17, 1), (18, 1), (18, 2), (17, 3), (17, 5)]]
    if pose == 'cheer':
        out += [(1, 2, AMBER), (19, 7, AMBER), (17, 2, BLUE), (0, 9, BLUE)]
    return out


MARK = _mark_cells()
NOTCH = {p: _notch_cells(p) for p in NOTCH_POSES}


def cells(d, cs, x0, y0, s, xmin=0):
    for x, y, c in cs:
        px, py = x0 + (x - xmin) * s, y0 + y * s
        d.rectangle([px, py, px + s - 1, py + s - 1], fill=c)


def notch(d, pose, x, y, s, t=0.0, bob=True):
    off = -s if (bob and int(t * 3) % 2 == 0) else 0
    cells(d, NOTCH[pose], x, y + off, s, xmin=-1)


# ---------------- drawing helpers ----------------

def _background():
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    for y in range(12, H, 24):
        for x in range(12, W, 24):
            d.rectangle([x, y, x + 1, y + 1], fill=DOT)
    return im


BG_IMG = _background()


def text(d, xy, s, f, fill=TEXT):
    d.fontmode = '1'
    d.text(xy, s, font=f, fill=fill)


def highlight(d, xy, s, f, pad=14):
    x, y = xy
    bb = f.getbbox(s)
    d.rectangle([x - pad, y + bb[1] - pad, x + f.getlength(s) + pad, y + bb[3] + pad], fill=BLUE)
    text(d, (x, y), s, f, fill=BG)


def stepped_frame(d, box, fill, edge, step=6, b=6):
    x0, y0, x1, y1 = box
    d.rectangle([x0 + step, y0, x1 - step, y1], fill=edge)
    d.rectangle([x0, y0 + step, x1, y1 - step], fill=edge)
    d.rectangle([x0 + step + b, y0 + b, x1 - step - b, y1 - b], fill=fill)
    d.rectangle([x0 + b, y0 + step + b, x1 - b, y1 - step - b], fill=fill)


def title_block(d, lines, y=300, f=B72, lh=92):
    for i, ln in enumerate(lines):
        text(d, (X0, y + i * lh), ln, f)
    return y + len(lines) * lh


def body_block(d, lines, y, fill=TEXT, f=R48, lh=64):
    for i, ln in enumerate(lines):
        text(d, (X0, y + i * lh), ln, f, fill)
    return y + len(lines) * lh


class Ctx:
    """Collects audio cues while frames are drawn (only on the first pass)."""
    def __init__(self):
        self.blips, self.chimes, self.record = [], [], True

    def blip(self, t):
        if self.record:
            self.blips.append(t)

    def chime(self, t):
        if self.record:
            self.chimes.append(t)


# ---------------- scene types ----------------
# Each takes (im, d, t_local, scene, t0, ctx). t0 = scene start time (absolute) for audio cues.

def sc_hook(im, d, t, s, t0, ctx, with_source=True):
    lines, step, y0, lh = s['lines'], 0.22, 420, 128
    k = 0
    for li, ln in enumerate(lines):
        cx = X0
        for word in ln.split(' '):
            wt = 0.25 + k * step
            if abs(t - wt) < 0.5 / FPS:
                ctx.blip(t0 + wt)
            if t >= wt:
                text(d, (cx, y0 + li * lh), word, H96)
            cx += H96.getlength(word + ' ')
            k += 1
    hl_at = 0.25 + k * step + 0.2
    hl = s.get('highlight_line')
    if hl is not None and t >= hl_at:
        highlight(d, (X0, y0 + hl * lh), lines[hl], H96, pad=16)
        if abs(t - hl_at) < 0.5 / FPS:
            ctx.chime(t0 + hl_at)
    y = y0 + len(lines) * lh + 60
    sub = s.get('source') if with_source else s.get('caption')
    if sub and t >= hl_at + 0.5:
        y = body_block(d, sub, y, QUIET if with_source else TEXT)
    if s.get('notch') and t >= 1.0:
        notch(d, s['notch'], 700, max(y + 40, 1180), 13, t)


def sc_statement(im, d, t, s, t0, ctx):
    sc_hook(im, d, t, s, t0, ctx, with_source=False)


def sc_bars(im, d, t, s, t0, ctx):
    title_block(d, s['title'])
    gx0, gy0, gx1, gy1 = X0 + 60, 560, W - 110, 1180
    d.rectangle([gx0, gy1, gx1, gy1 + 5], fill=QUIET)
    d.rectangle([gx0 - 5, gy0, gx0, gy1 + 5], fill=QUIET)
    unit = s.get('unit', '%')
    top_v = s.get('max', 100)
    text(d, (X0 - 30, gy0 - 20), f'{top_v}{unit}', font(False, 36), QUIET)
    text(d, (X0 + 4, gy1 - 24), '0', font(False, 36), QUIET)
    bars = s['bars']
    n = len(bars)
    colw = (gx1 - gx0 - 40) / n
    gap = 0.42
    for i, (lab, v) in enumerate(bars):
        bt = i * gap
        if abs(t - bt) < 0.5 / FPS:
            ctx.blip(t0 + bt)
        if t < bt:
            continue
        cx = gx0 + 30 + i * colw
        top = gy1 - (gy1 - gy0) * v / top_v
        top = gy1 - round((gy1 - top) / 20) * 20
        d.rectangle([cx, top, cx + 60, gy1 - 6], fill=BLUE)
        text(d, (cx - 4, gy1 + 22), str(lab), R40, QUIET)
        if i > 0 or s.get('label_first'):
            text(d, (cx - 10, top - 56), f'{v}{unit}', B40)
    ta = n * gap + 0.4
    if s.get('takeaway') and t >= ta:
        if abs(t - ta) < 0.5 / FPS:
            ctx.chime(t0 + ta)
        a = s['takeaway']
        text(d, (X0, 1290), a[0], R48)
        if len(a) > 1:
            highlight(d, (X0, 1360), a[1], B48, pad=10)


def sc_sawtooth(im, d, t, s, t0, ctx):
    title_block(d, s['title'])
    gx0, gy0, gx1, gy1 = X0 + 20, 600, W - 90, 1150
    d.rectangle([gx0, gy1, gx1, gy1 + 5], fill=QUIET)
    reviews, rates, step = [0.0, 0.22, 0.48, 0.80], [6.0, 3.2, 1.7, 0.9], 12
    draw_t = 3.2
    progress = min(1.0, t / draw_t)
    px, prev = gx0, None
    while px < gx0 + (gx1 - gx0) * progress:
        f_ = (px - gx0) / (gx1 - gx0)
        k = max(i for i, r in enumerate(reviews) if r <= f_)
        m = math.exp(-rates[k] * (f_ - reviews[k]) * 3)
        y = gy1 - (gy1 - gy0) * (0.25 + 0.75 * m)
        y = gy1 - round((gy1 - y) / step) * step
        lo, hi = (y, y) if prev is None else (min(prev, y), max(prev, y))
        d.rectangle([px, lo, px + step - 1, hi + step - 1], fill=BLUE)
        prev, px = y, px + step
    for r in reviews[1:]:
        if abs(t - r * draw_t) < 0.5 / FPS:
            ctx.blip(t0 + r * draw_t)
        if progress >= r:
            rx = gx0 + round((gx1 - gx0) * r / step) * step
            d.rectangle([rx, gy1 + 20, rx + 36, gy1 + 56], fill=TEXT)
    text(d, (gx0, gy1 + 80), s.get('axis_label', 'reviews'), R40, QUIET)
    if t >= draw_t + 0.1:
        if s.get('caption'):
            body_block(d, s['caption'], 1310)
        if s.get('notch'):
            notch(d, s['notch'], 760, 1250, 8, t)


def sc_timeline(im, d, t, s, t0, ctx):
    title_block(d, s['title'])
    y = 860
    d.rectangle([X0, y + 20, W - 90, y + 26], fill=BLUE_SOFT)
    xs = [X0, 290, 450, 580, 685, 770, 840, 895]
    gap = 0.3
    for i, x in enumerate(xs):
        if abs(t - i * gap) < 0.5 / FPS:
            ctx.blip(t0 + i * gap)
        if t >= i * gap:
            br = 0.45 + 0.55 * i / (len(xs) - 1)
            c = tuple(int(BG[j] + (BLUE[j] - BG[j]) * br) for j in range(3))
            d.rectangle([x, y, x + 40, y + 46], fill=c)
    ea = len(xs) * gap
    if t >= ea:
        if abs(t - ea) < 0.5 / FPS:
            ctx.chime(t0 + ea)
        ex = W - 90 - 70
        d.rectangle([ex, y - 12, ex + 70, y + 58], fill=AMBER)
        d.rectangle([ex + 12, y, ex + 26, y + 14], fill=(255, 226, 170))
        text(d, (ex - 120, y + 90), s.get('end_label', 'exam day'), B48)
    if s.get('caption') and t >= ea + 0.5:
        body_block(d, s['caption'], 1110)


_SCREENS = None


def screens():
    global _SCREENS
    if _SCREENS is None:
        with open(os.path.join(ASSETS, 'screens', 'screens.json')) as fh:
            _SCREENS = json.load(fh)
    return _SCREENS


_img_cache = {}


def sc_app(im, d, t, s, t0, ctx):
    y_end = title_block(d, s['title'])
    meta = screens()[s['screen']]
    path = os.path.join(ASSETS, 'screens', meta['file'])
    if t >= 0.3:
        if path not in _img_cache:
            _img_cache[path] = Image.open(path).convert('RGB')
        src = _img_cache[path]
        w = 900
        h = round(src.height * w / src.width)
        key = (path, w)
        if key not in _img_cache:
            _img_cache[key] = src.resize((w, h), Image.LANCZOS)
        img = _img_cache[key]
        x, y = (W - w) // 2, max(y_end + 60, 640)
        stepped_frame(d, (x - 14, y - 14, x + w + 14, y + h + 14), DEEP, BLUE_SOFT)
        im.paste(img, (x, y))
        box = meta.get('highlight') if s.get('highlight', True) else None
        if box and t >= 1.6:
            if abs(t - 1.6) < 0.5 / FPS:
                ctx.chime(t0 + 1.6)
            sx, sy, ex, ey = (x + round(box[0] * w / src.width), y + round(box[1] * h / src.height),
                              x + round(box[2] * w / src.width), y + round(box[3] * h / src.height))
            for k in range(6):
                d.rectangle([sx - 12 - k, sy - 10 - k, ex + 12 + k, ey + 10 + k], outline=BLUE)
        if s.get('caption') and t >= 2.2:
            cy = min(y + h + 60, SAFE_BOTTOM - 70)
            body_block(d, s['caption'], cy, QUIET, B48)


def sc_list(im, d, t, s, t0, ctx):
    y = title_block(d, s['title']) + 60
    gap = 0.6
    for i, item in enumerate(s['items']):
        it = 0.3 + i * gap
        if abs(t - it) < 0.5 / FPS:
            ctx.blip(t0 + it)
        if t >= it:
            d.rectangle([X0, y + 18, X0 + 22, y + 40], fill=BLUE)
            lines = item if isinstance(item, list) else [item]
            for j, ln in enumerate(lines):
                text(d, (X0 + 50, y + j * 60), ln, R48)
        y += 60 * (len(item) if isinstance(item, list) else 1) + 50
    if s.get('notch') and t >= 0.3 + len(s['items']) * gap:
        notch(d, s['notch'], 760, max(y + 20, 1150), 9, t)


GOOD = (34, 197, 94)  # #22C55E, right answers only


def sc_quiz(im, d, t, s, t0, ctx):
    """A question with 2-4 answer tiles, drawn like the app's live quiz; the right one turns green."""
    y = title_block(d, s['question']) + 50
    reveal = s.get('reveal_at', 2.4)
    th, gap = 112, 26
    for i, opt in enumerate(s['options']):
        it = 0.3 + i * 0.25
        if abs(t - it) < 0.5 / FPS:
            ctx.blip(t0 + it)
        if t < it:
            continue
        box = (X0, y, W - 90, y + th)
        right = i == s['answer']
        if t >= reveal and right:
            stepped_frame(d, box, GOOD, (120, 230, 160))
            text(d, (X0 + 40, y + 30), opt, B48, BG)
            text(d, (W - 90 - 80, y + 30), 'OK', B48, BG)
        else:
            dim = t >= reveal
            stepped_frame(d, box, CARD if not dim else DEEP, BLUE_SOFT if dim else BLUE)
            text(d, (X0 + 40, y + 30), opt, B48, QUIET if dim else TEXT)
        y += th + gap
    if abs(t - reveal) < 0.5 / FPS:
        ctx.chime(t0 + reveal)
    if s.get('caption') and t >= reveal + 0.4:
        body_block(d, s['caption'], y + 40)


def sc_end(im, d, t, s, t0, ctx):
    cells(d, MARK, X0, 300, 10)
    text(d, (X0 + 150, 318), 'Cramrade', font(True, 84))
    word = s.get('cta', 'PLAN')
    text(d, (X0, 560), 'Comment', H96)
    if t >= 0.5:
        if abs(t - 0.5) < 0.5 / FPS:
            ctx.chime(t0 + 0.5)
        highlight(d, (X0 + H96.getlength('Comment '), 560), word, H96, pad=16)
    text(d, (X0, 700), "and I'll send", B72)
    text(d, (X0, 792), 'you the link.', B72)
    if t >= 1.0:
        text(d, (X0, 1000), 'cramrade.app', B60, BLUE)
        if s.get('note'):  # Minh 2026-10-30: no 18+ line in videos
            text(d, (X0, 1080), s['note'], R48, QUIET)
        notch(d, 'cheer', 720, 1150, 12, t)


SCENES = {'hook': sc_hook, 'statement': sc_statement, 'bars': sc_bars, 'sawtooth': sc_sawtooth,
          'timeline': sc_timeline, 'app': sc_app, 'list': sc_list, 'quiz': sc_quiz, 'end': sc_end}
DEFAULT_DUR = {'hook': 4.2, 'statement': 4.0, 'bars': 5.0, 'sawtooth': 4.4, 'timeline': 4.4, 'app': 4.0,
               'list': 5.0, 'quiz': 5.0, 'end': 4.0}


# ---------------- validation ----------------

def check(script):
    errs = []
    sc = script.get('scenes', [])
    if not sc:
        errs.append('no scenes')
    if sc and sc[-1].get('type') != 'end':
        errs.append('last scene must be type "end"')

    def lim(lines, kind, where):
        for ln in lines or []:
            if len(ln) > LIMITS[kind]:
                errs.append(f'{where}: "{ln}" is {len(ln)} chars, max {LIMITS[kind]} for {kind} text')

    total = 0
    for i, s in enumerate(sc):
        t = s.get('type')
        w = f'scene {i + 1} ({t})'
        if t not in SCENES:
            errs.append(f'{w}: unknown type'); continue
        total += s.get('dur', DEFAULT_DUR[t])
        if t in ('hook', 'statement'):
            lim(s.get('lines'), 'headline', w)
            if not 1 <= len(s.get('lines', [])) <= 5:
                errs.append(f'{w}: 1-5 lines')
            lim(s.get('source') or s.get('caption'), 'body', w)
        if t in ('bars', 'sawtooth', 'timeline', 'app', 'list'):
            lim(s.get('title'), 'title', w)
            if len(s.get('title', [])) > 3:
                errs.append(f'{w}: title max 3 lines')
        if t in ('bars', 'sawtooth', 'timeline'):
            lim(s.get('caption'), 'body', w)
        if t == 'bars':
            if not 2 <= len(s.get('bars', [])) <= 6:
                errs.append(f'{w}: 2-6 bars')
            lim(s.get('takeaway'), 'body', w)
        if t == 'app' and s.get('screen') not in screens():
            errs.append(f'{w}: unknown screen "{s.get("screen")}", have {sorted(screens())}')
        if t == 'quiz':
            lim(s.get('question'), 'title', w)
            opts = s.get('options', [])
            if not 2 <= len(opts) <= 4:
                errs.append(f'{w}: 2-4 options')
            for o in opts:
                if len(o) > LIMITS['body'] - 4:
                    errs.append(f'{w}: option "{o}" too long (max {LIMITS["body"] - 4})')
            if not isinstance(s.get('answer'), int) or not 0 <= s['answer'] < len(opts):
                errs.append(f'{w}: "answer" must be the index of the right option')
            lim(s.get('caption'), 'body', w)
        if t == 'list':
            for it in s.get('items', []):
                lim(it if isinstance(it, list) else [it], 'body', w)
        if s.get('notch') and s['notch'] not in NOTCH_POSES:
            errs.append(f'{w}: notch pose must be one of {NOTCH_POSES}')
    if not 12 <= total <= 45:
        errs.append(f'total length {total:.1f}s, keep it between 12 and 45 s')
    return errs, total


# ---------------- render ----------------

def timeline(script):
    out, t = [], 0.0
    for s in script['scenes']:
        dur = s.get('dur', DEFAULT_DUR[s['type']])
        out.append((t, t + dur, s))
        t += dur
    return out, t


def frame(tl, T, ctx):
    for a, b, s in tl:
        if a <= T < b:
            im = BG_IMG.copy()
            SCENES[s['type']](im, ImageDraw.Draw(im), T - a, s, a, ctx)
            return im
    return BG_IMG.copy()


SR = 44100
NOTES = {'F2': 87.31, 'G2': 98.0, 'A2': 110.0, 'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'G3': 196.0,
         'A3': 220.0, 'B3': 246.94, 'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.0}
PROGS = [
    [('A2', 'C4', 'E4'), ('F2', 'A3', 'C4'), ('C3', 'E4', 'G4'), ('G2', 'D4', 'G4')],
    [('C3', 'E4', 'G4'), ('A2', 'C4', 'E4'), ('F2', 'A3', 'C4'), ('G2', 'B3', 'D4')],
    [('D3', 'F4', 'A3'), ('A2', 'C4', 'E4'), ('C3', 'E4', 'G4'), ('G2', 'B3', 'D4')],
]


def _sq(freq, dur, vol, duty=0.5):
    n = int(SR * dur)
    tt = np.arange(n) / SR
    return np.where((tt * freq) % 1 < duty, 1.0, -1.0) * vol * np.minimum(1, np.linspace(1, 0, n) * 4)


def audio(path, dur, ctx, seed=0):
    total = np.zeros(int(SR * (dur + 0.5)))

    def add(i, s):
        if 0 <= i < len(total):
            s = s[:len(total) - i]
            total[i:i + len(s)] += s

    bpm = 104 + (seed % 3) * 8
    beat = 60 / bpm
    prog = PROGS[seed % len(PROGS)]
    t, bar = 0.0, 0
    while t < dur:
        bass, n1, n2 = prog[bar % 4]
        for _ in range(4):
            add(int(t * SR), _sq(NOTES[bass], beat * 0.9, 0.05, 0.25))
            for k, nn in enumerate((n1, n2, n1, n2)):
                add(int((t + k * beat / 4) * SR), _sq(NOTES[nn], beat / 4 * 0.8, 0.025, 0.125))
            t += beat
        bar += 1
    for bt in ctx.blips:
        add(int(bt * SR), _sq(1318.5, 0.05, 0.05))
    for ct in ctx.chimes:
        for k, f in enumerate((783.99, 987.77, 1318.5)):
            add(int((ct + k * 0.06) * SR), _sq(f, 0.09, 0.05))
    fade = int(SR * 1.2)
    total[-fade:] *= np.linspace(1, 0, fade)
    with wave.open(path, 'w') as wv:
        wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
        wv.writeframes((np.clip(total, -1, 1) * 32767).astype(np.int16).tobytes())


def render(script, out, sheet=None):
    tl, dur = timeline(script)
    ctx = Ctx()
    base = os.path.splitext(out)[0]
    silent, wav = base + '.silent.mp4', base + '.wav'
    proc = subprocess.Popen([FFMPEG, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                             '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                             '-crf', '18', '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)):
        proc.stdin.write(frame(tl, i / FPS, ctx).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit('ffmpeg video encode failed')
    audio(wav, dur, ctx, seed=script.get('seed', 0))
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac',
                    '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], check=True)
    os.remove(silent); os.remove(wav)
    if sheet:
        contact_sheet(tl, sheet)
    return dur


def contact_sheet(tl, path):
    """One still per scene, taken near the end of the scene (everything revealed)."""
    ctx = Ctx(); ctx.record = False
    thumbs = []
    for a, b, s in tl:
        im = frame(tl, b - 0.2, ctx).resize((360, 640))
        thumbs.append(im)
    sheet = Image.new('RGB', (len(thumbs) * 370 - 10, 640), (60, 60, 60))
    for i, im in enumerate(thumbs):
        sheet.paste(im, (i * 370, 0))
    sheet.save(path)


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    with open(argv[1]) as fh:
        script = json.load(fh)
    errs, dur = check(script)
    if errs:
        print('SCRIPT ERRORS:'); [print(' -', e) for e in errs]; return 1
    if '--check' in argv:
        print(f'ok, {dur:.1f}s'); return 0
    out = argv[2]
    sheet = argv[argv.index('--sheet') + 1] if '--sheet' in argv else None
    d = render(script, out, sheet)
    print(f'rendered {out} ({d:.1f}s)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
