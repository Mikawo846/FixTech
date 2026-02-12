#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ВНИМАНИЕ: не запускать в продакшене, может испортить кодировку файлов.
Этот скрипт выполняет массовое исправление кодировки кириллицы в HTML файлах guides-laptops.
Запускать только вручную на копии проекта.
"""

import os
from pathlib import Path

def fix_double_utf8_encoding(content):
    """
    Fix double UTF-8 encoding corruption
    The text was originally UTF-8, but got decoded as Latin-1 and then saved as UTF-8
    """
    try:
        # Decode the content as Latin-1 to get the bytes that represent the original UTF-8
        latin1_bytes = content.encode('latin1', errors='ignore')
        # Decode those bytes as UTF-8 to get the original text
        fixed_content = latin1_bytes.decode('utf-8', errors='ignore')
        return fixed_content
    except Exception as e:
        print(f"Error in double encoding fix: {e}")
        return content

def has_corrupted_cyrillic(content):
    """Check if content has corrupted Cyrillic characters"""
    # Look for patterns like Ð°, Ð±, Ð², etc. (corrupted Cyrillic)
    corrupted_patterns = ['Ð°', 'Ð±', 'Ð²', 'Ð³', 'Ð´', 'Ðµ', 'Ð¶', 'Ð·', 'Ð¸', 'Ð¹']
    return any(pattern in content for pattern in corrupted_patterns)

def fix_file_encoding(file_path):
    """Fix encoding issues in a single file"""
    try:
        # Read file as UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not has_corrupted_cyrillic(content):
            return False  # No corruption found

        # Fix the double encoding
        fixed_content = fix_double_utf8_encoding(content)

        # If still corrupted, try alternative approach
        if has_corrupted_cyrillic(fixed_content):
            # Manual character replacement for common corrupted sequences
            replacements = {
                'Ð°': 'а', 'Ð±': 'б', 'Ð²': 'в', 'Ð³': 'г', 'Ð´': 'д', 'Ðµ': 'е', 'Ð¶': 'ж',
                'Ð·': 'з', 'Ð¸': 'и', 'Ð¹': 'й', 'Ðº': 'к', 'Ð»': 'л', 'Ð¼': 'м', 'Ð½': 'н',
                'Ð¾': 'о', 'Ð¿': 'п', 'Ñ': 'р', 'Ñ': 'с', 'Ñ': 'т', 'Ñ': 'у', 'Ñ': 'ф',
                'Ñ': 'х', 'Ñ': 'ц', 'Ñ': 'ч', 'Ñ': 'ш', 'Ñ': 'щ', 'Ñ': 'ъ', 'Ñ': 'ы',
                'Ñ': 'ь', 'Ñ': 'э', 'Ñ': 'ю', 'Ñ': 'я',
                'Ð': 'А', 'Ð': 'Б', 'Ð': 'В', 'Ð': 'Г', 'Ð': 'Д', 'Ð': 'Е', 'Ð': 'Ж',
                'Ð': 'З', 'Ð': 'И', 'Ð': 'Й', 'Ð': 'К', 'Ð': 'Л', 'Ð': 'М', 'Ð': 'Н',
                'Ð': 'О', 'Ð': 'П', 'Ð ': 'Р', 'Ð¡': 'С', 'Ð¢': 'Т', 'Ð£': 'У', 'Ð¤': 'Ф',
                'Ð¥': 'Х', 'Ð¦': 'Ц', 'Ð§': 'Ч', 'Ð¨': 'Ш', 'Ð©': 'Щ', 'Ðª': 'Ъ', 'Ð«': 'Ы',
                'Ð¬': 'Ь', 'Ð­': 'Э', 'Ð®': 'Ю', 'Ð¯': 'Я',
                'â': '→', 'â': '"', 'â': '"', 'â': '"', 'â': '—', 'â': '–',
                'â¢': '™', 'â¬': '€', 'â': ',', 'â': '"', 'â°': '‰'
            }

            fixed_content = content
            for corrupted, correct in replacements.items():
                fixed_content = fixed_content.replace(corrupted, correct)

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
