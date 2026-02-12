#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ВНИМАНИЕ: не запускать в продакшене, может испортить кодировку файлов.
Этот скрипт выполняет массовое исправление двойной UTF-8 кодировки в HTML файлах guides-laptops.
Запускать только вручную на копии проекта.
"""

import os
from pathlib import Path

def fix_double_utf8_encoding(content):
    """
    Properly fix double UTF-8 encoding corruption
    When UTF-8 text is incorrectly decoded as Latin-1 and then saved as UTF-8
    """
    try:
        # The content contains UTF-8 bytes that were misinterpreted as Latin-1
        # We need to encode back to Latin-1 bytes, then decode properly as UTF-8

        # Method: encode as Latin-1 (which gives us the original UTF-8 bytes)
        # then decode as UTF-8
        latin1_bytes = content.encode('latin1', errors='strict')
        fixed_content = latin1_bytes.decode('utf-8', errors='strict')
        return fixed_content
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If strict conversion fails, try with error handling
        try:
            latin1_bytes = content.encode('latin1', errors='replace')
            fixed_content = latin1_bytes.decode('utf-8', errors='replace')
            return fixed_content
        except Exception:
            return content

def has_double_encoding(content):
    """Check if content has double UTF-8 encoding corruption"""
    # Look for telltale signs of double encoding
    indicators = [
        'Ð°', 'Ð±', 'Ð²', 'Ð³', 'Ð´', 'Ðµ', 'Ð¶', 'Ð·', 'Ð¸', 'Ð¹', 'Ðº', 'Ð»', 'Ð¼',
        'Ð½', 'Ð¾', 'Ð¿', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ',
        'â', 'â', 'â', 'â', 'â', 'â',
        'ен', 'н', 'н', 'н', 'н', 'н', 'н', 'н', 'н', 'н', 'н'
    ]
    return any(indicator in content for indicator in indicators)

def process_file(file_path):
    """Process a single file to fix encoding"""
    try:
        # Read file as UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not has_double_encoding(content):
            return False

        # Apply the double encoding fix
        fixed_content = fix_double_utf8_encoding(content)

        # Verify the fix worked (should have fewer corruption indicators)
        original_bad_chars = sum(1 for char in ['Ð', 'Ñ', 'â'] if char in content)
        fixed_bad_chars = sum(1 for char in ['Ð', 'Ñ', 'â'] if char in fixed_content)

        if fixed_bad_chars < original_bad_chars or fixed_bad_chars == 0:
            # Fix appears successful, save it
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed: {file_path}")
            return True
        else:
            print(f"Fix didn't improve {file_path}")
            return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function"""
    guides_laptops_dir = Path("c:/Users/yashi/Desktop/Новая папка/FixTech-main/guides-laptops")

    if not guides_laptops_dir.exists():
        print(f"Directory not found: {guides_laptops_dir}")
        return

    html_files = list(guides_laptops_dir.glob("*.html"))

    print(f"Processing {len(html_files)} files for double UTF-8 encoding...")

    fixed_count = 0
    for html_file in html_files:
        if process_file(html_file):
            fixed_count += 1

    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    print("ВНИМАНИЕ: Этот скрипт может испортить кодировку файлов.")
    print("Запускать только вручную на копии проекта.")
    print("Для запуска раскомментируйте строку ниже:")
    # main()
    print("Скрипт завершён без изменений.")
