#!/usr/bin/env python3
"""Remove [web:NNN] artifacts from text files in the repo."""
import re
from pathlib import Path

pattern = re.compile(r"\[web:\d+\]")

root = Path('.').resolve()
files_changed = []
repl_count_total = 0
for p in root.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.html', '.htm', '.md', '.txt'}:
        try:
            s = p.read_text(encoding='utf-8')
        except Exception:
            continue
        new = pattern.sub('', s)
        if new != s:
            p.write_text(new, encoding='utf-8')
            c = len(pattern.findall(s))
            files_changed.append((str(p.relative_to(root)), c))
            repl_count_total += c

print(f'Files modified: {len(files_changed)}')
for fname, cnt in files_changed:
    print(f' - {fname}: {cnt} replacements')
print(f'Total replacements: {repl_count_total}')

if len(files_changed) == 0:
    print('No files needed changes.')
else:
    print('Done.')
