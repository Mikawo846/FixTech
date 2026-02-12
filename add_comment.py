import re

# Path to laptops.html
laptops_path = r'c:\Users\yashi\Desktop\Новая папка\FixTech-main\laptops.html'

# Read the laptops.html
with open(laptops_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the article with the specific href
filename = 'Chasto pojavljaetsja soobshchenie setevoy kabel ne podklyuchen noutbuk.html'
pattern = r'href="guides-laptops/' + re.escape(filename) + r'"'
match = re.search(pattern, content)
if match:
    start = match.start()
    # Find the end of this article
    after = content[start:]
    article_end_match = re.search(r'</article>', after)
    if article_end_match:
        end_pos = start + article_end_match.end()
        # Add the comment
        comment = '\n<!-- File exists -->'
        content = content[:end_pos] + comment + content[end_pos:]

# Write back
with open(laptops_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added comment for", filename)
