"""Engine v2: Notch in a dark pixel line-art room, voiceover, word-by-word captions, lo-fi bed.

    python engine/v2/notch_v2.py SHOTS.json OUT.mp4 [--sheet SHEET.png]

SHOTS.json: {"voice": "path.mp3", "words": "path.json" (list of {text,start,end}),
             "emphasis": {"word": "blue"|"amber"}, "shots": [{"t": start_s, "set": ..., "pose": ...,
             "props": [...], "cam": {"z": [z0, z1], "c": [x, y]}}, ...], "end_t": seconds}

Everything is drawn on a 270x480 pixel canvas and scaled 4x with nearest-neighbour, so the whole frame
reads as pixel art. Captions are drawn at full resolution on top. Colours follow the brand rule:
the room is white line-art on near-black; only Notch (blue) and exam day (amber) carry colour.
"""
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
import render as R  # noqa: E402  (sprites, fonts, ffmpeg path)

PW, PH, S = 270, 480, 4
W, H, FPS = PW * S, PH * S, 30
BG = (6, 8, 18)
LINE = (138, 146, 180)
LINE_DIM = (60, 66, 96)
LINE_HI = (205, 210, 232)
BLUE, BLUE_SOFT, AMBER, TEXT = R.BLUE, R.BLUE_SOFT, R.AMBER, R.TEXT
GOOD = (34, 197, 94)

# ---------------- Notch: extra poses on top of the app's sprite ----------------
R._ARMS.update({
    'sad':   [(2, 12), (2, 13), (2, 14), (17, 12), (17, 13), (17, 14)],
    'study': [(3, 13), (4, 14), (5, 15), (16, 13), (15, 14), (14, 15)],
    'no':    [(2, 9), (1, 8), (1, 7), (17, 9), (18, 8), (18, 7)],
    'wake':  [(2, 12), (2, 13), (2, 14), (17, 10), (18, 9), (18, 8), (19, 7)],
})
R._FACE.update({
    'sad':   [(8, 9), (11, 9), (8, 12), (9, 11), (10, 11), (11, 12)],
    'study': [(8, 10), (9, 10), (11, 10), (12, 10), (9, 12), (10, 12)],
    'no':    [(8, 8), (8, 9), (11, 8), (11, 9), (9, 12), (10, 12)],
    'wake':  [(8, 9), (9, 9), (11, 9), (12, 9), (9, 12), (10, 12), (9, 13), (10, 13)],
})
POSES = {p: R._notch_cells(p) for p in R._ARMS}
BLINK = {p: [c for c in POSES[p] if not (c[2] == TEXT and c[1] <= 9)] +
         [(x, 9, TEXT) for x, y, col in POSES[p] if col == TEXT and y in (7, 8) and x in (8, 9, 11, 12)]
         for p in POSES}


def draw_notch(img, pose, cx, by, cell=3, t=0.0, blink=False, squash=0.0):
    """Notch centred at cx with feet at by, on the pixel canvas."""
    d = ImageDraw.Draw(img)
    cs = (BLINK if blink else POSES)[pose]
    sy = 1.0 - squash
    bob = int(round(math.sin(t * 2 * math.pi * 0.9) * 1.2))
    for x, y, col in cs:
        px = cx + (x - 10) * cell
        py = by - int((20 - y) * cell * sy) + bob
        d.rectangle([px, py, px + cell - 1, py + max(1, int(cell * sy)) - 1], fill=col)


# ---------------- pixel line-art helpers ----------------

def rect(d, box, col=LINE, w=1):
    d.rectangle(box, outline=col, width=w)


def set_room(d, t, morning=False, oy=-52):
    def Y(v):
        return v + oy
    d.line([0, Y(372), PW, Y(372)], fill=LINE, width=1)
    rect(d, [24, Y(60), 104, Y(150)])
    d.line([64, Y(60), 64, Y(150)], fill=LINE_DIM)
    d.line([24, Y(105), 104, Y(105)], fill=LINE_DIM)
    if morning:
        for a in range(0, 360, 45):
            r1, r2 = 13, 18
            d.line([84 + math.cos(math.radians(a)) * r1, Y(82) + math.sin(math.radians(a)) * r1,
                    84 + math.cos(math.radians(a)) * r2, Y(82) + math.sin(math.radians(a)) * r2], fill=LINE_HI)
        d.ellipse([76, Y(74), 92, Y(90)], outline=LINE_HI)
    else:
        d.ellipse([78, Y(70), 94, Y(86)], outline=LINE_HI)
        d.ellipse([83, Y(68), 99, Y(84)], fill=BG)
        for sx, sy in ((36, 74), (48, 128), (90, 132), (40, 96)):
            d.point((sx, Y(sy)), fill=LINE_HI)
    d.line([160, Y(120), 250, Y(120)], fill=LINE)
    xs = 164
    for wd, ht in ((8, 26), (6, 20), (10, 30), (7, 24), (9, 28), (6, 18)):
        rect(d, [xs, Y(120 - ht), xs + wd, Y(120)])
        xs += wd + 2
    d.line([110, Y(300), 262, Y(300)], fill=LINE, width=2)
    d.line([118, Y(300), 118, Y(372)], fill=LINE)
    d.line([254, Y(300), 254, Y(372)], fill=LINE)
    d.line([240, Y(300), 240, Y(262)], fill=LINE)
    d.line([240, Y(262), 228, Y(248)], fill=LINE)
    d.polygon([(220, Y(244)), (236, Y(244)), (242, Y(256)), (214, Y(256))], outline=LINE_HI)
    rect(d, [150, Y(160), 210, Y(210)])
    d.line([150, Y(170), 210, Y(170)], fill=LINE)
    for i in range(1, 4):
        d.line([150 + i * 15, Y(170), 150 + i * 15, Y(210)], fill=LINE_DIM)
    d.line([150, Y(190), 210, Y(190)], fill=LINE_DIM)


def prop_books(d, x, y):
    for i, (wd, col) in enumerate(((44, LINE_HI), (38, LINE), (46, LINE_HI))):
        rect(d, [x - wd // 2, y - 8 * (i + 1), x + wd // 2, y - 8 * i], col)


def prop_clock(d, x, y, t, spin=False):
    d.ellipse([x - 16, y - 16, x + 16, y + 16], outline=LINE_HI)
    a = (t * 540 if spin else 60) % 360
    d.line([x, y, x + 12 * math.sin(math.radians(a)), y - 12 * math.cos(math.radians(a))], fill=BLUE)
    d.line([x, y, x + 7 * math.sin(math.radians(a / 12 + 90)), y - 7 * math.cos(math.radians(a / 12 + 90))], fill=LINE_HI)


def prop_bubble(d, x, y, t, fade=0.0, glow=False):
    """Thought bubble with note lines that dissolve as fade goes 0 -> 1."""
    d.ellipse([x - 6, y + 46, x + 2, y + 54], outline=LINE)
    d.ellipse([x + 4, y + 34, x + 16, y + 46], outline=LINE)
    rect(d, [x - 10, y - 46, x + 100, y + 30], LINE_HI)
    rng = np.random.default_rng(7)
    for row in range(5):
        for col in range(18):
            if rng.random() < fade * 1.15:
                continue
            px, py = x + 2 + col * 5, y - 36 + row * 13
            d.rectangle([px, py, px + 3, py + 2], fill=(BLUE if glow else LINE))


def prop_brain(d, x, y, t, lit=False, leak=0.0):
    col = BLUE if lit else LINE_HI
    d.ellipse([x - 34, y - 26, x + 34, y + 26], outline=col)
    d.line([x, y - 26, x, y + 26], fill=col)
    for k in range(-1, 2):
        d.arc([x - 28, y - 10 + k * 12, x - 6, y + 4 + k * 12], 200, 340, fill=col)
        d.arc([x + 6, y - 10 + k * 12, x + 28, y + 4 + k * 12], 200, 340, fill=col)
    if leak > 0:  # little note squares floating out the top and fading
        for i in range(5):
            ph = (leak * 1.4 + i * 0.21) % 1.0
            px = x - 26 + i * 13
            py = y - 30 - ph * 70
            shade = int(205 * (1 - ph))
            d.rectangle([px, py, px + 5, py + 4], outline=(shade, shade, min(255, shade + 20)))


def prop_calendar(d, t, ticks=(), exam=False, glow3=False):
    """Big 7x2 calendar card. ticks = day indices (0-based) with a blue tick; day 13 = exam."""
    x0, y0, cw, ch = 30, 96, 30, 42
    rect(d, [x0 - 6, y0 - 34, x0 + cw * 7 + 6, y0 + ch * 2 + 8], LINE_HI)
    for i in range(14):
        cx, cy = x0 + (i % 7) * cw, y0 + (i // 7) * ch
        rect(d, [cx, cy, cx + cw - 3, cy + ch - 3], LINE_DIM)
        if i == 13:
            d.rectangle([cx + 4, cy + 8, cx + cw - 7, cy + ch - 7], fill=AMBER if exam else LINE_DIM)
    for i in ticks:
        cx, cy = x0 + (i % 7) * cw, y0 + (i // 7) * ch
        colr = BLUE
        if glow3:
            colr = (170, 190, 255) if int(t * 6) % 2 else BLUE
        d.line([cx + 7, cy + 18, cx + 12, cy + 24, cx + 22, cy + 8], fill=colr, width=2)
        d.text((cx + 4, cy + 27), '10m', font=pix_font(8), fill=LINE_HI)


SETS = {}
_pf = {}


def pix_font(size):
    if size not in _pf:
        _pf[size] = ImageFont.truetype(os.path.join(ENGINE, 'assets', 'fonts', 'Monocraft.ttf'), size)
    return _pf[size]



def shot_desk_night(d, img, t, lt, s):
    set_room(d, t)
    prop_books(d, 150, 248)
    prop_clock(d, 232, 150, lt, spin=True)
    draw_notch(img, 'study', 186, 248, 4, t)


def shot_morning(d, img, t, lt, s):
    set_room(d, t, morning=True)
    prop_books(d, 150, 248)
    draw_notch(img, 'wake', 186, 248, 4, t, squash=max(0, 0.15 - lt * 0.4))


def shot_gone(d, img, t, lt, s):
    prop_bubble(d, 82, 100, t, fade=min(1, max(0, (lt - 0.25) / 1.0)))
    draw_notch(img, 'sad', 135, 318, 5, t)


def shot_not_you(d, img, t, lt, s):
    d.line([0, 320, PW, 320], fill=LINE)
    draw_notch(img, 'no', 135, 320, 6, t)


def shot_brain_leak(d, img, t, lt, s):
    prop_brain(d, 150, 130, t, leak=lt / 3.0)
    draw_notch(img, 'point', 82, 318, 5, t)


def shot_fix(d, img, t, lt, s):
    d.line([0, 320, PW, 320], fill=LINE)
    draw_notch(img, 'cheer', 135, 320, 6, t, squash=max(0, 0.2 - lt * 0.6))


def _cal(ticks, exam=False, glow3=False, pose='point'):
    def f(d, img, t, lt, s):
        prop_calendar(d, t, ticks, exam, glow3)
        draw_notch(img, pose, 200, 318, 4, t)
    return f


def shot_sticks(d, img, t, lt, s):
    prop_calendar(d, t, (0, 2, 7), glow3=True)
    prop_brain(d, 82, 275, t, lit=True)
    draw_notch(img, 'cheer', 205, 318, 4, t)


def shot_exam(d, img, t, lt, s):
    prop_calendar(d, t, (0, 2, 7), exam=True)
    d.text((196, 196), 'EXAM', font=pix_font(10), fill=AMBER)
    draw_notch(img, 'point', 120, 318, 4, t)


def shot_end(d, img, t, lt, s):
    draw_notch(img, 'hello', 135, 250, 6, t)


SETS.update({'desk_night': shot_desk_night, 'morning': shot_morning, 'gone': shot_gone,
             'not_you': shot_not_you, 'brain_leak': shot_brain_leak, 'fix': shot_fix,
             'cal_1': _cal((0,)), 'cal_2': _cal((0, 2)), 'cal_3': _cal((0, 2, 7)),
             'sticks': shot_sticks, 'exam': shot_exam, 'end': shot_end})


# ---------------- captions ----------------
_font_cache = {}


def cap_font(size):
    if size not in _font_cache:
        _font_cache[size] = ImageFont.truetype(os.path.join(ENGINE, 'assets', 'fonts', 'Monocraft-Bold.ttf'), size)
    return _font_cache[size]


def clean(w):
    return w.strip()


def draw_caption(im, word, age, colour, y=1410):
    pop = 1.0 + 0.18 * max(0.0, 1.0 - age / 0.09)
    size = int(132 * pop)
    f = cap_font(size)
    while f.getlength(word) > W - 120 and size > 70:
        size -= 6
        f = cap_font(size)
    d = ImageDraw.Draw(im)
    wlen = f.getlength(word)
    d.text(((W - wlen) / 2, y - size / 2), word, font=f, fill=colour, stroke_width=12, stroke_fill=(0, 0, 0))


# ---------------- audio: soft lo-fi bed + whooshes ----------------

def lofi(dur, sr=44100, seed=3):
    rng = np.random.default_rng(seed)
    n = int(dur * sr)
    out = np.zeros(n)
    bpm = 78
    beat = 60 / bpm
    chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]  # Fmaj7 Em7 Dm7 Cmaj7

    def hz(m):
        return 440 * 2 ** ((m - 69) / 12)

    def add(i, sig):
        j = min(n, i + len(sig))
        if j > i:
            out[i:j] += sig[:j - i]

    bar = beat * 4
    t_bar = np.arange(int(bar * sr)) / sr
    env = np.exp(-t_bar * 1.1) * (1 - np.exp(-t_bar * 40))
    for b in range(int(dur / bar) + 1):
        ch = chords[b % 4]
        sig = np.zeros_like(t_bar)
        for m in ch:
            f = hz(m)
            sig += (np.sin(2 * np.pi * f * t_bar) + 0.25 * np.sin(4 * np.pi * f * t_bar) + 0.08 * np.sin(6 * np.pi * f * t_bar))
        sig *= env * (1 + 0.08 * np.sin(2 * np.pi * 4.5 * t_bar)) * 0.05
        add(int(b * bar * sr), sig)
        bass = np.sin(2 * np.pi * hz(ch[0] - 12) * t_bar) * np.exp(-t_bar * 0.9) * 0.08
        add(int(b * bar * sr), bass)
    tk = np.arange(int(0.25 * sr)) / sr
    kick = np.sin(2 * np.pi * (55 + 70 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 14) * 0.22
    hat = rng.normal(0, 1, int(0.05 * sr)) * np.exp(-np.arange(int(0.05 * sr)) / sr * 90) * 0.025
    snare = rng.normal(0, 1, int(0.18 * sr)) * np.exp(-np.arange(int(0.18 * sr)) / sr * 22) * 0.06
    nb = int(dur / beat) + 1
    for k in range(nb):
        i = int(k * beat * sr)
        if k % 4 in (0,) or (k % 8 == 6):
            add(i, kick)
        if k % 4 == 2:
            add(i, snare)
        add(i + int(beat * 0.5 * sr), hat)
        add(i, hat * 0.6)
    # vinyl crackle
    crack = (rng.random(n) < 0.0007) * rng.normal(0, 0.05, n)
    out += crack + rng.normal(0, 0.0025, n)
    # gentle low-pass
    k = 9
    out = np.convolve(out, np.ones(k) / k, mode='same')
    return out


def whoosh(sr=44100, dur=0.35, seed=1):
    rng = np.random.default_rng(seed)
    n = int(dur * sr)
    t = np.arange(n) / sr
    x = rng.normal(0, 1, n)
    x = np.convolve(x, np.ones(25) / 25, mode='same')
    envl = np.sin(np.pi * t / dur) ** 2
    return x * envl * 0.25


def build_audio(voice_path, shots, total, path, sr=44100):
    tmp = path + '.voice.wav'
    subprocess.run([R.FFMPEG, '-y', '-loglevel', 'error', '-i', voice_path, '-ac', '1', '-ar', str(sr), tmp], check=True)
    with wave.open(tmp) as wf:
        v = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    os.remove(tmp)
    n = int(total * sr)
    voice = np.zeros(n)
    voice[:min(n, len(v))] = v[:n]
    bed = lofi(total, sr)[:n]
    # duck the bed under the voice
    envv = np.convolve(np.abs(voice), np.ones(2205) / 2205, mode='same')
    duck = 1.0 - 0.55 * np.clip(envv / (envv.max() + 1e-9) * 3, 0, 1)
    mix = voice * 0.95 + bed * duck * 0.55
    for s in shots[1:]:
        i = int(max(0, s['t'] - 0.12) * sr)
        wsh = whoosh(sr, seed=int(s['t'] * 10))
        j = min(n, i + len(wsh))
        mix[i:j] += wsh[:j - i] * 0.35
    fade = int(0.6 * sr)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = mix / max(1e-9, np.abs(mix).max()) * 0.92
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes((mix * 32767).astype(np.int16).tobytes())


# ---------------- frame ----------------

def ease(x):
    return x * x * (3 - 2 * x)


def frame(spec, words, t):
    shots = spec['shots']
    idx = max(i for i, s in enumerate(shots) if s['t'] <= t)
    s = shots[idx]
    t_end = shots[idx + 1]['t'] if idx + 1 < len(shots) else spec['end_t']
    lt = t - s['t']
    canvas = Image.new('RGB', (PW, PH), BG)
    d = ImageDraw.Draw(canvas)
    SETS[s['set']](d, canvas, t, lt, s)
    # camera: zoom z0->z1 around centre c, nearest-neighbour so pixels stay square
    z0, z1 = s.get('cam', {}).get('z', [1.0, 1.0])
    cx, cy = s.get('cam', {}).get('c', [PW / 2, PH / 2])
    k = ease(min(1.0, lt / max(0.3, t_end - s['t'])))
    z = z0 + (z1 - z0) * k
    if lt < 0.12:  # punch-in on every cut
        z *= 1.0 + 0.06 * (1 - lt / 0.12)
    cw, ch = PW / z, PH / z
    x0 = min(max(0, cx - cw / 2), PW - cw)
    y0 = min(max(0, cy - ch / 2), PH - ch)
    view = canvas.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    big = view.resize((W, H), Image.NEAREST)
    # glow: blur the bright blue pixels and add them back
    arr = np.asarray(big).astype(np.int16)
    mask = (arr[:, :, 2] > 200) & (arr[:, :, 0] < 160)
    if mask.any():
        small = Image.fromarray((mask * 255).astype(np.uint8)).resize((W // 8, H // 8), Image.BILINEAR)
        glow = np.asarray(small.filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BILINEAR)).astype(np.float32) / 255
        arr = np.clip(arr + (glow[:, :, None] * np.array([40, 60, 160]) * 0.9), 0, 255)
    im = Image.fromarray(arr.astype(np.uint8))
    # caption
    spoken = [w for w in words if not w['text'].startswith('[')]
    cur = [w for w in spoken if w['start'] - 0.04 <= t < (w['end'] + 0.25)]
    if cur and s['set'] != 'end':
        w = cur[-1]
        txt = clean(w['text'])
        key = txt.strip('.,?!').lower()
        col = {'blue': BLUE, 'amber': AMBER}.get(spec.get('emphasis', {}).get(key), TEXT)
        draw_caption(im, txt, t - w['start'], col)
    if s['set'] == 'end':
        d2 = ImageDraw.Draw(im)
        f1, f2, f3 = cap_font(104), cap_font(56), cap_font(40)
        a = min(1.0, lt / 0.25)
        y = 1200
        word = 'PLAN'
        t1 = 'Comment '
        total = f1.getlength(t1 + word)
        x = (W - total) / 2
        d2.text((x, y), t1, font=f1, fill=TEXT, stroke_width=10, stroke_fill=(0, 0, 0))
        px = x + f1.getlength(t1)
        if a >= 1.0:
            d2.rectangle([px - 14, y - 6, px + f1.getlength(word) + 14, y + 120], fill=BLUE)
        d2.text((px, y), word, font=f1, fill=(6, 8, 18) if a >= 1.0 else TEXT)
        sub = 'cramrade.app'
        d2.text(((W - f2.getlength(sub)) / 2, 1360), sub, font=f2, fill=BLUE)
        note = 'Beta, for students 18+'
        d2.text(((W - f3.getlength(note)) / 2, 1440), note, font=f3, fill=(163, 171, 209))
    return im


def render(spec_path, out, sheet=None):
    spec = json.load(open(spec_path))
    base = os.path.dirname(os.path.abspath(spec_path))
    words = json.load(open(os.path.join(base, spec['words'])))
    total = spec['end_t']
    nframes = int(total * FPS)
    silent = out + '.silent.mp4'
    proc = subprocess.Popen([R.FFMPEG, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                             '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                             '-crf', '18', '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    stills = []
    marks = [s['t'] + 0.6 for s in spec['shots']]
    for i in range(nframes):
        t = i / FPS
        im = frame(spec, words, t)
        proc.stdin.write(im.tobytes())
        if marks and t >= marks[0]:
            stills.append(im.resize((270, 480)))
            marks.pop(0)
    proc.stdin.close()
    proc.wait()
    wav = out + '.wav'
    build_audio(os.path.join(base, spec['voice']), spec['shots'], total, wav)
    subprocess.run([R.FFMPEG, '-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-c:v', 'copy',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-shortest',
                    '-movflags', '+faststart', out], check=True)
    os.remove(silent)
    os.remove(wav)
    if sheet and stills:
        cols = 6
        rows = math.ceil(len(stills) / cols)
        sh = Image.new('RGB', (cols * 280, rows * 490), (40, 40, 40))
        for k, st in enumerate(stills):
            sh.paste(st, ((k % cols) * 280 + 5, (k // cols) * 490 + 5))
        sh.save(sheet)
    print(f'rendered {out} ({total:.1f}s)')


if __name__ == '__main__':
    a = sys.argv[1:]
    sheet = a[a.index('--sheet') + 1] if '--sheet' in a else None
    render(a[0], a[1], sheet)
