import re
import os

# Path to laptops.html
laptops_path = r'c:\Users\yashi\Desktop\Новая папка\FixTech-main\laptops.html'
guides_dir = r'c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-laptops'

# Read the laptops.html
with open(laptops_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all hrefs
hrefs = re.findall(r'href="guides-laptops/([^"]+\.html)"', content)

existing_files = []
for filename in hrefs:
    file_path = os.path.join(guides_dir, filename)
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        existing_files.append(filename)

print("Existing files:", len(existing_files))

# Now, for each existing file, add the comment
for filename in existing_files:
    # Find the href line
    pattern = r'href="guides-laptops/' + re.escape(filename) + r'"'
    match = re.search(pattern, content)
    if match:
        # Find the position of the href
        start = match.start()
        # Find the next </article> after this position
        after = content[start:]
        article_end = re.search(r'</article>', after)
        if article_end:
            end_pos = start + article_end.end()
            # Insert the comment after </article>
            comment = '\n<!-- File exists -->'
            content = content[:end_pos] + comment + content[end_pos:]

# Write back
with open(laptops_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
