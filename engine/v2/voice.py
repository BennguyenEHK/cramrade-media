"""Notch's voiceover + per-word timings for engine v2.

    python engine/v2/voice.py "SCRIPT TEXT" OUT_PREFIX            -> OUT_PREFIX-voice.mp3, OUT_PREFIX-words.json

1. ElevenLabs (the real Notch voice), when the environment variable ELEVENLABS_API_KEY is set and
   api.elevenlabs.io is reachable: POST /v1/text-to-speech/{voice}/with-timestamps returns the audio and a
   per-character alignment, which is turned into per-word timings. Voice "Notch" WWN2ZT8HeZwUNFy2bh9r.
   Model: eleven_v4, then eleven_v3, then eleven_multilingual_v2 if a model is refused. One take per call
   (every call costs credits: never loop on errors).
2. Fallback: Kokoro (open source, model files from GitHub releases), voice am_liam at speed 0.92, the
   approved fallback in docs/voice-research.md. Kokoro has no timestamps, so each sentence is synthesised
   separately and its words are spread over the sentence by character length (good enough for
   one-word captions). Prints FALLBACK so the run can say so in the review email.

Inline ElevenLabs tags such as [excited] are kept for ElevenLabs and removed for Kokoro; the words JSON
keeps tags as their own entries (the engine skips them in captions).
"""
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

VOICE_ID = 'WWN2ZT8HeZwUNFy2bh9r'
MODELS = ('eleven_v4', 'eleven_v3', 'eleven_multilingual_v2')
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.path.expanduser('~'), '.cache', 'kokoro')
KOKORO_FILES = {
    'kokoro-v1.0.onnx': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx',
    'voices-v1.0.bin': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin',
}


def words_from_alignment(al):
    chars, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    words, cur, s0, e0 = [], '', None, None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur:
                words.append({'text': cur, 'start': round(s0, 3), 'end': round(e0, 3)})
            cur, s0 = '', None
            continue
        if not cur:
            s0 = s
        cur += c
        e0 = e
    if cur:
        words.append({'text': cur, 'start': round(s0, 3), 'end': round(e0, 3)})
    return words


def elevenlabs(text, prefix):
    key = os.environ.get('ELEVENLABS_API_KEY')
    if not key:
        return 'no ELEVENLABS_API_KEY in the environment'
    last = ''
    for model in MODELS:
        body = json.dumps({'text': text, 'model_id': model}).encode()
        req = urllib.request.Request(
            f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format=mp3_44100_128',
            data=body, headers={'xi-api-key': key, 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            last = f'{model}: HTTP {e.code} {e.read()[:300]!r}'
            if e.code in (400, 422) and b'model' in last.encode().lower():
                continue  # model not available on this account: try the next one
            return last
        except Exception as e:  # network blocked, timeout
            return f'{model}: {e}'
        open(prefix + '-voice.mp3', 'wb').write(base64.b64decode(data['audio_base64']))
        al = data.get('alignment') or data.get('normalized_alignment')
        json.dump(words_from_alignment(al), open(prefix + '-words.json', 'w'))
        return None
    return last


def kokoro(text, prefix):
    import urllib.request as u
    os.makedirs(CACHE, exist_ok=True)
    for name, url in KOKORO_FILES.items():
        p = os.path.join(CACHE, name)
        if not os.path.exists(p):
            u.urlretrieve(url, p)
    try:
        from kokoro_onnx import Kokoro
    except ImportError:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--break-system-packages', 'kokoro-onnx', 'soundfile'], check=True)
        from kokoro_onnx import Kokoro
    import numpy as np
    import soundfile as sf
    k = Kokoro(os.path.join(CACHE, 'kokoro-v1.0.onnx'), os.path.join(CACHE, 'voices-v1.0.bin'))
    clean = re.sub(r'\[[^\]]*\]\s*', '', text)
    sentences = [s for s in re.split(r'(?<=[.!?])\s+', clean.strip()) if s]
    pieces, words, t, sr = [], [], 0.0, 24000
    for s in sentences:
        audio, sr = k.create(s, voice='am_liam', speed=0.92, lang='en-us')
        audio = np.asarray(audio, dtype=np.float32)
        # trim leading/trailing silence so word spreading lines up
        nz = np.where(np.abs(audio) > 0.01)[0]
        if len(nz):
            audio = audio[max(0, nz[0] - 600): nz[-1] + 1200]
        dur = len(audio) / sr
        ws = s.split()
        weights = [len(w) + 2 for w in ws]
        tot = sum(weights)
        acc = 0.0
        for w, wt in zip(ws, weights):
            a = t + dur * acc / tot
            acc += wt
            words.append({'text': w, 'start': round(a, 3), 'end': round(t + dur * acc / tot - 0.02, 3)})
        pieces.append(audio)
        gap = np.zeros(int(0.22 * sr), dtype=np.float32)
        pieces.append(gap)
        t += dur + 0.22
    wav = prefix + '-voice.wav'
    sf.write(wav, np.concatenate(pieces), sr)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'loudnorm=I=-16:TP=-1.5', '-b:a', '160k',
                    prefix + '-voice.mp3'], check=True)
    os.remove(wav)
    json.dump(words, open(prefix + '-words.json', 'w'))


def main(text, prefix):
    err = elevenlabs(text, prefix)
    if err is None:
        print('VOICE elevenlabs', prefix + '-voice.mp3')
        return 0
    print('ElevenLabs unavailable:', err)
    kokoro(text, prefix)
    print('FALLBACK kokoro am_liam', prefix + '-voice.mp3')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
