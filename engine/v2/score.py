"""Original scores for the "Notch explains" launch videos, composed in code (no samples, royalty-free, ours).

    python engine/v2/score.py OUTDIR [--sfx DIR]     writes score-01-recall.mp3, score-02-spacing.mp3, score-03-group.mp3

Each cue is written to the exact length of its video and its changes land on the video's cuts
(times taken from samples/launch/*.json), so the music "acts out" the story:
  01 recall   E minor, marimba + felt piano. Notes dissolve on "that feeling is lying", a lift on the 61% reveal,
              a soft groove for "the workout", a dip for "just watching", bells on the app highlight.
  02 spacing  D major, celesta bells over a quiet clock. During "the gaps shrink" the bells ring on the same
              review days the app would pick (Cramrade's ~1/5-of-days-left rule), so you hear the gaps close in.
  03 group    F major, pizzicato bass + marimba. Sleepy until "Flip it", then a light groove where two marimbas
              answer each other (quizzing), right/wrong blips synced to the answer list, a small podium fanfare.
Optional --sfx DIR adds ElevenLabs sound-effect textures (pencil.mp3 for 01, library.mp3 for 03) very quietly.

Study-friendly rules kept: no lyrics, soft attacks, little above 7 kHz, narrow dynamics, sits under a voice.
"""
import os
import subprocess
import sys
import wave

import numpy as np
from scipy.signal import butter, sosfilt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import music as M  # noqa: E402  felt_piano, bell, pad, sub, Track, hz, write

SR = M.SR
hz = M.hz
rng = np.random.default_rng(21)


# ---------------- instruments ----------------

def marimba(f, vel=0.5, dur=1.2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 5.5) + 0.35 * np.sin(2 * np.pi * f * 4.0 * t) * np.exp(-t * 18)
    s += 0.08 * np.sin(2 * np.pi * f * 9.9 * t) * np.exp(-t * 45)
    return s * (1 - np.exp(-t * 600)) * vel * 0.16


def pluck(f, vel=0.5, dur=1.0, bright=0.5):
    """Karplus-Strong string (pizzicato / harp)."""
    n = int(dur * SR)
    p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    out = np.zeros(n)
    a = 0.5 + 0.49 * bright
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = a * buf[i % p] + (1 - a) * buf[(i + 1) % p]
    out *= np.exp(-np.arange(n) / SR * 2.5)
    out = sosfilt(butter(2, min(3000, f * 5), 'low', fs=SR, output='sos'), out)  # warm, not twangy
    return out * vel * 0.3


def celesta(f, vel=0.5):
    n = int(2.6 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2) + 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 4)
    s += 0.06 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 7)
    return s * (1 - np.exp(-t * 900)) * vel * 0.13


def kick(vel=0.5):
    t = np.arange(int(0.35 * SR)) / SR
    return np.sin(2 * np.pi * (48 + 60 * np.exp(-t * 28)) * t) * np.exp(-t * 11) * vel * 0.3


def shaker(vel=0.4, dur=0.09):
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    x = sosfilt(butter(2, [3500, 7000], 'band', fs=SR, output='sos'), x)
    env = np.sin(np.pi * np.arange(n) / n) ** 2
    return x * env * vel * 0.06


def tick(vel=0.4):
    n = int(0.05 * SR)
    x = rng.normal(0, 1, n) * np.exp(-np.arange(n) / SR * 160)
    x = sosfilt(butter(2, [1800, 4200], 'band', fs=SR, output='sos'), x)
    return x * vel * 0.25


def thud(f=110, vel=0.5):
    """Soft 'wrong answer' bump: low, short, not harsh."""
    t = np.arange(int(0.3 * SR)) / SR
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 14) * vel * 0.15


def riser(t0f, t1f, dur, vel=0.4):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = np.geomspace(t0f, t1f, n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = rng.normal(0, 1, n)
    x = sosfilt(butter(2, [800, 5000], 'band', fs=SR, output='sos'), x)
    return (0.5 * np.sin(ph) + 0.15 * x) * (t / dur) ** 2 * vel * 0.12


def tape_stop(sig, dur):
    """Slow a short audio buffer to a halt (pitch drops) over dur seconds."""
    n = int(dur * SR)
    speed = np.linspace(1.0, 0.0, n) ** 1.3
    pos = np.cumsum(speed)
    pos = pos[pos < len(sig) - 1]
    return np.interp(pos, np.arange(len(sig)), sig) * np.linspace(1, 0, len(pos))


def chord_pad(tr, t0, dur, notes, vel=1.0, pan=0.0):
    tr.add(t0, M.pad([hz(m) for m in notes], dur) * vel, pan)


def arp(tr, t0, t1, notes, step, inst, vel=0.45, pan_span=0.4, drop=None):
    """Repeat an arpeggio from t0 to t1. drop(t) -> probability a note is skipped (for dissolves)."""
    t, i = t0, 0
    while t < t1 - 0.05:
        if drop is None or rng.random() > drop(t):
            m = notes[i % len(notes)]
            tr.add(t + rng.normal(0, 0.006), inst(hz(m), vel * (0.85 + 0.3 * rng.random())),
                   pan=-pan_span / 2 + pan_span * ((i % len(notes)) / max(1, len(notes) - 1)))
        t += step
        i += 1


def load_sfx(path, dur):
    if not path or not os.path.exists(path):
        return None
    tmp = path + '.tmp.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), tmp], check=True)
    with wave.open(tmp) as wf:
        x = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    os.remove(tmp)
    # ElevenLabs returns short clips (~2 s): loop them with 0.4 s crossfades up to dur
    need, xf = int(dur * SR), int(0.4 * SR)
    out = x.copy()
    while len(out) < need:
        seg = x if rng.random() > 0.5 else x[::-1]
        ramp = np.linspace(0, 1, xf)
        out[-xf:] = out[-xf:] * (1 - ramp) + seg[:xf] * ramp
        out = np.concatenate([out, seg[xf:]])
    x = out[:need]
    x = sosfilt(butter(2, [150, 6000], 'band', fs=SR, output='sos'), x)
    return x / (np.abs(x).max() + 1e-9)


# ---------------- cue 01: recall (32.4 s) ----------------

def cue_recall(sfx_dir=None):
    T = 32.4
    tr = M.Track(T)
    b = 60 / 84
    E = 40  # E2
    # 0-3.7 re-reading, familiar: marimba Em9 arpeggio, warm pad
    chord_pad(tr, 0.0, 3.6, [52, 55, 59, 62])
    tr.add(0.0, M.sub(hz(E), 3.6))
    arp(tr, 0.0, 3.7, [64, 67, 71, 74, 71, 67], b / 2, marimba, 0.42)
    # 3.7-6.1 "that feeling is lying to you": same figure, notes fall out, darker C
    chord_pad(tr, 3.7, 2.3, [48, 52, 55, 59], 0.8)
    arp(tr, 3.7, 6.1, [64, 67, 71, 74, 71, 67], b / 2, marimba, 0.38, drop=lambda t: min(0.9, (t - 3.7) / 2.2))
    # 6.1-12.3 the study, 40%: sparse, held Am9 -> Cmaj7, single felt-piano notes
    chord_pad(tr, 6.1, 3.0, [45, 52, 55, 59, 62], 0.9)
    chord_pad(tr, 9.2, 3.0, [48, 52, 55, 59, 64], 0.9)
    tr.add(6.1, M.sub(hz(33), 3.0))
    tr.add(9.2, M.sub(hz(36), 3.0))
    for k, m in enumerate([69, 67, 64, 67, 71, 69]):
        tr.add(6.3 + k * 1.0, M.felt_piano(hz(m), 0.9, 0.38, rng), 0.1)
    # 12.3 the 61% reveal: lift to G major, bell, plucked arpeggio climbing
    tr.add(12.3, M.bell(hz(79), 0.45), 0.25)
    chord_pad(tr, 12.3, 4.0, [55, 59, 62, 66])
    tr.add(12.3, M.sub(hz(43), 4.0))
    arp(tr, 12.3, 16.4, [67, 71, 74, 78, 79, 78, 74, 71], b / 2, marimba, 0.48)
    # 16.5-21.5 "the workout" (groove) with a dip on "just watching" (19.1-21.5)
    prog = [([55, 59, 62], 43), ([54, 57, 62], 42), ([52, 55, 59], 40), ([48, 52, 55], 36)]
    for k in range(int((29.2 - 16.5) / (2 * b)) + 1):
        t0 = 16.5 + k * 2 * b
        if t0 >= 29.2:
            break
        notes, root = prog[k % 4]
        chord_pad(tr, t0, 2 * b, notes, 0.75)
        watching = 19.1 <= t0 < 21.5
        if not watching:
            tr.add(t0, kick(0.45))
            tr.add(t0 + b, kick(0.3))
            tr.add(t0, M.sub(hz(root), 2 * b * 0.9))
        for e in range(4):
            if not watching:
                tr.add(t0 + e * b / 2, shaker(0.18 if e % 2 else 0.1), 0.3)
        figure = [notes[0] + 12, notes[2] + 12, notes[1] + 12, notes[2] + 12]
        for e, m in enumerate(figure):
            tr.add(t0 + e * b / 2, marimba(hz(m), 0.3 if watching else 0.45), -0.2)
    # 24.05-29.2 the app: shimmer bells on the highlight (26.75 + 0.5 s box)
    for t0, m in ((24.1, 83), (26.75 + 0.55, 86), (27.25 + 0.55, 83)):
        tr.add(t0, M.bell(hz(m), 0.35), 0.3)
    # 29.2 end: resolve, Cramrade climb motif in G (G A B D) + summit bell
    chord_pad(tr, 29.2, 3.0, [55, 59, 62, 69], 1.1)
    tr.add(29.2, M.sub(hz(43), 3.0))
    for i, m in enumerate([67, 69, 71, 74]):
        tr.add(29.25 + i * 0.32, M.felt_piano(hz(m), 1.0, 0.5, rng), 0.1)
    tr.add(29.25 + 4 * 0.32 + 0.05, M.bell(hz(79), 0.5), 0.2)
    out = tr.mix(reverb=0.38)
    sfx = load_sfx(os.path.join(sfx_dir, 'pencil.mp3') if sfx_dir else None, 6.2)
    if sfx is not None:  # pencil on paper under the opening, fading out as the feeling "dissolves"
        n = len(sfx)
        env = np.minimum(1, np.arange(n) / (0.3 * SR)) * np.clip((6.1 * SR - np.arange(n)) / (2.0 * SR), 0, 1)
        out[:, :n] += sfx * env * 0.022
    return out


# ---------------- cue 02: spacing (31.45 s) ----------------

def review_days(exam_at):
    out, day = [0], 0
    while True:
        left = exam_at - day
        if left <= 1:
            break
        day += 1 if left <= 7 else min(14, max(1, round(left * 0.2)))
        if day >= exam_at:
            break
        out.append(day)
    return out


def cue_spacing(sfx_dir=None):
    T = 31.45
    tr = M.Track(T)
    D = 38
    # quiet clock for the whole cue, one tick per second, stops for the ending
    t = 0.25
    while t < 28.5:
        tr.add(t, tick(0.35 if int(t) % 2 else 0.25), 0.4 if int(t) % 2 else -0.4)
        t += 1.0
    # 0-3.5 "20 days. When do you review?": open fifth, lone celesta notes
    chord_pad(tr, 0.0, 3.5, [50, 57, 62], 0.8)
    tr.add(0.0, M.sub(hz(D), 3.5))
    for t0, m in ((0.3, 74), (1.6, 69), (2.9, 76)):
        tr.add(t0, celesta(hz(m), 0.45), 0.2)
    # 3.5-8.2 1,350 people: an arpeggio that fills in (denser and denser), Bm9
    chord_pad(tr, 3.5, 4.7, [47, 54, 57, 61, 62])
    tr.add(3.5, M.sub(hz(35), 4.7))
    arp(tr, 3.5, 8.2, [71, 74, 78, 81, 78, 74], 0.18, celesta, 0.32, drop=lambda t: max(0.0, 0.85 - (t - 3.5) / 3.5))
    # 8.2-12.15 a fifth of the time: 5-note figure, first note accented, Gmaj7
    chord_pad(tr, 8.2, 3.95, [43, 50, 54, 59, 62])
    tr.add(8.2, M.sub(hz(31), 3.95))
    for rep in range(3):
        for i, m in enumerate([79, 74, 71, 74, 71]):
            tr.add(8.4 + rep * 1.3 + i * 0.22, celesta(hz(m), 0.55 if i == 0 else 0.25), 0.3 if i == 0 else -0.1)
    # 12.15-14.15 "Cramrade uses about a fifth" (app card): A sus -> A
    chord_pad(tr, 12.15, 2.0, [45, 52, 57, 62, 64])
    tr.add(12.15, M.sub(hz(33), 2.0))
    tr.add(12.65, M.bell(hz(81), 0.3), 0.3)
    # 14.15-18.2 "20 days out, review, then wait 4 days": two bells a gap apart
    chord_pad(tr, 14.15, 4.0, [50, 54, 57, 62])
    tr.add(14.15, M.sub(hz(D), 4.0))
    day = 4.0 / 20
    tr.add(14.4, M.bell(hz(74), 0.45), -0.2)
    tr.add(14.4 + 4 * day * 3.0, M.bell(hz(78), 0.45), 0.2)
    # 18.2-23.65 the gaps shrink: bells on Cramrade's review days for a 20-day plan, rising toward the exam
    rd = review_days(20)
    span = 23.4 - 18.4
    scale = [62, 64, 66, 69, 71, 74, 76, 78, 81, 83, 86]
    chord_pad(tr, 18.2, 2.8, [50, 54, 57, 61], 0.9)
    chord_pad(tr, 21.0, 2.7, [47, 54, 57, 62], 0.9)
    tr.add(18.2, M.sub(hz(D), 2.8))
    tr.add(21.0, M.sub(hz(35), 2.7))
    for i, dd in enumerate(rd):
        tr.add(18.4 + dd / 20 * span, celesta(hz(scale[i]), 0.5), -0.3 + 0.6 * i / len(rd))
    # exam day lands on the cut to the plan screenshot: warm low chord
    tr.add(23.65, M.felt_piano(hz(38), 2.0, 0.5, rng))
    chord_pad(tr, 23.65, 2.4, [50, 54, 57, 61, 64], 1.1)
    tr.add(23.65, M.bell(hz(86), 0.35), 0.3)
    # 26.05-28.55 move the date: a quick downward glide, then the bells re-space for a 16-day plan
    tr.add(26.05, riser(900, 300, 0.6, 0.5))
    chord_pad(tr, 26.05, 2.5, [43, 50, 55, 59])
    for i, dd in enumerate(review_days(16)):
        tr.add(26.6 + dd / 16 * 1.8, celesta(hz(scale[i] - 2), 0.35), 0.2)
    # 28.55 end: D major resolve + climb motif D E F# A + summit bell
    chord_pad(tr, 28.55, 2.9, [50, 54, 57, 62, 64], 1.1)
    tr.add(28.55, M.sub(hz(D), 2.9))
    for i, m in enumerate([62, 64, 66, 69]):
        tr.add(28.6 + i * 0.3, M.felt_piano(hz(m), 1.0, 0.5, rng), 0.1)
    tr.add(28.6 + 4 * 0.3 + 0.05, M.bell(hz(74), 0.5), 0.2)
    return tr.mix(reverb=0.42)


# ---------------- cue 03: group (29.4 s) ----------------

def cue_group(sfx_dir=None):
    T = 29.4
    tr = M.Track(T)
    b = 60 / 96
    # 0-6.9 the sleepy study group: slow pizzicato walk, droopy felt piano, nobody's awake
    walk = [41, 45, 48, 45, 38, 41, 43, 45]
    for i, m in enumerate(walk):
        tr.add(0.05 + i * b * 1.6, pluck(hz(m), 0.55, 1.2, 0.15), -0.1)
    for k, (t0, notes) in enumerate(((0.0, [53, 57, 60, 64]), (3.4, [50, 53, 57, 60]))):
        chord_pad(tr, t0, 3.4, notes, 0.7)
        for j, m in enumerate(notes[1:]):
            tr.add(t0 + 0.3 + j * 0.5, M.felt_piano(hz(m + 12) * 0.997, 1.2, 0.3, rng), 0.15)
    # 6.9-8.4 "nobody remembers": a held note that tape-stops
    held = M.felt_piano(hz(69), 1.5, 0.45, rng)[: int(1.5 * SR)]
    tr.add(6.9, tape_stop(held, 1.3), 0.1)
    # 8.4 "Flip it": riser into a bright downbeat
    tr.add(7.7, riser(300, 1500, 0.7, 0.6))
    tr.add(8.4, kick(0.6))
    tr.add(8.4, M.bell(hz(84), 0.4), 0.3)
    # 8.4-26.6 light groove: F - Dm - Bb - C, shaker 8ths, kick on 1 and 3, walking pizz
    prog = [([53, 57, 60], 41), ([50, 53, 57], 38), ([46, 50, 53], 34), ([48, 52, 55], 36)]
    t0, k = 8.4, 0
    while t0 < 26.6 - 0.1:
        notes, root = prog[k % 4]
        chord_pad(tr, t0, 4 * b, notes, 0.6)
        tr.add(t0, kick(0.45))
        tr.add(t0 + 2 * b, kick(0.35))
        for e in range(8):
            tr.add(t0 + e * b / 2, shaker(0.16 if e % 2 else 0.09), 0.35)
        for e, iv in enumerate((0, 7, 12, 7)):
            tr.add(t0 + e * b, pluck(hz(root + iv), 0.5, 0.7, 0.35), -0.1)
        # quiz call (left) and answer (right) on marimba
        call = [notes[2] + 12, notes[1] + 12, notes[2] + 12]
        ans = [notes[0] + 12, notes[1] + 12, notes[0] + 24]
        for e, m in enumerate(call):
            tr.add(t0 + e * b / 2, marimba(hz(m), 0.42), -0.55)
        for e, m in enumerate(ans):
            tr.add(t0 + 2 * b + e * b / 2, marimba(hz(m), 0.42), 0.55)
        t0 += 4 * b
        k += 1
    # 9.3-12.9 against the clock: ticks on every 8th
    t = 9.3
    while t < 12.9:
        tr.add(t, tick(0.4), 0.5)
        t += b / 2
    # 12.9 "sticks better": lift pad + bell
    tr.add(12.9, M.bell(hz(77), 0.4), 0.2)
    chord_pad(tr, 12.9, 3.5, [65, 69, 72], 0.6)
    # 16.5 the answer list: right, right, wrong, right (rows appear at +0.15, +0.35, +0.55, +0.75)
    for i, ok in enumerate((True, True, False, True)):
        t1 = 16.5 + 0.15 + i * 0.2
        if ok:
            tr.add(t1, marimba(hz(84), 0.5), 0.3)
            tr.add(t1 + 0.07, marimba(hz(88), 0.45), 0.3)
        else:
            tr.add(t1, thud(98, 0.7), -0.2)
    # 23.8 podium fanfare (small): F A C F
    for i, m in enumerate([65, 69, 72, 77]):
        tr.add(23.85 + i * 0.12, marimba(hz(m), 0.55), -0.2 + i * 0.15)
    tr.add(23.85 + 0.5, M.bell(hz(89), 0.4), 0.3)
    # 26.6 end: F resolve + climb motif F G A C + summit bell
    chord_pad(tr, 26.6, 2.8, [53, 57, 60, 67], 1.1)
    tr.add(26.6, M.sub(hz(41), 2.8))
    for i, m in enumerate([65, 67, 69, 72]):
        tr.add(26.65 + i * 0.3, M.felt_piano(hz(m), 1.0, 0.5, rng), 0.1)
    tr.add(26.65 + 4 * 0.3 + 0.05, M.bell(hz(77), 0.5), 0.2)
    out = tr.mix(reverb=0.32)
    sfx = load_sfx(os.path.join(sfx_dir, 'library.mp3') if sfx_dir else None, 8.4)
    if sfx is not None:  # quiet library murmur under the sleepy part, cut by "Flip it"
        n = len(sfx)
        env = np.minimum(1, np.arange(n) / (0.4 * SR)) * np.clip((8.3 * SR - np.arange(n)) / (0.5 * SR), 0, 1)
        out[:, :n] += sfx * env * 0.03
    return out


def finish(x, T):
    n = int(T * SR)
    x = x[:, :n]
    fade = int(0.9 * SR)
    x[:, -fade:] *= np.linspace(1, 0, fade)
    return x


def main(outdir, sfx_dir=None):
    os.makedirs(outdir, exist_ok=True)
    for name, fn, T in (('score-01-recall', cue_recall, 32.4), ('score-02-spacing', cue_spacing, 31.45),
                        ('score-03-group', cue_group, 29.4)):
        M.write(os.path.join(outdir, name + '.mp3'), finish(fn(sfx_dir), T), -19.5)
        print('wrote', name)


if __name__ == '__main__':
    a = sys.argv[1:]
    sfx = a[a.index('--sfx') + 1] if '--sfx' in a else None
    main(a[0] if a else '.', sfx)
