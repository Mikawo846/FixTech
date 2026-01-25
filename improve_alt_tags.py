#!/usr/bin/env python3
import os
import re
from pathlib import Path

def extract_title_from_h1(content):
    """Extract text from first <h1> tag"""
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    if h1_match:
        # Remove HTML tags from h1 content
        h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1))
        return h1_text.strip()
    return ""

def should_skip_image(img_tag):
    """Check if image should be skipped (logo, icon, etc.)"""
    img_lower = img_tag.lower()
    
    # Skip if contains logo/icon indicators
    skip_patterns = [
        'logo', 'icon', 'favicon', 'brand', 'emblem',
        'logotype', 'symbol', 'avatar'
    ]
    
    for pattern in skip_patterns:
        if pattern in img_lower:
            return True
    
    # Skip if src contains logo/icon paths
    src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
    if src_match:
        src = src_match.group(1).lower()
        for pattern in skip_patterns:
            if pattern in src:
                return True
    
    return False

def improve_alt_tag(img_tag, h1_text):
    """Improve alt tag for image"""
    # Extract current alt
    alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag, re.IGNORECASE)
    
    if not alt_match:
        # No alt attribute - add one
        if h1_text:
            new_alt = f"{h1_text[:50]} - пошаговая инструкция по ремонту"
            if len(new_alt) > 100:
                new_alt = new_alt[:97].rstrip() + "..."
            return re.sub(r'<img([^>]*?)>', f'<img\\1 alt="{new_alt}">', img_tag, flags=re.IGNORECASE)
        return img_tag
    
    current_alt = alt_match.group(1).strip()
    
    # Skip if alt is already good (>= 20 chars)
    if len(current_alt) >= 20:
        return img_tag
    
    # Improve alt tag
    if h1_text:
        if current_alt:
            new_alt = f"{current_alt} - пошаговая инструкция по ремонту"
        else:
            new_alt = f"{h1_text[:50]} - пошаговая инструкция по ремонту"
        
        # Ensure length is 50-100 characters
        if len(new_alt) > 100:
            new_alt = new_alt[:97].rstrip() + "..."
        elif len(new_alt) < 50 and current_alt:
            # If too short, add more context from h1
            h1_snippet = h1_text[:30]
            new_alt = f"{current_alt} - {h1_snippet} - пошаговая инструкция по ремонту"
            if len(new_alt) > 100:
                new_alt = new_alt[:97].rstrip() + "..."
        
        # Replace alt attribute
        return re.sub(r'alt=["\'][^"\']*["\']', f'alt="{new_alt}"', img_tag, flags=re.IGNORECASE)
    
    return img_tag

def process_html_content(content):
    """Process HTML content to improve alt tags"""
    # Extract h1 text for context
    h1_text = extract_title_from_h1(content)
    
    # Find all img tags
    img_pattern = r'<img[^>]*>'
    img_matches = list(re.finditer(img_pattern, content, re.IGNORECASE))
    
    changes_made = 0
    # Process from end to beginning to avoid position shifts
    for match in reversed(img_matches):
        img_tag = match.group()
        
        # Skip if should be ignored
        if should_skip_image(img_tag):
            continue
        
        # Improve alt tag
        new_img_tag = improve_alt_tag(img_tag, h1_text)
        
        if new_img_tag != img_tag:
            # Replace in content
            content = content[:match.start()] + new_img_tag + content[match.end():]
            changes_made += 1
    
    return content, changes_made

def process_html_file(file_path):
    """Process single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changes = process_html_content(content)
        
        if changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, f"Improved {changes} image(s)"
        else:
            return False, "No changes needed"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def process_directory(root_dir):
    """Process all HTML files in directory"""
    root_path = Path(root_dir)
    processed = 0
    skipped = 0
    errors = 0
    total_images_improved = 0
    
    print(f"Scanning directory: {root_dir}")
    
    for html_file in root_path.rglob('*.html'):
        # Skip files in excluded directories
        excluded_dirs = {'__pycache__', 'backups', 'scripts'}
        if any(excluded_dir in html_file.parts for excluded_dir in excluded_dirs):
            continue
        
        # Skip files starting with underscore
        if html_file.name.startswith('_'):
            continue
        
        success, message = process_html_file(html_file)
        
        if success:
            processed += 1
            # Extract number of images improved from message
            if "Improved" in message:
                import re
                match = re.search(r'Improved (\d+)', message)
                if match:
                    total_images_improved += int(match.group(1))
            print(f"✓ {html_file.relative_to(root_path)} - {message}")
        else:
            if "No changes needed" in message:
                skipped += 1
                print(f"- {html_file.relative_to(root_path)} - {message}")
            else:
                errors += 1
                print(f"✗ {html_file.relative_to(root_path)} - {message}")
    
    print(f"\nResults:")
    print(f"  Processed: {processed}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total images improved: {total_images_improved}")
    print(f"  Total files: {processed + skipped + errors}")

def main():
    # Get current directory
    root_dir = os.getcwd()
    
    print("ALT Tags Improver")
    print("=" * 40)
    print("This script will:")
    print("- Find all <img> tags (except logos/icons)")
    print("- Improve empty or short alt attributes")
    print("- Add context from H1 tags")
    print("- Target length: 50-100 characters")
    
    print(f"\nProcessing directory: {root_dir}")
    
    # Ask user for confirmation
    response = input("\nContinue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Process directory
    process_directory(root_dir)

if __name__ == '__main__':
    main()
