#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ВНИМАНИЕ: не запускать в продакшене, может испортить кодировку файлов.
Этот скрипт выполняет массовое восстановление кириллицы из бэкапов или исправление кодировки в HTML файлах guides-laptops.
Запускать только вручную на копии проекта.
"""

import os
from pathlib import Path

def fix_double_utf8_encoding_precise(content):
    """
    Fix double UTF-8 encoding corruption properly
    This happens when UTF-8 bytes are decoded as Latin-1 and then saved as UTF-8
    """
    try:
        # The content contains UTF-8 bytes that were decoded as Latin-1
        # We need to encode back to Latin-1 bytes, then decode as UTF-8
        # First, encode the content as Latin-1 to get the original UTF-8 bytes
        latin1_bytes = content.encode('latin1', errors='replace')
        # Then decode those bytes as UTF-8
        fixed_content = latin1_bytes.decode('utf-8', errors='replace')
        return fixed_content
    except Exception as e:
        print(f"Double encoding fix failed: {e}")
        return content

def has_corrupted_cyrillic(content):
    """Check if content has corrupted Cyrillic characters from double encoding"""
    # Look for specific patterns that indicate double UTF-8 encoding corruption
    corrupted_indicators = [
        'Ð°', 'Ð±', 'Ð²', 'Ð³', 'Ð´', 'Ðµ', 'Ð¶', 'Ð·', 'Ð¸', 'Ð¹', 'Ðº', 'Ð»', 'Ð¼',
        'Ð½', 'Ð¾', 'Ð¿', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ', 'Ñ',
        'â', 'â', 'â', 'â', 'â', 'â',  # corrupted punctuation
        'ен', 'н', 'н', 'н', 'н', 'н', 'н', 'н', 'н', 'н', 'н'  # specific corrupted sequences
    ]
    return any(indicator in content for indicator in corrupted_indicators)

def restore_from_backup(file_path):
    """Restore file from backup if available"""
    backup_path = str(file_path) + '.bak'
    if os.path.exists(backup_path):
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            print(f"Restored from backup: {file_path}")
            return True
        except Exception as e:
            print(f"Failed to restore from backup {backup_path}: {e}")
    return False

def fix_file_encoding(file_path):
    """Fix encoding issues in a single file"""
    try:
        # First try to restore from backup
        if restore_from_backup(file_path):
            return True

        # Read file as UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not has_corrupted_cyrillic(content):
            return False  # No corruption found

        # Try the precise double encoding fix
        fixed_content = fix_double_utf8_encoding_precise(content)

        # If the fix worked and reduced corruption, use it
        original_corruption_count = sum(1 for indicator in ['Ð°', 'Ð±', 'Ð²', 'â', 'â'] if indicator in content)
        fixed_corruption_count = sum(1 for indicator in ['Ð°', 'Ð±', 'Ð²', 'â', 'â'] if indicator in fixed_content)

        if fixed_corruption_count < original_corruption_count:
            # Fix worked, save it
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed encoding: {file_path}")
            return True
        else:
            print(f"Fix didn't improve {file_path}, skipping")
            return False

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
    restored_count = 0

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
