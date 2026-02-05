#!/usr/bin/env python3
"""
Массовое удаление статических cookie-баннеров из HTML файлов
"""

import os
import re
import glob

def remove_cookie_banner_from_file(file_path):
    """Удаляет статический cookie-баннер из одного файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # Паттерны для поиска и удаления cookie-баннера
        patterns = [
            # Полный баннер с inline стилями
            r'<div id="cookie-banner"[^>]*>.*?</div>\s*</div>\s*(?=<!--|</body>|</html>|<script|$)',
            
            # Баннер с классом cookie-banner
            r'<div[^>]*class="cookie-banner[^"]*"[^>]*>.*?</div>\s*</div>\s*(?=<!--|</body>|</html>|<script|$)',
            
            # Упрощенный паттерн для cookie-banner
            r'<!-- Cookie Consent Banner -->\s*<div[^>]*id="cookie-banner"[^>]*>.*?</div>\s*</div>',
            
            # Альтернативный вариант
            r'<div[^>]*id="cookie-banner"[^>]*class="[^"]*cookie-banner[^"]*"[^>]*>.*?</div>\s*</div>'
        ]
        
        removed_any = False
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            if matches:
                for match in matches:
                    content = content.replace(match, '')
                    removed_any = True
                    print(f"Удален баннер из {file_path}")
        
        # Дополнительная очистка - удаляем лишние пустые строки
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if removed_any or content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")
        return False

def main():
    """Основная функция"""
    print("Начинаю массовое удаление cookie-баннеров...")
    
    # Ищем все HTML файлы
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Найдено {len(html_files)} HTML файлов")
    
    removed_count = 0
    processed_count = 0
    
    for file_path in html_files:
        processed_count += 1
        if remove_cookie_banner_from_file(file_path):
            removed_count += 1
        
        if processed_count % 100 == 0:
            print(f"Обработано {processed_count} файлов, удалено баннеров: {removed_count}")
    
    print(f"\nГотово!")
    print(f"Всего обработано файлов: {processed_count}")
    print(f"Удалено баннеров из файлов: {removed_count}")

if __name__ == "__main__":
    main()
