import os
import re
from pathlib import Path

guides_dir = Path(r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-laptops")

new_header_block = '''</style>
  <script async src="https://timeweb.cloud/api/v1/cloud-ai/agents/3cc03620-d051-4d8d-b5af-f7b6cd083a35/embed.js?collapsed=true"></script>
</head>
<body>
  <header class="header">
    <div class="container">
      <div class="header__inner">
        <a href="../index.html" class="logo">
          <span class="logo__icon"></span>
          <span class="logo__text">Repairo</span>
        </a>
        <nav class="nav">
          <ul class="nav__list">
            <li><a href="../tv.html" class="nav__link">Телевизоры</a></li>
            <li><a href="../cameras.html" class="nav__link">Фотоаппараты</a></li>
            <li><a href="../consoles.html" class="nav__link">Приставки</a></li>
            <li><a href="../laptops.html" class="nav__link">Ноутбуки</a></li>
            <li><a href="../smartphones.html" class="nav__link">Смартфоны</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </header>'''

for file_path in guides_dir.glob("*.html"):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Find and replace the header block from </style> to </header>
        pattern = r'</style>.*?</header>'
        new_content = re.sub(pattern, new_header_block, content, flags=re.DOTALL)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Updated header: {file_path.name}")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

print("All header blocks updated.")
