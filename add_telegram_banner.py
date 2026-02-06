#!/usr/bin/env python3
import os
import re
import glob

def add_telegram_banner_to_file(file_path):
    """Добавляет Telegram баннер в середину контента HTML файла"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Проверяем, нет ли уже баннера
        if 'telegram-banner' in content:
            print(f"Баннер уже существует в {file_path}")
            return False
        
        # CSS стили для Telegram баннера
        telegram_css = '''    /* Telegram рекламный баннер */
    .telegram-banner {
      display: flex;
      justify-content: center;
      text-decoration: none;
      color: inherit;
      width: 100%;
      margin: 40px 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .telegram-banner-container {
      width: 100%;
      max-width: 500px;
      min-height: 120px;
      border-radius: 16px;
      background: linear-gradient(135deg, #0088cc 0%, #005f8f 100%);
      border: 1px solid #005f8f;
      display: flex;
      align-items: center;
      padding: 20px;
      box-shadow: 0 4px 16px rgba(0, 136, 204, 0.2);
      overflow: hidden;
      box-sizing: border-box;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .telegram-banner-container:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 136, 204, 0.3);
    }

    .telegram-logo {
      width: 60px;
      height: 60px;
      min-width: 60px;
      background: #ffffff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 20px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .telegram-logo svg {
      width: 32px;
      height: 32px;
      fill: #0088cc;
    }

    .telegram-content {
      flex: 1;
      color: #ffffff;
    }

    .telegram-title {
      font-size: 16px;
      font-weight: 600;
      margin: 0 0 8px 0;
      line-height: 1.3;
    }

    .telegram-subtitle {
      font-size: 14px;
      opacity: 0.9;
      margin: 0 0 12px 0;
      line-height: 1.4;
    }

    .telegram-button {
      display: inline-flex;
      align-items: center;
      padding: 8px 16px;
      background: #ffffff;
      color: #0088cc;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 600;
      text-decoration: none;
      transition: background 0.2s ease, transform 0.2s ease;
    }

    .telegram-button:hover {
      background: #f0f8ff;
      transform: scale(1.05);
    }

    .telegram-button svg {
      width: 16px;
      height: 16px;
      margin-left: 6px;
      fill: #0088cc;
    }

    /* Адаптив для мобильных */
    @media (max-width: 480px) {
      .telegram-banner-container {
        max-width: 100%;
        margin: 20px 0;
        padding: 15px;
        min-height: 100px;
      }

      .telegram-logo {
        width: 50px;
        height: 50px;
        min-width: 50px;
        margin-right: 15px;
      }

      .telegram-logo svg {
        width: 26px;
        height: 26px;
      }

      .telegram-title {
        font-size: 14px;
      }

      .telegram-subtitle {
        font-size: 12px;
      }

      .telegram-button {
        font-size: 12px;
        padding: 6px 12px;
      }
    }
'''
        
        # HTML баннера
        telegram_banner_html = '''        <!-- Telegram рекламный баннер -->
        <a href="https://t.me/RepairoRU" target="_blank" rel="noopener noreferrer" class="telegram-banner">
          <div class="telegram-banner-container">
            <div class="telegram-logo">
              <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.56c-.21 2.22-1.12 7.58-1.58 10.06-.19 1.07-.57 1.43-.94 1.46-.8.07-1.4-.52-2.17-1.03-1.21-.79-1.89-1.28-3.06-2.05-1.35-.87-.47-1.35.3-2.13.2-.21 3.71-3.39 3.77-3.68.01-.04.01-.18-.07-.26s-.2-.05-.29-.03c-.12.03-2.11 1.34-5.95 3.93-.56.38-1.07.57-1.53.56-.5-.01-1.47-.28-2.19-.51-.88-.28-1.58-.43-1.52-.91.03-.25.38-.51 1.04-.78 4.07-1.77 6.78-2.94 8.13-3.51 3.88-1.62 4.68-1.9 5.19-1.91.12 0 .37.03.54.17.14.12.18.28.2.44-.01.06 0 .11-.01.17z"/>
              </svg>
            </div>
            <div class="telegram-content">
              <div class="telegram-title">Новости из мира технологий</div>
              <div class="telegram-subtitle">В нашем новом Telegram-канале. Подписывайтесь и будьте в числе первых!</div>
              <div class="telegram-button">
                Подписаться
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.56c-.21 2.22-1.12 7.58-1.58 10.06-.19 1.07-.57 1.43-.94 1.46-.8.07-1.4-.52-2.17-1.03-1.21-.79-1.89-1.28-3.06-2.05-1.35-.87-.47-1.35.3-2.13.2-.21 3.71-3.39 3.77-3.68.01-.04.01-.18-.07-.26s-.2-.05-.29-.03c-.12.03-2.11 1.34-5.95 3.93-.56.38-1.07.57-1.53.56-.5-.01-1.47-.28-2.19-.51-.88-.28-1.58-.43-1.52-.91.03-.25.38-.51 1.04-.78 4.07-1.77 6.78-2.94 8.13-3.51 3.88-1.62 4.68-1.9 5.19-1.91.12 0 .37.03.54.17.14.12.18.28.2.44-.01.06 0 .11-.01.17z"/>
                </svg>
              </div>
            </div>
          </div>
        </a>
'''
        
        # Добавляем CSS стили перед </style>
        content = re.sub(r'(\s*</style>)', f'\n{telegram_css}\n\\1', content)
        
        # Находим середину контента для вставки баннера
        # Ищем разные структуры контента
        article_patterns = [
            r'<div class="guide-content">',
            r'<article class="guide-content">',
            r'<div class="content">',
            r'<main>',
            r'<div class="article-content">',
            r'<section class="content">'
        ]
        
        article_match = None
        for pattern in article_patterns:
            article_match = re.search(pattern, content)
            if article_match:
                break
        
        if article_match:
            # Находим все h2 заголовки в статье
            h2_pattern = r'<h2[^>]*>(.*?)</h2>'
            h2_matches = list(re.finditer(h2_pattern, content[article_match.end():], re.DOTALL))
            
            if len(h2_matches) >= 2:
                # Вставляем баннер после предпоследнего h2 заголовка (ближе к концу)
                if len(h2_matches) >= 3:
                    target_h2 = h2_matches[-2]  # Предпоследний заголовок
                else:
                    target_h2 = h2_matches[0]   # Если заголовков мало, после первого
                
                insert_pos = article_match.end() + target_h2.end()
                
                # Ищем конец абзаца после h2 для более органичной вставки
                paragraph_pattern = r'(?s)</h2>.*?</p>'
                paragraph_match = re.search(paragraph_pattern, content[article_match.end() + target_h2.end():article_match.end() + target_h2.end() + 2000])
                
                if paragraph_match:
                    insert_pos = article_match.end() + target_h2.end() + paragraph_match.end()
                
                content = content[:insert_pos] + '\n' + telegram_banner_html + '\n' + content[insert_pos:]
                
                # Сохраняем файл
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                print(f"Баннер добавлен в {file_path}")
                return True
            else:
                print(f"Недостаточно h2 заголовков в {file_path}")
                return False
        else:
            print(f"Не найден article content в {file_path}")
            return False
            
    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")
        return False

def main():
    """Основная функция"""
    base_dir = "c:\\Users\\yashi\\Desktop\\Новая папка\\FixTech-main"
    
    # Исключенные файлы
    excluded_files = {
        'index.html',
        'tv.html',
        'cameras.html', 
        'consoles.html',
        'laptops.html',
        'smartphones.html',
        'small-appliances.html',
        'large-appliances.html',
        'auto-electronics.html',
        'articles.html'
    }
    
    # Находим все HTML файлы в папках guides-*
    guide_patterns = [
        os.path.join(base_dir, 'guides-*.html'),
        os.path.join(base_dir, 'guides-*', '*.html'),
        os.path.join(base_dir, 'articles', '*.html'),
        os.path.join(base_dir, 'gaids', '*.html')
    ]
    
    html_files = []
    for pattern in guide_patterns:
        html_files.extend(glob.glob(pattern))
    
    # Фильтруем исключенные файлы
    files_to_process = []
    for file_path in html_files:
        filename = os.path.basename(file_path)
        if filename not in excluded_files:
            files_to_process.append(file_path)
    
    print(f"Найдено {len(files_to_process)} файлов для обработки")
    
    # Обрабатываем файлы
    success_count = 0
    for file_path in files_to_process:
        if add_telegram_banner_to_file(file_path):
            success_count += 1
    
    print(f"\nГотово! Баннер добавлен в {success_count} из {len(files_to_process)} файлов")

if __name__ == "__main__":
    main()
