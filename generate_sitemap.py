#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
from pathlib import Path

def should_exclude_file(file_path):
    """Check if file should be excluded from sitemap"""
    # Convert to Path object for easier handling
    path = Path(file_path)
    
    # Check if file is in excluded directories
    excluded_dirs = {'static', 'assets', 'img', 'images', 'css', 'js'}
    if any(excluded_dir in path.parts for excluded_dir in excluded_dirs):
        return True
    
    # Check if filename starts with underscore
    if path.name.startswith('_'):
        return True
    
    return False

def collect_html_files(root_dir):
    """Recursively collect all HTML files"""
    html_files = []
    root_path = Path(root_dir)
    
    for html_file in root_path.rglob('*.html'):
        if not should_exclude_file(html_file):
            # Get relative path from root
            relative_path = html_file.relative_to(root_path)
            html_files.append(relative_path)
    
    return sorted(html_files)

def generate_sitemap(html_files, base_url='https://repairo.ru'):
    """Generate sitemap XML content"""
    # Create root element
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Add URL entries
    for html_file in html_files:
        url = ET.SubElement(urlset, 'url')
        
        # Create loc element with full URL
        loc = ET.SubElement(url, 'loc')
        # Convert Windows path separators to web path separators
        file_path = str(html_file).replace('\\', '/')
        loc.text = f'{base_url}/{file_path}'
        
        # Add changefreq
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'weekly'
        
        # Add priority
        priority = ET.SubElement(url, 'priority')
        priority.text = '0.5'
    
    # Generate XML string with proper formatting
    ET.indent(urlset, space="  ", level=0)
    xml_str = ET.tostring(urlset, encoding='unicode', method='xml')
    
    # Add XML declaration
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    return xml_declaration + xml_str

def generate_robots_txt(base_url='https://repairo.ru'):
    """Generate robots.txt content"""
    return f"""User-agent: *
Allow: /

Host: {base_url.replace('https://', '')}

Sitemap: {base_url}/sitemap.xml
"""

def main():
    # Get current directory (root of the project)
    root_dir = os.getcwd()
    print(f"Scanning directory: {root_dir}")
    
    # Collect HTML files
    html_files = collect_html_files(root_dir)
    print(f"Found {len(html_files)} HTML files")
    
    # Generate sitemap
    sitemap_content = generate_sitemap(html_files)
    
    # Write sitemap.xml
    sitemap_path = os.path.join(root_dir, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print(f"Generated sitemap.xml with {len(html_files)} URLs")
    
    # Generate robots.txt
    robots_content = generate_robots_txt()
    
    # Write robots.txt
    robots_path = os.path.join(root_dir, 'robots.txt')
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print("Generated robots.txt")
    
    # Display first few URLs for verification
    print("\nFirst 10 URLs in sitemap:")
    for i, html_file in enumerate(html_files[:10]):
        file_path = str(html_file).replace('\\', '/')
        print(f"  https://repairo.ru/{file_path}")
    
    if len(html_files) > 10:
        print(f"  ... and {len(html_files) - 10} more URLs")

if __name__ == '__main__':
    main()
