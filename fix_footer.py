#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления футера в index.html
Создаёт три одинаковых столбца с заголовками и черточками
"""

import re

# Читаем index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Новая структура футера с тремя одинаковыми колонками
new_footer_grid = '''            <div class="footer__grid">
                <!-- Колонка 1: Разделы -->
                <div class="footer__col">
                    <h3 class="footer__title">Разделы</h3>
                    <ul class="footer__links">
                        <li><a href="index.html" class="footer__link">Главная</a></li>
                        <li><a href="index.html#categories" class="footer__link">Все гайды</a></li>
                        <li><a href="contacts.html" class="footer__link">Контакты</a></li>
                    </ul>
                </div>
                
                <!-- Колонка 2: Категории -->
                <div class="footer__col">
                    <h3 class="footer__title">Категории</h3>
                    <ul class="footer__links">
                        <li><a href="tv.html" class="footer__link">Телевизоры</a></li>
                        <li><a href="smartphones.html" class="footer__link">Смартфоны</a></li>
                        <li><a href="laptops.html" class="footer__link">Ноутбуки</a></li>
                        <li><a href="consoles.html" class="footer__link">Приставки</a></li>
                        <li><a href="cameras.html" class="footer__link">Фотоаппараты</a></li>
                        <li><a href="small-appliances.html" class="footer__link">Мелкая техника</a></li>
                    </ul>
                </div>
                
                <!-- Колонка 3: Контакты -->
                <div class="footer__col">
                    <h3 class="footer__title">Контакты</h3>
                    <ul class="footer__links">
                        <li><a href="https://t.me/techfix_kz" class="footer__link"><i class="fab fa-telegram"></i> Telegram</a></li>
                        <li><a href="https://instagram.com/techfix_kz" class="footer__link"><i class="fab fa-instagram"></i> Instagram</a></li>
                        <li><a href="mailto:support@techfix.kz" class="footer__link"><i class="fas fa-envelope"></i> Email</a></li>
                    </ul>
                </div>
            </div>'''

# Ищем и заменяем старую структуру footer__grid
# Паттерн: от <div class="footer__grid"> до закрывающего </div> (перед footer__bottom)
pattern = r'(<div class="footer__grid">)(.*?)(</div>\s*<div class="footer__bottom">)'

replacement = r'\1\n' + new_footer_grid + r'\n            \3'

# Выполняем замену
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Сохраняем результат
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Футер успешно обновлён!")
print("✅ Теперь в футере три одинаковых столбца:")
print("   1. Разделы")
print("   2. Категории") 
print("   3. Контакты")
print("\nКаждый столбец имеет:")
print("   - Заголовок (h3)")
print("   - Черточку (через CSS footer__title::after)")
print("   - Список ссылок")
