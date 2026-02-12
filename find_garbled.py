import os
from pathlib import Path

guides_dir = Path(r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-laptops")

for file_path in guides_dir.glob("*.html"):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            if "footer__text" in content:
                lines = content.split('\n')
                for line in lines:
                    if "footer__text" in line and "???????? ????????????? ??????????? ? 2024 ????" in line:
                        print(file_path.name)
                        break
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
