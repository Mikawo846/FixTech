import os
import glob

script_to_add = '  <script async src="https://timeweb.cloud/api/v1/cloud-ai/agents/3cc03620-d051-4d8d-b5af-f7b6cd083a35/embed.js?collapsed=true"></script>\n'

# Find all .html files
html_files = glob.glob('**/*.html', recursive=True)

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if script already exists
    if '3cc03620-d051-4d8d-b5af-f7b6cd083a35' in content:
        print(f"Script already in {file_path}")
        continue
    
    # Find </head>
    head_end = content.find('</head>')
    if head_end == -1:
        print(f"No </head> found in {file_path}")
        continue
    
    # Insert script before </head>
    new_content = content[:head_end] + script_to_add + content[head_end:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added script to {file_path}")