"""Refresh the app screenshots from cramrade.app's PUBLIC pages (sample data only, no login).

    python engine/capture.py            try every screen that has a "live" entry in screens.json

For each screen it finds an anchor text on the page, clips a region relative to it, and checks the
result is a real image (right size, not blank). On any failure it keeps the stored library file,
so a video run never breaks because the site changed or is unreachable. Prints one line per screen.

Never point this at a signed-in workspace: public videos must only show sample data.
"""
import json
import os
import sys

from PIL import Image, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
SCREENS = os.path.join(HERE, 'assets', 'screens')
VIEWPORT = {'width': 1488, 'height': 812}
SCALE = 1.722  # matches the resolution of the stored library shots


def good(path, meta):
    im = Image.open(path).convert('L')
    want_w = meta['live']['w'] * SCALE
    if abs(im.width - want_w) > 40:
        return False, f'width {im.width} vs ~{want_w:.0f}'
    if ImageStat.Stat(im).stddev[0] < 12:
        return False, 'looks blank'
    return True, 'ok'


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('playwright missing: keeping library shots'); return 0
    with open(os.path.join(SCREENS, 'screens.json')) as fh:
        manifest = json.load(fh)
    todo = {k: v for k, v in manifest.items() if 'live' in v}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=SCALE)
        for name, meta in todo.items():
            live = meta['live']
            tmp = os.path.join(SCREENS, f'.{name}.new.png')
            try:
                page.goto(live['url'], wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(1500)
                anchor = page.get_by_text(live['anchor'], exact=False).first
                anchor.scroll_into_view_if_needed(timeout=10000)
                page.wait_for_timeout(600)
                b = anchor.bounding_box()
                if not b:
                    raise RuntimeError('anchor not visible')
                clip = {'x': b['x'] - live['dx'], 'y': b['y'] - live['dy'], 'width': live['w'], 'height': live['h']}
                page.mouse.move(VIEWPORT['width'] - 5, VIEWPORT['height'] - 5)
                page.screenshot(path=tmp, clip=clip)
                ok, why = good(tmp, meta)
                if not ok:
                    raise RuntimeError(why)
                os.replace(tmp, os.path.join(SCREENS, meta['file']))
                print(f'{name}: refreshed')
            except Exception as e:  # keep the library copy
                if os.path.exists(tmp):
                    os.remove(tmp)
                print(f'{name}: kept library copy ({type(e).__name__}: {str(e)[:80]})')
        browser.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
