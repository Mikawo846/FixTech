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

def extract_first_paragraph(content):
    """Extract first paragraph after h1"""
    # Find first h1
    h1_pos = content.lower().find('<h1')
    if h1_pos == -1:
        return ""
    
    # Find end of h1
    h1_end = content.lower().find('</h1>', h1_pos)
    if h1_end == -1:
        return ""
    
    # Look for first paragraph after h1
    after_h1 = content[h1_end + 5:]
    p_match = re.search(r'<p[^>]*>(.*?)</p>', after_h1, re.DOTALL | re.IGNORECASE)
    if p_match:
        # Remove HTML tags from paragraph
        p_text = re.sub(r'<[^>]+>', '', p_match.group(1))
        return p_text.strip()
    return ""

def generate_description(h1_text, first_paragraph):
    """Generate meta description"""
    if not h1_text:
        return ""
    
    # Take first 80 characters from first paragraph
    if first_paragraph:
        paragraph_snippet = first_paragraph[:80]
        if len(first_paragraph) > 80:
            paragraph_snippet = paragraph_snippet.rstrip() + "..."
    else:
        paragraph_snippet = ""
    
    # Build description
    description = f"Пошаговая инструкция: {h1_text}"
    if paragraph_snippet:
        description += f". {paragraph_snippet}"
    description += ". Советы экспертов, таблицы, FAQ."
    
    # Ensure length is 140-160 characters
    if len(description) > 160:
        # Truncate to 160 characters, try to end at word boundary
        description = description[:157].rstrip() + "..."
    elif len(description) < 140 and paragraph_snippet:
        # If too short, try to extend paragraph snippet
        if len(first_paragraph) > 80:
            extended_snippet = first_paragraph[:120]
            if len(first_paragraph) > 120:
                extended_snippet = extended_snippet.rstrip() + "..."
            description = f"Пошаговая инструкция: {h1_text}. {extended_snippet}. Советы экспертов, таблицы, FAQ."
    
    return description

def add_meta_description(content):
    """Add meta description after title tag"""
    # Find title tag
    title_match = re.search(r'<title[^>]*>.*?</title>', content, re.DOTALL | re.IGNORECASE)
    if not title_match:
        return content, "Title tag not found"
    
    # Check if meta description already exists
    if re.search(r'<meta[^>]*name=["\']description["\'][^>]*>', content, re.IGNORECASE):
        return content, "Meta description already exists"
    
    # Extract h1 and first paragraph
    h1_text = extract_title_from_h1(content)
    first_paragraph = extract_first_paragraph(content)
    
    # Generate description
    description = generate_description(h1_text, first_paragraph)
    if not description:
        return content, "Could not generate description"
    
    # Create meta tag
    meta_tag = f'\n    <meta name="description" content="{description}">'
    
    # Insert after title tag
    title_end = title_match.end()
    new_content = content[:title_end] + meta_tag + content[title_end:]
    
    return new_content, f"Added description ({len(description)} chars): {description[:50]}..."

def process_html_file(file_path):
    """Process single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, message = add_meta_description(content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, message
        else:
            return False, message
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def process_directory(root_dir):
    """Process all HTML files in directory"""
    root_path = Path(root_dir)
    processed = 0
    skipped = 0
    errors = 0
    
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
            print(f"✓ {html_file.relative_to(root_path)} - {message}")
        else:
            if "already exists" in message or "Title tag not found" in message:
                skipped += 1
                print(f"- {html_file.relative_to(root_path)} - {message}")
            else:
                errors += 1
                print(f"✗ {html_file.relative_to(root_path)} - {message}")
    
    print(f"\nResults:")
    print(f"  Processed: {processed}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total: {processed + skipped + errors}")

def main():
    # Get current directory
    root_dir = os.getcwd()
    
    print("Meta Description Generator")
    print("=" * 40)
    
    # Ask user for confirmation
    print(f"This will add meta descriptions to HTML files in: {root_dir}")
    print("Files that already have meta descriptions will be skipped.")
    
    response = input("\nContinue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Process directory
    process_directory(root_dir)

if __name__ == '__main__':
    main()
