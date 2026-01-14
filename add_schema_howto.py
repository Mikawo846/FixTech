#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

def extract_title_from_h1(content):
    """Extract text from first <h1> tag"""
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    if h1_match:
        # Remove HTML tags from h1 content
        h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1))
        return h1_text.strip()
    return ""

def extract_meta_description(content):
    """Extract content from meta description"""
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if desc_match:
        return desc_match.group(1).strip()
    return ""

def extract_first_image(content):
    """Extract first image URL from page"""
    img_match = re.search(r'<img[^>]*src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if img_match:
        src = img_match.group(1)
        # Convert relative URLs to absolute
        if src.startswith('./'):
            src = src[2:]
        elif src.startswith('/'):
            src = src[1:]
        return f"https://repairo.ru/{src}"
    return ""

def extract_h2_headings(content, max_steps=8):
    """Extract h2 headings as steps"""
    h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL | re.IGNORECASE)
    steps = []
    
    for i, h2_content in enumerate(h2_matches[:max_steps]):
        # Remove HTML tags from h2 content
        step_text = re.sub(r'<[^>]+>', '', h2_content).strip()
        if step_text:
            steps.append({
                "@type": "HowToStep",
                "name": step_text,
                "text": step_text,
                "url": f"#step-{i+1}"
            })
    
    return steps

def generate_howto_schema(content):
    """Generate HowTo schema.org JSON-LD"""
    # Extract required data
    name = extract_title_from_h1(content)
    description = extract_meta_description(content)
    image = extract_first_image(content)
    steps = extract_h2_headings(content)
    
    if not name or not steps:
        return None
    
    # Build schema
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description or f"Пошаговая инструкция по ремонту: {name}",
        "totalTime": "PT30M",
        "step": steps
    }
    
    # Add image if found
    if image:
        schema["image"] = image
    
    return schema

def insert_schema_before_body(content, schema):
    """Insert schema JSON-LD before </body> tag"""
    if not schema:
        return content, False
    
    # Convert schema to JSON string
    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
    
    # Create script tag
    script_tag = f'\n<script type="application/ld+json">\n{schema_json}\n</script>\n'
    
    # Find </body> tag
    body_end_match = re.search(r'</body>', content, re.IGNORECASE)
    if not body_end_match:
        return content, False
    
    # Insert before </body>
    insert_pos = body_end_match.start()
    new_content = content[:insert_pos] + script_tag + content[insert_pos:]
    
    return new_content, True

def process_html_file(file_path):
    """Process single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if schema already exists
        if re.search(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>', content, re.DOTALL | re.IGNORECASE):
            return False, "Schema already exists", 0
        
        # Generate schema
        schema = generate_howto_schema(content)
        if not schema:
            return False, "Could not generate schema (no H1 or H2 found)", 0
        
        # Insert schema
        new_content, inserted = insert_schema_before_body(content, schema)
        
        if inserted:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            steps_count = len(schema.get('step', []))
            return True, "Schema added successfully", steps_count
        else:
            return False, "Could not insert schema", 0
    
    except Exception as e:
        return False, f"Error: {str(e)}", 0

def process_directory(root_dir):
    """Process all HTML files in directory"""
    root_path = Path(root_dir)
    processed = 0
    skipped = 0
    errors = 0
    total_steps = 0
    
    print(f"🔍 Сканирование директории: {root_dir}")
    print("=" * 60)
    
    for html_file in root_path.rglob('*.html'):
        # Skip files in excluded directories
        excluded_dirs = {'__pycache__', 'backups', 'scripts'}
        if any(excluded_dir in html_file.parts for excluded_dir in excluded_dirs):
            continue
        
        # Skip files starting with underscore
        if html_file.name.startswith('_'):
            continue
        
        success, message, steps = process_html_file(html_file)
        relative_path = html_file.relative_to(root_path)
        
        if success:
            processed += 1
            total_steps += steps
            print(f"✅ Обработан: {relative_path} - {message} ({steps} шагов)")
        else:
            if "already exists" in message or "Could not generate schema" in message:
                skipped += 1
                print(f"⏭️  Пропущен: {relative_path} - {message}")
            else:
                errors += 1
                print(f"❌ Ошибка: {relative_path} - {message}")
    
    print("=" * 60)
    print("📊 СТАТИСТИКА:")
    print(f"   ✅ Обработано файлов: {processed}")
    print(f"   ⏭️  Пропущено файлов: {skipped}")
    print(f"   ❌ Ошибок: {errors}")
    print(f"   📋 Всего шагов добавлено: {total_steps}")
    print(f"   📁 Всего файлов: {processed + skipped + errors}")
    print("=" * 60)

def main():
    # Get current directory
    root_dir = os.getcwd()
    
    print("🔧 Schema.org HowTo Generator")
    print("=" * 60)
    print("📋 Скрипт выполнит:")
    print("   • Рекурсивная обработка всех .html файлов")
    print("   • Извлечение H2 заголовков как шагов (максимум 8)")
    print("   • Генерация HowTo schema.org JSON-LD")
    print("   • Использование H1 для name, meta description для description")
    print("   • Добавление первого изображения и totalTime")
    print("   • Вставка перед </body> тегом")
    print("   • Проверка на дубликаты")
    print("   • Поддержка кириллицы (UTF-8)")
    print("   • Сохранение форматирования HTML")
    
    print(f"\n📂 Директория обработки: {root_dir}")
    
    # Ask user for confirmation
    response = input("\n🚀 Продолжить? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Отменено.")
        return
    
    # Process directory
    process_directory(root_dir)

if __name__ == '__main__':
    main()
