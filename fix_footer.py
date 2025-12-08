#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_footer.py — массовое выравнивание футеров по шаблону

Проходит по всем HTML-файлам в репозитории, делает резервную
копию каждого файла и заменяет существующую сетку футера на
унифицированную версию. Сохраняет оригиналы с расширением .bak.

Использует безопасные регулярные выражения, пытаясь найти
несколько распространённых шаблонов футера (`footer__grid`,
`footer-container`, общий `<footer> ... <div class="footer-bottom">`).
"""

import re
from pathlib import Path
from datetime import datetime


new_footer_grid = '''<div class="footer__grid">
                <div class="footer__col footer__col--logo">
                    <a href="/index.html" class="footer-logo">
                        <span class="logo__icon"> </span>
                        <span class="logo__text">TechFix</span>
                    </a>
                    <p class="footer__text">Помогаем ремонтировать электронику с 2024 года</p>
                </div>
                <div class="footer__col">
                    <h3 class="footer__title">Разделы</h3>
                    <ul class="footer__links">
                        <li><a href="/index.html" class="footer__link">Главная</a></li>
                        <li><a href="/all-guides.html" class="footer__link">Все гайды</a></li>
                        <li><a href="/contacts.html" class="footer__link">Контакты</a></li>
                    </ul>
                </div>
                <div class="footer__col">
                    <h3 class="footer__title">Категории</h3>
                    <ul class="footer__links">
                        <li><a href="/tv.html" class="footer__link">Телевизоры</a></li>
                        <li><a href="/smartphones.html" class="footer__link">Смартфоны</a></li>
                        <li><a href="/laptops.html" class="footer__link">Ноутбуки</a></li>
                    </ul>
                </div>
            </div>'''


def backup_file(path: Path):
    stamp = datetime.now().strftime('%Y%m%d%H%M%S')
    bak = path.with_suffix(path.suffix + f'.bak-{stamp}')
    path.rename(bak)
    return bak


def replace_footer_grid(content: str) -> (str, bool):
    """Попытаться заменить несколько известных шаблонов футера.
    Возвращает (new_content, changed).
    """
    patterns = [
        # pattern 1: footer__grid ... footer__bottom
        (re.compile(r'(<div[^>]+class=["\"][^"\']*footer__grid[^"\']*["\"][^>]*>)(.*?)(</div>\s*<div[^>]+class=["\"]footer__bottom["\"][^>]*>)', re.DOTALL|re.IGNORECASE), True),
        # pattern 2: footer-container ... footer-bottom
        (re.compile(r'(<div[^>]+class=["\"][^"\']*footer-container[^"\']*["\"][^>]*>)(.*?)(</div>\s*<div[^>]+class=["\"]footer-bottom["\"][^>]*>)', re.DOTALL|re.IGNORECASE), True),
        # pattern 3: generic <footer ...> ... <div class="footer-bottom">
        (re.compile(r'(<footer[^>]*>.*?)(<div[^>]+class=["\"]footer-bottom["\"][^>]*>)', re.DOTALL|re.IGNORECASE), False),
    ]

    for pattern, has_grid in patterns:
        m = pattern.search(content)
        if not m:
            continue

        if has_grid:
            start = m.group(1)
            tail = m.group(3)
            new = start + '\n' + new_footer_grid + '\n' + tail
            new_content = content[:m.start()] + new + content[m.end():]
            return new_content, True
        else:
            # Insert new grid right before footer-bottom
            prefix = m.group(1)
            footer_bottom = m.group(2)
            new = prefix + '\n' + new_footer_grid + '\n' + footer_bottom
            new_content = content[:m.start()] + new + content[m.end():]
            return new_content, True

    return content, False


def process_html_file(path: Path):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        print(f"✗ Не удалось прочитать {path}")
        return False

    new_text, changed = replace_footer_grid(text)

    if not changed:
        return False

    # backup and write
    bak = path.with_suffix(path.suffix + '.bak')
    # don't overwrite existing bak — create timestamped backup
    if not bak.exists():
        path.rename(bak)
        bak_path = bak
    else:
        bak_path = backup_file(path)

    # write new content to original path
    path.write_text(new_text, encoding='utf-8')
    print(f"✓ Обновлён: {path} (резервная копия: {bak_path.name})")
    return True


def main():
    root = Path('.')
    html_files = list(root.rglob('*.html'))
    if not html_files:
        print('HTML файлы не найдены')
        return

    updated = 0
    for f in html_files:
        if process_html_file(f):
            updated += 1

    print(f"\nГотово. Обновлено файлов: {updated} из {len(html_files)}")


if __name__ == '__main__':
    main()
