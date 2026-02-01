import os
import re

# --- НАСТРОЙКИ ---

# 1. ГДЕ ИСКАТЬ:
# Укажите путь к папке, ГДЕ лежат ваши файлы/ноутбуки, которые нужно сканировать.
# Если скрипт лежит прямо в этой папке, оставьте "."
SEARCH_FOLDER = "." 

# 2. ЧТО ИСКАТЬ (часть домена):
OLD_DOMAIN_PART = "postimg.cc" 

# 3. КУДА СОХРАНИТЬ РЕЗУЛЬТАТ (ваш точный путь):
OUTPUT_FILE = r"C:\Users\yashi\Desktop\Новая папка\FixTech-main\laptop_images_list.txt"

# Регулярка для поиска URL
URL_PATTERN = re.compile(r'(https?://[^\s"\'<>)]*' + re.escape(OLD_DOMAIN_PART) + r'[^\s"\'<>)]*)')

def scan_files():
    found_urls = set()
    files_scanned = 0
    
    print(f"🔍 Сканирую папку: {os.path.abspath(SEARCH_FOLDER)}")
    print(f"🎯 Ищу ссылки с: '{OLD_DOMAIN_PART}'")

    # Убедимся, что папка для сохранения результата существует
    output_dir = os.path.dirname(OUTPUT_FILE)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"📁 Создана папка для отчета: {output_dir}")
        except OSError as e:
            print(f"❌ Ошибка создания папки {output_dir}: {e}")
            return

    for root, dirs, files in os.walk(SEARCH_FOLDER):
        for filename in files:
            # Не сканируем сам файл отчета, если он вдруг лежит в сканируемой папке
            if os.path.abspath(os.path.join(root, filename)) == os.path.abspath(OUTPUT_FILE):
                continue
            
            # Не сканируем сам скрипт
            if filename == os.path.basename(__file__):
                continue

            filepath = os.path.join(root, filename)
            files_scanned += 1
            
            try:
                # Открываем с errors='ignore', чтобы не падать на бинарных файлах (картинках, pyc и т.д.)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = URL_PATTERN.findall(content)
                    if matches:
                        for url in matches:
                            clean_url = url.rstrip('.,;:')
                            found_urls.add(clean_url)
            except Exception as e:
                # Тихо пропускаем ошибки чтения (например, если файл занят системой)
                pass

    sorted_urls = sorted(list(found_urls))
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(sorted_urls))
        
        print(f"\n✅ УСПЕХ!")
        print(f"📂 Проверено файлов: {files_scanned}")
        print(f"🔗 Найдено ссылок: {len(sorted_urls)}")
        print(f"💾 Файл сохранен: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"\n❌ Ошибка при записи файла {OUTPUT_FILE}: {e}")

if __name__ == '__main__':
    scan_files()
