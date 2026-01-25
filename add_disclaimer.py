#!/usr/bin/env python3
import os
import glob
import re

# Disclaimer text
disclaimer = '''    <p class="disclaimer">
        Администрация сайта не несёт ответственности за возможные повреждения техники
        и иные последствия, возникшие в результате самостоятельного ремонта по
        материалам и инструкциям, размещённым на сайте. Все работы вы выполняете
        на свой страх и риск.
    </p>'''

def add_disclaimer_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if disclaimer already exists
    if 'class="disclaimer"' in content:
        print(f"Disclaimer already exists in {filepath}")
        return

    # Find footer
    footer_match = re.search(r'<footer[^>]*>.*?</footer>', content, re.DOTALL)
    if footer_match:
        footer_content = footer_match.group(0)
        # Find footer__bottom or add before </footer>
        bottom_match = re.search(r'(<div class="footer__bottom">.*?</div>)', footer_content, re.DOTALL)
        if bottom_match:
            # Add before the copyright
            new_bottom = bottom_match.group(1).replace('<p class="footer__copyright">', disclaimer + '\n                <p class="footer__copyright">')
            new_footer = footer_content.replace(bottom_match.group(1), new_bottom)
        else:
            # Add before </footer>
            new_footer = footer_content.replace('</footer>', disclaimer + '\n    </footer>')
        new_content = content.replace(footer_match.group(0), new_footer)
    else:
        # No footer, add before </body>
        new_content = content.replace('</body>', disclaimer + '\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Added disclaimer to {filepath}")

def main():
    # Find all HTML files
    html_files = glob.glob('**/*.html', recursive=True)
    for filepath in html_files:
        add_disclaimer_to_file(filepath)

if __name__ == '__main__':
    main()