#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ВНИМАНИЕ: не запускать в продакшене, может испортить кодировку файлов.
Этот скрипт выполняет массовое исправление кодировки кириллицы в HTML файлах guides-laptops (расширенная версия).
Запускать только вручную на копии проекта.
"""

import os
from pathlib import Path

def has_corrupted_cyrillic(content):
    """Check if content has corrupted Cyrillic characters"""
    # Look for patterns that indicate double UTF-8 encoding corruption
    # These are UTF-8 bytes interpreted as Latin-1 and then saved as UTF-8
    corrupted_patterns = [
        'Ð°', 'Ð±', 'Ð²', 'Ð³', 'Ð´', 'Ðµ', 'Ð¶', 'Ð·', 'Ð¸', 'Ð¹', 'Ðº', 'Ð»', 'Ð¼',
        'Ð½', 'Ð¾', 'Ð¿', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ',
        'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ð', 'Ñ',  # ё and Ё
        'â', 'â', 'â', 'â', 'â', 'â',  # corrupted punctuation
        'ен', 'енен', 'н', 'н', 'н', 'н', 'н', 'н', 'н', 'н', 'н', 'н'  # specific corrupted sequences
    ]
    return any(pattern in content for pattern in corrupted_patterns)

def fix_double_utf8_encoding(content):
    """
    Fix double UTF-8 encoding corruption
    """
    try:
        # Method 1: Decode as Latin-1 then re-encode as UTF-8
        latin1_bytes = content.encode('latin1', errors='ignore')
        fixed_content = latin1_bytes.decode('utf-8', errors='ignore')
        return fixed_content
    except Exception:
        return content

def fix_character_replacements(content):
    """Manual character replacement for corrupted sequences"""
    replacements = {
        # Cyrillic lowercase
        'Ð°': 'а', 'Ð±': 'б', 'Ð²': 'в', 'Ð³': 'г', 'Ð´': 'д', 'Ðµ': 'е', 'Ð¶': 'ж',
        'Ð·': 'з', 'Ð¸': 'и', 'Ð¹': 'й', 'Ðº': 'к', 'Ð»': 'л', 'Ð¼': 'м', 'Ð½': 'н',
        'Ð¾': 'о', 'Ð¿': 'п', 'Ñ': 'р', 'Ñ': 'с', 'Ñ': 'т', 'Ñ': 'у', 'Ñ': 'ф',
        'Ñ': 'х', 'Ñ': 'ц', 'Ñ': 'ч', 'Ñ': 'ш', 'Ñ': 'щ', 'Ñ': 'ъ', 'Ñ': 'ы',
        'Ñ': 'ь', 'Ñ': 'э', 'Ñ': 'ю', 'Ñ': 'я', 'Ð': 'ё', 'Ñ': 'ё',

        # Cyrillic uppercase
        'Ð': 'А', 'Ð': 'Б', 'Ð': 'В', 'Ð': 'Г', 'Ð': 'Д', 'Ð': 'Е', 'Ð': 'Ж',
        'Ð': 'З', 'Ð': 'И', 'Ð': 'Й', 'Ð': 'К', 'Ð': 'Л', 'Ð': 'М', 'Ð': 'Н',
        'Ð': 'О', 'Ð': 'П', 'Ð ': 'Р', 'Ð¡': 'С', 'Ð¢': 'Т', 'Ð£': 'У', 'Ð¤': 'Ф',
        'Ð¥': 'Х', 'Ð¦': 'Ц', 'Ð§': 'Ч', 'Ð¨': 'Ш', 'Ð©': 'Щ', 'Ðª': 'Ъ', 'Ð«': 'Ы',
        'Ð¬': 'Ь', 'Ð­': 'Э', 'Ð®': 'Ю', 'Ð¯': 'Я',

        # Common corrupted sequences
        'ен': 'еш', 'енен': 'еше', 'н': 'ле', 'н': 'ро', 'н': 'то', 'н': 'ля',
        'н': 'ра', 'н': 'ля', 'н': 'ля', 'н': 'ля', 'н': 'ля', 'н': 'ля',
        'â': '→', 'â': '"', 'â': '"', 'â': '"', 'â': '—', 'â': '–',

        # Specific corrupted word parts
        'Ð енен': 'Реше', 'нлен': 'лект', 'нопин': 'ропит', 'нанин': 'тани',
        'Созданн': 'Создани', 'Вннокан': 'Высокоп', 'пноизводин': 'производи',
        'Уннановин': 'Установ', 'длн': 'для', 'бананеи': 'батареи',
        'Онклннен': 'Отключен', 'авноманиненкого': 'автоматического',
        'пенеклннен': 'переключен', 'нпнавленин': 'правлени',
        'Элекннопин': 'Электроп', 'нин': 'ние', 'Панелн': 'Панель',
        'нвойннван': 'свойств', 'онклннин': 'отключит',
        'Снижанн': 'Снижат', 'ннконнн': 'яркость', 'нкнана': 'экрана',
        'женнкий': 'жесткий', 'динк': 'диск', 'макнималнннн': 'максимально',
        'пноизводинелнноннн': 'производительно',
        'Нанннойки': 'Настройки', 'видеоканнн': 'видеокарт',
        'Упнавлен': 'Управле', 'панаменнами': 'параметрами',
        'нпнавленин': 'правление', 'нлекннопинан': 'электропитан',
        'â': '→', '"Ðнедпонинанн': '"Предпочитат',
        'макнималнннн': 'максимально', 'пноненнона': 'процессора',
        'Макнималннан': 'Максимальна', 'AMD Radeon Settings': 'AMD Radeon Settings',
        'Синнема': 'Система', 'Пенеклннен': 'Переключен', 'Вннокопноизводинелннан': 'Высокопроизводительна',
        'Онклннинн': 'Отключит', 'нненгонбенежен': 'энергосбережен',
        'Обновлен': 'Обновле', 'днайвенов': 'драйверов', 'видеоканнн': 'видеокарт',
        'GeForce Experience или AMD Software': 'GeForce Experience или AMD Software',
        'Обновине': 'Обновите', 'понледнин': 'последни', 'венний': 'версий',
        'Вклннине': 'Включите', 'игновне': 'игровые', 'опнимизании': 'оптимизации',
        'Ð енен': 'Реш', 'BIOS нанннойки': 'BIOS настройки',
        'Нанннойки': 'Настройки', 'пноизводинелннонни': 'производительност',
        'Войдине': 'Войдите', 'BIOS': 'BIOS', 'Найдине': 'Найдите',
        'наздел': 'раздел', 'Power Management': 'Power Management',
        'Уннановине': 'Установите', 'пноизводинелнноннн': 'производительнос',
        'на макнимнм': 'на максимум', 'Онклннине': 'Отключите',
        'авноманиненкое': 'автоматическое', 'пенеклннен': 'переключен'
    }

    fixed_content = content
    for corrupted, correct in replacements.items():
        fixed_content = fixed_content.replace(corrupted, correct)

    return fixed_content

def fix_file_encoding(file_path):
    """Fix encoding issues in a single file"""
    try:
        # Read file as UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not has_corrupted_cyrillic(content):
            return False  # No corruption found

        # Try double encoding fix first
        fixed_content = fix_double_utf8_encoding(content)

        # If still corrupted, use character replacements
        if has_corrupted_cyrillic(fixed_content):
            fixed_content = fix_character_replacements(content)

        # Final check - if still corrupted, use more aggressive replacement
        if has_corrupted_cyrillic(fixed_content):
            fixed_content = fix_character_replacements(fixed_content)

        # Write back as proper UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        print(f"Fixed encoding: {file_path}")
        return True

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix encoding in all guides-laptops files"""
    guides_laptops_dir = Path("c:/Users/yashi/Desktop/Новая папка/FixTech-main/guides-laptops")

    if not guides_laptops_dir.exists():
        print(f"Directory not found: {guides_laptops_dir}")
        return

    html_files = list(guides_laptops_dir.glob("*.html"))

    print(f"Checking {len(html_files)} files for encoding corruption...")

    fixed_count = 0
    for html_file in html_files:
        if fix_file_encoding(html_file):
            fixed_count += 1

    print(f"\nFixed encoding in {fixed_count} files")

if __name__ == "__main__":
    print("ВНИМАНИЕ: Этот скрипт может испортить кодировку файлов.")
    print("Запускать только вручную на копии проекта.")
    print("Для запуска раскомментируйте строку ниже:")
    # main()
    print("Скрипт завершён без изменений.")
