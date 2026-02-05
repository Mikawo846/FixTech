#!/usr/bin/env python3
import os
import re
import glob

# Только CSS стили для статического баннера
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

# Статический HTML баннер без скриптов
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

def add_banner_to_file(file_path):
    """Добавляет статический баннер в HTML файл"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, есть ли уже баннер в файле
        if 'ym-hero-link' in content:
            print(f"Пропускаем {file_path} - баннер уже есть")
            return False
        
        # Находим место для добавления CSS (перед </style>)
        css_pattern = r'(\s*</style>)'
        if re.search(css_pattern, content):
            content = re.sub(css_pattern, f'\n\n{BANNER_CSS}\n\\1', content)
        else:
            # Если нет тега style, добавляем CSS в head
            head_pattern = r'(</head>)'
            if re.search(head_pattern, content):
                content = re.sub(head_pattern, f'<style>\n{BANNER_CSS}\n</style>\n\\1', content)
        
        # Находим место для добавления HTML баннера (после h1 или после первого изображения)
        # Ищем после первого h1 или после первого div class="guide-image-block"
        html_patterns = [
            r'(<h1[^>]*>.*?</h1>\s*</div>\s*)',
            r'(<div class="guide-image-block">.*?</div>\s*)'
        ]
        
        banner_added = False
        for pattern in html_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, f'\\1\n\n{BANNER_HTML}\n\n', content, flags=re.DOTALL)
                banner_added = True
                break
        
        # Если не нашли подходящего места, добавляем после первого <h1>
        if not banner_added:
            h1_pattern = r'(<h1[^>]*>.*?</h1>)'
            if re.search(h1_pattern, content, re.DOTALL):
                content = re.sub(h1_pattern, f'\\1\n\n{BANNER_HTML}\n\n', content, flags=re.DOTALL)
        
        # Записываем измененный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Добавлен статический баннер в {file_path}")
        return True
        
    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")
        return False

def main():
    """Главная функция"""
    # Находим все HTML файлы в папках guides-*
    base_dir = "."
    guide_dirs = glob.glob(os.path.join(base_dir, "guides-*"))
    
    total_files = 0
    processed_files = 0
    
    for guide_dir in guide_dirs:
        html_files = glob.glob(os.path.join(guide_dir, "*.html"))
        for html_file in html_files:
            total_files += 1
            if add_banner_to_file(html_file):
                processed_files += 1
    
    print(f"\nОбработка завершена!")
    print(f"Всего файлов: {total_files}")
    print(f"Обработано файлов: {processed_files}")

if __name__ == "__main__":
    main()
