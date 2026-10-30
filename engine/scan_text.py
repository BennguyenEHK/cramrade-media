"""Scan images and videos for text that must not appear (Minh's rule, 2026-10-30: no "18+" in any video).

    python engine/scan_text.py PATH [PATH ...]     files or folders (.png .jpg .mp4); exit 1 if anything is found

Videos are sampled at 2 frames per second. Each frame/image is read with tesseract (upscaled 2x, so small
labels are read too). Plain "18" alone is ignored on purpose: OCR often reads "10" as "18".
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image

BAD = re.compile(r'(?<![\w.,])[1iIl|]8\s*\+|for students|\b18\s*(and|or)\s*(over|older)\b|students\s*18|adult learners|eighteen', re.I)


def ocr(img):
    with tempfile.NamedTemporaryFile(suffix='.png') as tf:
        im = Image.open(img).convert('L')
        im = im.resize((im.width * 2, im.height * 2))
        im.save(tf.name)
        return subprocess.run(['tesseract', tf.name, '-', '--psm', '11'], capture_output=True, text=True).stdout


def scan_image(path):
    t = ' '.join(ocr(path).split())
    m = BAD.search(t)
    return [(path, m.group(0), t[max(0, m.start() - 40):m.end() + 40])] if m else []


def scan_video(path):
    hits = []
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-vf', 'fps=2,scale=540:-1', os.path.join(d, 'f%04d.png')], check=True)
        for f in sorted(glob.glob(os.path.join(d, '*.png'))):
            for _, word, ctx in scan_image(f):
                sec = (int(os.path.basename(f)[1:5]) - 1) / 2
                hits.append((f'{path} @ {sec:.1f}s', word, ctx))
    return hits


def main(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for ext in ('png', 'jpg', 'jpeg', 'mp4'):
                files += glob.glob(os.path.join(p, '**', f'*.{ext}'), recursive=True)
        else:
            files.append(p)
    hits = []
    for f in sorted(files):
        hits += scan_video(f) if f.lower().endswith('.mp4') else scan_image(f)
    seen = set()
    for where, word, ctx in hits:  # first hit per file is enough
        f = where.split(' @ ')[0]
        if f in seen:
            continue
        seen.add(f)
        print(f'FOUND "{word}" in {where}: ...{ctx}...')
    print(f'scanned {len(files)} files, {len(seen)} with forbidden text')
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or ['.']))
