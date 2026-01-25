#!/usr/bin/env python3
"""Insert Google gtag snippet after the first <head> tag in each .html file in the repo.
Skips files that already contain the tracking ID.
Creates a .bak backup for each modified file.
"""
import re
from pathlib import Path

TRACKING_ID = 'G-YE88Y994NX'
SNIPPET = (
    '<!-- Google tag (gtag.js) -->\n'
    '<script async src="https://www.googletagmanager.com/gtag/js?id={id}"></script>\n'
    '<script>\n'
    "  window.dataLayer = window.dataLayer || [];\n"
    "  function gtag(){{dataLayer.push(arguments);}}\n"
    "  gtag('js', new Date());\n\n"
    "  gtag('config', '{id}');\n"
    '</script>'
).format(id=TRACKING_ID)

HEAD_RE = re.compile(r'(<head\b[^>]*>)', flags=re.IGNORECASE)

root = Path(__file__).resolve().parents[1]
html_files = list(root.rglob('*.html'))
modified = []
skipped = []

for f in html_files:
    text = f.read_text(encoding='utf-8')
    if TRACKING_ID in text:
        skipped.append(str(f.relative_to(root)))
        continue
    m = HEAD_RE.search(text)
    if not m:
        skipped.append(str(f.relative_to(root)))
        continue
    # Insert snippet right after the <head...> match
    new_text = text[: m.end()] + '\n' + SNIPPET + '\n' + text[m.end():]
    # Backup original
    bak = f.with_suffix(f.suffix + '.bak')
    bak.write_text(text, encoding='utf-8')
    f.write_text(new_text, encoding='utf-8')
    modified.append(str(f.relative_to(root)))

print(f'Modified {len(modified)} files; skipped {len(skipped)} files.')
if modified:
    for p in modified[:200]:
        print(p)
    if len(modified) > 200:
        print('...')
