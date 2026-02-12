#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ВНИМАНИЕ: не запускать в продакшене, может испортить кодировку файлов.
Этот скрипт выполняет массовую конвертацию HTML файлов в guides-laptops обратно в cp1251.
Запускать только вручную на копии проекта.
"""

import os
from pathlib import Path

def convert_file_to_cp1251(file_path):
    """Convert single file from UTF-8 back to cp1251"""
    try:
        # Read as UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Encode to cp1251
        cp1251_bytes = content.encode('cp1251', errors='replace')
        
        # Write as cp1251 bytes
        with open(file_path, 'wb') as f:
            f.write(cp1251_bytes)
        
        print(f"Converted back: {file_path}")
        return True
    except Exception as e:
        print(f"Error converting back {file_path}: {e}")
        return False

def main():
    """Main function"""
    guides_laptops_dir = Path("c:/Users/yashi/Desktop/Новая папка/FixTech-main/guides-laptops")

    if not guides_laptops_dir.exists():
        print(f"Directory not found: {guides_laptops_dir}")
        return

    html_files = list(guides_laptops_dir.glob("*.html"))
    print(f"Converting {len(html_files)} HTML files back from UTF-8 to cp1251...")

    converted_count = 0
    for html_file in html_files:
        if convert_file_to_cp1251(html_file):
            converted_count += 1

    print(f"\nConverted back {converted_count} files to cp1251")

if __name__ == "__main__":
    print("ВНИМАНИЕ: Этот скрипт может испортить кодировку файлов.")
    print("Запускать только вручную на копии проекта.")
    print("Для запуска раскомментируйте строку ниже:")
    # main()
    print("Скрипт завершён без изменений.")
