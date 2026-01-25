import os
import re

fixed_count = 0

for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    original = f.read()
                
                # Удаляем только строки с маркерами конфликтов
                fixed = re.sub(r'^<<<<<<< HEAD\n', '', original, flags=re.MULTILINE)
                fixed = re.sub(r'^=======\n', '', fixed, flags=re.MULTILINE)
                fixed = re.sub(r'^>>>>>>> [a-f0-9]+.*\n', '', fixed, flags=re.MULTILINE)
                
                if fixed != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(fixed)
                    fixed_count += 1
                    print(f"Исправлен: {filepath}")
            except Exception as e:
                print(f"Ошибка в {filepath}: {e}")

print(f"\nГотово! Исправлено файлов: {fixed_count}")
