#!/usr/bin/env python3
"""
Скрипт для массового удаления маркеров конфликта слияния из HTML файлов
"""

import os
import re
from pathlib import Path

# Путь к корневой директории проекта
ROOT_DIR = Path(__file__).parent

def fix_merge_conflicts_in_file(file_path):
    """Исправляет маркеры конфликта в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Удаляем маркеры конфликта и содержимое между ними
        # Паттерн для удаления <<<<<<< HEAD ... ======= ... >>>>>>> hash
        conflict_pattern = r'<<<<<<< HEAD.*?=======.*?>>>>>>> [a-f0-9]+'
        
        # Заменяем все вхождения паттерна на пустую строку
        content = re.sub(conflict_pattern, '', content, flags=re.DOTALL)
        
        # Также удаляем отдельные маркеры если они остались
        content = re.sub(r'<<<<<<< HEAD', '', content)
        content = re.sub(r'=======', '', content)
        content = re.sub(r'>>>>>>> [a-f0-9]+', '', content)
        
        # Если содержимое изменилось, сохраняем файл
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Исправлен: {file_path}")
            return True
        else:
            print(f"⏭️  Пропуск: {file_path} (конфликтов не найдено)")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при обработке {file_path}: {e}")
        return False

def main():
    """Основная функция"""
    print("🔧 Начинаю исправление конфликтов слияния во всех HTML файлах...")
    
    # Находим все HTML файлы
    html_files = list(ROOT_DIR.rglob('*.html'))
    
    print(f"📁 Найдено HTML файлов: {len(html_files)}")
    
    fixed_count = 0
    error_count = 0
    
    for html_file in html_files:
        if fix_merge_conflicts_in_file(html_file):
            fixed_count += 1
        else:
            # Проверяем, была ли ошибка или просто не найдено конфликтов
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if '<<<<<<<' in content:
                    error_count += 1
            except:
                error_count += 1
    
    print(f"\n📊 Результаты:")
    print(f"✅ Исправлено файлов: {fixed_count}")
    print(f"❌ Ошибок: {error_count}")
    print(f"🎉 Готово! Конфликты слияния устранены.")

if __name__ == '__main__':
    main()
