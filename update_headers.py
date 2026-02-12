import os
import re

folder = r"c:\Users\yashi\Desktop\Новая папка\FixTech-main\guides-laptops"

new_header = """  <header class="header">
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
  </header>"""

new_footer = """    <footer class="footer">
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
    </footer>"""

for filename in os.listdir(folder):
    if filename.endswith('.html'):
        filepath = os.path.join(folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            content = re.sub(r'<header>.*?</header>', new_header, content, flags=re.DOTALL)
            content = re.sub(r'<footer>.*?</footer>', new_footer, content, flags=re.DOTALL)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")
        except Exception as e:
            print(f"Error updating {filename}: {e}")
