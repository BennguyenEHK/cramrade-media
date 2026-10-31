"""Post queue helper.

    python engine/queue.py check queue/2026-W45.json   validate one week's queue (exit 1 on problems)
    python engine/queue.py today [YYYY-MM-DD]          print the items due that day (default: today, Chicago):
                                                       status 'ready' (approved) and 'review' (needs Minh's OK)

A queue file lists one item per video. The daily publish run reads it and books the posts in Buffer.

Posting time: `time` ("HH:MM", Chicago) is the default for every channel; an optional
`times` {"tiktok": "20:00", "instagram": "18:00", "youtube": "17:00"} overrides it per channel.
`today` prints `due_at` (default) and `due_at_by_channel` (one ISO time per channel).
"""
import datetime as dt
import glob
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = ZoneInfo('America/Chicago')
RAW = 'https://raw.githubusercontent.com/BennguyenEHK/cramrade-media/main/'
CHANNELS = ('tiktok', 'instagram', 'youtube')
KINDS = {'fact', 'quiz', 'tips', 'feature', 'build', 'trend'}
REQUIRED = ('date', 'time', 'video', 'kind', 'caption', 'hashtags', 'tiktok_title', 'youtube_title')
BANNED = (r'\bfree\b', r'\bteens?\b', r'high ?school', r'app store', r'play store', r'download the app',
          r'ai study plan', r'guarantee', r'nothing leaves your device', r'\bthe first\b', r'\bthe only\b',
          r'\$\d', r'improve (your )?grades by',
          r'18\s*\+', r'\b18 and over\b', r'students 18', r'sign up now')


def problems(q):
    out = []
    seen = set()
    for i, it in enumerate(q.get('items', [])):
        w = f'item {i + 1} ({it.get("date", "?")})'
        for k in REQUIRED:
            if not it.get(k):
                out.append(f'{w}: missing {k}')
        for ch, hm in (it.get('times') or {}).items():
            if ch not in CHANNELS or not re.fullmatch(r'([01]\d|2[0-3]):[0-5]\d', str(hm)):
                out.append(f'{w}: times must map tiktok/instagram/youtube to "HH:MM"')
        if it.get('status', 'ready') not in ('ready', 'review', 'hold', 'booked', 'archived'):
            out.append(f'{w}: status must be ready, review, hold, booked or archived')
        if it.get('kind') not in KINDS:
            out.append(f'{w}: kind must be one of {sorted(KINDS)}')
        if it.get('date') in seen:
            out.append(f'{w}: two items on one date')
        seen.add(it.get('date'))
        if it.get('video') and not os.path.exists(os.path.join(ROOT, it['video'])):
            out.append(f'{w}: video file {it["video"]} is not in the repo')
        tags = it.get('hashtags', [])
        if not 3 <= len(tags) <= 5 or any(not t.startswith('#') for t in tags):
            out.append(f'{w}: 3-5 hashtags, each starting with #')
        yt = it.get('youtube_title', '')
        if len(yt) > 100 or '#Shorts' not in yt:
            out.append(f'{w}: youtube_title must be <= 100 chars and contain #Shorts')
        if len(it.get('tiktok_title', '')) > 90:
            out.append(f'{w}: tiktok_title max 90 chars')
        text = (it.get('caption', '') + ' ' + yt).lower()
        for b in BANNED:
            if re.search(b, text):
                out.append(f'{w}: caption matches banned wording /{b}/ (see docs/knowledge.md section 5)')
        if it.get('kind') == 'fact' and not it.get('sources'):
            out.append(f'{w}: fact videos need sources (URLs)')
        if len(it.get('caption', '')) > 1500:
            out.append(f'{w}: caption too long')
    return out


def post_text(it):
    return it['caption'].rstrip() + '\n\n' + ' '.join(it['hashtags'])


def due(day):
    items = []
    for path in sorted(glob.glob(os.path.join(ROOT, 'queue', '*.json'))):
        with open(path) as fh:
            q = json.load(fh)
        for it in q.get('items', []):
            # 'review' = waiting for Minh's OK by email (PUBLISH.md step 2); 'ready' = already approved
            if it.get('date') == day and it.get('status', 'ready') in ('ready', 'review'):
                at = lambda hm: dt.datetime.fromisoformat(f'{day}T{hm}').replace(tzinfo=TZ).isoformat()
                times = it.get('times') or {}
                it = dict(it, queue_file=os.path.relpath(path, ROOT), video_url=RAW + it['video'],
                          text=post_text(it), due_at=at(it['time']),
                          due_at_by_channel={ch: at(times.get(ch, it['time'])) for ch in CHANNELS})
                items.append(it)
    return items


def main(argv):
    if len(argv) >= 2 and argv[1] == 'check':
        with open(argv[2]) as fh:
            errs = problems(json.load(fh))
        print('\n'.join(errs) if errs else 'queue ok')
        return 1 if errs else 0
    if len(argv) >= 2 and argv[1] == 'today':
        day = argv[2] if len(argv) > 2 else dt.datetime.now(TZ).date().isoformat()
        print(json.dumps(due(day), indent=2))
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
