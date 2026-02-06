#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления путей к скриптам в HTML файлах в подпапках
"""

import os
import re

def fix_script_paths(file_path):
    """Исправляет пути к скриптам в HTML файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # Исправляем путь к cookie-consent.js
        content = re.sub(
            r'src="cookie-consent\.js"',
            'src="../cookie-consent.js"',
            content
        )
        
        # Исправляем путь к script.js
        content = re.sub(
            r'src="script\.js"',
            'src="../script.js"',
            content
        )
        
        # Исправляем пути к CSS файлам
        content = re.sub(
            r'href="styles\.css"',
            'href="../styles.css"',
            content
        )
        
        content = re.sub(
            r'href="styles-header\.css"',
            'href="../styles-header.css"',
            content
        )
        
        content = re.sub(
            r'href="cookie-override\.css"',
            'href="../cookie-override.css"',
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"✅ Исправлены пути в файле: {file_path}")
            return True
        else:
            print(f"ℹ️  Пути уже корректны в файле: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при обработке файла {file_path}: {e}")
        return False

def main():
    """Основная функция"""
    base_path = r"c:\Users\yashi\Desktop\Новая папка\FixTech-main"
    
    # Находим все HTML файлы в подпапках
    subdirectories = [
        'articles', 'gaids', 'guides-auto-electronics', 'guides-cameras',
        'guides-consoles', 'guides-laptops', 'guides-large-appliances',
        'guides-small-appliances', 'guides-smartphones'
    ]
    
    total_files = 0
    fixed_files = 0
    
    print("Начинаю исправление путей к скриптам в подпапках...")
    print()
    
    for subdir in subdirectories:
        subdir_path = os.path.join(base_path, subdir)
        if os.path.exists(subdir_path):
            print(f"Обработка папки: {subdir}")
            for filename in os.listdir(subdir_path):
                if filename.endswith('.html'):
                    file_path = os.path.join(subdir_path, filename)
                    total_files += 1
                    if fix_script_paths(file_path):
                        fixed_files += 1
        else:
            print(f"⚠️  Папка не найдена: {subdir}")
    
    print()
    print(f"Готово! Обработано файлов: {total_files}")
    print(f"Исправлено файлов: {fixed_files}")

if __name__ == "__main__":
    main()
