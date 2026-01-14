#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для автоматического выравнивания CSS-свойств по двоеточию.
Использование: python align_css.py <input_file> <output_file>
"""

import re
import sys
from pathlib import Path

def align_css_properties(css_content):
    """
    Выравнивает CSS-свойства в каждом правиле по двоеточию.
    """
    # Регулярное выражение для поиска CSS правил
    rule_pattern = re.compile(r'([^{}]+)\{([^{}]+)\}', re.DOTALL)
    
    def align_rule(match):
        selector = match.group(1).strip()
        properties = match.group(2).strip()
        
        if not properties:
            return f"{selector} {{}}" 
        
        # Разбиваем на отдельные свойства
        prop_lines = [line.strip() for line in properties.split(';') if line.strip()]
        
        if not prop_lines:
            return f"{selector} {{}}" 
        
        # Находим максимальную длину имени свойства
        max_prop_len = 0
        parsed_props = []
        
        for prop in prop_lines:
            if ':' in prop:
                parts = prop.split(':', 1)
                prop_name = parts[0].strip()
                prop_value = parts[1].strip() if len(parts) > 1 else ''
                parsed_props.append((prop_name, prop_value))
                max_prop_len = max(max_prop_len, len(prop_name))
            else:
                # Комментарии или другое
                parsed_props.append((prop, None))
        
        # Формируем выровненные свойства
        aligned_lines = []
        for item in parsed_props:
            if item[1] is not None:  # Это свойство
                prop_name, prop_value = item
                padding = ' ' * (max_prop_len - len(prop_name))
                aligned_lines.append(f"    {prop_name}{padding} : {prop_value};")
            else:  # Комментарий или другое
                aligned_lines.append(f"    {item[0]}")
        
        result = f"{selector} {{\n" + "\n".join(aligned_lines) + "\n}}"
        return result
    
    # Применяем выравнивание ко всем правилам
    aligned_css = rule_pattern.sub(align_rule, css_content)
    
    return aligned_css

def process_file(input_path, output_path=None):
    """
    Обрабатывает файл CSS или HTML с встроенными стилями.
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Ошибка: Файл {input_path} не найден")
        return
    
    # Читаем содержимое
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем тип файла
    if input_file.suffix == '.css':
        # Обрабатываем весь файл
        aligned_content = align_css_properties(content)
    elif input_file.suffix == '.html':
        # Обрабатываем только содержимое <style> тегов
        def align_style_tag(match):
            css_content = match.group(1)
            return f"<style>\n{align_css_properties(css_content)}\n</style>"
        
        aligned_content = re.sub(
            r'<style[^>]*>\s*([\s\S]*?)\s*</style>',
            align_style_tag,
            content,
            flags=re.IGNORECASE
        )
    else:
        print(f"Предупреждение: Неизвестное расширение файла {input_file.suffix}")
        aligned_content = content
    
    # Определяем выходной файл
    if output_path is None:
        output_path = input_file.parent / f"{input_file.stem}_aligned{input_file.suffix}"
    else:
        output_path = Path(output_path)
    
    # Записываем результат
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(aligned_content)
    
    print(f"✓ Файл обработан: {output_path}")
    print(f"  Размер до:  {len(content)} байт")
    print(f"  Размер после: {len(aligned_content)} байт")

def process_directory(directory_path):
    """
    Обрабатывает все CSS и HTML файлы в директории.
    """
    directory = Path(directory_path)
    
    if not directory.is_dir():
        print(f"Ошибка: {directory_path} не является директорией")
        return
    
    # Находим все CSS и HTML файлы
    css_files = list(directory.rglob('*.css'))
    html_files = list(directory.rglob('*.html'))
    
    all_files = css_files + html_files
    
    if not all_files:
        print("Файлы .css или .html не найдены")
        return
    
    print(f"Найдено файлов: {len(all_files)}")
    print()
    
    for file in all_files:
        try:
            process_file(file)
        except Exception as e:
            print(f"✗ Ошибка при обработке {file}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python align_css.py <файл.css|файл.html>")
        print("  python align_css.py <файл.css> <выходной_файл.css>")
        print("  python align_css.py <директория>  # обработать все файлы")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    path = Path(input_path)
    
    if path.is_dir():
        process_directory(input_path)
    else:
        process_file(input_path, output_path)

if __name__ == '__main__':
    main()
