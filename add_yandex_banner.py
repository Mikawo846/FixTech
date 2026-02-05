#!/usr/bin/env python3
"""
Скрипт для массового добавления статического рекламного баннера
во все HTML файлы проекта, кроме главной страницы (index.html)
"""

import os
import re
from pathlib import Path

# Путь к корневой директории проекта
ROOT_DIR = Path(__file__).parent

# HTML код баннера для вставки
BANNER_HTML = '''        <!-- Яндекс Маркет рекламный блок -->
        <a href="https://market.yandex.ru/catalog--bytovaia-tekhnika/54419/list?hid=198118&rs=eJwzUvjEKMvBILDwEKsEg8Kzbh6Nw4dZNS4D8c7lFhp9c1-wAQC3uAwP&clid=14635360&refid=rbck8fgamv681iu59go3iqxwddedl4x9&erid=5jtCeReNx12oajxS2bzShmZ&mclid=1003&distr_type=7&utm_source=partner_network&pp=900&utm_medium=link_list&utm_campaign=14635360"
           target="_blank"
           rel="noopener noreferrer sponsored"
           class="ym-hero-link">
          <div class="ym-hero-banner">
            <div class="ym-hero-images">
              <div class="ym-hero-image">
                <img src="https://avatars.mds.yandex.net/get-mpic/14770882/2a00000197f4dbee777f8afddccaf44faa53/optimize"
                     alt="Распродажа бытовой электроники 1">
              </div>
              <div class="ym-hero-image">
                <img src="https://avatars.mds.yandex.net/get-mpic/15580298/img_id8867318964670654684.jpeg/optimize"
                     alt="Распродажа бытовой электроники 2">
              </div>
              <div class="ym-hero-image">
                <img src="https://avatars.mds.yandex.net/get-mpic/10096780/2a000001953b534fed2494e0b30fadd9b458/optimize"
                     alt="Распродажа бытовой электроники 3">
              </div>
            </div>
            <div class="ym-hero-content">
              <h3 class="ym-hero-title">Распродажа бытовой электроники на Яндекс Маркете</h3>
              <div class="ym-hero-top">
                <div class="ym-hero-rating">
                  ⭐ Выгодные предложения
                  <span class="ym-hero-rating-count">Скидки до 50%</span>
                </div>
              </div>
              <button class="ym-hero-button">За скидками</button>
            </div>
          </div>
          <div class="ym-hero-legal">
            Реклама. ООО "ЯНДЕКС", ИНН 7736207543. clid: 14635360, erid: 5jtCeReNx12oajxS2bzShmZ
          </div>
        </a>'''

# CSS стили для баннера
BANNER_CSS = '''    /* Яндекс Маркет рекламный баннер */
    .ym-hero-link {
      display: block;
      text-decoration: none;
      color: inherit;
      max-width: 100%;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* Горизонтальный баннер-карточка */
    .ym-hero-banner {
      width: 100%;
      max-width: 600px;
      min-height: 140px;
      border-radius: 16px;
      background: #ffffff;
      border: 1px solid #e5e7eb;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
      overflow: hidden;
      box-sizing: border-box;
      margin: 40px auto;
    }

    /* Контейнер для изображений */
    .ym-hero-images {
      display: flex;
      height: 120px;
      overflow: hidden;
    }

    .ym-hero-image {
      flex: 1;
      min-width: 0;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      border-right: 1px solid #e5e7eb;
      background: #f8f9fa;
    }

    .ym-hero-image:last-child {
      border-right: none;
    }

    .ym-hero-image img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      transition: transform 0.3s ease;
      background: #f8f9fa;
    }

    .ym-hero-image:hover img {
      transform: scale(1.02);
    }

    /* Правая часть: контент */
    .ym-hero-content {
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
    }

    /* Название товара */
    .ym-hero-title {
      font-size: 14px;
      font-weight: 600;
      color: #111827;
      line-height: 1.3;
      margin: 0 0 4px 0;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    /* Рейтинг */
    .ym-hero-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .ym-hero-rating {
      font-size: 13px;
      font-weight: 500;
      color: #111827;
      background: #f9fafb;
      border-radius: 999px;
      padding: 4px 10px;
    }

    .ym-hero-rating-count {
      color: #6b7280;
    }

    /* Фиолетовая кнопка */
    .ym-hero-button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 9px 16px;
      border-radius: 999px;
      border: none;
      background: #6a00ff;
      color: #ffffff;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(88, 28, 135, 0.35);
      transition: background 0.15s ease, transform 0.15s ease,
                  box-shadow 0.15s ease;
    }

    .ym-hero-button::after {
      content: "→";
      margin-left: 6px;
      font-size: 14px;
    }

    .ym-hero-button:hover {
      background: #7c3aed;
      transform: translateY(-1px);
      box-shadow: 0 4px 10px rgba(88, 28, 135, 0.45);
    }

    /* Юридический блок */
    .ym-hero-legal {
      margin-top: 6px;
      max-width: 600px;
      font-size: 11px;
      line-height: 1.3;
      color: #6b7280;
      margin-left: auto;
      margin-right: auto;
    }

    /* Адаптив */
    @media (max-width: 480px) {
      .ym-hero-banner {
        max-width: 100%;
        margin: 20px 0;
      }

      .ym-hero-images {
        height: 100px;
      }

      .ym-hero-content {
        padding: 12px 12px;
      }

      .ym-hero-title {
        font-size: 13px;
      }

      .ym-hero-button {
        font-size: 13px;
        padding: 8px 14px;
      }

      .ym-hero-legal {
        font-size: 10px;
      }
    }'''

def has_banner_css(content):
    """Проверяет, есть ли в файле CSS стили для баннера"""
    return '.ym-hero-link' in content or 'Яндекс Маркет рекламный баннер' in content

def add_banner_css(content):
    """Добавляет CSS стили для баннера в секцию <style>"""
    # Ищем конец секции style
    style_pattern = r'(\s*</style>)'
    
    if re.search(style_pattern, content):
        # Добавляем CSS перед закрывающим тегом </style>
        return re.sub(style_pattern, f'\n{BANNER_CSS}\n\\1', content)
    else:
        # Если секции style нет, добавляем ее в head
        head_pattern = r'(\s*</head>)'
        css_with_tags = f'\n  <style>\n{BANNER_CSS}\n  </style>\n'
        return re.sub(head_pattern, f'{css_with_tags}\\1', content)

def find_banner_insertion_point(content):
    """Находит подходящее место для вставки баннера"""
    lines = content.split('\n')
    
    # Ищем различные паттерны для определения места вставки
    patterns = [
        # После таблицы
        r'</table>',
        # После параграфа с описанием
        r'</p>\s*$',
        # После заголовка h2
        r'</h2>',
        # После div с классом guide-content
        r'<div class="guide-content">',
    ]
    
    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.search(pattern, line):
                # Пропускаем первые несколько строк (head section)
                if i > 20:
                    return i + 1
    
    # Если не нашли подходящего места, вставляем после первого h2
    for i, line in enumerate(lines):
        if '<h2>' in line and i > 20:
            return i + 2
    
    # Если ничего не нашли, вставляем в середине контента
    return len(lines) // 2

def add_banner_to_file(file_path):
    """Добавляет баннер в HTML файл"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, нет ли уже баннера
        if 'ym-hero-banner' in content:
            print(f"⏭️  Пропуск: {file_path} (баннер уже есть)")
            return True
        
        # Добавляем CSS стили если их нет
        if not has_banner_css(content):
            content = add_banner_css(content)
        
        # Находим место для вставки баннера
        insertion_point = find_banner_insertion_point(content)
        lines = content.split('\n')
        
        # Вставляем баннер
        lines.insert(insertion_point, BANNER_HTML)
        updated_content = '\n'.join(lines)
        
        # Сохраняем файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Добавлен баннер: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обработке {file_path}: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Начинаю добавление статического баннера во все HTML файлы...")
    
    # Находим все HTML файлы
    html_files = list(ROOT_DIR.rglob('*.html'))
    
    # Исключаем главную страницу
    html_files = [f for f in html_files if f.name != 'index.html']
    
    print(f"📁 Найдено HTML файлов: {len(html_files)}")
    
    success_count = 0
    error_count = 0
    
    for html_file in html_files:
        if add_banner_to_file(html_file):
            success_count += 1
        else:
            error_count += 1
    
    print(f"\n📊 Результаты:")
    print(f"✅ Успешно обработано: {success_count}")
    print(f"❌ Ошибок: {error_count}")
    print(f"🎉 Готово! Баннер добавлен во все файлы.")

if __name__ == '__main__':
    main()
