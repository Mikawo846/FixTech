#!/usr/bin/env python3
import re
from pathlib import Path

root = Path('.')
pattern = re.compile(r"\[web:\d+\]")

modified = []
for p in root.rglob('*'):
    if p.suffix.lower() in ('.html', '.md', '.markdown'):
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        new = pattern.sub('', text)
        if new != text:
            p.write_text(new, encoding='utf-8')
            modified.append(str(p))

print('Modified files:')
for m in modified:
    print(m)
print(f'Total: {len(modified)}')
