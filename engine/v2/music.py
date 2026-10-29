"""Cramrade theme music, "Base Camp": composed in code, royalty-free, made for studying.

    python engine/v2/music.py OUTDIR            writes theme (90 s loop), bed (for videos), sting (4 s)

Inspired by cramrade.app: snowy pixel mountains, mist, a winding amber path from a village up to the
summit flag (exam day). Musical mapping:
- cold, airy room: a soft pad and a very quiet wind texture, lots of reverb;
- the path: a short rising motif (D E F# A) that climbs, then rests;
- the summit flag: one soft bell note that answers the motif, rarely;
- the village: warm felt-piano chords.

Study-friendly rules: 66 bpm, no drums, no lyrics, two bars per chord, the melody plays at most every
other phrase with long rests, soft attacks, little high-frequency content, narrow dynamics, and the
same key and pulse throughout so nothing surprises the ear.
"""
import os
import subprocess
import sys
import wave

import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 44100
BPM = 66
BEAT = 60 / BPM
BAR = BEAT * 4


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def adsr(n, a, d, s, r, sr=SR):
    t = np.arange(n) / sr
    env = np.ones(n) * s
    ai, di = int(a * sr), int(d * sr)
    env[:ai] = np.linspace(0, 1, max(ai, 1))[:min(ai, n)] if ai else env[:0]
    if ai < n:
        seg = env[ai:ai + di]
        env[ai:ai + di] = np.linspace(1, s, max(di, 1))[:len(seg)]
    ri = int(r * sr)
    if ri:
        env[-ri:] *= np.linspace(1, 0, ri)
    return env


def felt_piano(freq, dur, vel=0.5, rng=None):
    n = int((dur + 1.8) * SR)
    t = np.arange(n) / SR
    tone = np.zeros(n)
    for k, amp, dec in ((1, 1.0, 1.6), (2, 0.35, 2.4), (3, 0.12, 3.5), (4, 0.05, 4.5)):
        det = 1 + (rng.normal(0, 0.0007) if rng is not None else 0)
        tone += amp * np.sin(2 * np.pi * freq * k * det * t) * np.exp(-t * dec)
    attack = 1 - np.exp(-t * 90)  # soft felt hammer, no click
    release = np.ones(n)
    ri = int(1.6 * SR)
    release[int(dur * SR):int(dur * SR) + ri] = np.linspace(1, 0, ri)[:max(0, min(ri, n - int(dur * SR)))]
    release[int(dur * SR) + ri:] = 0
    return tone * attack * release * vel * 0.22


def bell(freq, vel=0.4):
    n = int(5.0 * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for ratio, amp, dec in ((1, 1.0, 0.9), (2.0, 0.4, 1.4), (2.76, 0.25, 2.2), (5.4, 0.08, 4.0)):
        sig += amp * np.sin(2 * np.pi * freq * ratio * t) * np.exp(-t * dec)
    return sig * (1 - np.exp(-t * 300)) * vel * 0.12


def pad(freqs, dur):
    n = int((dur + 2.5) * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):  # cents-ish chorus, very slow beating
            ff = f * (1 + det / 100)
            sig += np.sin(2 * np.pi * ff * t + np.sin(2 * np.pi * 0.11 * t) * 0.3)
            sig += 0.18 * np.sin(2 * np.pi * ff * 2 * t)
    env = np.minimum(1, t / 1.8) * np.clip((dur + 2.5 - t) / 2.5, 0, 1)
    return sig * env * 0.010


def sub(freq, dur):
    n = int((dur + 1.0) * SR)
    t = np.arange(n) / SR
    env = np.minimum(1, t / 0.4) * np.clip((dur + 1.0 - t) / 1.0, 0, 1)
    return np.sin(2 * np.pi * freq * t) * env * 0.06


def reverb_ir(seconds=3.2, seed=5):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = rng.normal(0, 1, (2, n)) * np.exp(-t * 2.2)
    sos = butter(2, 5500, 'low', fs=SR, output='sos')
    return sosfilt(sos, ir, axis=1) * 0.06


class Track:
    def __init__(self, dur):
        self.n = int(dur * SR)
        self.dry = np.zeros((2, self.n + int(8 * SR)))

    def add(self, t, sig, pan=0.0):
        i = int(t * SR)
        if i < 0:
            sig, i = sig[-i:], 0
        j = min(self.dry.shape[1], i + len(sig))
        if j <= i:
            return
        l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
        self.dry[0, i:j] += sig[:j - i] * l
        self.dry[1, i:j] += sig[:j - i] * r

    def mix(self, reverb=0.45, loop=False):
        ir = reverb_ir()
        wet = np.stack([fftconvolve(self.dry[c], ir[c])[:self.dry.shape[1]] for c in range(2)])
        out = self.dry * (1 - reverb * 0.5) + wet * reverb
        if loop:  # fold the tail back onto the start so the loop is seamless
            tail = out[:, self.n:self.n + int(6 * SR)]
            out = out[:, :self.n].copy()
            out[:, :tail.shape[1]] += tail
        else:
            out = out[:, :self.n]
        sos = butter(2, 7000, 'low', fs=SR, output='sos')  # keep it soft, nothing sharp
        out = sosfilt(sos, out, axis=1)
        sos = butter(1, 45, 'high', fs=SR, output='sos')
        return sosfilt(sos, out, axis=1)


# D major world: Dmaj9, Bm9, Gmaj7(add9), Asus2 -> A6. Voicings kept close and low-mid.
PROG = [
    {'root': 38, 'chord': [50, 54, 57, 61, 64]},  # D: D F# A C# E
    {'root': 35, 'chord': [50, 54, 57, 59, 61]},  # Bm9: D F# A B C#
    {'root': 31, 'chord': [50, 54, 55, 59, 62]},  # Gmaj7add9: D F# G B D
    {'root': 33, 'chord': [49, 52, 57, 59, 64]},  # Asus2/6: C# E A B E
]
CLIMB = [62, 64, 66, 69]            # D E F# A: the path up the mountain
ANSWER = [71, 69, 66]               # B A F#: looking back down
SUMMIT = 74                         # D5 bell: the flag on top


def compose(dur, melody_every=2, bells=True, seed=11, sparse_chords=False):
    rng = np.random.default_rng(seed)
    tr = Track(dur)
    phrase = BAR * 2                # one chord lasts two bars
    nph = int(np.ceil(dur / phrase))
    # wind: very quiet filtered noise, slowly breathing
    n = tr.n
    wind = rng.normal(0, 1, n)
    wind = sosfilt(butter(2, [180, 900], 'band', fs=SR, output='sos'), wind)
    wind *= (0.5 + 0.5 * np.sin(2 * np.pi * np.arange(n) / SR / 13.0)) * 0.0035
    tr.add(0, wind)
    for p in range(nph):
        t0 = p * phrase
        ch = PROG[p % 4]
        tr.add(t0, pad([hz(m) for m in ch['chord'][:3]], phrase * 0.45))   # breathes out mid-phrase
        tr.add(t0, sub(hz(ch['root']), phrase * 0.4))
        # felt piano: a soft broken chord, few notes, lots of air between them
        hits = [0, 1.5, 4.5] if not sparse_chords else [0, 4.5]
        for k, beat in enumerate(hits):
            notes = ch['chord'][k::2] if k else ch['chord'][:3]
            for j, m in enumerate(notes):
                strum = j * 0.045 + rng.normal(0, 0.012)
                tr.add(t0 + beat * BEAT + strum, felt_piano(hz(m), 2.6, vel=0.5 - 0.08 * k, rng=rng),
                       pan=(-0.25 + 0.5 * (j / max(1, len(notes) - 1))))
        # melody: the climb on every `melody_every`-th phrase, then silence
        if melody_every and p % melody_every == 1:
            motif = CLIMB if (p // melody_every) % 2 == 0 else ANSWER
            for i, m in enumerate(motif):
                when = t0 + (2 + i * 1.5) * BEAT + rng.normal(0, 0.02)
                tr.add(when, felt_piano(hz(m), 1.8, vel=0.42, rng=rng), pan=0.15)
            if bells and motif is CLIMB and (p // melody_every) % 4 == 0:
                tr.add(t0 + (2 + 4 * 1.5 + 1) * BEAT, bell(hz(SUMMIT)), pan=0.3)
    return tr


def sting():
    rng = np.random.default_rng(3)
    tr = Track(5.0)
    ch = PROG[0]
    tr.add(0.0, pad([hz(m) for m in ch['chord'][:3]], 3.0))
    for i, m in enumerate(CLIMB):
        tr.add(0.15 + i * 0.42, felt_piano(hz(m), 1.2, vel=0.5, rng=rng), pan=0.1)
    tr.add(0.15 + 4 * 0.42 + 0.1, bell(hz(SUMMIT), vel=0.55), pan=0.2)
    for j, m in enumerate(ch['chord']):
        tr.add(1.95 + j * 0.05, felt_piano(hz(m), 2.5, vel=0.38, rng=rng), pan=-0.2 + j * 0.1)
    tr.add(1.95, sub(hz(ch['root']), 2.5))
    out = tr.mix(reverb=0.5)
    fade = int(0.8 * SR)
    out[:, -fade:] *= np.linspace(1, 0, fade)
    return out


def write(path, stereo, target_lufs):
    tmp = path + '.wav'
    x = stereo / max(1e-9, np.abs(stereo).max()) * 0.8
    with wave.open(tmp, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((x.T * 32767).astype(np.int16).tobytes())
    ff = 'ffmpeg'
    subprocess.run([ff, '-y', '-loglevel', 'error', '-i', tmp, '-af',
                    f'loudnorm=I={target_lufs}:TP=-2:LRA=7', '-ar', str(SR), '-b:a', '192k', path], check=True)
    os.remove(tmp)


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    loop_dur = PROG.__len__() * BAR * 2 * 3          # 12 chords = 3 times round = ~87 s
    theme = compose(loop_dur, melody_every=2).mix(loop=True)
    write(os.path.join(outdir, 'cramrade-theme-base-camp.mp3'), theme, -18)
    bed = compose(BAR * 2 * 4 * 2, melody_every=4, bells=False, sparse_chords=True, seed=4).mix(loop=True)
    write(os.path.join(outdir, 'cramrade-bed-base-camp.mp3'), bed, -20)
    write(os.path.join(outdir, 'cramrade-sting.mp3'), sting(), -16)
    print('theme %.1fs, bed %.1fs, sting 5s' % (loop_dur, BAR * 16))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
