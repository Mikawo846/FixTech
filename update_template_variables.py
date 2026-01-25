#!/usr/bin/env python3
import os
import re
from pathlib import Path

def update_meta_description_to_template(content):
    """Replace static meta description with template variable"""
    # Find meta description tag with content attribute
    meta_pattern = r'<meta[^>]*name=["\']description["\'][^>]*content=["\'][^"\']*["\'][^>]*>'
    
    def replace_meta(match):
        return '<meta name="description" content="{{ description }}">'
    
    new_content = re.sub(meta_pattern, replace_meta, content, flags=re.IGNORECASE)
    return new_content

def process_html_file(file_path):
    """Process single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = update_meta_description_to_template(content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "Updated meta description to template variable"
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
    
    print(f"Updating HTML files to use template variables in: {root_dir}")
    
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
            print(f"✓ {html_file.relative_to(root_path)} - {message}")
        else:
            if "No changes needed" in message:
                skipped += 1
                print(f"- {html_file.relative_to(root_path)} - {message}")
            else:
                errors += 1
                print(f"✗ {html_file.relative_to(root_path)} - {message}")
    
    print(f"\nResults:")
    print(f"  Updated: {processed}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total: {processed + skipped + errors}")

def main():
    # Get current directory
    root_dir = os.getcwd()
    
    print("HTML Template Variable Updater")
    print("=" * 40)
    
    # Ask user for confirmation
    print(f"This will update meta description tags to use template variables in: {root_dir}")
    
    response = input("\nContinue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Process directory
    process_directory(root_dir)

if __name__ == '__main__':
    main()
