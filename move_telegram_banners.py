#!/usr/bin/env python3
import os
import re
import glob

def move_telegram_banner_to_end(file_path):
    """Перемещает существующий Telegram баннер в самый низ страницы"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Проверяем, есть ли баннер в файле
        if 'telegram-banner' not in content:
            print(f"Баннер не найден в {file_path}")
            return False
        
        # Находим и удаляем старый баннер
        banner_pattern = r'        <!-- Telegram рекламный баннер -->.*?</a>\s*'
        content = re.sub(banner_pattern, '', content, flags=re.DOTALL)
        
        # Ищем место для вставки в самый низ - перед </article> или </main>
        insert_patterns = [
            (r'(</article>)', 'before'),
            (r'(</main>)', 'before'),
            (r'(</div>\s*</section>)', 'before'),
            (r'(</section>)', 'before')
        ]
        
        insert_pos = None
        for pattern, position in insert_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                if position == 'before':
                    insert_pos = match.start()
                else:
                    insert_pos = match.end()
                break
        
        if insert_pos is None:
            # Если не нашли стандартные контейнеры, ищем перед footer
            footer_match = re.search(r'(\s*<footer)', content, re.IGNORECASE)
            if footer_match:
                insert_pos = footer_match.start()
            else:
                print(f"Не найдено подходящее место для вставки в {file_path}")
                return False
        
        # HTML баннера для вставки
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
        
        content = content[:insert_pos] + '\n' + telegram_banner_html + '\n' + content[insert_pos:]
        
        # Сохраняем файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Баннер перемещен в конец {file_path}")
        return True
            
    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")
        return False

def main():
    """Основная функция"""
    base_dir = "c:\\Users\\yashi\\Desktop\\Новая папка\\FixTech-main"
    
    # Находим все HTML файлы с баннерами
    guide_patterns = [
        os.path.join(base_dir, 'guides-*', '*.html'),
        os.path.join(base_dir, 'articles', '*.html'),
        os.path.join(base_dir, 'gaids', '*.html')
    ]
    
    html_files = []
    for pattern in guide_patterns:
        html_files.extend(glob.glob(pattern))
    
    print(f"Найдено {len(html_files)} файлов для перемещения баннеров")
    
    # Обрабатываем файлы
    success_count = 0
    for file_path in html_files:
        if move_telegram_banner_to_end(file_path):
            success_count += 1
    
    print(f"\nГотово! Баннер перемещен в {success_count} из {len(html_files)} файлов")

if __name__ == "__main__":
    main()
