import re
import os

# Path to laptops.html
laptops_path = r'c:\Users\yashi\Desktop\Новая папка\FixTech-main\laptops.html'

# Path to guides-laptops
guides_path = r'c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-laptops'

# Read the laptops.html
with open(laptops_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all guide articles
articles = re.findall(r'<article class="guide-card">(.*?)</article>', content, re.DOTALL)
print(f"Found {len(articles)} articles")

for article in articles:
    # Check if href to guides-laptops/
    href_match = re.search(r'href="guides-laptops/([^"]+\.html)"', article)
    if href_match:
        filename = href_match.group(1)
        filepath = os.path.join(guides_path, filename)
        if os.path.exists(filepath):
            # Check if comment already there
            start = content.find(article)
            after = content[start + len(article):]
            if '<!-- File exists -->' not in after[:100]:
                # Add the comment
                insert_pos = start + len(article)
                content = content[:insert_pos] + '\n<!-- File exists -->' + content[insert_pos:]

# Write back
with open(laptops_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Marked existing files.")

# Now find unmarked again
unmarked = []
for article in articles:
    # Check if href to guides-laptops/
    href_match = re.search(r'href="guides-laptops/([^"]+\.html)"', article)
    if href_match:
        filename = href_match.group(1)
        # Check if after this article there is <!-- File exists -->
        start = content.find(article)
        after = content[start + len(article):]
        if '<!-- File exists -->' not in after[:100]:
            unmarked.append(filename)

print(f"Still unmarked: {len(unmarked)}")

# Write unmarked to file
with open('unmarked_after_marking.txt', 'w', encoding='utf-8') as f:
    for filename in unmarked:
        f.write(filename + '\n')
