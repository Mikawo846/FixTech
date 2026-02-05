#!/usr/bin/env python3
import os
import re

def fix_footer_paths(file_path):
    """Исправляет относительные пути в футере для корневых файлов"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Заменяем ../ на пустую строку для всех путей в футере
        content = re.sub(r'href="\.\.\/', 'href="', content)
        
        # Записываем изменения если контент изменился
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Исправлены пути: {file_path}")
            return True
        else:
            print(f"⏭️  Пропущен (без изменений): {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при обработке {file_path}: {e}")
        return False

def main():
    # Список корневых HTML файлов
    root_files = [
        'index.html',
        'smartphones.html',
        'laptops.html', 
        'tv.html',
        'cameras.html',
        'consoles.html',
        'auto-electronics.html',
        'large-appliances.html',
        'small-appliances.html',
        'articles.html'
    ]
    
    print(f"🔧 Проверка корневых файлов...")
    print()
    
    updated_count = 0
    
    for html_file in root_files:
        if os.path.exists(html_file):
            if fix_footer_paths(html_file):
                updated_count += 1
        else:
            print(f"⚠️  Файл не найден: {html_file}")
    
    print()
    print(f"🎉 Готово! Исправлено файлов: {updated_count}")

if __name__ == "__main__":
    main()
