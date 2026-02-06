#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для добавления cookie-consent.js в HTML файлы, где он отсутствует
"""

import os
import re

# Список файлов, которые нужно обновить
files_to_update = [
    r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\gaids\Otkaz vstroyennogo kulera (yesli yest' aktivnoye okhlazhdeniye).html",
    r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\gaids\Peregrev iz-za raboty ryadom s batareyami ili pod solnechnymi luchami.html",
    r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-laptops\Na chto smotret v razbore bu noutbuka na foto obyavleniy.html",
    r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-large-appliances\dishwasher-not-removing-oil.html",
    r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-large-appliances\remove-plastic-object-from-dishwasher-drum.html",
    r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-small-appliances\Ochistka kofemashiny ot kofejnogo naleta.html",
    r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-small-appliances\Ustranenie slabogo raspylenija v uvlazhnitele.html"
]

def add_cookie_script(file_path):
    """Добавляет скрипт cookie-consent.js в HTML файл"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Проверяем, что скрипт еще не добавлен
        if 'cookie-consent.js' in content:
            print(f"Скрипт уже существует в файле: {file_path}")
            return True
        
        # Определяем путь к скрипту в зависимости от расположения файла
        script_path = '../cookie-consent.js' if ('gaids\\' in file_path or 'guides-' in file_path) else 'cookie-consent.js'
        
        # Ищем комментарий о cookie и добавляем скрипт после него
        cookie_comment_pattern = r'(<!-- Cookie Consent Banner -->\s*)'
        replacement = fr'\1<!-- Cookie Consent Script -->\n<script src="{script_path}"></script>\n'
        
        new_content = re.sub(cookie_comment_pattern, replacement, content)
        
        # Если не нашли комментарий, ищем конец footer
        if new_content == content:
            footer_pattern = r'(</footer>\s*)'
            replacement = fr'\1<!-- Cookie Consent Script -->\n<script src="{script_path}"></script>\n'
            new_content = re.sub(footer_pattern, replacement, content)
        
        # Если все еще не нашли место, добавляем в конец файла
        if new_content == content:
            new_content = content.rstrip() + f'\n<!-- Cookie Consent Script -->\n<script src="{script_path}"></script>\n'
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"✅ Скрипт добавлен в файл: {file_path}")
            return True
        else:
            print(f"⚠️  Не удалось найти место для вставки скрипта в файле: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при обработке файла {file_path}: {e}")
        return False

def main():
    """Основная функция"""
    print("Начинаю добавление скрипта cookie-consent.js в оставшиеся файлы...")
    print(f"Всего файлов для обработки: {len(files_to_update)}")
    print()
    
    success_count = 0
    for file_path in files_to_update:
        if add_cookie_script(file_path):
            success_count += 1
        print()
    
    print(f"Готово! Обработано файлов: {success_count}/{len(files_to_update)}")

if __name__ == "__main__":
    main()
