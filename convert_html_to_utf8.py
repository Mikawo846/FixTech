#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ВНИМАНИЕ: не запускать в продакшене, может испортить кодировку файлов.
Этот скрипт выполняет массовую конвертацию всех HTML файлов в UTF-8.
Запускать только вручную на копии проекта.
"""
import os
import chardet
import glob
import codecs

def convert_file_to_utf8(filepath):
    try:
        # Try to read as UTF-8 first
        with codecs.open(filepath, 'r', 'utf-8') as f:
            content = f.read()
        print(f"{filepath}: already UTF-8")
        return False
    except UnicodeDecodeError:
        # Detect encoding
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            detected_encoding = result['encoding']
            confidence = result['confidence']
            print(f"{filepath}: detected {detected_encoding} (confidence: {confidence:.2f})")

            if detected_encoding and confidence > 0.5:
                try:
                    content = raw_data.decode(detected_encoding)
                    # Write back as UTF-8
                    with codecs.open(filepath, 'w', 'utf-8') as f:
                        f.write(content)
                    print(f"Converted {filepath} to UTF-8")
                    return True
                except Exception as e:
                    print(f"Failed to convert {filepath}: {e}")
                    return False
            else:
                print(f"Low confidence or no encoding detected for {filepath}")
                return False

def process_html_files():
    html_files = glob.glob('**/*.html', recursive=True)
    converted_count = 0
    for filepath in html_files:
        if convert_file_to_utf8(filepath):
            converted_count += 1
    print(f"Total HTML files converted: {converted_count}")

if __name__ == "__main__":
    print("ВНИМАНИЕ: Этот скрипт может испортить кодировку файлов.")
    print("Запускать только вручную на копии проекта.")
    print("Для запуска раскомментируйте строку ниже:")
    # process_html_files()
    print("Скрипт завершён без изменений.")
