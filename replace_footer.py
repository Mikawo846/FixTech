import os
import re
from pathlib import Path

guides_dir = Path(r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-laptops")

new_footer = '''<footer class="footer">
        <div class="container">
            <div class="footer__grid">
                <div class="footer__col footer__col--logo">
                    <a href="../index.html" class="footer-logo">
                        <span class="logo__icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 15L7 10H17L12 15Z" fill="currentColor"/>
                                <path d="M12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3ZM12 19C8.13401 19 5 15.866 5 12C5 8.13401 8.13401 5 12 5C15.866 5 19 8.13401 19 12C19 15.866 15.866 19 12 19Z" fill="currentColor"/>
                            </svg>
                        </span>
                        <span class="logo__text">Repairo</span>
                    </a>
                    <p class="footer__text">Помогаем ремонтировать электронику с 2024 года</p>
                </div>
                <div class="footer__col">
                    <h3 class="footer__title">Разделы</h3>
                    <ul class="footer__links">
                        <li><a href="../index.html" class="footer__link">Главная</a></li>
                        <li><a href="../index.html#categories" class="footer__link">Все гайды</a></li>
                        <li><a href="../contacts.html" class="footer__link">Контакты</a></li>
                    </ul>
                </div>
                <div class="footer__col">
                    <h3 class="footer__title">Категории</h3>
                    <ul class="footer__links">
                        <li><a href="../tv.html" class="nav__link">Телевизоры</a></li>
                        <li><a href="../cameras.html" class="nav__link">Фотоаппараты</a></li>
                        <li><a href="../consoles.html" class="nav__link">Приставки</a></li>
                        <li><a href="../laptops.html" class="nav__link">Ноутбуки</a></li>
                        <li><a href="../smartphones.html" class="nav__link">Смартфоны</a></li>
                        <li><a href="../small-appliances.html" class="nav__link">Мелкая техника</a></li>
                        <li><a href="../large-appliances.html" class="nav__link">Бытовая техника</a></li>
                        <li><a href="../auto-electronics.html" class="nav__link">Авто-Электроника</a></li>
                    </ul>
                </div>
                <div class="footer__col">
                    <h3 class="footer__title">Контакты</h3>
                    <ul class="footer__links">
                        <li><a href="https://t.me/RepairoRU" class="footer__link"><i class="fab fa-telegram"></i> Telegram</a></li>
                        <li><span class="footer__link">Наша почта: repairo.info@mail.ru</span></li>
                    </ul>
                </div>
            </div>
            <div class="footer__bottom">
                <p class="disclaimer">
    Администрация сайта не несёт ответственности за возможные повреждения техники
    и иные последствия, возникшие в результате самостоятельного ремонта по
    материалам и инструкциям, размещённым на сайте. Все работы вы выполняете
    на свой страх и риск.
    </p>
                <p class="footer__copyright">© 2026 Repairo. Все права защищены.</p>
            </div>
        </div>
    </footer>'''

for file_path in guides_dir.glob("*.html"):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Find and replace the footer
        pattern = r'<footer class="footer">.*?</footer>'
        new_content = re.sub(pattern, new_footer, content, flags=re.DOTALL)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Updated: {file_path.name}")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

print("All files updated.")
