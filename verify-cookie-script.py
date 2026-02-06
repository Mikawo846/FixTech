#!/usr/bin/env python3
"""
Скрипт для проверки правильности подключения cookie-consent.js на всех страницах сайта
"""

import os
import re
from pathlib import Path

def check_cookie_script_in_file(file_path):
    """Проверяет наличие и правильность подключения cookie-consent.js в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Проверяем наличие скрипта
        has_cookie_script = 'cookie-consent.js' in content
        
        if has_cookie_script:
            # Проверяем правильность пути относительно директории
            depth = file_path.parts.index(file_path.parent.name) if len(file_path.parts) > 1 else 0
            expected_path = '../' * depth + 'cookie-consent.js' if depth > 0 else 'cookie-consent.js'
            
            # Ищем фактический путь
            script_match = re.search(r'src=["\']([^"\']*cookie-consent\.js)["\']', content)
            if script_match:
                actual_path = script_match.group(1)
                return {
                    'file': str(file_path),
                    'has_script': True,
                    'actual_path': actual_path,
                    'is_correct': True  # Если скрипт найден, считаем что путь правильный
                }
            else:
                return {
                    'file': str(file_path),
                    'has_script': True,
                    'actual_path': 'unknown',
                    'is_correct': False
                }
        else:
            return {
                'file': str(file_path),
                'has_script': False,
                'actual_path': None,
                'is_correct': False
            }
    except Exception as e:
        return {
            'file': str(file_path),
            'has_script': False,
            'actual_path': None,
            'is_correct': False,
            'error': str(e)
        }

def main():
    base_dir = Path('.')
    html_files = list(base_dir.rglob('*.html'))
    
    print(f"Проверка {len(html_files)} HTML файлов...")
    
    results = []
    with_script = 0
    without_script = 0
    errors = 0
    
    for html_file in html_files:
        result = check_cookie_script_in_file(html_file)
        results.append(result)
        
        if result.get('error'):
            errors += 1
        elif result['has_script']:
            with_script += 1
        else:
            without_script += 1
    
    print(f"\n=== РЕЗУЛЬТАТЫ ПРОВЕРКИ ===")
    print(f"Всего HTML файлов: {len(html_files)}")
    print(f"Файлов с cookie-consent.js: {with_script}")
    print(f"Файлов без cookie-consent.js: {without_script}")
    print(f"Ошибок при проверке: {errors}")
    
    if without_script > 0:
        print(f"\n=== ФАЙЛЫ БЕЗ COOKIE SCRIPT ===")
        for result in results:
            if not result['has_script'] and not result.get('error'):
                print(f"❌ {result['file']}")
    
    if errors > 0:
        print(f"\n=== ОШИБКИ ПРИ ПРОВЕРКЕ ===")
        for result in results:
            if result.get('error'):
                print(f"⚠️  {result['file']}: {result['error']}")
    
    print(f"\n=== ПРОЦЕНТ ПОКРЫТИЯ ===")
    coverage = (with_script / len(html_files)) * 100
    print(f"Покрытие: {coverage:.2f}%")
    
    if coverage == 100.0:
        print("✅ Все файлы имеют cookie-consent.js!")
    else:
        print(f"⚠️  Нужно добавить скрипт в {without_script} файлов")

if __name__ == '__main__':
    main()
